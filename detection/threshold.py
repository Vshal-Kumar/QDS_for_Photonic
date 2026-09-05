"""Static threshold derivation from baseline empirical percentiles."""

import numpy as np


def compute_static_threshold(
    baseline_tvds: np.ndarray,
    percentile: float = 95.0
) -> float:
    """Calculate a static decision threshold from the (100 - alpha)% percentile of normal TVD deviations."""
    if len(baseline_tvds) == 0:
        return 0.05
    val = float(np.percentile(baseline_tvds, percentile))
    return max(0.01, val)
