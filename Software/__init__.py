"""Compatibility package so tests can import `Software.main`.

This package dynamically loads the real `main.py` from the project root and
re-exports key symbols (MLEvaluator, etc.).
"""

from .main import *  # pragma: no cover
