from pathlib import Path

from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

from .constants import FPS


class VideoService:
    def __init__(
            self,
            images_dir: str = "output/images",
            audio_path: str = "output/audio/merged.wav",
            output_path: str = "output/product.mp4",
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
