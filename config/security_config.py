"""Security policy, authentication tokens, and freshness configuration parameters."""

from dataclasses import dataclass, field
from typing import Dict, Set


@dataclass
class SecurityConfig:
    """Parameters governing authentication, freshness, and authorization."""
    
    # Nonce validity window in seconds (freshness window)
    nonce_validity_window_sec: float = 300.0
    
    # Cryptographic nonce length in bytes
    nonce_byte_length: int = 16
    
    # Pre-shared identity registry (SignerID -> Secret Key / Certificate)
    authorized_signers: Dict[str, str] = field(
        default_factory=lambda: {
            "Alice": "alice_sec_key_qds_2026_x89a",
            "Alice_Backup": "alice_backup_key_qds_77c1"
        }
    )
    
    # Authorized verifier roles / identities
    authorized_verifiers: Set[str] = field(
        default_factory=lambda: {"Bob", "Charlie_Auditor", "Bob_Secondary"}
    )
    
    # Statistical significance level for hypothesis testing alpha
    significance_level_alpha: float = 0.05
    
    # Critical anomaly score threshold for immediate rejection
    critical_anomaly_threshold: float = 0.60
    
    # Suspicious anomaly score threshold
    suspicious_anomaly_threshold: float = 0.30
