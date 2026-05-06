import json
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

from src.constants import FONTS_DIR, OUTPUT_DIR, AUDIO_DIR, CROPPED_IMAGES_DIR
from ..subtitle_service import SubtitleConfig, SubtitleService
from .constants import FPS


class VideoService:
    def __init__(self):
        self.font_path = FONTS_DIR / "Montserrat-Bold.ttf"
        self.output_path = OUTPUT_DIR / "product.mp4"
        self.audio_path = AUDIO_DIR / "merged.wav"
        self.timeline_path = AUDIO_DIR / "timeline.json"
        self.target_image_size = (1920, 1080)

        # ✅ Validation
        self.__validate_paths()

    def __validate_paths(self):
        if not self.timeline_path.exists():
            raise ValueError(f"Timeline file not found: {self.timeline_path}")

        if not self.audio_path.exists():
            raise ValueError(f"Audio file not found: {self.audio_path}")

        if not self.font_path.exists():
            raise ValueError(f"Font not found: {self.font_path}")

    def __load_timeline(self):
        with open(self.timeline_path) as f:
            timeline = json.load(f)

        if not timeline:
            raise RuntimeError("Timeline is empty!")

        return timeline

    def __create_image_clips(self, timeline):
        clips = []

        for scene in timeline:
            img_path = CROPPED_IMAGES_DIR / f"{scene['index']}.png"

            if not img_path.exists():
                raise ValueError(f"Missing image: {img_path}")

            total_duration = float(scene["duration"]) + float(scene["pause"])

            clip = (
                ImageClip(str(img_path))
                .resized(new_size=self.target_image_size)
                .with_start(float(scene["start"]))
                .with_duration(total_duration)
            )

            clips.append(clip)

        return clips

    def __get_total_duration(self, timeline):
        return max(
            float(scene["end"]) + float(scene["pause"])
            for scene in timeline
        )

    def __build_subtitles(self, timeline):
        subtitle_config = SubtitleConfig(
            font=str(self.font_path),
            fontsize=80,
            color="white",
            stroke_color="black",
            stroke_width=4,
            position="bottom",
            margin=100,
            wrap_width=30,
        )

        subtitle_service = SubtitleService(
            timeline=timeline,
            video_size=self.target_image_size,
            config=subtitle_config,
        )

        return subtitle_service.build()

    def run(self) -> None:
        # 📄 Timeline
        timeline = self.__load_timeline()

        # 🎬 Clips
        image_clips = self.__create_image_clips(timeline)

        # 💬 Subtitles
        subtitle_clips = self.__build_subtitles(timeline)

        # 🎯 Duration
        total_duration = self.__get_total_duration(timeline)

        # 🎥 Composite
        final_clip = (
            CompositeVideoClip(
                [*image_clips, *subtitle_clips],
                size=self.target_image_size,
            )
            .with_duration(total_duration)
        )

        # 🔊 Audio
        audio = AudioFileClip(str(self.audio_path))
        final_clip = final_clip.with_audio(audio)

        # 🎞️ Render
        final_clip.write_videofile(
            str(self.output_path),
            fps=FPS,
            codec="libx264",
            audio_codec="aac",
        )
