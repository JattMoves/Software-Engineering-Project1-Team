# acmecli/run.py
import json
from acmecli.url_category import detect_category, model_id_from_hf_url
from acmecli.metrics import ramp_up


def run_urls(filename: str) -> int:
    """
    Read URLs from a file, detect category, compute ramp-up metrics (if MODEL),
    and print each result as a JSON line.
    Returns exit code 0 on success.
    """
    with open(filename, "r") as f:
        for line in f:
            url = line.strip()
            if not url:
                continue

            category = detect_category(url)
            rec = {
                "url": url,
                "category": category,
            }

            if category == "MODEL":
                model_id = model_id_from_hf_url(url)
                if model_id:
                    score, latency_ms = ramp_up.compute_ramp_up(model_id)
                    rec["ramp_up_time"] = latency_ms
                    rec["net_score"] = score

            print(json.dumps(rec))

    return 0
