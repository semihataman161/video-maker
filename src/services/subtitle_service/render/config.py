from dataclasses import dataclass


@dataclass
class SubtitleRenderConfig:
    font: str
    fontsize: int = 60
    color: str = "white"
    active_color: str = "yellow"
    stroke_color: str = "black"
    stroke_width: int = 2
    position: str = "bottom"
    vertical_margin: int = 50
    word_spacing: int = 10
