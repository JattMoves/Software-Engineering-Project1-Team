from acmecli.metrics.ramp_up import _cap_ratio, _freshness_score

def test_cap_ratio():
    assert _cap_ratio(0, 100) == 0.0
    assert _cap_ratio(100, 100) == 1.0
    assert _cap_ratio(150, 100) == 1.0

def test_freshness_brackets():
    assert 0.3 <= _freshness_score(None) <= 1.0  # tolerant default path
