from dataclasses import dataclass


@dataclass
class WatermarkConfig:
    channel_name: str
    logo_path: str | None = None
    font: str = "Arial"
    fontsize: int = 40
    color: str = "white"
    opacity: float = 0.7
    margin: int = 30
