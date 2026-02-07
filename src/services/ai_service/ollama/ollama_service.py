import subprocess
import socket
import time
from typing import Optional

from ..ai_service import AiService


class OllamaService(AiService):
    def __init__(
            self,
            model: str,
            host: str = "127.0.0.1",
            port: int = 11434,
            startup_timeout: int = 10,
    ):
        self.model = model
        self.host = host
        self.port = port
        self.startup_timeout = startup_timeout
        self._process: Optional[subprocess.Popen] = None

    def __is_running(self) -> bool:
        try:
            with socket.create_connection((self.host, self.port), timeout=1):
                return True
        except OSError:
            return False

    def __wait_until_ready(self) -> None:
        start_time = time.time()

        while time.time() - start_time < self.startup_timeout:
            if self.__is_running():
                return
            time.sleep(0.5)

        raise RuntimeError("❌ Ollama server failed to start")

    def start(self) -> None:
        if self.__is_running():
            return

        print("🦙 Starting Ollama server...")
        self._process = subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        self.__wait_until_ready()

    def stop(self) -> None:
        if self._process and self._process.poll() is None:
            print("🛑 Stopping Ollama server...")
            self._process.terminate()
            self._process.wait(timeout=5)
            self._process = None

    def generate(self, prompt: str) -> str:
        result = subprocess.run(
            ["ollama", "run", self.model],
            input=prompt,
            text=True,
            capture_output=True,
            check=True,
        )
        return result.stdout.strip()
