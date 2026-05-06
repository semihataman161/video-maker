import time
from typing import Callable


class TimerService:
    def __init__(self):
        self.results = {}

    def __format_time(self, seconds: float) -> str:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"

    def measure(self, step_name: str, func: Callable):
        print(f"{step_name}...")
        start = time.perf_counter()

        func()

        end = time.perf_counter()
        duration = end - start

        self.results[step_name] = duration
        print(f"⏱ {step_name} took {self.__format_time(duration)}\n")

    def summary(self):
        print("\n📊 Execution Summary:")
        total = 0

        for step, duration in self.results.items():
            print(f" - {step}: {self.__format_time(duration)}")
            total += duration

        print(f"\n🚀 Total time: {self.__format_time(total)}")
