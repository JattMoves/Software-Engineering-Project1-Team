import pytest

from acmecli.url_category import detect_category, model_id_from_hf_url


def test_detect_category_model_basic():
    url = "https://huggingface.co/google/gpt2"
    assert detect_category(url) == "MODEL"


def test_detect_category_dataset_basic():
    url = "https://huggingface.co/datasets/xlangai/AgentNet"
    assert detect_category(url) == "DATASET"


def test_detect_category_code_basic():
    url = "https://github.com/huggingface/transformers"
    assert detect_category(url) == "CODE"


def test_detect_category_unknown():
    assert detect_category("https://example.com/whatever") == "UNKNOWN"
    assert detect_category("") == "UNKNOWN"


def test_model_id_from_hf_url_happy_and_ignores_datasets():
    assert model_id_from_hf_url("https://huggingface.co/google/gpt2") == "google/gpt2"
    assert model_id_from_hf_url("https://huggingface.co/google/gpt2/tree/main") == "google/gpt2"
    assert model_id_from_hf_url("https://huggingface.co/datasets/xlangai/AgentNet") is None
    assert model_id_from_hf_url("https://github.com/huggingface/transformers") is None
