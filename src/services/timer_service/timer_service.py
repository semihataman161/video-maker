import time
from typing import Callable


class TimerService:
    def __init__(self):
        self.results = {}

    def measure(self, step_name: str, func: Callable):
        print(f"{step_name}...")
        start = time.perf_counter()

        func()

        end = time.perf_counter()
        duration = end - start

        self.results[step_name] = duration
        print(f"⏱ {step_name} took {duration:.2f} seconds\n")

    def summary(self):
        print("\n📊 Execution Summary:")
        total = 0

        for step, duration in self.results.items():
            print(f" - {step}: {duration:.2f}s")
            total += duration

        print(f"\n🚀 Total time: {total:.2f}s")
