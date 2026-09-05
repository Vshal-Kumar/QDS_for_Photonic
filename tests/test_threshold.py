"""Unit tests for adaptive threshold calculation and decision arbitration."""

import pytest
import numpy as np
from detection.baseline import BaselineProfile
from detection.adaptive_threshold import compute_adaptive_threshold
from detection.anomaly_score import compute_composite_anomaly_score
from detection.decision_engine import DecisionEngine
from core.results import ProtocolCheckResult, StatisticalResult
from qds.verification import QDSVerificationResult


def test_adaptive_threshold_shot_scaling():
    """Verify adaptive threshold decreases as measurement shot count increases (1/sqrt(N) scaling)."""
    profile = BaselineProfile(
        distance_km=50.0,
        mean_distribution_vector=np.ones(6) / 6.0,
        variance_vector=np.ones(6) * 0.001,
        mean_fidelity=0.98,
        mean_tvd=0.03
    )
    
    tau_100, _ = compute_adaptive_threshold(profile, shots=100)
    tau_1000, _ = compute_adaptive_threshold(profile, shots=1000)
    tau_10000, _ = compute_adaptive_threshold(profile, shots=10000)
    
    # More shots -> lower statistical variance -> tighter threshold
    assert tau_100 > tau_1000 > tau_10000


def test_decision_engine_arbitration():
    """Verify DecisionEngine correctly maps clean, suspicious, and attacked states."""
    engine = DecisionEngine()
    proto_pass = ProtocolCheckResult()
    qds_pass = QDSVerificationResult(is_valid=True, mismatch_rate=0.0, average_fidelity=0.99, threshold=0.15, qubit_fidelities=[1.0])
    
    # 1. Clean run
    stat_clean = StatisticalResult(
        total_variation_distance=0.02,
        adaptive_threshold=0.05,
        critical_threshold=0.12,
        anomaly_score=0.10
    )
    dec_clean = engine.arbitrate_decision(proto_pass, qds_pass, stat_clean)
    assert dec_clean.decision == "ACCEPT"
    assert dec_clean.threat_detected is False
    
    # 2. Suspicious run
    stat_susp = StatisticalResult(
        total_variation_distance=0.07,
        adaptive_threshold=0.05,
        critical_threshold=0.12,
        anomaly_score=0.45
    )
    dec_susp = engine.arbitrate_decision(proto_pass, qds_pass, stat_susp)
    assert dec_susp.decision == "SUSPICIOUS"
    assert dec_susp.threat_detected is True
    
    # 3. Critical Attack run
    stat_atk = StatisticalResult(
        total_variation_distance=0.25,
        adaptive_threshold=0.05,
        critical_threshold=0.12,
        anomaly_score=0.85
    )
    dec_atk = engine.arbitrate_decision(proto_pass, qds_pass, stat_atk)
    assert dec_atk.decision == "REJECT"
    assert dec_atk.threat_detected is True
