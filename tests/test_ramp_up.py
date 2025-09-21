from acmecli.metrics.ramp_up import _cap_ratio

def test_cap_ratio_basic():
    assert _cap_ratio(50, 100) == 0.5
