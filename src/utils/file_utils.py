from pathlib import Path
from typing import Iterable


def create_directory(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def create_directories(paths: Iterable[Path]):
    for path in paths:
        create_directory(path)


def validate_path(path: Path | str):
    if Path(path).exists():
        return path
    else:
        raise ValueError(f"File not found: {path}")


def validate_paths(paths: list[str]):
    for path in paths:
        validate_path(path)


def get_next_filename(directory: str, extension: str = ".png", prefix: str = ""):
    validate_path(directory)

    dir_path = Path(directory)

    max_num = 0
    existing_files = dir_path.glob(f"{prefix}*{extension}")

    for f in existing_files:
        name_without_prefix = f.stem
        if prefix and name_without_prefix.startswith(prefix):
            name_without_prefix = name_without_prefix[len(prefix):]

        if name_without_prefix.isdigit():
            max_num = max(max_num, int(name_without_prefix))

    return str(dir_path / f"{prefix}{max_num + 1}{extension}")
