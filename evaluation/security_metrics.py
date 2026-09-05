"""Security evaluation metrics: FAR, FRR, Detection Probability, Precision, Recall, and F1."""

from dataclasses import dataclass
from typing import List
from core.results import SimulationResult


@dataclass
class SecurityMetricsSummary:
    """Consolidated security performance metrics."""
    total_trials: int
    legitimate_trials: int
    attack_trials: int
    true_positives: int  # Attacks correctly detected (SUSPICIOUS or REJECT)
    false_positives: int  # Legitimate erroneously rejected (FRR)
    true_negatives: int  # Legitimate correctly accepted (ACCEPT)
    false_negatives: int  # Attacks erroneously accepted (FAR)
    
    detection_probability: float  # P_D = TP / (TP + FN)
    false_acceptance_rate: float  # FAR = FN / Total Attacks
    false_rejection_rate: float  # FRR = FP / Total Legitimate
    precision: float
    recall: float
    f1_score: float


def compute_security_metrics(results: List[SimulationResult]) -> SecurityMetricsSummary:
    """Compute standard cybersecurity and threat detection metrics from a batch of simulation results."""
    total = len(results)
    if total == 0:
        return SecurityMetricsSummary(0, 0, 0, 0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        
    legit_results = [r for r in results if r.attack_type in ["none", "clean", ""]]
    attack_results = [r for r in results if r.attack_type not in ["none", "clean", ""]]
    
    n_legit = len(legit_results)
    n_attack = len(attack_results)
    
    # Legitimate trials: positive means false positive (rejected/suspicious)
    fp = sum(1 for r in legit_results if r.final_decision != "ACCEPT")
    tn = sum(1 for r in legit_results if r.final_decision == "ACCEPT")
    
    # Attack trials: positive means true positive (rejected/suspicious), negative means false acceptance
    tp = sum(1 for r in attack_results if r.final_decision != "ACCEPT")
    fn = sum(1 for r in attack_results if r.final_decision == "ACCEPT")
    
    p_d = tp / max(1, n_attack) if n_attack > 0 else 1.0
    far = fn / max(1, n_attack) if n_attack > 0 else 0.0
    frr = fp / max(1, n_legit) if n_legit > 0 else 0.0
    
    precision = tp / max(1, tp + fp)
    recall = p_d
    f1 = (2 * precision * recall) / max(1e-6, precision + recall)
    
    return SecurityMetricsSummary(
        total_trials=total,
        legitimate_trials=n_legit,
        attack_trials=n_attack,
        true_positives=tp,
        false_positives=fp,
        true_negatives=tn,
        false_negatives=fn,
        detection_probability=p_d,
        false_acceptance_rate=far,
        false_rejection_rate=frr,
        precision=precision,
        recall=recall,
        f1_score=f1
    )
