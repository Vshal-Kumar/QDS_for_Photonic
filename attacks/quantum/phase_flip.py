"""Pauli Z (Phase-Flip) quantum state manipulation attack."""

import numpy as np
from quantum.pauli_states import PAULI_Z, to_density_matrix


def apply_phase_flip_attack(rho: np.ndarray, attack_strength: float = 1.0) -> np.ndarray:
    """Apply Pauli Z (Phase-Flip) attack: rho' = (1 - pa)*rho + pa * (Z * rho * Z).
    
    Args:
        rho: Input 2x2 quantum density matrix.
        attack_strength: Attack probability pa in [0.0, 1.0].
    """
    rho = to_density_matrix(rho)
    pa = float(np.clip(attack_strength, 0.0, 1.0))
    if pa == 0.0:
        return rho
    
    flipped = PAULI_Z @ rho @ PAULI_Z
    rho_prime = (1.0 - pa) * rho + pa * flipped
    return to_density_matrix(rho_prime)
