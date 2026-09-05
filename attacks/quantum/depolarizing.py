"""Adversarial quantum depolarizing attack channel."""

import numpy as np
from quantum.pauli_states import PAULI_X, PAULI_Y, PAULI_Z, to_density_matrix


def apply_adversarial_depolarizing_attack(rho: np.ndarray, attack_strength: float = 1.0) -> np.ndarray:
    """Apply maximal entropy Pauli depolarizing attack:
    rho' = (1 - pa)*rho + (pa/3)*(X*rho*X + Y*rho*Y + Z*rho*Z).
    """
    rho = to_density_matrix(rho)
    pa = float(np.clip(attack_strength, 0.0, 1.0))
    if pa == 0.0:
        return rho
        
    x_term = PAULI_X @ rho @ PAULI_X
    y_term = PAULI_Y @ rho @ PAULI_Y
    z_term = PAULI_Z @ rho @ PAULI_Z
    
    noisy_rho = (1.0 - pa) * rho + (pa / 3.0) * (x_term + y_term + z_term)
    return to_density_matrix(noisy_rho)
