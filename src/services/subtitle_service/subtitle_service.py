from pathlib import Path
from ..constants import OUTPUT_DIR


class SubtitleService:
    def __init__(
            self,
            script_path: Path = OUTPUT_DIR / "script.txt",
            subtitle_dir: Path = OUTPUT_DIR / "subtitle",
            subtitle_name: str = "subtitle.srt",
    ):
        self.script_path = Path(script_path)
        self.subtitle_dir = Path(subtitle_dir)
        self.subtitle_path = self.subtitle_dir / subtitle_name

    def __create(self) -> None:
        text = self.script_path.read_text()

        self.subtitle_dir.mkdir(parents=True, exist_ok=True)

        lines = text.split(". ")
        srt = ""

        for i, line in enumerate(lines):
            srt += (
                f"{i + 1}\n"
                f"00:00:{i:02},000 --> 00:00:{i + 2:02},000\n"
                f"{line}\n\n"
            )

        self.subtitle_path.write_text(srt)

    def run(self) -> None:
        self.__create()
