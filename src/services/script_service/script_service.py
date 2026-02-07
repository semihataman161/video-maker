from pathlib import Path
import re

from ..ai_service import AiService
from ..constants import OUTPUT_DIR
from .constants import BASE_DIR, CHUNK_CHAR_LIMIT


class ScriptService:
    def __init__(
            self,
            ai_service: AiService,
            output_dir=Path(OUTPUT_DIR),
            script_dir=Path(OUTPUT_DIR / "script"),
            prompt_path=Path(BASE_DIR / "prompts" / "story_prompt.txt"),
    ):
        self.ai_service = ai_service
        self.output_dir = Path(output_dir)
        self.script_dir = Path(script_dir)
        self.script_dir.mkdir(parents=True, exist_ok=True)
        self.script_path = Path(self.script_dir / "merged.txt")
        self.prompt_path = Path(prompt_path)

    def __create_script(self) -> str:
        prompt = self.prompt_path.read_text()
        script = self.ai_service.generate(prompt)

        self.script_path.write_text(script)

        return script

    def __write_chunk(self, idx: int, content: str) -> None:
        chunk_path = self.script_dir / f"chunk_{idx:03}.txt"
        chunk_path.write_text(content.strip())

    def __create_chunks(self) -> None:
        text = self.script_path.read_text()
        sentences = re.split(r"(?<=[.!?])\s+", text)

        chunk = ""
        idx = 0

        for sentence in sentences:
            if len(chunk) + len(sentence) <= CHUNK_CHAR_LIMIT:
                chunk += sentence + " "
            else:
                self.__write_chunk(idx, chunk)
                chunk = sentence + " "
                idx += 1

        if chunk:
            self.__write_chunk(idx, chunk)

    def run(self) -> None:
        try:
            self.ai_service.start()
            self.__create_script()
        finally:
            self.ai_service.stop()

        self.__create_chunks()
