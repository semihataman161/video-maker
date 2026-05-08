from typing import Protocol
from moviepy.video.VideoClip import VideoClip


class EffectProtocol(Protocol):
    def get_clip(self, clip: VideoClip) -> VideoClip:
        ...
