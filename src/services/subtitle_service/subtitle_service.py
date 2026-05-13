from typing import Any
from dataclasses import dataclass
from pathlib import Path
from moviepy.video.VideoClip import TextClip

from .subtitle_protocol import SubtitleProtocol


@dataclass
class SubtitleConfig:
    font: str
    fontsize: int = 60
    color: str = "white"
    active_color: str = "yellow"
    stroke_color: str = "black"
    stroke_width: int = 2
    position: str = "bottom"
    vertical_margin: int = 50
    words_per_chunk: int = 4
    word_spacing: int = 10


class SubtitleService(SubtitleProtocol):
    def __init__(
            self,
            timeline: list[dict[str, Any]],
            video_size: tuple[int, int],
            config: SubtitleConfig
    ):
        self.timeline = timeline
        self.video_width = int(video_size[0])
        self.video_height = int(video_size[1])
        self.config = config

        # ✅ Validation
        self.__validate_paths()

    def __validate_paths(self):
        if not Path(self.config.font).exists():
            raise ValueError(f"Font not found: {self.config.font}")

    def __get_y_position(self):
        if self.config.position == "bottom":
            return int(self.video_height - self.config.vertical_margin)

        if self.config.position == "top":
            return int(self.config.vertical_margin)

        return int(self.video_height / 2)

    def __create_text_clip(self, text: str, color: str):
        return TextClip(
            text=text,
            font=self.config.font,
            font_size=self.config.fontsize,
            color=color,
            stroke_color=self.config.stroke_color,
            stroke_width=self.config.stroke_width,
            transparent=True,
        )

    def __create_positioned_clip(
            self,
            text: str,
            color: str,
            start: float,
            duration: float,
            x: int,
            y: int,
    ):
        return (
            self.__create_text_clip(
                text=text,
                color=color,
            )
            .with_start(start)
            .with_duration(duration)
            .with_position((x, y))
        )

    def __create_measurement_clips(self, chunk_words: list[dict[str, Any]]):
        return [
            self.__create_text_clip(text=word_data["word"], color=self.config.color)
            for word_data in chunk_words
        ]

    def __calculate_total_width(self, measurement_clips: list[TextClip]):
        words_width = sum(clip.w for clip in measurement_clips)
        spacing_width = (len(measurement_clips) - 1) * self.config.word_spacing
        return words_width + spacing_width

    def __calculate_start_x(self, total_width: int):
        return int((self.video_width - total_width) / 2)

    def __create_active_clip(
            self,
            word_data: dict[str, Any],
            x: int,
            y: int,
    ):
        return self.__create_positioned_clip(
            text=word_data["word"],
            color=self.config.active_color,
            start=float(word_data["start"]),
            duration=float(word_data["end"]) - float(word_data["start"]),
            x=x,
            y=y,
        )

    def __create_inactive_clip(
            self,
            word_data: dict[str, Any],
            chunk_end: float,
            x: int,
            y: int,
    ):
        remaining_duration = chunk_end - float(word_data["end"])
        if remaining_duration <= 0:
            return None

        return self.__create_positioned_clip(
            text=word_data["word"],
            color=self.config.color,
            start=float(word_data["end"]),
            duration=remaining_duration,
            x=x,
            y=y,
        )

    def __build_word_clips(
            self,
            word_data: dict[str, Any],
            chunk_end: float,
            x: int,
            y: int,
    ):
        clips = []

        active_clip = self.__create_active_clip(word_data=word_data, x=x, y=y)
        clips.append(active_clip)

        inactive_clip = self.__create_inactive_clip(word_data=word_data, chunk_end=chunk_end, x=x, y=y)
        if inactive_clip:
            clips.append(inactive_clip)

        return clips

    def __build_chunk(self, chunk_words: list[dict[str, Any]]):
        clips = []

        measurement_clips = (self.__create_measurement_clips(chunk_words))
        total_width = self.__calculate_total_width(measurement_clips)

        current_x = self.__calculate_start_x(total_width)
        y = self.__get_y_position()

        chunk_end = float(chunk_words[-1]["end"])

        for index, word_data in enumerate(chunk_words):
            word_width = measurement_clips[index].w

            word_clips = self.__build_word_clips(
                word_data=word_data,
                chunk_end=chunk_end,
                x=current_x,
                y=y,
            )
            clips.extend(word_clips)

            current_x += word_width + self.config.word_spacing

        return clips

    def __chunk_words(self, words: list[dict[str, Any]]):
        chunk_size = self.config.words_per_chunk

        return [
            words[i:i + chunk_size]
            for i in range(0, len(words), chunk_size)
        ]

    def __build_scene(self, scene: dict[str, Any]):
        clips = []
        word_chunks = self.__chunk_words(scene["words"])

        for chunk_words in word_chunks:
            chunk_clips = self.__build_chunk(chunk_words)
            clips.extend(chunk_clips)

        return clips

    def get_clip(self):
        clips = []

        for scene in self.timeline:
            scene_clips = self.__build_scene(scene)
            clips.extend(scene_clips)

        return clips
