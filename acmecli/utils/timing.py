# Latency measurement decorators
import time
from typing import Callable, Any, Tuple

def measure_latency(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Tuple[Any, int]:
        start = time.time()
        result = func(*args, **kwargs)
        latency = int((time.time() - start) * 1000)  # milliseconds
        return result, latency
    return wrapper
