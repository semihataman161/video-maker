from pathlib import Path
from typing import Any
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.fx.CrossFadeIn import CrossFadeIn

from src.core import OverlayProtocol
from src.utils.timeline_utils import get_timeline, get_total_duration
from src.utils.file_utils import validate_path
from src.utils.resolution_utils import get_resolution
from src.constants import RESOLUTION, CROPPED_IMAGES_DIR, OUTPUT_DIR
from ..effect_service import EffectProtocol
from ..outro_service import OutroProtocol
from .constants import FPS, AUDIO_PATH


class VideoService:
    def __init__(
            self,
            overlays: list[OverlayProtocol] = None,
            effect_service: EffectProtocol | None = None,
            outro_service: OutroProtocol = None,
    ):
        self.overlays = overlays or []
        self.effect_service = effect_service
        self.outro_service = outro_service

        self.resolution = get_resolution(RESOLUTION)

        validate_path(AUDIO_PATH)

    def __create_image_clip(self, img_path: Path, start: float, total_duration: float):
        clip = (
            ImageClip(str(img_path))
            .resized(new_size=self.resolution)
            .with_start(start)
            .with_duration(total_duration)
        )

        # 💬 Optional effects
        if self.effect_service:
            return self.effect_service.get_clip(clip)

        return clip

    def __create_image_clips(self, timeline: list[dict[str, Any]]):
        clips = []
        total_scenes = len(timeline)

        TRANSITION_INTERVAL = 6
        CROSSFADE_DURATION = 0.5

        for index, scene in enumerate(timeline):
            total_duration = float(scene["duration"]) + float(scene["pause"])
            start_time = float(scene["start"])

            if index == total_scenes - 1 and self.outro_service:
                outro_clip = self.outro_service.get_clip(duration=total_duration)
                outro_clip = outro_clip.with_start(start_time)
                clips.append(outro_clip)
                continue

            img_path = CROPPED_IMAGES_DIR / f"{scene['index']}.png"

            if not img_path.exists():
                raise ValueError(f"Missing image: {img_path}")

            is_transition_scene = (index > 0) and (index % TRANSITION_INTERVAL == 0)

            if is_transition_scene:
                start_time = max(0.0, start_time - CROSSFADE_DURATION)
                total_duration += CROSSFADE_DURATION

            clip = self.__create_image_clip(
                img_path=img_path,
                start=start_time,
                total_duration=total_duration,
            )

            if is_transition_scene:
                clip = clip.with_effects([CrossFadeIn(duration=CROSSFADE_DURATION)])

            clips.append(clip)

        return clips

    def run(self):
        # 📄 Timeline
        timeline = get_timeline()
        total_duration = get_total_duration(timeline)

        # 🎬 Image Clips
        image_clips = self.__create_image_clips(timeline)
        clips = [*image_clips]

        # 💬 Optional overlays
        for overlay in self.overlays:
            overlay_clips = overlay.get_clip(total_duration=total_duration)
            clips.extend(overlay_clips)

        final_clip = (
            CompositeVideoClip(
                clips,
                size=self.resolution,
            )
            .with_duration(total_duration)
        )

        # 🔊 Audio
        audio = AudioFileClip(str(AUDIO_PATH))
        final_clip = final_clip.with_audio(audio)

        output_path = OUTPUT_DIR / f"product_{RESOLUTION}.mp4"

        # 🎞️ Render
        final_clip.write_videofile(
            str(output_path),
            fps=FPS,
            codec="libx264",
            audio_codec="aac",
        )

        print(f"✅ DONE → {output_path}")
