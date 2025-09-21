# acmecli/metrics/ramp_up.py
import time
from datetime import datetime, timezone
from huggingface_hub import model_info


def _cap_ratio(value, cap: int) -> float:
    """Return min(value/cap, 1.0). Handles None as 0.0."""
    if value is None:
        return 0.0
    try:
        return min(float(value) / cap, 1.0)
    except Exception:
        return 0.0


def _freshness_score(last_modified: str) -> float:
    """
    Convert lastModified timestamp to freshness score between 0 and 1.
    More recent = closer to 1.0. Returns fallback 0.3 on failure.
    """
    if not last_modified:
        return 0.3
    try:
        dt = datetime.fromisoformat(last_modified.replace("Z", "+00:00"))
        now = datetime.now(timezone.utc)
        delta_days = (now - dt).days
        if delta_days < 0:
            return 0.5  # future timestamps? fallback
        if delta_days < 30:
            return 1.0
        elif delta_days < 180:
            return 0.8
        elif delta_days < 365:
            return 0.6
        elif delta_days < 730:
            return 0.4
        else:
            return 0.2
    except Exception:
        return 0.3


def compute_ramp_up(model_id: str):
    """
    Compute a ramp-up score for a Hugging Face model based on:
    - Downloads
    - Likes
    - Freshness
    Returns (score, latency_ms).
    """
    start = time.time()
    try:
        info = model_info(model_id)
    except Exception:
        return (0.0, int((time.time() - start) * 1000))

    downloads = getattr(info, "downloads", None)
    likes = getattr(info, "likes", None)
    last_modified = getattr(info, "lastModified", None)

    d_score = _cap_ratio(downloads, 100_000)
    l_score = _cap_ratio(likes, 5_000)
    f_score = _freshness_score(last_modified)

    score = (d_score + l_score + f_score) / 3.0
    latency_ms = int((time.time() - start) * 1000)
    return (score, latency_ms)
