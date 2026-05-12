import math
import random
from typing import Literal
from moviepy.video.VideoClip import ImageClip

from src.constants import TARGET_IMAGE_SIZE
from .effect_protocol import EffectProtocol
from .constants import (
    LINEAR_MOTION_MAX_DURATION,
    OSCILLATION_SPEED,
    MAX_DYNAMIC_SCALE,
    PAN_SPEED,
    MAX_ZOOM,
    ZOOM_IN_PER_SECOND,
    ZOOM_OUT_PER_SECOND,
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

    def __get_resized_clip(self, clip: ImageClip, scale: float) -> ImageClip:
        new_size = (
            int(TARGET_IMAGE_SIZE[0] * scale),
            int(TARGET_IMAGE_SIZE[1] * scale),
        )
        return clip.resized(new_size=new_size)

    def __linear_zoom_in(self, clip: ImageClip) -> ImageClip:
        duration = clip.duration
        final_scale = min(MAX_ZOOM, 1 + (ZOOM_IN_PER_SECOND * duration))

        return clip.resized(
            lambda t: min(final_scale, 1 + (ZOOM_IN_PER_SECOND * t))
        )

    def __linear_zoom_out(self, clip: ImageClip) -> ImageClip:
        duration = clip.duration
        start_scale = min(MAX_ZOOM, 1 + (ZOOM_OUT_PER_SECOND * duration))
        resized_clip = self.__get_resized_clip(clip, start_scale)

        return resized_clip.resized(
            lambda t: max(1.0, start_scale - (ZOOM_OUT_PER_SECOND * t))
        )

    def __oscillating_zoom_in(self, clip: ImageClip) -> ImageClip:
        base_scale = 1 + (MAX_ZOOM - 1) / 2
        amplitude = (MAX_ZOOM - 1) / 2

        return clip.resized(
            lambda t: base_scale + (math.sin(t * OSCILLATION_SPEED) * amplitude)
        )

    def __oscillating_zoom_out(self, clip: ImageClip) -> ImageClip:
        base_scale = 1 + (MAX_ZOOM - 1) / 2
        amplitude = (MAX_ZOOM - 1) / 2

        return clip.resized(
            lambda t: base_scale - (math.sin(t * OSCILLATION_SPEED) * amplitude)
        )

    def __zoom_in(self, clip: ImageClip) -> ImageClip:
        if clip.duration <= LINEAR_MOTION_MAX_DURATION:
            return self.__linear_zoom_in(clip)

        return self.__oscillating_zoom_in(clip)

    def __zoom_out(self, clip: ImageClip) -> ImageClip:
        if clip.duration <= LINEAR_MOTION_MAX_DURATION:
            return self.__linear_zoom_out(clip)

        return self.__oscillating_zoom_out(clip)

    def __calculate_pan_scale(self, duration: float):
        required_extra_height = duration * PAN_SPEED
        required_scale = (TARGET_IMAGE_SIZE[1] + required_extra_height) / TARGET_IMAGE_SIZE[1]
        return min(MAX_DYNAMIC_SCALE, required_scale)

    def __get_vertical_limit(self, clip: ImageClip) -> float:
        extra_height = clip.h - TARGET_IMAGE_SIZE[1]
        return max(0, extra_height)

    def __linear_pan_up(self, clip: ImageClip) -> ImageClip:
        duration = clip.duration
        scale = self.__calculate_pan_scale(duration)
        resized_clip = self.__get_resized_clip(clip, scale)
        limit = self.__get_vertical_limit(resized_clip)

        return resized_clip.with_position(
            lambda t: ("center", max(-limit, -(PAN_SPEED * t)))
        )

    def __linear_pan_down(self, clip: ImageClip) -> ImageClip:
        duration = clip.duration
        scale = self.__calculate_pan_scale(duration)
        resized_clip = self.__get_resized_clip(clip, scale)
        limit = self.__get_vertical_limit(resized_clip)

        return resized_clip.with_position(
            lambda t: ("center", min(0, -limit + (PAN_SPEED * t)))
        )

    def __oscillating_pan_up(self, clip: ImageClip) -> ImageClip:
        resized_clip = self.__get_resized_clip(clip, MAX_DYNAMIC_SCALE)
        limit = self.__get_vertical_limit(resized_clip)
        amplitude = limit / 2

        return resized_clip.with_position(
            lambda t: ("center", -amplitude + (math.sin(t * OSCILLATION_SPEED) * amplitude))
        )

    def __oscillating_pan_down(self, clip: ImageClip) -> ImageClip:
        resized_clip = self.__get_resized_clip(clip, MAX_DYNAMIC_SCALE)
        limit = self.__get_vertical_limit(resized_clip)
        amplitude = limit / 2

        return resized_clip.with_position(
            lambda t: ("center", -amplitude - (math.sin(t * OSCILLATION_SPEED) * amplitude))
        )

    def __pan_up(self, clip: ImageClip) -> ImageClip:
        if clip.duration <= LINEAR_MOTION_MAX_DURATION:
            return self.__linear_pan_up(clip)

        return self.__oscillating_pan_up(clip)

    def __pan_down(self, clip: ImageClip) -> ImageClip:
        if clip.duration <= LINEAR_MOTION_MAX_DURATION:
            return self.__linear_pan_down(clip)

        return self.__oscillating_pan_down(clip)

    def get_clip(self, clip: ImageClip):
        effects = {
            "zoom_in": self.__zoom_in,
            "zoom_out": self.__zoom_out,
            "pan_up": self.__pan_up,
            "pan_down": self.__pan_down,
        }

        if self.mode == "random":
            effect_functions = list(effects.values())
            selected_effect = random.choice(effect_functions)
            return selected_effect(clip)

        return effects[self.mode](clip)
