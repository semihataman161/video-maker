import json
from pathlib import Path
from typing import Iterable


def create_directory(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def create_directories(paths: Iterable[Path]):
    for path in paths:
        create_directory(path)


def is_path_exist(path: Path | str):
    return Path(path).exists()


def try_validate_path(path: Path | str):
    if is_path_exist(path):
        return path
    else:
        raise ValueError(f"File not found: {path}")


def validate_paths(paths: list[str]):
    for path in paths:
        try_validate_path(path)


def safe_validate_path(path: Path | str):
    if is_path_exist(path):
        return path
    else:
        return False


def get_next_file_path(directory: str, extension: str = ".png", prefix: str = ""):
    try_validate_path(directory)

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


def get_filename(file_path: Path | str):
    return Path(file_path).name


def __read_file(file_path: Path | str, encoding: str = "utf-8"):
    with open(file_path, "r", encoding=encoding) as file:
        return file.read()


def safe_read_file(file_path: Path | str, encoding: str = "utf-8"):
    is_exist = safe_validate_path(file_path)
    if not is_exist:
        return ""

    return __read_file(file_path, encoding)


def try_read_file(file_path: Path | str, encoding: str = "utf-8"):
    try_validate_path(file_path)
    return __read_file(file_path, encoding)


def safe_read_json(file_path: Path | str, default_value: dict | list, encoding: str = "utf-8"):
    file_content = safe_read_file(file_path, encoding)

    if not file_content.strip():
        return default_value

    return json.loads(file_content)


def try_read_json(file_path: Path | str, encoding: str = "utf-8"):
    file_content = try_read_file(file_path, encoding)
    return json.loads(file_content)


def save_file(file_path: Path | str, content: str, encoding: str = "utf-8"):
    parent_dir = Path(file_path).parent
    try_validate_path(parent_dir)

    with open(file_path, "w", encoding=encoding) as file:
        file.write(content)


def save_json(file_path: Path | str, content: dict | list, indent: int = 4, encoding: str = "utf-8"):
    json_content = json.dumps(content, indent=indent, ensure_ascii=False)
    save_file(file_path, json_content, encoding)
