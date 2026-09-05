"""Pearson's Chi-Square Goodness-of-Fit test and p-value calculation."""

from typing import Tuple
import numpy as np
import scipy.stats


def compute_chi_square_test(
    observed_distribution: np.ndarray,
    expected_distribution: np.ndarray,
    shots: int = 1000,
    eps: float = 1e-6
) -> Tuple[float, float, int]:
    """Execute Pearson's Chi-Square Goodness-of-Fit test between observed and expected distributions.
    
    Formula:
        chi^2 = sum_i (O_i - E_i)^2 / E_i
        where O_i = shots * observed_i and E_i = shots * expected_i.
        
    Returns:
        chi2_statistic (float): Pearson's chi-square test statistic.
        p_value (float): Probability of observing chi2 >= statistic under H0 (normal channel).
        dof (int): Degrees of freedom (k - 1).
    """
    obs = np.asarray(observed_distribution, dtype=float)
    exp = np.asarray(expected_distribution, dtype=float)
    
    # Scale to counts
    o_counts = obs * shots
    e_counts = exp * shots
    
    # Avoid division by zero
    e_counts = np.clip(e_counts, eps, None)
    
    chi2_stat = float(np.sum(((o_counts - e_counts) ** 2) / e_counts))
    dof = max(1, len(obs) - 1)
    
    # Survival function sf = 1 - cdf (exact tail probability)
    p_val = float(scipy.stats.chi2.sf(chi2_stat, df=dof))
    
    return chi2_stat, p_val, dof
