import subprocess
from pathlib import Path
from pydub import AudioSegment
from .constants import PIPER_MODEL


class AudioService:
    def __init__(self):
        self.chunks_dir = Path("output/chunks")
        self.audio_dir = Path("output/audio")
        self.audio_dir.mkdir(parents=True, exist_ok=True)

    def __create_chunks(self) -> None:
        for chunk in sorted(self.chunks_dir.glob("*.txt")):
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
