import json
from pathlib import Path
from functools import wraps
from typing import Callable, Any

from src.utils.file_utils import validate_path
from ..timer_service import TimerService


class TimerServiceCache(TimerService):
    def __init__(self, cache_file=".timer_cache.json"):
        super().__init__()

        self.cache_file = Path(cache_file)

        loaded_results = self.__load()
        if loaded_results:
            self.results = loaded_results

    def __load(self) -> dict:
        if self.cache_file.exists():
            try:
                with open(self.cache_file, "r", encoding="utf-8") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                return {}
        return {}

    def __save(self):
        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=4)

    def track(self, step_name: str):
        parent_decorator = super().track(step_name)

        def decorator(func: Callable) -> Callable:
            parent_wrapper = parent_decorator(func)

            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                result = parent_wrapper(*args, **kwargs)
                self.__save()
                return result

            return wrapper

        return decorator

    def summary(self):
        super().summary()

        if validate_path(self.cache_file):
            self.cache_file.unlink()
