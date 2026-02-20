from pathlib import Path
from TTS.api import TTS

from ..constants import OUTPUT_DIR
from .constants import BASE_DIR


class AudioService:
    def __init__(self, script: str):
        self.script = script.strip()
        self.audio_dir = Path(OUTPUT_DIR / "audio")
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        self.speaker_wav = Path(BASE_DIR / "speaker.wav")

        # Initialize XTTS (CPU mode for macOS)
        self.tts = TTS(
            model_name="tts_models/multilingual/multi-dataset/xtts_v2",
            progress_bar=True,
            gpu=False,  # macOS → must stay False
        )

    def run(self) -> None:
        if not self.script:
            raise ValueError("Script content is empty.")

        output_path = self.audio_dir / "output.wav"

        self.tts.tts_to_file(
            text=self.script,
            speaker_wav=str(self.speaker_wav),
            language="en",
            file_path=str(output_path),
        )
