from moviepy.video.VideoClip import TextClip, ImageClip


class BaseRenderer:
    def __init__(self, video_size: tuple[int, int]):
        self.video_width = int(video_size[0])
        self.video_height = int(video_size[1])

    @staticmethod
    def create_text_clip(text: str, font: str, fontsize: int, color: str, **kwargs):
        return TextClip(
            text=text,
            font=font,
            font_size=fontsize,
            color=color,
            transparent=True,
            **kwargs
        )

    @staticmethod
    def create_image_clip(image_path: str, **kwargs):
        return ImageClip(image_path, **kwargs)

    @staticmethod
    def place_clip(clip, x: int | float, y: int | float, start: float = 0.0, duration: float | None = None):
        positioned = clip.with_position((x, y)).with_start(start)

        if duration is not None:
            positioned = positioned.with_duration(duration)

        return positioned
