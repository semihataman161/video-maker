import numpy as np
from typing import Literal
from moviepy import VideoFileClip, VideoClip, ColorClip, vfx

from src.core import OverlayProtocol
from src.utils.resolution_utils import get_size_by_resolution
from src.constants import VIDEO_RESOLUTION


class OverlayVideoService(OverlayProtocol):
    """
    Applies a pre-rendered particle or visual effect overlay on top of the scene.

    Overlay modes (choose based on the source overlay video):

        - "transparent"
          Uses an overlay video with a transparent alpha channel
          (e.g. ProRes 4444 MOV or VP9 WebM).
          This is the highest-quality option. The overlay is composited
          directly using its alpha channel without any blend mode.

        - "light_overlay"
          Uses a light-colored overlay on a black background.
          Internally applies Screen blending, making the black background
          disappear while preserving bright elements such as dust, sparks,
          smoke, light leaks, or glowing particles.

        - "dark_overlay"
          Uses a dark-colored overlay on a white or light background.
          Internally applies Multiply blending, causing the white background
          disappear while preserving dark elements such as film dust,
          scratches, dirt, or vintage film damage.
    """

    def __init__(
            self,
            video_path,
            mode: Literal["transparent", "light_overlay", "dark_overlay"],
            opacity: float = 1.0
    ):
        self.video_path = str(video_path)
        self.mode = mode
        self.opacity = opacity

        self.size = get_size_by_resolution(VIDEO_RESOLUTION)

    @staticmethod
    def __luma(frame: np.ndarray) -> np.ndarray:
        f = frame.astype("float32") / 255.0
        return 0.2126 * f[:, :, 0] + 0.7152 * f[:, :, 1] + 0.0722 * f[:, :, 2]

    def get_clip(self, total_duration: float):
        has_mask = (self.mode == "transparent")
        clip = (
            VideoFileClip(self.video_path, has_mask=has_mask)
            .resized(self.size)
            .with_effects([vfx.Loop(duration=total_duration)])
            .with_duration(total_duration)
        )

        if self.mode == "transparent":
            if self.opacity < 1.0 and clip.mask is not None:
                clip = clip.with_mask(
                    clip.mask.image_transform(lambda f: f * self.opacity)
                )
            return [clip]

        if self.mode == "light_overlay":
            mask = VideoClip(
                frame_function=lambda t: self.__luma(clip.get_frame(t)) * self.opacity,
                duration=total_duration,
                is_mask=True,
            )
            return [clip.with_mask(mask)]

        if self.mode == "dark_overlay":
            mask = VideoClip(
                frame_function=lambda t: (1.0 - self.__luma(clip.get_frame(t))) * self.opacity,
                duration=total_duration,
                is_mask=True,
            )
            black = ColorClip(self.size, color=(0, 0, 0)).with_duration(total_duration)
            return [black.with_mask(mask)]
