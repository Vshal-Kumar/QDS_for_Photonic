"""Quantum Digital Signature (QDS) protocol configuration parameters."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class ProtocolConfig:
    """Parameters governing the QDS protocol execution."""
    
    # Number of signature qubits per message block
    signature_qubit_count: int = 16
    
    # Hash algorithm used for message hashing
    hash_algorithm: str = "sha256"
    
    # Allowed Pauli signature eigenstates
    allowed_states: List[str] = field(
        default_factory=lambda: ["|0>", "|1>", "|+>", "|->", "|+_y>", "|-_y>"]
    )
    
    # QDS acceptance error threshold for quantum verification (mismatch rate)
    qds_mismatch_threshold: float = 0.15
    
    # Security parameter for information-theoretic privacy amplification
    security_parameter: int = 128
    
    # Bell state used for teleportation: Phi+ = (|00> + |11>) / sqrt(2)
    bell_state_type: str = "Phi+"
