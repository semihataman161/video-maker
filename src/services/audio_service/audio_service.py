import json
from pathlib import Path
from pydub import AudioSegment
from TTS.api import TTS

from src.utils.device_utils import get_device
from src.constants import AUDIO_DIR


class AudioService:
    def __init__(self, chunks: list[str]):
        self.chunks = chunks

        self.speaker_wav = Path(__file__).with_name("speaker.wav")
        self.model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
        self.pause = 0.4
        self.device = get_device()

        print(f"🔊 Loading TTS on {self.device}")
        self.tts = TTS(
            model_name=self.model_name,
            gpu=(self.device == "cuda")
        )

    def __generate_audio_file(self, index: int, text: str) -> Path:
        temp_path = AUDIO_DIR / f"chunk_{index}.wav"

        self.tts.tts_to_file(
            text=text,
            speaker_wav=str(self.speaker_wav),
            language="en",
            file_path=str(temp_path),
            temperature=0.6,
        )

        return temp_path

    def __load_audio_segment(self, path: Path) -> tuple[AudioSegment, float]:
        segment = AudioSegment.from_wav(path)
        duration = len(segment) / 1000
        return segment, duration

    def __create_timeline_entry(
            self,
            index: int,
            text: str,
            start: float,
            duration: float
    ) -> dict:
        return {
            "index": index,
            "text": text,
            "start": start,
            "end": start + duration,
            "duration": duration,
            "pause": self.pause
        }

    def __append_with_pause(
            self,
            combined: AudioSegment,
            segment: AudioSegment
    ) -> AudioSegment:
        silence = AudioSegment.silent(duration=int(self.pause * 1000))
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

        timeline_entry = self.__create_timeline_entry(
            index=index,
            text=chunk,
            start=current_time,
            duration=duration
        )

        combined = self.__append_with_pause(combined, segment)

        new_current_time = current_time + duration + self.pause

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

    def __export_audio(self, combined: AudioSegment) -> None:
        final_audio_path = AUDIO_DIR / "merged.wav"
        combined.export(final_audio_path, format="wav")

    def __save_timeline(self, timeline: list[dict]) -> None:
        timeline_path = AUDIO_DIR / "timeline.json"
        with open(timeline_path, "w") as f:
            json.dump(timeline, f, indent=2)

        print(f"🧠 Timeline saved → {timeline_path}")

    def run(self) -> None:
        combined, timeline = self.__process_chunks()
        self.__export_audio(combined)
        self.__save_timeline(timeline)
