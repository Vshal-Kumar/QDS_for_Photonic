"""Verifier entity (Bob) responsible for quantum state reception and Pauli correction."""

from typing import List, Optional
import numpy as np

from quantum.pauli_correction import apply_pauli_correction, apply_pauli_correction_density
from quantum.pauli_states import to_density_matrix
from qds.signature import QuantumDigitalSignature, SignatureElement


class Verifier:
    """Represents the authentic Verifier (Bob) in the QDS protocol."""
    
    def __init__(self, verifier_id: str = "Bob") -> None:
        self.verifier_id = verifier_id
        
    def reconstruct_signature_states(
        self,
        signature: QuantumDigitalSignature,
        received_quantum_states: Optional[List[np.ndarray]] = None
    ) -> List[np.ndarray]:
        """Apply Pauli correction to each received qubit to reconstruct the original signature states.
        
        Correction Unitary: U = Z^c1 * X^c2 using Alice's classical BSM bits (c1, c2).
        """
        reconstructed_density_matrices: List[np.ndarray] = []
        
        states_to_process = (
            received_quantum_states
            if received_quantum_states is not None
            else [el.quantum_state_vec for el in signature.elements]
        )
        
        for i, el in enumerate(signature.elements):
            raw_state = states_to_process[i]
            c1, c2 = el.bsm_classical_bits
            
            if raw_state.ndim == 1:
                # 1D vector correction
                corr_vec = apply_pauli_correction(raw_state, c1, c2)
                rho = to_density_matrix(corr_vec)
            else:
                # 2D density matrix correction
                rho = apply_pauli_correction_density(raw_state, c1, c2)
                
            el.reconstructed_density_matrix = rho
            reconstructed_density_matrices.append(rho)
            
        return reconstructed_density_matrices
