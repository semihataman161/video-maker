import time
from typing import Callable, Any
from functools import wraps


class TimerService:
    def __init__(self):
        self.results = {}

    @staticmethod
    def __format_time(seconds: float):
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes} minutes, {secs} seconds"

    def track(self, step_name: str):
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Any:
                print(f"{step_name}...")
                start = time.perf_counter()

                result = func(*args, **kwargs)

                end = time.perf_counter()
                duration = end - start

                self.results[step_name] = duration
                print(f"⏱ {step_name} took {self.__format_time(duration)}\n")

                return result

            return wrapper

        return decorator

    def summary(self):
        print("\n📊 Execution Summary:")
        total = 0

        for step, duration in self.results.items():
            print(f" - {step}: {self.__format_time(duration)}")
            total += duration

        print(f"\n🚀 Total time: {self.__format_time(total)}")
