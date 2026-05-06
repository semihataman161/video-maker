import textwrap
from dataclasses import dataclass
from pathlib import Path
from moviepy.video.VideoClip import TextClip


@dataclass
class SubtitleConfig:
    font: str
    fontsize: int = 60
    color: str = "white"
    stroke_color: str = "black"
    stroke_width: int = 2
    position: str = "bottom"
    margin: int = 50
    wrap_width: int = 40


class SubtitleService:
    def __init__(self, timeline, video_size, config: SubtitleConfig):
        self.timeline = timeline
        self.video_width = int(video_size[0])
        self.video_height = int(video_size[1])
        self.config = config

        # ✅ Validation
        self.__validate_paths()

    def __validate_paths(self):
        if not Path(self.config.font).exists():
            raise ValueError(f"Font not found: {self.config.font}")

    def __wrap_text(self, text: str) -> str:
        return "\n".join(
            textwrap.wrap(text, width=self.config.wrap_width)
        )

    def __get_position(self):
        if self.config.position == "bottom":
            return "center", int(self.video_height - self.config.margin)
        elif self.config.position == "top":
            return "center", int(self.config.margin)
        return "center", "center"

    def __create_clip(self, scene):
        wrapped_text = self.__wrap_text(scene["text"])
        max_width = int(self.video_width * 0.8)

        clip = (
            TextClip(
                text=wrapped_text,
                font=self.config.font,
                font_size=int(self.config.fontsize),
                color=self.config.color,
                stroke_color=self.config.stroke_color,
                stroke_width=int(self.config.stroke_width),
                method="caption",
                size=(max_width, None),
            )
            .with_start(float(scene["start"]))
            .with_duration(float(scene["duration"]))
            .with_position(self.__get_position())
        )

        return clip

    def build(self):
        subtitle_clips = []

        for scene in self.timeline:
            subtitle_clips.append(self.__create_clip(scene))

        return subtitle_clips
