from pathlib import Path
from functools import wraps
from typing import Callable, Any

from src.utils.file_utils import safe_read_json, save_json
from ..timer_service import TimerService


class TimerServiceCache(TimerService):
    def __init__(self, cache_file=".timer_cache.json"):
        super().__init__()

        self.results = safe_read_json(cache_file, {})
        self.cache_file = Path(cache_file)

    def track(self, step_name: str):
        parent_decorator = super().track(step_name)

        def decorator(func: Callable) -> Callable:
            parent_wrapper = parent_decorator(func)

            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                result = parent_wrapper(*args, **kwargs)
                save_json(self.cache_file, self.results)
                return result

            return wrapper

        return decorator

    def summary(self):
        super().summary()
        self.cache_file.unlink()
