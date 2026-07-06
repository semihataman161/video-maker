from src.core import OverlayProtocol, BaseRenderer
from src.utils.file_utils import try_validate_path
from src.utils.resolution_utils import get_size_by_resolution
from src.constants import VIDEO_RESOLUTION
from .config import WatermarkConfig


class WatermarkService(BaseRenderer, OverlayProtocol):
    def __init__(self, config: WatermarkConfig):
        size = get_size_by_resolution(VIDEO_RESOLUTION)
        super().__init__(size)

        self.config = config

        self.scale_factor = self.video_height / 1080.0

        self.dynamic_fontsize = int(self.config.fontsize * self.scale_factor)
        self.dynamic_margin = int(self.config.margin * self.scale_factor)
        self.dynamic_logo_width = int(self.config.logo_width * self.scale_factor)
        self.dynamic_logo_height = int(self.config.logo_height * self.scale_factor)

        try_validate_path(self.config.font)

    def get_clip(self, total_duration: float = 0.0):
        clips = []

        # Text Watermark (Bottom Right)
        text_clip = self.create_text_clip(
            text=self.config.channel_name,
            font=self.config.font,
            fontsize=self.dynamic_fontsize,
            color=self.config.color
        ).with_opacity(self.config.opacity)

        x_text = self.video_width - text_clip.w - self.dynamic_margin
        y_text = self.video_height - text_clip.h - self.dynamic_margin

        clips.append(
            self.place_clip(text_clip, x=x_text, y=y_text, duration=total_duration)
        )

        # Logo Watermark (Top Left)
        if self.config.logo_path:
            try_validate_path(self.config.logo_path)

            logo_clip = (
                self.create_image_clip(self.config.logo_path)
                .resized(new_size=(self.dynamic_logo_width, self.dynamic_logo_height))
                .with_opacity(self.config.opacity)
            )

            clips.append(
                self.place_clip(
                    logo_clip,
                    x=self.dynamic_margin,
                    y=self.dynamic_margin,
                    duration=total_duration
                )
            )

        return clips
