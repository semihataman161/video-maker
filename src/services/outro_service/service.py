from moviepy.video.VideoClip import ColorClip, ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.fx.FadeIn import FadeIn

from src.utils.file_utils import validate_path
from src.utils.resolution_utils import get_resolution
from src.constants import VIDEO_RESOLUTION
from .protocol import OutroProtocol


class OutroService(OutroProtocol):
    def __init__(self, image_path: str, image_size: tuple[int, int], bg_color: tuple[int, int, int] = (0, 0, 0)):
        self.image_path = image_path
        self.resolution = get_resolution(VIDEO_RESOLUTION)
        self.bg_color = bg_color

        scale_factor = self.resolution[1] / 1080.0

        self.dynamic_image_size = (
            int(image_size[0] * scale_factor),
            int(image_size[1] * scale_factor)
        )

        validate_path(self.image_path)

    def get_clip(self, duration):
        bg_clip = ColorClip(size=self.resolution, color=self.bg_color).with_duration(duration)

        image_clip = (
            ImageClip(str(self.image_path))
            .resized(new_size=self.dynamic_image_size)
            .with_duration(duration)
            .with_position(("center", "center"))
        )

        composite = CompositeVideoClip([bg_clip, image_clip], size=self.resolution)
        return composite.with_effects([FadeIn(duration=1.0)])
