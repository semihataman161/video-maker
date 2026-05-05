import json
from pathlib import Path
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

from ..constants import OUTPUT_DIR
from .constants import FPS


class VideoService:
    def __init__(
            self,
            images_dir=Path(OUTPUT_DIR / "images" / "cropped"),
            audio_path=Path(OUTPUT_DIR / "audio" / "output.wav"),
            timeline_path=Path(OUTPUT_DIR / "audio" / "timeline.json"),
            output_path=Path(OUTPUT_DIR / "product.mp4"),
    ):
        self.images_dir = Path(images_dir)
        self.audio_path = Path(audio_path)
        self.timeline_path = Path(timeline_path)
        self.output_path = Path(output_path)

        self.TARGET_SIZE = (1920, 1080)

    def run(self) -> None:
        if not self.timeline_path.exists():
            raise RuntimeError("Timeline file not found!")

        with open(self.timeline_path) as f:
            timeline = json.load(f)

        if not timeline:
            raise RuntimeError("Timeline is empty!")

        clips = []

        for scene in timeline:
            img_path = self.images_dir / f"{scene['index']}.png"

            if not img_path.exists():
                raise RuntimeError(f"Missing image: {img_path}")

            total_duration = scene["duration"] + scene["pause"]

            clip = (
                ImageClip(str(img_path))
                .resized(new_size=self.TARGET_SIZE)
                .with_start(scene["start"])
                .with_duration(total_duration)
            )

            clips.append(clip)

        total_video_duration = max(
            scene["end"] + scene["pause"] for scene in timeline
        )

        final_clip = (
            CompositeVideoClip(
                clips,
                size=self.TARGET_SIZE
            )
            .with_duration(total_video_duration)
        )

        if not self.audio_path.exists():
            raise RuntimeError("Audio file not found!")

        audio = AudioFileClip(str(self.audio_path))

        final_clip = final_clip.with_audio(audio)

        final_clip.write_videofile(
            str(self.output_path),
            fps=FPS,
            codec="libx264",
            audio_codec="aac",
        )
