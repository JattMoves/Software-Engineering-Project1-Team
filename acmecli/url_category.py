def detect_category(url: str) -> str:
    """
    Detects whether a Hugging Face URL points to a MODEL, DATASET, or SPACE.
    Returns one of: 'MODEL', 'DATASET', 'SPACE'
    """
    if "/datasets/" in url:
        return "DATASET"
    elif "/spaces/" in url:
        return "SPACE"
    else:
        return "MODEL"
