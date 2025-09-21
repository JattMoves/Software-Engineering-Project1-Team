import types
from acmecli.metrics import ramp_up


def test_cap_ratio():
    assert ramp_up._cap_ratio(0, 100) == 0.0
    assert ramp_up._cap_ratio(100, 100) == 1.0
    assert ramp_up._cap_ratio(150, 100) == 1.0
    assert ramp_up._cap_ratio(None, 100) == 0.0


def test_freshness_score_bounds():
    s = ramp_up._freshness_score(None)
    assert 0.0 <= s <= 1.0
    assert ramp_up._freshness_score("invalid-date") == 0.3


def test_compute_ramp_up_monkeypatch(monkeypatch):
    fake = types.SimpleNamespace(downloads=50_000, likes=2_500, lastModified="2025-01-01T00:00:00Z")

    def fake_model_info(model_id):
        return fake

    monkeypatch.setattr(ramp_up, "model_info", fake_model_info)

    score, latency_ms = ramp_up.compute_ramp_up("google/gpt2")
    assert 0.0 <= score <= 1.0
    assert isinstance(latency_ms, int) and latency_ms >= 0


def test_compute_ramp_up_perf(monkeypatch):
    fake = types.SimpleNamespace(downloads=1, likes=1, lastModified="2025-01-01T00:00:00Z")
    monkeypatch.setattr(ramp_up, "model_info", lambda m: fake)
    score, latency_ms = ramp_up.compute_ramp_up("org/model")
    assert isinstance(latency_ms, int)
    assert latency_ms >= 0
