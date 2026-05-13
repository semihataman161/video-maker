import whisper
from TTS.api import TTS
from pydub import AudioSegment
from pathlib import Path

from src.utils.device_utils import get_device
from src.utils.timeline_utils import save_timeline
from src.constants import AUDIO_DIR
from .constants import SPEAKER_WAV, MODEL_NAME, PAUSE


class AudioService:
    def __init__(self, chunks: list[str]):
        self.chunks = chunks

        self.device = get_device()

        print(f"🔊 Loading TTS on {self.device}")
        self.tts = TTS(
            model_name=MODEL_NAME,
            gpu=(self.device == "cuda")
        )

        print("🧠 Loading Whisper model")
        self.whisper_model = whisper.load_model("base")

    def __generate_audio_file(self, index: int, text: str):
        temp_path = AUDIO_DIR / f"chunk_{index}.wav"

        self.tts.tts_to_file(
            text=text,
            speaker_wav=str(SPEAKER_WAV),
            language="en",
            file_path=str(temp_path),
            temperature=0.6,
        )

        return temp_path

    def __load_audio_segment(self, path: Path) -> tuple[AudioSegment, float]:
        segment = AudioSegment.from_wav(path)
        duration = len(segment) / 1000
        return segment, duration

    def __transcribe_words(self, audio_path: Path, offset: float):
        result = self.whisper_model.transcribe(
            str(audio_path),
            word_timestamps=True,
            fp16=False,
        )

        words = []

        for segment in result["segments"]:
            for word in segment["words"]:
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
        temp_path = self.__generate_audio_file(index, chunk)

        segment, duration = self.__load_audio_segment(temp_path)

        words = self.__transcribe_words(
            audio_path=temp_path,
            offset=current_time,
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

        for i, chunk in enumerate(self.chunks, start=1):
            combined, timeline_entry, current_time = self.__process_chunk(
                index=i,
                chunk=chunk,
                combined=combined,
                current_time=current_time
            )
            timeline.append(timeline_entry)

        return combined, timeline

    def __export_audio(self, combined: AudioSegment):
        final_audio_path = AUDIO_DIR / "merged.wav"
        combined.export(final_audio_path, format="wav")

    def run(self):
        combined, timeline = self.__process_chunks()
        self.__export_audio(combined)
        save_timeline(timeline)
