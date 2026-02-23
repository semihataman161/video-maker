from pathlib import Path
import re
from pydub import AudioSegment
from TTS.api import TTS
import torch

from ..constants import OUTPUT_DIR
from .constants import BASE_DIR


class AudioService:
    def __init__(self, script: str):
        self.script = script.strip()
        self.audio_dir = Path(OUTPUT_DIR / "audio")
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        self.speaker_wav = Path(BASE_DIR / "speaker.wav")

        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2").to(device)


def split_script(self, max_chars=400):
    paragraphs = [p.strip() for p in self.script.split("\n\n") if p.strip()]
    chunks = []

    for p in paragraphs:
        if len(p) <= max_chars:
            chunks.append(p)
        else:
            sentences = re.split(r'(?<=[.!?]) +', p)
            current = ""
            for s in sentences:
                if len(current) + len(s) < max_chars:
                    current += " " + s
                else:
                    chunks.append(current.strip())
                    current = s
            if current:
                chunks.append(current.strip())

    return chunks


def run(self) -> None:
    if not self.script:
        raise ValueError("Script content is empty.")

    chunks = self.split_script()
    combined = AudioSegment.empty()

    for i, chunk in enumerate(chunks):
        temp_path = self.audio_dir / f"chunk_{i}.wav"

        self.tts.tts_to_file(
            text=chunk,
            speaker_wav=str(self.speaker_wav),
            language="en",
            file_path=str(temp_path),
            temperature=0.6,
        )

        segment = AudioSegment.from_wav(temp_path)
        silence = AudioSegment.silent(duration=400)
        combined += segment + silence

    final_path = self.audio_dir / "output.wav"
    combined.export(final_path, format="wav")
