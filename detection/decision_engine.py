"""Deterministic Tri-State Decision Engine arbitrating protocol, quantum, and statistical evidence."""

from dataclasses import dataclass
from typing import Optional

from core.results import ProtocolCheckResult, StatisticalResult
from qds.verification import QDSVerificationResult


@dataclass
class DecisionOutcome:
    """Final decision outcome and full audit explanation."""
    decision: str  # "ACCEPT", "SUSPICIOUS", "REJECT"
    threat_detected: bool
    reason: str
    anomaly_score: float
    statistical_distance: float
    threshold: float


class DecisionEngine:
    """Master decision arbitrator combining protocol security, QDS fidelity, and statistical physics."""
    
    def __init__(
        self,
        suspicious_anomaly_threshold: float = 0.30,
        critical_anomaly_threshold: float = 0.60
    ) -> None:
        self.suspicious_anomaly_threshold = suspicious_anomaly_threshold
        self.critical_anomaly_threshold = critical_anomaly_threshold
        
    def arbitrate_decision(
        self,
        protocol_checks: ProtocolCheckResult,
        qds_verification: QDSVerificationResult,
        statistical_result: StatisticalResult
    ) -> DecisionOutcome:
        """Evaluate all security evidence and render a final deterministic decision."""
        
        # 1. Hard Protocol Security Failures (Immediate Rejection)
        if not protocol_checks.signer_authenticated:
            return DecisionOutcome(
                decision="REJECT",
                threat_detected=True,
                reason=f"Signer Authentication Failed: {protocol_checks.signer_error}",
                anomaly_score=1.0,
                statistical_distance=statistical_result.total_variation_distance,
                threshold=statistical_result.adaptive_threshold
            )
            
        if not protocol_checks.verifier_authorized:
            return DecisionOutcome(
                decision="REJECT",
                threat_detected=True,
                reason=f"Unauthorized Verifier: {protocol_checks.verifier_error}",
                anomaly_score=1.0,
                statistical_distance=statistical_result.total_variation_distance,
                threshold=statistical_result.adaptive_threshold
            )
            
        if not protocol_checks.nonce_valid:
            return DecisionOutcome(
                decision="REJECT",
                threat_detected=True,
                reason=f"Freshness Violation / Replay Detected: {protocol_checks.nonce_error}",
                anomaly_score=1.0,
                statistical_distance=statistical_result.total_variation_distance,
                threshold=statistical_result.adaptive_threshold
            )
            
        if not protocol_checks.session_valid:
            return DecisionOutcome(
                decision="REJECT",
                threat_detected=True,
                reason=f"Invalid Session State: {protocol_checks.session_error}",
                anomaly_score=1.0,
                statistical_distance=statistical_result.total_variation_distance,
                threshold=statistical_result.adaptive_threshold
            )
            
        if not protocol_checks.message_intact:
            return DecisionOutcome(
                decision="REJECT",
                threat_detected=True,
                reason=f"Message Tampering Detected: {protocol_checks.message_error}",
                anomaly_score=1.0,
                statistical_distance=statistical_result.total_variation_distance,
                threshold=statistical_result.adaptive_threshold
            )
            
        if not protocol_checks.signature_intact:
            return DecisionOutcome(
                decision="REJECT",
                threat_detected=True,
                reason=f"Signature Bundle or State Integrity Violation: {protocol_checks.signature_error}",
                anomaly_score=1.0,
                statistical_distance=statistical_result.total_variation_distance,
                threshold=statistical_result.adaptive_threshold
            )
            
        # 2. QDS Signature Validity Failure (Forgery / State Degradation)
        if not qds_verification.is_valid:
            return DecisionOutcome(
                decision="REJECT",
                threat_detected=True,
                reason=f"QDS Verification Failed: {qds_verification.error_message}",
                anomaly_score=max(0.85, statistical_result.anomaly_score),
                statistical_distance=statistical_result.total_variation_distance,
                threshold=statistical_result.adaptive_threshold
            )
            
        # 3. Statistical Threat Detection Arbitrament
        tvd = statistical_result.total_variation_distance
        tau = statistical_result.adaptive_threshold
        tau_crit = statistical_result.critical_threshold
        anomaly = statistical_result.anomaly_score
        
        # Definite Rejection (Critical Statistical Anomaly / Pauli State Manipulation)
        if tvd > tau_crit or anomaly >= self.critical_anomaly_threshold:
            return DecisionOutcome(
                decision="REJECT",
                threat_detected=True,
                reason=(
                    f"Quantum State Manipulation Detected: TVD {tvd:.4f} exceeded critical threshold {tau_crit:.4f} "
                    f"(Anomaly Score {anomaly:.2f})."
                ),
                anomaly_score=anomaly,
                statistical_distance=tvd,
                threshold=tau
            )
            
        # Suspicious Flag (Borderline Channel Noise / Low-Strength Attack)
        if tvd > tau or anomaly >= self.suspicious_anomaly_threshold:
            return DecisionOutcome(
                decision="SUSPICIOUS",
                threat_detected=True,
                reason=(
                    f"Suspicious Quantum Channel Deviation: TVD {tvd:.4f} exceeded adaptive baseline threshold {tau:.4f} "
                    f"(Anomaly Score {anomaly:.2f})."
                ),
                anomaly_score=anomaly,
                statistical_distance=tvd,
                threshold=tau
            )
            
        # Clean Acceptance
        return DecisionOutcome(
            decision="ACCEPT",
            threat_detected=False,
            reason=(
                f"Verification Successful: Protocol checks passed, QDS fidelity intact, "
                f"statistical distance {tvd:.4f} within baseline threshold {tau:.4f}."
            ),
            anomaly_score=anomaly,
            statistical_distance=tvd,
            threshold=tau
        )
