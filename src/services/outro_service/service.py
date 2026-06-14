from moviepy.video.VideoClip import ColorClip, ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

from src.constants import TARGET_IMAGE_SIZE
from src.utils.file_utils import validate_path
from .protocol import OutroProtocol


class OutroService(OutroProtocol):
    def __init__(self, image_path: str, image_size: tuple[int, int], bg_color: tuple[int, int, int] = (0, 0, 0)):
        self.image_path = image_path
        self.image_size = image_size
        self.bg_color = bg_color

        validate_path(self.image_path)

    def get_clip(self, duration):
        bg_clip = ColorClip(size=TARGET_IMAGE_SIZE, color=self.bg_color).with_duration(duration)

        image_clip = (
            ImageClip(str(self.image_path))
            .resized(new_size=self.image_size)
            .with_duration(duration)
            .with_position(("center", "center"))
        )

        return CompositeVideoClip([bg_clip, image_clip], size=TARGET_IMAGE_SIZE)
