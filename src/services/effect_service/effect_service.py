import random
from typing import Literal
from moviepy.video.VideoClip import ImageClip

from src.constants import TARGET_IMAGE_SIZE
from .effect_protocol import EffectProtocol
from .constants import (
    MAX_DYNAMIC_SCALE,
    ZOOM_IN_PER_SECOND,
    ZOOM_OUT_PER_SECOND,
    MAX_ZOOM,
    PAN_SPEED
)

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

    def __calculate_pan_scale(self, duration: float):
        required_extra_height = duration * PAN_SPEED
        required_scale = (TARGET_IMAGE_SIZE[1] + required_extra_height) / TARGET_IMAGE_SIZE[1]
        return min(MAX_DYNAMIC_SCALE, required_scale)

    def __get_resized_clip(self, clip: ImageClip, scale: float) -> ImageClip:
        resized_size = (
            int(TARGET_IMAGE_SIZE[0] * scale),
            int(TARGET_IMAGE_SIZE[1] * scale),
        )
        return clip.resized(new_size=resized_size)

    def __get_vertical_limit(self, clip: ImageClip) -> float:
        extra_height = clip.h - TARGET_IMAGE_SIZE[1]
        return max(0, extra_height)

    def __zoom_in(self, clip: ImageClip) -> ImageClip:
        duration = clip.duration
        final_scale = min(MAX_ZOOM, 1 + (ZOOM_IN_PER_SECOND * duration))

        return clip.resized(
            lambda t: min(final_scale, 1 + (ZOOM_IN_PER_SECOND * t))
        )

    def __zoom_out(self, clip: ImageClip) -> ImageClip:
        duration = clip.duration
        start_scale = min(MAX_ZOOM, 1 + (ZOOM_OUT_PER_SECOND * duration))
        resized_clip = self.__get_resized_clip(clip, start_scale)

        return resized_clip.resized(
            lambda t: max(1.0, start_scale - (ZOOM_OUT_PER_SECOND * t))
        )

    def __pan_up(self, clip: ImageClip) -> ImageClip:
        duration = clip.duration
        scale = self.__calculate_pan_scale(duration)
        resized_clip = self.__get_resized_clip(clip, scale)
        limit = self.__get_vertical_limit(resized_clip)

        return resized_clip.with_position(
            lambda t: ("center", max(-limit, -(PAN_SPEED * t)))
        )

    def __pan_down(self, clip: ImageClip) -> ImageClip:
        duration = clip.duration
        scale = self.__calculate_pan_scale(duration)
        resized_clip = self.__get_resized_clip(clip, scale)
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
