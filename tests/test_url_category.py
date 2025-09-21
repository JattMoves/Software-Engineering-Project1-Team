from acmecli.url_category import detect_category

def test_detect_model():
    url = "https://huggingface.co/google/gpt2"
    assert detect_category(url) == "MODEL"
