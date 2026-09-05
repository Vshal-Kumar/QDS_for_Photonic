"""Pauli X (Bit-Flip) quantum state manipulation attack."""

import numpy as np
from quantum.pauli_states import PAULI_X, to_density_matrix


def apply_bit_flip_attack(rho: np.ndarray, attack_strength: float = 1.0) -> np.ndarray:
    """Apply Pauli X (Bit-Flip) attack: rho' = (1 - pa)*rho + pa * (X * rho * X).
    
    Args:
        rho: Input 2x2 quantum density matrix.
        attack_strength: Attack probability pa in [0.0, 1.0].
    """
    rho = to_density_matrix(rho)
    pa = float(np.clip(attack_strength, 0.0, 1.0))
    if pa == 0.0:
        return rho
    
    flipped = PAULI_X @ rho @ PAULI_X
    rho_prime = (1.0 - pa) * rho + pa * flipped
    return to_density_matrix(rho_prime)
