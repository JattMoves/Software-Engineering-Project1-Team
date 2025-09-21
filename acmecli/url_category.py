# acmecli/url_category.py
# acmecli/url_category.py
from urllib.parse import urlparse


def detect_category(url: str) -> str | None:
    """
    Detect category of a given URL:
    - Hugging Face model: "MODEL"
    - Hugging Face dataset: "DATASET"
    - GitHub repo: "CODE"
    """
    if not url:
        return None

    parsed = urlparse(url)
    host = parsed.netloc.lower()
    path = parsed.path.strip("/")

    if "huggingface.co" in host:
        if path.startswith("datasets/"):
            return "DATASET"
        return "MODEL"
    if "github.com" in host:
        return "CODE"
    return None


def model_id_from_hf_url(url: str) -> str | None:
    """
    Extract model ID (e.g. 'org/model') from a Hugging Face model URL.
    Returns None for dataset URLs.
    """
    parsed = urlparse(url)
    path_parts = parsed.path.strip("/").split("/")
    if not path_parts or path_parts[0] == "datasets":
        return None
    # at least org + model
    if len(path_parts) >= 2:
        return f"{path_parts[0]}/{path_parts[1]}"
    return None
