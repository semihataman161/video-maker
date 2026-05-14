from pathlib import Path
from typing import Iterable


def create_directory(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def create_directories(paths: Iterable[Path]):
    for path in paths:
        create_directory(path)


def validate_path(path: str):
    if not Path(path).exists():
        raise ValueError(f"File not found: {path}")


def validate_paths(paths: list[str]):
    for path in paths:
        validate_path(path)
