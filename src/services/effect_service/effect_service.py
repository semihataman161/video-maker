import random
from typing import Literal

from .effect_protocol import EffectProtocol

EffectMode = Literal[
    "random",
    "zoom_in",
    "zoom_out",
    "pan_up",
    "pan_down",
]


class EffectService(EffectProtocol):
    ZOOM_IN_PER_SECOND = 0.01
    MAX_ZOOM_IN = 1.15

    ZOOM_OUT_PER_SECOND = 0.01
    MAX_ZOOM_OUT = 1.0

    PAN_SPEED = 8

    def __init__(self, mode: EffectMode):
        self.mode = mode

    def __zoom_in(self, clip):
        return clip.resized(
            lambda t: min(
                self.MAX_ZOOM_IN,
                1 + (self.ZOOM_IN_PER_SECOND * t)
            )
        )

    def __zoom_out(self, clip):
        return clip.resized(
            lambda t: max(
                self.MAX_ZOOM_OUT,
                self.MAX_ZOOM_IN - (
                        self.ZOOM_OUT_PER_SECOND * t
                )
            )
        )

    def __pan_up(self, clip):
        return clip.with_position(
            lambda t: (
                "center",
                -(self.PAN_SPEED * t)
            )
        )

    def __pan_down(self, clip):
        duration = clip.duration
        total_movement = (self.PAN_SPEED * duration)

        return clip.with_position(
            lambda t: (
                "center",
                -total_movement + (
                        self.PAN_SPEED * t
                )
            )
        )

    def get_clip(self, clip):
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
