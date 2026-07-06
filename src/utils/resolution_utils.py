from src.constants import RESOLUTIONS


def get_size_by_resolution(key) -> tuple[int, int]:
    if key not in RESOLUTIONS:
        raise ValueError(
            f"Unsupported resolution: '{key}'. "
            f"Available options: {', '.join(RESOLUTIONS.keys())}"
        )
    return RESOLUTIONS[key]
