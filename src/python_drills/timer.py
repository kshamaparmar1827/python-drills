import time
from typing import Self


class Timer:
    def __init__(self, label: str) -> None:
        self.label = label
        self.start = 0
        self.elapsed = 0

    def __enter__(self) -> Self:
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.elapsed = time.perf_counter() - self.start
        print(f"[{self.label}] took {self.elapsed:.3f}s")
