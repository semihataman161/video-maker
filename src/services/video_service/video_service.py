from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

from src.utils.timeline_utils import get_timeline
from src.constants import TARGET_IMAGE_SIZE, OUTPUT_DIR, AUDIO_DIR, CROPPED_IMAGES_DIR
from .constants import FPS


class VideoService:
    def __init__(self, subtitle_service=None):
        self.subtitle_service = subtitle_service

        self.output_path = OUTPUT_DIR / "product.mp4"
        self.audio_path = AUDIO_DIR / "merged.wav"

        # ✅ Validation
        self.__validate_paths()

    def __validate_paths(self):
        if not self.audio_path.exists():
            raise ValueError(f"Audio file not found: {self.audio_path}")

    def __create_image_clips(self, timeline):
        clips = []

        for scene in timeline:
            img_path = CROPPED_IMAGES_DIR / f"{scene['index']}.png"

            if not img_path.exists():
                raise ValueError(f"Missing image: {img_path}")

            total_duration = float(scene["duration"]) + float(scene["pause"])

            clip = (
                ImageClip(str(img_path))
                .resized(new_size=TARGET_IMAGE_SIZE)
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

    def run(self) -> None:
        # 📄 Timeline
        timeline = get_timeline()

        # 🎬 Image Clips
        image_clips = self.__create_image_clips(timeline)

        # 🎯 Base clips
        clips = [*image_clips]

        # 💬 Optional subtitles
        if self.subtitle_service:
            subtitle_clips = self.subtitle_service.build()
            clips.extend(subtitle_clips)

        # 🎯 Duration
        total_duration = self.__get_total_duration(timeline)

        # 🎥 Composite
        final_clip = (
            CompositeVideoClip(
                clips,
                size=TARGET_IMAGE_SIZE,
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
