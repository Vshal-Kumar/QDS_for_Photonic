"""Data structures for comprehensive simulation and benchmark results."""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional


@dataclass
class ProtocolCheckResult:
    """Outcome of protocol-level security checks."""
    signer_authenticated: bool = True
    signer_error: Optional[str] = None
    verifier_authorized: bool = True
    verifier_error: Optional[str] = None
    nonce_valid: bool = True
    nonce_error: Optional[str] = None
    session_valid: bool = True
    session_error: Optional[str] = None
    message_intact: bool = True
    message_error: Optional[str] = None
    signature_intact: bool = True
    signature_error: Optional[str] = None
    
    @property
    def all_passed(self) -> bool:
        return (
            self.signer_authenticated
            and self.verifier_authorized
            and self.nonce_valid
            and self.session_valid
            and self.message_intact
            and self.signature_intact
        )


@dataclass
class StatisticalResult:
    """Outcome of quantum measurement statistical analysis."""
    shots: int = 1000
    observed_distribution: Dict[str, float] = field(default_factory=dict)
    baseline_distribution: Dict[str, float] = field(default_factory=dict)
    total_variation_distance: float = 0.0
    chi_square_statistic: float = 0.0
    chi_square_p_value: float = 1.0
    z_scores: Dict[str, float] = field(default_factory=dict)
    adaptive_threshold: float = 0.05
    critical_threshold: float = 0.12
    anomaly_score: float = 0.0
    statistical_threat_detected: bool = False


@dataclass
class TimingBreakdown:
    """Timing breakdown in milliseconds for verification efficiency evaluation."""
    quantum_sim_ms: float = 0.0
    channel_sim_ms: float = 0.0
    teleportation_ms: float = 0.0
    measurement_ms: float = 0.0
    statistical_analysis_ms: float = 0.0
    protocol_checks_ms: float = 0.0
    total_verification_ms: float = 0.0


@dataclass
class SimulationResult:
    """Comprehensive result of an end-to-end QDS simulation run."""
    
    # Run identifiers
    run_id: str = ""
    session_id: str = ""
    message_text: str = ""
    
    # Configuration inputs
    distance_km: float = 0.0
    attack_type: str = "none"
    attack_strength: float = 0.0
    shots: int = 1000
    
    # Photonic & Quantum channel metrics
    transmission: float = 1.0
    quantum_fidelity: float = 1.0
    quantum_purity: float = 1.0
    qds_mismatch_rate: float = 0.0
    qds_signature_valid: bool = True
    
    # Protocol & Statistical security outputs
    protocol_checks: ProtocolCheckResult = field(default_factory=ProtocolCheckResult)
    statistics: StatisticalResult = field(default_factory=StatisticalResult)
    
    # Arbitrated Final Decision ("ACCEPT", "SUSPICIOUS", "REJECT")
    final_decision: str = "ACCEPT"
    decision_reason: str = "All protocol checks passed; statistical distance within normal threshold."
    threat_detected: bool = False
    
    # Performance & Timing metrics
    timing: TimingBreakdown = field(default_factory=TimingBreakdown)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to hierarchical dictionary."""
        return {
            "run_id": self.run_id,
            "session_id": self.session_id,
            "message_text": self.message_text,
            "distance_km": self.distance_km,
            "attack_type": self.attack_type,
            "attack_strength": self.attack_strength,
            "shots": self.shots,
            "transmission": self.transmission,
            "quantum_fidelity": self.quantum_fidelity,
            "quantum_purity": self.quantum_purity,
            "qds_mismatch_rate": self.qds_mismatch_rate,
            "qds_signature_valid": self.qds_signature_valid,
            "protocol_checks": {
                "all_passed": self.protocol_checks.all_passed,
                "signer_authenticated": self.protocol_checks.signer_authenticated,
                "verifier_authorized": self.protocol_checks.verifier_authorized,
                "nonce_valid": self.protocol_checks.nonce_valid,
                "session_valid": self.protocol_checks.session_valid,
                "message_intact": self.protocol_checks.message_intact,
                "signature_intact": self.protocol_checks.signature_intact,
            },
            "statistics": {
                "shots": self.statistics.shots,
                "total_variation_distance": self.statistics.total_variation_distance,
                "chi_square_statistic": self.statistics.chi_square_statistic,
                "chi_square_p_value": self.statistics.chi_square_p_value,
                "adaptive_threshold": self.statistics.adaptive_threshold,
                "critical_threshold": self.statistics.critical_threshold,
                "anomaly_score": self.statistics.anomaly_score,
                "statistical_threat_detected": self.statistics.statistical_threat_detected,
                "observed_distribution": self.statistics.observed_distribution,
                "baseline_distribution": self.statistics.baseline_distribution,
                "z_scores": self.statistics.z_scores,
            },
            "final_decision": self.final_decision,
            "decision_reason": self.decision_reason,
            "threat_detected": self.threat_detected,
            "timing": {
                "quantum_sim_ms": self.timing.quantum_sim_ms,
                "channel_sim_ms": self.timing.channel_sim_ms,
                "teleportation_ms": self.timing.teleportation_ms,
                "measurement_ms": self.timing.measurement_ms,
                "statistical_analysis_ms": self.timing.statistical_analysis_ms,
                "protocol_checks_ms": self.timing.protocol_checks_ms,
                "total_verification_ms": self.timing.total_verification_ms,
            }
        }
