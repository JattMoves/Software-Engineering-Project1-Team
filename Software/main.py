"""Shim module to expose MLEvaluator as Software.main for tests.

This imports the real implementation from the top-level `main.py` in the
project root (which is on sys.path during tests).
"""
from main import MLEvaluator, main as run_main  # re-export symbols from project main

__all__ = ["MLEvaluator", "run_main"]
