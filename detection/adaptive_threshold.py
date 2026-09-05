"""Adaptive distance- and measurement-shot-aware statistical threshold engine."""

import numpy as np
import scipy.stats
from detection.baseline import BaselineProfile


def compute_adaptive_threshold(
    baseline_profile: BaselineProfile,
    shots: int = 1000,
    significance_level_alpha: float = 0.05,
    critical_factor: float = 2.2
) -> tuple[float, float]:
    """Compute adaptive decision threshold tau(L, N) and critical threshold tau_crit(L, N).
    
    Mathematical Scaling:
    By the Central Limit Theorem for empirical distributions:
        E[D_TV(N)] = E[D_TV(N_ref)] * sqrt(N_ref / N)
        Std[D_TV(N)] = Std[D_TV(N_ref)] * sqrt(N_ref / N)
        
    Primary Threshold tau(L, N, alpha):
        tau = E[D_TV(N)] + z_(1-alpha) * Std[D_TV(N)] + delta_channel(L)
        
    Critical Threshold tau_crit(L, N):
        tau_crit = critical_factor * tau
    """
    n_ref = 1000.0
    n_actual = max(10, shots // 3)  # Shots per basis
    shot_scale = np.sqrt(n_ref / n_actual)
    
    # Scaled baseline mean TVD and standard deviation for actual shot count
    mu_d0 = baseline_profile.mean_tvd * shot_scale
    sigma_d0 = float(np.sqrt(np.mean(baseline_profile.variance_vector))) * shot_scale
    
    # One-tailed normal quantile (e.g. z_0.95 = 1.645)
    z_quantile = float(scipy.stats.norm.ppf(1.0 - significance_level_alpha))
    
    # Distance-dependent optical channel dispersion offset
    distance_offset = 0.00025 * baseline_profile.distance_km
    
    # Primary Adaptive Threshold
    tau = mu_d0 + (z_quantile * sigma_d0) + distance_offset
    tau = float(max(0.025, min(0.40, tau)))
    
    # Critical Decision Threshold
    tau_crit = float(min(0.65, tau * critical_factor))
    
    return tau, tau_crit
