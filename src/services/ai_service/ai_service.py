from abc import ABC, abstractmethod


class AiService(ABC):
    @abstractmethod
    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def generate(self, prompt: str) -> str:
        pass
