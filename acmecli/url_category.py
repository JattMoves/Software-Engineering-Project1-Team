"""
URL categorization utilities for ACME CLI.

Functions:
- detect_category(url) -> "MODEL" | "DATASET" | "CODE" | "UNKNOWN"
- model_id_from_hf_url(url) -> "org/model" | None
"""

from __future__ import annotations

from typing import Literal, Optional
from urllib.parse import urlparse

Category = Literal["MODEL", "DATASET", "CODE", "UNKNOWN"]


def detect_category(url: str) -> Category:
    """
    Classify a URL into one of the supported categories.

    Rules (Phase 1):
      - Hugging Face dataset URLs contain '/datasets/'
      - Hugging Face model URLs are on huggingface.co but NOT '/datasets/'
      - GitHub repo URLs are code
      - Otherwise: UNKNOWN
    """
    if not url:
        return "UNKNOWN"

    parsed = urlparse(url)
    host = parsed.netloc.lower()
    path = parsed.path.lower()

    if "huggingface.co" in host:
        if path.startswith("/datasets/") or "/datasets/" in path:
            return "DATASET"
        return "MODEL"

    if "github.com" in host:
        return "CODE"

    return "UNKNOWN"


def model_id_from_hf_url(url: str) -> Optional[str]:
    """
    Extract 'org/model' from a Hugging Face MODEL url.
    Returns None for dataset/invalid URLs.
    Examples:
      https://huggingface.co/google/gpt2                -> google/gpt2
      https://huggingface.co/google/gpt2/tree/main      -> google/gpt2
      https://huggingface.co/datasets/xlangai/AgentNet  -> None
    """
    if not url:
        return None

    parsed = urlparse(url)
    if "huggingface.co" not in parsed.netloc.lower():
        return None

    parts = parsed.path.strip("/").split("/")
    if not parts or parts[0] == "datasets":
        return None

    # Need at least org + model
    if len(parts) >= 2:
        return f"{parts[0]}/{parts[1]}"
    return None
