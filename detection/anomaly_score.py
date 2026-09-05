"""Composite anomaly score computation based on calibrated statistical hypothesis tests."""

import numpy as np


def compute_composite_anomaly_score(
    total_variation_distance: float,
    adaptive_threshold: float,
    critical_threshold: float,
    chi_square_p_value: float,
    max_z_score: float,
    qds_mismatch_rate: float,
    significance_alpha: float = 0.05
) -> float:
    """Compute a deterministic, calibrated composite anomaly score in [0.0, 1.0].
    
    Calibration Rules:
    1. TVD component:
       - TVD <= tau: [0.0, 0.25] (normal shot fluctuation)
       - tau < TVD <= tau_crit: [0.25, 0.60] (suspicious region)
       - TVD > tau_crit: [0.60, 1.00] (critical state perturbation)
    2. Chi-square p-value component:
       - p >= alpha: 0.0 (H0 not rejected)
       - p < alpha: scales linearly from 0.0 to 1.0 as p -> 0
    3. Z-score component:
       - max_z <= 1.96: 0.0 (within 95% normal confidence interval)
       - max_z > 1.96: scales linearly (max_z - 1.96) / 3.0 up to 1.0
    4. QDS mismatch component:
       - mismatch <= 0.15: 0.0 (below QDS threshold)
       - mismatch > 0.15: scales up to 1.0
    """
    # 1. TVD score
    if total_variation_distance <= adaptive_threshold:
        score_tvd = 0.25 * (total_variation_distance / max(1e-6, adaptive_threshold))
    elif total_variation_distance <= critical_threshold:
        interp = (total_variation_distance - adaptive_threshold) / max(1e-6, critical_threshold - adaptive_threshold)
        score_tvd = 0.25 + (0.35 * interp)
    else:
        score_tvd = 0.60 + 0.40 * min(1.0, (total_variation_distance - critical_threshold) / max(1e-6, 1.0 - critical_threshold))
        
    # 2. Chi-square hypothesis score (only activates when H0 is rejected at level alpha)
    if chi_square_p_value >= significance_alpha:
        score_chi2 = 0.0
    else:
        score_chi2 = float(np.clip(1.0 - (chi_square_p_value / max(1e-6, significance_alpha)), 0.0, 1.0))
        
    # 3. Z-score component (only activates beyond 95% critical value 1.96)
    if max_z_score <= 1.96:
        score_z = 0.0
    else:
        score_z = float(np.clip((max_z_score - 1.96) / 3.0, 0.0, 1.0))
        
    # 4. QDS mismatch component
    if qds_mismatch_rate <= 0.15:
        score_mismatch = 0.0
    else:
        score_mismatch = float(np.clip((qds_mismatch_rate - 0.15) / 0.35, 0.0, 1.0))
        
    # Weighted linear combination
    composite = (
        0.40 * score_tvd +
        0.25 * score_chi2 +
        0.20 * score_z +
        0.15 * score_mismatch
    )
    
    return float(np.clip(composite, 0.0, 1.0))
