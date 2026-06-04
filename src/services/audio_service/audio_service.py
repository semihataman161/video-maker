import os
import subprocess
import torch
import torchaudio
import whisperx
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
from pydub import AudioSegment
from pathlib import Path

from src.utils.file_utils import validate_path
from src.utils.device_utils import get_device
from src.utils.timeline_utils import save_timeline
from src.constants import AUDIO_DIR
from .constants import SPEAKERS_DIR, PAUSE

# ─── MPS Fallback ───
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

# ─── CPU Performans ───
torch.set_num_threads(os.cpu_count())
torch.set_num_interop_threads(os.cpu_count())

# ─── Ayarlanabilir Parametreler ───
# Konuşma hızı: 1.0 = orijinal, 0.78 = %22 yavaş
SPEED_FACTOR = 0.78


def _load_tts_model() -> tuple[ChatterboxMultilingualTTS, str]:
    """MPS'i dener, başarısız olursa CPU'ya düşer."""
    if torch.backends.mps.is_available():
        try:
            print("   🍎 MPS algılandı, GPU'da yükleniyor...")
            model = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
            model.t3 = model.t3.to("mps")
            model.s3gen = model.s3gen.to("mps")
            model.ve = model.ve.to("mps")
            model.device = torch.device("mps")

            _ = model.generate("test", language_id="en", exaggeration=0.5, cfg_weight=0.5)
            print("   ✅ MPS çalışıyor!")
            return model, "mps"
        except Exception as e:
            print(f"   ⚠️ MPS başarısız: {e}")
            print("   🔄 CPU'ya geçiliyor...")

    if torch.cuda.is_available():
        print("   🚀 CUDA algılandı")
        model = ChatterboxMultilingualTTS.from_pretrained(device="cuda")
        return model, "cuda"

    print("   💻 CPU modunda yükleniyor...")
    model = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
    return model, "cpu"


class AudioService:
    def __init__(self, chunks: list[str], language: str):
        self.chunks = chunks
        self.language = language

        self.speaker_wav = SPEAKERS_DIR / f"{language}.wav"
        validate_path(self.speaker_wav)

        print(f"🔊 Loading Chatterbox Multilingual TTS...")
        self.tts, self.device = _load_tts_model()
        print(f"   ✅ TTS model ready on '{self.device}'")

        self.whisper_device = "cpu"
        print(f"🗣️ Loading WhisperX alignment model for '{self.language}'")
        self.alignment_model, self.metadata = whisperx.load_align_model(
            language_code=self.language,
            device=self.whisper_device,
        )

    @torch.inference_mode()
    def __generate_audio_file(self, index: int, text: str) -> Path:
        temp_path = AUDIO_DIR / f"chunk_{index}.wav"

        wav_tensor = self.tts.generate(
            text,
            language_id=self.language,
            audio_prompt_path=str(self.speaker_wav),
            exaggeration=0.5,
            cfg_weight=0.5,
        )

        torchaudio.save(str(temp_path), wav_tensor.cpu(), self.tts.sr)
        return temp_path

    def __trim_trailing_silence(self, path: Path) -> None:
        """
        Sesin sonundaki sessizlik ve artifact'ları güvenli şekilde kırpar.

        Sondan geriye doğru 50ms'lik pencerelerle tarar,
        ses seviyesi eşiğin altındaysa sessiz sayar ve keser.
        Konuşmaya dokunmaz — sadece gerçek sessizliği kırpar.
        """
        segment = AudioSegment.from_wav(path)

        chunk_ms = 50
        silence_thresh_dbfs = -40

        end = len(segment)

        # Sondan geriye doğru sessiz bölgeyi bul
        while end > chunk_ms:
            window = segment[end - chunk_ms: end]
            if window.dBFS > silence_thresh_dbfs:
                break
            end -= chunk_ms

        # 100ms güvenlik marjı ekle (keskin kesilmesin)
        end = min(end + 100, len(segment))

        if end < len(segment):
            trimmed = segment[:end].fade_out(30)
            trimmed.export(str(path), format="wav")

    def __slow_down_audio(self, path: Path) -> None:
        """
        ffmpeg atempo filtresi ile sesi pitch koruyarak yavaşlatır.
        """
        if SPEED_FACTOR >= 1.0:
            return

        temp_output = path.with_suffix(".slow.wav")

        subprocess.run(
            [
                "ffmpeg", "-y",
                "-i", str(path),
                "-filter:a", f"atempo={SPEED_FACTOR}",
                "-ar", "24000",
                str(temp_output),
            ],
            capture_output=True,
            check=True,
        )

        temp_output.replace(path)

    def __load_audio_segment(self, path: Path) -> tuple[AudioSegment, float]:
        segment = AudioSegment.from_wav(path)
        duration = len(segment) / 1000
        return segment, duration

    def __align_words(
            self,
            audio_path: Path,
            text: str,
            offset: float,
            duration: float,
    ):
        audio = whisperx.load_audio(str(audio_path))

        transcript = [{
            "start": 0,
            "end": duration,
            "text": text,
        }]

        aligned_result = whisperx.align(
            transcript=transcript,
            model=self.alignment_model,
            align_model_metadata=self.metadata,
            audio=audio,
            device=self.whisper_device,
        )

        words = []

        for segment in aligned_result["segments"]:
            for word in segment["words"]:
                if "start" not in word or "end" not in word:
                    continue

                words.append({
                    "word": word["word"].strip(),
                    "start": float(word["start"]) + offset,
                    "end": float(word["end"]) + offset,
                })

        return words

    def __create_timeline_entry(
            self,
            index: int,
            text: str,
            start: float,
            duration: float,
            words: list[dict]
    ) -> dict:
        return {
            "index": index,
            "text": text,
            "start": start,
            "end": start + duration,
            "duration": duration,
            "pause": PAUSE,
            "words": words,
        }

    def __append_with_pause(
            self,
            combined: AudioSegment,
            segment: AudioSegment
    ) -> AudioSegment:
        silence = AudioSegment.silent(duration=int(PAUSE * 1000))
        return combined + segment + silence

    def __process_chunk(
            self,
            index: int,
            chunk: str,
            combined: AudioSegment,
            current_time: float
    ) -> tuple[AudioSegment, dict, float]:
        # 1. Ses üret
        temp_path = self.__generate_audio_file(index, chunk)

        # 2. Sondaki sessizlik/artifact'ı kırp (güvenli)
        self.__trim_trailing_silence(temp_path)

        # 3. Yavaşlat — ffmpeg atempo
        self.__slow_down_audio(temp_path)

        # 4. Yükle
        segment, duration = self.__load_audio_segment(temp_path)

        # 5. Kelime hizalama
        words = self.__align_words(
            audio_path=temp_path,
            text=chunk,
            offset=current_time,
            duration=duration,
        )

        timeline_entry = self.__create_timeline_entry(
            index=index,
            text=chunk,
            start=current_time,
            duration=duration,
            words=words,
        )

        combined = self.__append_with_pause(combined, segment)
        new_current_time = current_time + duration + PAUSE

        return combined, timeline_entry, new_current_time

    def __process_chunks(self) -> tuple[AudioSegment, list[dict]]:
        combined = AudioSegment.empty()
        timeline = []
        current_time = 0

        total = len(self.chunks)
        for i, chunk in enumerate(self.chunks, start=1):
            print(f"   ⏳ Chunk {i}/{total}: {chunk[:50]}...")
            combined, timeline_entry, current_time = self.__process_chunk(
                index=i,
                chunk=chunk,
                combined=combined,
                current_time=current_time
            )
            timeline.append(timeline_entry)
            print(f"   ✅ Chunk {i}/{total} done")

        return combined, timeline

    def __export_audio(self, combined: AudioSegment):
        final_audio_path = AUDIO_DIR / "merged.wav"
        combined.export(final_audio_path, format="wav")

    def run(self):
        combined, timeline = self.__process_chunks()
        self.__export_audio(combined)
        save_timeline(timeline)
