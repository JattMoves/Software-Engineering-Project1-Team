import pytest

from acmecli.metrics.ramp_up import ramp_up


@pytest.mark.timeout(15)
def test_ramp_up_returns_tuple_and_ranges():
    score, ms = ramp_up("google/gpt2")
    assert isinstance(score, float)
    assert 0.0 <= score <= 1.0
    assert isinstance(ms, int)
    assert ms >= 0
