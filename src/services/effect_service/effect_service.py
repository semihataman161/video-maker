import random
from typing import Literal
from moviepy.video.VideoClip import ImageClip

from src.constants import TARGET_IMAGE_SIZE
from .effect_protocol import EffectProtocol
from .constants import SAFE_SCALE, ZOOM_IN_PER_SECOND, ZOOM_OUT_PER_SECOND, MAX_ZOOM, PAN_SPEED

EffectMode = Literal[
    "random",
    "zoom_in",
    "zoom_out",
    "pan_up",
    "pan_down",
]


class EffectService(EffectProtocol):
    def __init__(self, mode: EffectMode):
        self.mode = mode

    def __get_resized_clip(self, clip: ImageClip):
        overscaled_size = (
            int(TARGET_IMAGE_SIZE[0] * SAFE_SCALE),
            int(TARGET_IMAGE_SIZE[1] * SAFE_SCALE),
        )
        return clip.resized(new_size=overscaled_size)

    def __get_vertical_limit(self, clip: ImageClip):
        extra_height = clip.h - TARGET_IMAGE_SIZE[1]

        if extra_height < 0:
            return 0

        return extra_height

    def __zoom_in(self, clip: ImageClip):
        duration = clip.duration

        final_scale = min(MAX_ZOOM, 1 + (ZOOM_IN_PER_SECOND * duration))

        return clip.resized(
            lambda t: min(final_scale, 1 + (ZOOM_IN_PER_SECOND * t))
        )

    def __zoom_out(self, clip: ImageClip):
        resized_clip = self.__get_resized_clip(clip)
        duration = resized_clip.duration

        start_scale = min(MAX_ZOOM, 1 + (ZOOM_OUT_PER_SECOND * duration))

        return resized_clip.resized(
            lambda t: max(1.0, start_scale - (ZOOM_OUT_PER_SECOND * t))
        )

    def __pan_up(self, clip: ImageClip):
        resized_clip = self.__get_resized_clip(clip)
        limit = self.__get_vertical_limit(resized_clip)

        return resized_clip.with_position(
            lambda t: ("center", max(-limit, -(PAN_SPEED * t)))
        )

    def __pan_down(self, clip: ImageClip):
        resized_clip = self.__get_resized_clip(clip)
        limit = self.__get_vertical_limit(resized_clip)

        return resized_clip.with_position(
            lambda t: ("center", min(0, -limit + (PAN_SPEED * t)))
        )

    def get_clip(self, clip: ImageClip):
        effects = {
            "zoom_in": self.__zoom_in,
            "zoom_out": self.__zoom_out,
            "pan_up": self.__pan_up,
            "pan_down": self.__pan_down,
        }

        if self.mode == "random":
            selected_effect = random.choice(list(effects.values()))
            return selected_effect(clip)

        return effects[self.mode](clip)
