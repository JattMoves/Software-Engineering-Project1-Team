import json
import time
from huggingface_hub import list_models, model_info

def compute_net_score(ramp_up_score: float) -> float:
    """For M3, NetScore = ramp_up_score only (others = 0)."""
    return ramp_up_score

def output_result(model_id: str, ramp_up_score: float, ramp_up_latency: int):
    """Prints one NDJSON line with all required fields (Table 1)."""

    start_net = time.perf_counter_ns()
    net_score = compute_net_score(ramp_up_score)
    net_latency = int((time.perf_counter_ns() - start_net) / 1_000_000)  # ms

    result = {
        "name": model_id,
        "category": "MODEL",
        "net_score": net_score,
        "net_score_latency": net_latency,
        "ramp_up_time": ramp_up_score,
        "ramp_up_time_latency": ramp_up_latency,
        "documentation": 0,
        "documentation_latency": 0,
        "license": 0,
        "license_latency": 0,
        "bus_factor": 0,
        "bus_factor_latency": 0,
        "correctness": 0,
        "correctness_latency": 0,
        "test": 0,
        "test_latency": 0,
        "ci": 0,
        "ci_latency": 0,
        "lgtm": 0,
        "lgtm_latency": 0,
        "responsiveness": 0,
        "responsiveness_latency": 0
    }

    print(json.dumps(result))

models = list_models(filter="text-generation", limit=5)

for model in models:
    t0 = time.perf_counter_ns()
    info = model_info(model.modelId)
    ramp_latency = int((time.perf_counter_ns() - t0) / 1_000_000)  # ms

    downloads = getattr(info, "downloads", 0) or 0
    ramp_up_score = min(downloads, 100000) / 100000  # simple normalization

    # Output NDJSON line
    output_result(model.modelId, ramp_up_score, ramp_latency)
