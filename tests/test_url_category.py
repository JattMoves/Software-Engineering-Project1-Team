from acmecli.url_category import detect_category, model_id_from_hf_url


def test_detect_model():
    assert detect_category("https://huggingface.co/google/gemma-2b/tree/main") == "MODEL"
    assert detect_category("https://huggingface.co/google/gpt2") == "MODEL"


def test_detect_dataset():
    assert detect_category("https://huggingface.co/datasets/xlangai/AgentNet") == "DATASET"


def test_detect_github_code():
    assert detect_category("https://github.com/user/repo") == "CODE"


def test_model_id_parse():
    assert model_id_from_hf_url("https://huggingface.co/google/gpt2") == "google/gpt2"
    assert model_id_from_hf_url("https://huggingface.co/org/model/subpath") == "org/model"
    assert model_id_from_hf_url("https://huggingface.co/datasets/org/ds") is None

