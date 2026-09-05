"""Quantum state consistency verification across teleported signature states."""

from dataclasses import dataclass
from typing import List
import numpy as np

from quantum.pauli_states import get_pauli_state, to_density_matrix, quantum_fidelity
from qds.signature import QuantumDigitalSignature


@dataclass
class QuantumStateVerificationResult:
    """Outcome of quantum-level verification across all teleported states."""
    passed: bool
    average_fidelity: float
    min_fidelity: float
    fidelity_list: List[float]
    error_message: str = ""


def verify_teleported_signature_states(
    signature: QuantumDigitalSignature,
    reconstructed_states: List[np.ndarray],
    min_acceptable_average_fidelity: float = 0.80
) -> QuantumStateVerificationResult:
    """Evaluate fidelity of all reconstructed quantum states against expected Pauli eigenstates."""
    fidelities: List[float] = []
    
    for i, el in enumerate(signature.elements):
        expected_vec = get_pauli_state(el.state_name)
        expected_rho = to_density_matrix(expected_vec)
        recon_rho = reconstructed_states[i]
        
        fid = quantum_fidelity(expected_rho, recon_rho)
        fidelities.append(fid)
        
    avg_fid = float(np.mean(fidelities)) if fidelities else 0.0
    min_fid = float(np.min(fidelities)) if fidelities else 0.0
    
    passed = avg_fid >= min_acceptable_average_fidelity
    
    return QuantumStateVerificationResult(
        passed=passed,
        average_fidelity=avg_fid,
        min_fidelity=min_fid,
        fidelity_list=fidelities,
        error_message="" if passed else f"Average quantum fidelity {avg_fid:.3f} below minimum acceptable threshold {min_acceptable_average_fidelity}."
    )
