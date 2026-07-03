from typing import Protocol, Any


class OverlayProtocol(Protocol):
    def get_clip(self, total_duration) -> list[Any]:
        ...
