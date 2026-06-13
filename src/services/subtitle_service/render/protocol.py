from typing import Protocol
from collections.abc import Sequence
from moviepy.video.VideoClip import VideoClip


class SubtitleRenderProtocol(Protocol):
    def get_clip(self) -> Sequence[VideoClip]:
        ...
