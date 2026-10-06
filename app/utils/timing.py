import time
from contextlib import contextmanager


@contextmanager
def measure_elapsed(label: str):
    start = time.perf_counter()
    yield
    elapsed_ms = (time.perf_counter() - start) * 1000
    print(f"{label}: {elapsed_ms:.2f} ms")
