from pathlib import Path
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

from ..constants import OUTPUT_DIR
from .constants import FPS


class VideoService:
    def __init__(
            self,
            images_dir=Path(OUTPUT_DIR / "images"),
            audio_path=Path(OUTPUT_DIR / "audio" / "merged.wav"),
            output_path=Path(OUTPUT_DIR / "product.mp4"),
    ):
        self.images_dir = Path(images_dir)
        self.audio_path = Path(audio_path)
        self.output_path = Path(output_path)

    def __create(self) -> None:
        images = sorted(self.images_dir.glob("*.jpg"))

        if not images:
            raise RuntimeError("No images created!")

        audio = AudioFileClip(str(self.audio_path))

        duration_per_image = audio.duration / len(images)

        clip = ImageSequenceClip(
            [str(img) for img in images],
            fps=1 / duration_per_image,
        )

        clip = clip.with_audio(audio)

        clip.write_videofile(
            str(self.output_path),
            fps=FPS,
            codec="libx264",
            audio_codec="aac",
        )

    def run(self) -> None:
        self.__create()
