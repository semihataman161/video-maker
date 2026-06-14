from dataclasses import dataclass


@dataclass
class WatermarkConfig:
    channel_name: str
    logo_path: str | None = None
    logo_width: int | None = None
    logo_height: int | None = None
    font: str = "Arial"
    fontsize: int = 40
    color: str = "white"
    opacity: float = 0.7
    margin: int = 30

    def __post_init__(self):
        if self.logo_path and (self.logo_width is None or self.logo_height is None):
            raise ValueError(
                "ValueError: 'logo_width' and 'logo_height' are required when 'logo_path' is provided."
            )
