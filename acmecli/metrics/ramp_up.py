def _cap_ratio(numerator: float, denominator: float) -> float:
    """
    Simple utility to safely divide and cap result to [0,1].
    Example: _cap_ratio(50, 100) = 0.5
    """
    if denominator <= 0:
        return 0.0
    ratio = numerator / denominator
    return max(0.0, min(1.0, ratio))
