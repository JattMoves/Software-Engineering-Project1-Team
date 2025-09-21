from urllib.parse import urlparse

def detect_category(url: str) -> str:
    # MODEL: https://huggingface.co/<org>/<model>[/...]
    # DATASET: https://huggingface.co/datasets/<org>/<ds>
    # CODE (heuristic): github.com/<org>/<repo>
    p = urlparse(url)
    host, path = p.netloc, p.path.strip("/")
    if host == "huggingface.co" and not path.startswith("datasets/") and len(path.split("/")) >= 2:
        return "MODEL"
    if host == "huggingface.co" and path.startswith("datasets/"):
        return "DATASET"
    if host in {"github.com", "gitlab.com"}:
        return "CODE"
    return "UNKNOWN"

def model_id_from_hf_url(url: str) -> str | None:
    p = urlparse(url)
    if p.netloc != "huggingface.co":
        return None
    parts = p.path.strip("/").split("/")
    if parts and parts[0] == "datasets":
        return None
    if len(parts) >= 2:
        return f"{parts[0]}/{parts[1]}"
    return None
