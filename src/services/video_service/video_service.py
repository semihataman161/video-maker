from pathlib import Path
from typing import Any
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

from src.utils.timeline_utils import get_timeline, get_total_duration
from src.constants import (TARGET_IMAGE_SIZE, CROPPED_IMAGES_DIR)
from ..effect_service import EffectProtocol
from ..subtitle_service import SubtitleProtocol
from .constants import FPS, AUDIO_PATH, OUTPUT_PATH


class VideoService:
    def __init__(
            self,
            subtitle_service: SubtitleProtocol | None = None,
            effect_service: EffectProtocol | None = None,
    ):
        self.subtitle_service = subtitle_service
        self.effect_service = effect_service

        # ✅ Validation
        self.__validate_paths()

    def __validate_paths(self):
        if not AUDIO_PATH.exists():
            raise ValueError(f"Audio file not found: {AUDIO_PATH}")

    def __create_image_clip(self, img_path: Path, start: float, total_duration: float):
        clip = (
            ImageClip(str(img_path))
            .resized(new_size=TARGET_IMAGE_SIZE)
            .with_start(start)
            .with_duration(total_duration)
        )

        if self.effect_service:
            return self.effect_service.get_clip(clip)

        return clip

    def __create_image_clips(self, timeline: list[dict[str, Any]]):
        clips = []

        for scene in timeline:
            img_path = CROPPED_IMAGES_DIR / f"{scene['index']}.png"

            if not img_path.exists():
                raise ValueError(f"Missing image: {img_path}")

            total_duration = float(scene["duration"]) + float(scene["pause"])

            clip = self.__create_image_clip(
                img_path=img_path,
                start=float(scene["start"]),
                total_duration=total_duration,
            )

            clips.append(clip)

        return clips

    def run(self):
        # 📄 Timeline
        timeline = get_timeline()

        # 🎬 Image Clips
        image_clips = self.__create_image_clips(timeline)

        # 🎯 Base clips
        clips = [*image_clips]

        # 💬 Optional subtitles
        if self.subtitle_service:
            subtitle_clips = self.subtitle_service.get_clip()
            clips.extend(subtitle_clips)

        # 🎯 Duration
        total_duration = get_total_duration(timeline)

        # 🎥 Composite
        final_clip = (
            CompositeVideoClip(
                clips,
                size=TARGET_IMAGE_SIZE,
            )
            .with_duration(total_duration)
        )

        # 🔊 Audio
        audio = AudioFileClip(str(AUDIO_PATH))
        final_clip = final_clip.with_audio(audio)

        # 🎞️ Render
        final_clip.write_videofile(
            str(OUTPUT_PATH),
            fps=FPS,
            codec="libx264",
            audio_codec="aac",
        )
