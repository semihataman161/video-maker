import os
import re
import subprocess
import numpy as np
import soundfile as sf
from mlx_audio.tts.utils import load_model
from mlx_audio.stt import load
from pydub import AudioSegment
from pathlib import Path

from src.utils.file_utils import validate_paths
from src.utils.timeline_utils import save_timeline
from src.utils.chunk_utils import split_sentences
from src.constants import AUDIO_DIR
from .constants import TTS_MODEL, ALIGNMENT_MODEL, CHUNK_PAUSE, SENTENCE_PAUSE, SAMPLE_RATE, SPEAKERS_DIR

os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"


class AudioService:
    def __init__(self, chunks: list[str], language: str):
        self.chunks = chunks
        self.language = language

        speaker_dir = SPEAKERS_DIR / language
        self.speaker_wav = speaker_dir / "index.wav"
        self.ref_text_path = speaker_dir / "index.txt"

        validate_paths([self.speaker_wav, self.ref_text_path])

        self.speaker_wav = self.__prepare_reference_audio()
        self.ref_text = self.ref_text_path.read_text(encoding="utf-8").strip()

        print("🔊 Loading Qwen3-TTS (MLX)...")
        self.tts_model = load_model(TTS_MODEL)

        print("🗣️ Loading Qwen3-ForcedAligner...")
        self.alignment_model = load(ALIGNMENT_MODEL)

    def __prepare_reference_audio(self) -> str:
        ref_path = Path(self.speaker_wav)
        file_name = f"{ref_path.stem}_24k_mono.wav"
        converted_path = ref_path.parent / file_name

        if converted_path.exists():
            print(f"[{converted_path}] is already in the required format. Skipping conversion.")
            return str(converted_path)

        subprocess.run(
            [
                "ffmpeg", "-y",
                "-i", str(ref_path),
                "-ac", "1",
                "-ar", str(SAMPLE_RATE),
                "-sample_fmt", "s16",
                str(converted_path),
            ],
            capture_output=True,
            check=True,
        )

        return str(converted_path)

    def __generate_sentence_audio(self, sentence: str) -> np.ndarray:
        results = list(self.tts_model.generate(
            text=sentence,
            ref_audio=self.speaker_wav,
            ref_text=self.ref_text,
        ))

        all_audio = [
            np.array(r.audio, dtype=np.float32)
            for r in results
            if r.audio is not None
        ]

        if not all_audio:
            raise RuntimeError(f"Audio data is empty: {sentence[:50]}...")

        return np.concatenate(all_audio) if len(all_audio) > 1 else all_audio[0]

    def __generate_audio_file(self, index: int, text: str) -> Path:
        temp_path = AUDIO_DIR / f"chunk_{index}.wav"

        sentences = split_sentences(text)
        silence = np.zeros(int(SAMPLE_RATE * SENTENCE_PAUSE), dtype=np.float32)

        audio_parts = []
        for sentence in sentences:
            audio_parts.append(self.__generate_sentence_audio(sentence))
            audio_parts.append(silence)

        if audio_parts:
            audio_parts.pop()

        audio_array = np.concatenate(audio_parts)
        sf.write(str(temp_path), audio_array, SAMPLE_RATE)
        return temp_path

    def __load_audio_segment(self, path: Path) -> tuple[AudioSegment, float]:
        segment = AudioSegment.from_wav(path)
        return segment, len(segment) / 1000

    def __reattach_punctuation(self, aligned_words: list[dict], original_text: str) -> list[dict]:
        original_tokens = original_text.split()

        def strip_punct(token: str) -> str:
            return re.sub(r"[^\w']", "", token).lower()

        stripped_originals = [strip_punct(t) for t in original_tokens]

        match_idx = 0
        for word_entry in aligned_words:
            aligned_clean = strip_punct(word_entry["word"])

            while match_idx < len(stripped_originals):
                if stripped_originals[match_idx] == aligned_clean:
                    word_entry["word"] = original_tokens[match_idx]
                    match_idx += 1
                    break
                match_idx += 1

        return aligned_words

    def __align_words(self, audio_path: Path, text: str, offset: float) -> list[dict]:
        words = []

        result = self.alignment_model.generate(str(audio_path), text=text, language=self.language)

        for item in result:
            words.append({
                "word": item.text.strip(),
                "start": float(item.start_time) + offset,
                "end": float(item.end_time) + offset,
            })

        words = self.__reattach_punctuation(words, text)
        return words

    def __process_chunk(self, index: int, chunk: str, combined: AudioSegment, current_time: float):
        temp_path = self.__generate_audio_file(index, chunk)
        segment, duration = self.__load_audio_segment(temp_path)

        words = self.__align_words(temp_path, chunk, current_time)

        timeline_entry = {
            "index": index,
            "text": chunk,
            "start": current_time,
            "end": current_time + duration,
            "duration": duration,
            "pause": CHUNK_PAUSE,
            "words": words,
        }

        silence = AudioSegment.silent(duration=int(CHUNK_PAUSE * 1000))
        combined = combined + segment + silence
        return combined, timeline_entry, current_time + duration + CHUNK_PAUSE

    def run(self):
        combined = AudioSegment.empty()
        timeline = []
        current_time = 0

        total = len(self.chunks)
        for i, chunk in enumerate(self.chunks, start=1):
            print(f"   ⏳ Chunk {i}/{total}: {chunk[:50]}...")
            combined, entry, current_time = self.__process_chunk(i, chunk, combined, current_time)
            timeline.append(entry)
            print(f"   ✅ Chunk {i}/{total} done")

        final_path = AUDIO_DIR / "merged.wav"
        combined.export(final_path, format="wav")
        save_timeline(timeline)
