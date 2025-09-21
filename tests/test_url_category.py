from acmecli.url_category import detect_category, model_id_from_hf_url

def test_detect_model():
    assert detect_category("https://huggingface.co/google/gemma-2b/tree/main") == "MODEL"

def test_detect_dataset():
    assert detect_category("https://huggingface.co/datasets/xlangai/AgentNet") == "DATASET"

def test_model_id_parse():
    assert model_id_from_hf_url("https://huggingface.co/google/gpt2") == "google/gpt2"
