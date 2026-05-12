from typing import Protocol
from moviepy.video.VideoClip import ImageClip


class EffectProtocol(Protocol):
    def get_clip(self, clip: ImageClip) -> ImageClip:
        ...
