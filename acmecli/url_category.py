# url_category.py
"""
Module for classifying and handling different URL types (MODEL, DATASET, CODE).
"""

import re
from typing import Literal

Category = Literal["MODEL", "DATASET", "CODE", "UNKNOWN"]

class URLHandler:
    """Base class for URL handling."""

    def __init__(self, url: str):
        self.url = url

    def get_category(self) -> Category:
        raise NotImplementedError("Subclasses must implement this method")


class HFModelHandler(URLHandler):
    """Handles Hugging Face model URLs."""

    def get_category(self) -> Category:
        if "huggingface.co" in self.url and "/datasets/" not in self.url:
            return "MODEL"
        return "UNKNOWN"


class HFDatasetHandler(URLHandler):
    """Handles Hugging Face dataset URLs."""

    def get_category(self) -> Category:
        if "huggingface.co/datasets/" in self.url:
            return "DATASET"
        return "UNKNOWN"


class GitHubHandler(URLHandler):
    """Handles GitHub code repository URLs."""

    def get_category(self) -> Category:
        if "github.com" in self.url:
            return "CODE"
        return "UNKNOWN"


def categorize_url(url: str) -> Category:
    """
    Determines the category of a given URL.
    """
    handlers = [HFModelHandler(url), HFDatasetHandler(url), GitHubHandler(url)]
    for handler in handlers:
        category = handler.get_category()
        if category != "UNKNOWN":
            return category
    return "UNKNOWN"
