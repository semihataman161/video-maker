import subprocess
from pathlib import Path

from .constants import LLM_MODEL, CHUNK_CHAR_LIMIT

BASE_DIR = Path(__file__).parent


class ScriptService:
    def __init__(
            self,
            output_dir: str = "output",
            chunks_dir: str = "output/chunks",
            script_path: str = "output/script.txt",
            prompt_path: Path = BASE_DIR / "prompts" / "story_prompt.txt",
    ):
        self.output_dir = Path(output_dir)
        self.chunks_dir = Path(chunks_dir)
        self.script_path = Path(script_path)
        self.prompt_path = Path(prompt_path)

    def __create(self) -> str:
        prompt = self.prompt_path.read_text()

        result = subprocess.run(
            ["ollama", "run", LLM_MODEL],
            input=prompt,
            text=True,
            capture_output=True,
            check=True,
        )

        script = result.stdout.strip()

        self.output_dir.mkdir(exist_ok=True)
        self.script_path.write_text(script)

        return script

    def __write_chunk(self, idx: int, content: str) -> None:
        chunk_path = self.chunks_dir / f"chunk_{idx:03}.txt"
        chunk_path.write_text(content.strip())

    def __create_chunks(self) -> None:
        text = self.script_path.read_text()
        sentences = text.split(". ")

        self.chunks_dir.mkdir(parents=True, exist_ok=True)

        chunk = ""
        idx = 0

        for sentence in sentences:
            if len(chunk) + len(sentence) < CHUNK_CHAR_LIMIT:
                chunk += sentence + ". "
            else:
                self.__write_chunk(idx, chunk)
                chunk = sentence + ". "
                idx += 1

        if chunk:
            self.__write_chunk(idx, chunk)

    def run(self) -> None:
        self.__create()
        self.__create_chunks()
