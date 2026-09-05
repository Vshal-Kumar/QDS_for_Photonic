"""Verification logic for Quantum Digital Signatures."""

from dataclasses import dataclass
from typing import List
import numpy as np

from config.protocol_config import ProtocolConfig
from core.message import Message
from quantum.pauli_states import get_pauli_state, to_density_matrix, quantum_fidelity
from qds.signature import QuantumDigitalSignature


@dataclass
class QDSVerificationResult:
    """Outcome of quantum digital signature consistency verification."""
    is_valid: bool
    mismatch_rate: float
    average_fidelity: float
    threshold: float
    qubit_fidelities: List[float]
    error_message: str = ""


def verify_qds_signature(
    message: Message,
    signature: QuantumDigitalSignature,
    reconstructed_states: List[np.ndarray],
    config: ProtocolConfig = None
) -> QDSVerificationResult:
    """Verify the consistency between message hash and reconstructed quantum signature states.
    
    Verification Rule:
    1. Re-derive expected Pauli eigenstates from message hash bits.
    2. Compute quantum fidelity F_k = <psi_expected | rho_reconstructed | psi_expected> for all k.
    3. Calculate mismatch rate = (Count of states with fidelity < 0.80) / Total Qubits.
    4. Signature is accepted if mismatch rate <= qds_mismatch_threshold.
    """
    if config is None:
        config = ProtocolConfig()
        
    # Check hash match
    if signature.message_hash_hex != message.hash_hex:
        return QDSVerificationResult(
            is_valid=False,
            mismatch_rate=1.0,
            average_fidelity=0.0,
            threshold=config.qds_mismatch_threshold,
            qubit_fidelities=[0.0] * len(reconstructed_states),
            error_message="Message hash does not match signature header hash."
        )
        
    qubit_fidelities: List[float] = []
    mismatches = 0
    
    for i, el in enumerate(signature.elements):
        expected_state_vec = get_pauli_state(el.state_name)
        expected_rho = to_density_matrix(expected_state_vec)
        recon_rho = reconstructed_states[i]
        
        fid = quantum_fidelity(expected_rho, recon_rho)
        qubit_fidelities.append(fid)
        
        # Consider a qubit mismatched if fidelity drops significantly
        if fid < 0.80:
            mismatches += 1
            
    total_qubits = len(signature.elements)
    mismatch_rate = mismatches / max(1, total_qubits)
    avg_fidelity = float(np.mean(qubit_fidelities)) if qubit_fidelities else 0.0
    
    is_valid = mismatch_rate <= config.qds_mismatch_threshold
    
    return QDSVerificationResult(
        is_valid=is_valid,
        mismatch_rate=mismatch_rate,
        average_fidelity=avg_fidelity,
        threshold=config.qds_mismatch_threshold,
        qubit_fidelities=qubit_fidelities,
        error_message="" if is_valid else f"Mismatch rate {mismatch_rate:.3f} exceeded threshold {config.qds_mismatch_threshold}."
    )
