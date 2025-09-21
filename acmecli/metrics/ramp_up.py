"""
Ramp-up metric for Hugging Face models.

Returns:
  ramp_up(model_id) -> tuple[float, int]
    - score in [0, 1]
    - latency_ms (int >= 0)
"""

from __future__ import annotations

import time
from typing import Tuple

from huggingface_hub import model_info


def _cap_ratio(value: int | None, cap: int) -> float:
    """min(value/cap, 1.0); handles None and bad inputs as 0.0."""
    try:
        if value is None:
            return 0.0
        return min(float(value) / float(cap), 1.0)
    except Exception:
        return 0.0


def ramp_up(model_id: str) -> Tuple[float, int]:
    """
    Heuristic ramp-up score using lightweight HF Hub signals:
      - docs present (README)                         -> +0.30
      - example files present (.ipynb, example*, demo)-> +0.25
      - downloads (capped at 50k)                     -> +0.25 * ratio
      - likes (capped at 500)                         -> +0.20 * ratio

    The exact operationalization can evolve later; this is an MVP that is
    fast, deterministic, and requires no repo clone.
    """
    t0 = time.perf_counter()
    score = 0.0

    try:
        info = model_info(model_id)

        # README present?
        has_readme = any(s.rfilename.lower() in {"readme.md", "readme"} for s in info.siblings)
        if has_readme:
            score += 0.30

        # Any quick-start style files?
        name_l = [s.rfilename.lower() for s in info.siblings]
        has_examples = any(
            n.endswith(".ipynb") or n.startswith("example") or "demo" in n or "usage" in n
            for n in name_l
        )
        if has_examples:
            score += 0.25

        # Popularity as a proxy for discoverability/low-surprise setup
        score += 0.25 * _cap_ratio(getattr(info, "downloads", None), cap=50_000)
        score += 0.20 * _cap_ratio(getattr(info, "likes", None), cap=500)

        # Clamp to [0,1]
        score = max(0.0, min(score, 1.0))

    except Exception:
        # On any error, return neutral-low score (0.0) but still a latency value.
        score = 0.0

    latency_ms = int(round((time.perf_counter() - t0) * 1000))
    if latency_ms < 0:
        latency_ms = 0
    return float(score), int(latency_ms)
