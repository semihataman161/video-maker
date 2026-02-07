from pathlib import Path
import subprocess
from pydub import AudioSegment

from ..constants import OUTPUT_DIR
from .constants import PIPER_MODEL


class AudioService:
    def __init__(self):
        self.script_dir = Path(OUTPUT_DIR / "script")
        self.audio_dir = Path(OUTPUT_DIR / "audio")
        self.audio_dir.mkdir(parents=True, exist_ok=True)

    def __create_chunks(self) -> None:
        for chunk in sorted(self.script_dir.glob("*.txt")):
            out = self.audio_dir / f"{chunk.stem}.wav"

            subprocess.run(
                ["piper", "--model", PIPER_MODEL, "--output_file", str(out)],
                input=chunk.read_text(),
                text=True,
                check=True
            )

    def __merge(self, output_name) -> None:
        combined = AudioSegment.empty()

        for wav in sorted(self.audio_dir.glob("chunk_*.wav")):
            combined += AudioSegment.from_wav(wav)

        combined.export(self.audio_dir / output_name, format="wav")

    def run(self, output_name: str = "merged.wav") -> None:
        self.__create_chunks()
        self.__merge(output_name)
