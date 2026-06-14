from typing import Protocol
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip


class OutroProtocol(Protocol):
    def get_clip(self, duration: float) -> CompositeVideoClip:
        ...
