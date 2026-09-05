"""Statistical hypothesis testing: Null Hypothesis H0 (Normal) vs Alternative H1 (Attack)."""

from dataclasses import dataclass, field
from typing import Dict, Tuple
import numpy as np
import scipy.stats


@dataclass
class HypothesisTestResult:
    """Outcome of statistical hypothesis testing."""
    reject_null_h0: bool
    significance_level_alpha: float
    z_scores: Dict[str, float] = field(default_factory=dict)
    max_z_score: float = 0.0
    log_likelihood_ratio: float = 0.0
    critical_z_value: float = 1.96
    summary: str = ""


def compute_z_scores(
    observed_probs: np.ndarray,
    baseline_probs: np.ndarray,
    shots: int = 1000,
    keys: list[str] = None
) -> Tuple[Dict[str, float], float]:
    """Compute Z-score test statistics for each measurement bin:
    
    Formula:
        z_i = (p_hat_i - p_0_i) / sqrt(p_0_i * (1 - p_0_i) / N)
    """
    obs = np.asarray(observed_probs, dtype=float)
    base = np.asarray(baseline_probs, dtype=float)
    
    if keys is None:
        keys = [f"bin_{i}" for i in range(len(obs))]
        
    z_dict: Dict[str, float] = {}
    max_z = 0.0
    
    for i, k in enumerate(keys):
        p0 = base[i]
        p_hat = obs[i]
        
        # Standard error under H0
        se = np.sqrt(max(1e-10, p0 * (1.0 - p0) / max(1, shots)))
        z = (p_hat - p0) / se
        z_dict[k] = float(z)
        if abs(z) > max_z:
            max_z = abs(float(z))
            
    return z_dict, max_z


def evaluate_hypothesis_test(
    observed_probs: np.ndarray,
    baseline_probs: np.ndarray,
    shots: int = 1000,
    alpha: float = 0.05,
    keys: list[str] = None
) -> HypothesisTestResult:
    """Execute two-tailed statistical hypothesis test against significance level alpha."""
    z_dict, max_z = compute_z_scores(observed_probs, baseline_probs, shots, keys)
    
    # Critical two-tailed Z value for significance alpha (e.g., alpha=0.05 -> z_crit=1.96)
    z_crit = float(scipy.stats.norm.ppf(1.0 - alpha / 2.0))
    
    # Compute Log-Likelihood Ratio (LLR)
    eps = 1e-12
    obs_safe = np.clip(observed_probs, eps, 1.0)
    base_safe = np.clip(baseline_probs, eps, 1.0)
    llr = float(shots * np.sum(obs_safe * np.log(obs_safe / base_safe)))
    
    reject_h0 = max_z > z_crit
    
    summary = (
        f"Reject H0: Statistical manipulation detected (Max |Z| = {max_z:.2f} > {z_crit:.2f})"
        if reject_h0 else
        f"Accept H0: Observations consistent with normal channel (Max |Z| = {max_z:.2f} <= {z_crit:.2f})"
    )
    
    return HypothesisTestResult(
        reject_null_h0=reject_h0,
        significance_level_alpha=alpha,
        z_scores=z_dict,
        max_z_score=max_z,
        log_likelihood_ratio=llr,
        critical_z_value=z_crit,
        summary=summary
    )
