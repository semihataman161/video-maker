from pathlib import Path
import json
from moviepy.editor import ImageClip, concatenate_videoclips
from moviepy.audio.io.AudioFileClip import AudioFileClip

from ..constants import OUTPUT_DIR
from .constants import FPS


class VideoService:
    def __init__(
            self,
            images_dir=Path(OUTPUT_DIR / "images"),
            audio_path=Path(OUTPUT_DIR / "audio" / "output.wav"),
            timeline_path=Path(OUTPUT_DIR / "audio" / "timeline.json"),
            output_path=Path(OUTPUT_DIR / "product.mp4"),
    ):
        self.images_dir = Path(images_dir)
        self.audio_path = Path(audio_path)
        self.timeline_path = Path(timeline_path)
        self.output_path = Path(output_path)

    def run(self) -> None:
        if not self.timeline_path.exists():
            raise RuntimeError("Timeline file not found!")

        with open(self.timeline_path) as f:
            timeline = json.load(f)

        clips = []

        for scene in timeline:
            img_path = self.images_dir / f"{scene['index']}.png"

            if not img_path.exists():
                raise RuntimeError(f"Missing image: {img_path}")

            clip = ImageClip(str(img_path)).set_duration(scene["duration"])
            clips.append(clip)

        final_clip = concatenate_videoclips(clips, method="compose")

        audio = AudioFileClip(str(self.audio_path))
        final_clip = final_clip.set_audio(audio)

        final_clip.write_videofile(
            str(self.output_path),
            fps=FPS,
            codec="libx264",
            audio_codec="aac",
        )
