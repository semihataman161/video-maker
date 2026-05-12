from pathlib import Path
from typing import Iterable


def create_directory(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def create_directories(paths: Iterable[Path]):
    for path in paths:
        create_directory(path)
