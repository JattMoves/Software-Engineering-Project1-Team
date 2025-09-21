import time
from datetime import datetime, timezone
from huggingface_hub import model_info
from requests.exceptions import RequestException

CAP_DOWNLOADS = 100_000
CAP_LIKES = 5_000

def _cap_ratio(x: int | None, cap: int) -> float:
    if not x or x < 0: return 0.0
    return min(x, cap) / cap

def _freshness_score(last_modified: str | None) -> float:
    try:
        dt = datetime.fromisoformat(last_modified.replace("Z","+00:00")).astimezone(timezone.utc)
        days = (datetime.now(timezone.utc) - dt).days
    except Exception:
        return 0.3
    if days <= 90: return 1.0
    if days <= 180: return 0.8
    if days <= 365: return 0.5
    return 0.3

def compute_ramp_up(model_id: str) -> tuple[float, int]:
    t0 = time.perf_counter_ns()
    try:
        info = model_info(model_id)
        downloads = getattr(info, "downloads", None)
        likes = getattr(info, "likes", None)
        last = getattr(info, "lastModified", None)
    except (RequestException, Exception):
        # If HF API is unreachable, gated, or errors, return safe defaults
        ms = int((time.perf_counter_ns() - t0) / 1_000_000)
        return 0.0, ms

    d = _cap_ratio(downloads, CAP_DOWNLOADS)
    l = _cap_ratio(likes, CAP_LIKES)
    f = _freshness_score(last)

    score = 0.4*d + 0.4*l + 0.2*f
    ms = int((time.perf_counter_ns() - t0) / 1_000_000)
    return (max(0.0, min(1.0, float(score))), ms)
