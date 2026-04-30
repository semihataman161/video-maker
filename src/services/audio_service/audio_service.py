from pathlib import Path
import json
from pydub import AudioSegment
from TTS.api import TTS

from ..constants import OUTPUT_DIR
from .constants import BASE_DIR
from src.utils.device_utils import get_device


class AudioService:
    def __init__(self, chunks: list[str]):
        self.chunks = chunks
        self.audio_dir = Path(OUTPUT_DIR / "audio")
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        self.speaker_wav = Path(BASE_DIR / "speaker.wav")

        self.device = get_device()
        print(f"🔊 Loading TTS on {self.device}")
        self.tts = TTS(
            model_name="tts_models/multilingual/multi-dataset/xtts_v2"
        ).to(self.device)

    def run(self) -> None:
        if not self.chunks:
            raise ValueError("Chunks are empty.")

        combined = AudioSegment.empty()
        timeline = []
        current_time = 0

        for i, chunk in enumerate(self.chunks):
            temp_path = self.audio_dir / f"chunk_{i}.wav"

            self.tts.tts_to_file(
                text=chunk,
                speaker_wav=str(self.speaker_wav),
                language="en",
                file_path=str(temp_path),
                temperature=0.6,
            )

            segment = AudioSegment.from_wav(temp_path)
            duration = len(segment) / 1000

            timeline.append({
                "index": i,
                "text": chunk,
                "start": current_time,
                "end": current_time + duration,
                "duration": duration
            })

            silence_duration = 0.4
            silence = AudioSegment.silent(duration=int(silence_duration * 1000))

            combined += segment + silence
            current_time += duration + silence_duration

        final_audio_path = self.audio_dir / "output.wav"
        combined.export(final_audio_path, format="wav")

        timeline_path = self.audio_dir / "timeline.json"
        with open(timeline_path, "w") as f:
            json.dump(timeline, f, indent=2)

        print(f"🧠 Timeline saved → {timeline_path}")
