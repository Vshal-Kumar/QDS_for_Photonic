"""Analytical and empirical evaluation of Quantum Digital Signature forgery probabilities."""

from dataclasses import dataclass
from typing import List
import scipy.special
from core.results import SimulationResult


@dataclass
class ForgeryAnalysisResult:
    """Summary of forgery probability analysis."""
    signature_qubit_count: int
    mismatch_threshold: float
    theoretical_forgery_upper_bound: float
    empirical_forgery_trials: int
    forged_signatures_accepted: int
    empirical_forgery_probability: float


def compute_theoretical_forgery_bound(
    signature_qubit_count: int = 16,
    mismatch_threshold: float = 0.15,
    single_qubit_guess_success: float = 0.50
) -> float:
    """Compute the analytical upper bound on forgery probability P_forge(K, delta).
    
    Formula:
        P_forge <= sum_{m=0}^{floor(delta * K)} C(K, m) * (p_guess)^(K - m) * (1 - p_guess)^m
    """
    k = signature_qubit_count
    max_mismatches = int(mismatch_threshold * k)
    
    p_bound = 0.0
    for m in range(max_mismatches + 1):
        comb = scipy.special.comb(k, m)
        prob = comb * (single_qubit_guess_success ** (k - m)) * ((1.0 - single_qubit_guess_success) ** m)
        p_bound += prob
        
    return float(min(1.0, p_bound))


def evaluate_empirical_forgery(forgery_results: List[SimulationResult]) -> ForgeryAnalysisResult:
    """Compute empirical forgery acceptance probability from simulation results."""
    total = len(forgery_results)
    if total == 0:
        return ForgeryAnalysisResult(16, 0.15, 0.0, 0, 0, 0.0)
        
    accepted_forgeries = sum(1 for r in forgery_results if r.final_decision == "ACCEPT")
    emp_prob = accepted_forgeries / total
    
    k = 16
    thresh = 0.15
    theo_bound = compute_theoretical_forgery_bound(k, thresh)
    
    return ForgeryAnalysisResult(
        signature_qubit_count=k,
        mismatch_threshold=thresh,
        theoretical_forgery_upper_bound=theo_bound,
        empirical_forgery_trials=total,
        forged_signatures_accepted=accepted_forgeries,
        empirical_forgery_probability=emp_prob
    )
