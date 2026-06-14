from src.core import OverlayProtocol, BaseRenderer
from src.utils.file_utils import validate_path
from .config import WatermarkConfig


class WatermarkService(BaseRenderer, OverlayProtocol):
    def __init__(self, config: WatermarkConfig, video_size: tuple[int, int]):
        super().__init__(video_size)
        self.config = config
        validate_path(self.config.font)

    def get_clip(self, total_duration: float = 0.0):
        clips = []

        # Text Watermark (Bottom Right)
        text_clip = self.create_text_clip(
            text=self.config.channel_name,
            font=self.config.font,
            fontsize=self.config.fontsize,
            color=self.config.color
        ).with_opacity(self.config.opacity)

        x_text = self.video_width - text_clip.w - self.config.margin
        y_text = self.video_height - text_clip.h - self.config.margin

        clips.append(
            self.place_clip(text_clip, x=x_text, y=y_text, duration=total_duration)
        )

        # Logo Watermark (Top Left)
        if self.config.logo_path:
            validate_path(self.config.logo_path)

            logo_clip = (
                self.create_image_clip(self.config.logo_path)
                .resized(new_size=(self.config.logo_width, self.config.logo_height))
                .with_opacity(self.config.opacity)
            )

            clips.append(
                self.place_clip(logo_clip, x=self.config.margin, y=self.config.margin, duration=total_duration)
            )

        return clips
