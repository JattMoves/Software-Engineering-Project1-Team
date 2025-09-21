from typing import Protocol, Tuple

class Metric(Protocol):
    def compute(self, model_id: str) -> Tuple[float, int]:
        """Return (score in [0,1], latency_ms)."""
        ...
