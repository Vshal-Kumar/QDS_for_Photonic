"""Physical noise processes in optical fibers: depolarizing and dephasing channels."""

import numpy as np
from quantum.pauli_states import (
    PAULI_X,
    PAULI_Y,
    PAULI_Z,
    PAULI_I,
    to_density_matrix
)


def apply_depolarizing_channel(rho: np.ndarray, p_depol: float) -> np.ndarray:
    """Apply quantum depolarizing channel: E(rho) = (1 - p)*rho + (p/3)*(X*rho*X + Y*rho*Y + Z*rho*Z).
    
    Args:
        rho: Input 2x2 density matrix.
        p_depol: Depolarization probability in [0.0, 1.0].
        
    Returns:
        Noisy 2x2 density matrix.
    """
    rho = to_density_matrix(rho)
    p = float(np.clip(p_depol, 0.0, 1.0))
    if p == 0.0:
        return rho
        
    x_term = PAULI_X @ rho @ PAULI_X
    y_term = PAULI_Y @ rho @ PAULI_Y
    z_term = PAULI_Z @ rho @ PAULI_Z
    
    noisy_rho = (1.0 - p) * rho + (p / 3.0) * (x_term + y_term + z_term)
    return to_density_matrix(noisy_rho)


def apply_dephasing_channel(rho: np.ndarray, p_dephase: float) -> np.ndarray:
    """Apply phase damping (dephasing) channel: E(rho) = (1 - p)*rho + p*(Z*rho*Z).
    
    Models fiber birefringence phase drift.
    """
    rho = to_density_matrix(rho)
    p = float(np.clip(p_dephase, 0.0, 1.0))
    if p == 0.0:
        return rho
        
    z_term = PAULI_Z @ rho @ PAULI_Z
    noisy_rho = (1.0 - p) * rho + p * z_term
    return to_density_matrix(noisy_rho)


def compute_distance_noise_parameters(
    distance_km: float,
    gamma_depol_per_km: float = 0.001,
    gamma_dephase_per_km: float = 0.0015
) -> tuple[float, float]:
    """Compute physical noise probabilities accumulated over distance L (km).
    
    Formulas:
        p_depol(L) = 1 - exp(-gamma_depol * L)
        p_dephase(L) = 1 - exp(-gamma_dephase * L)
    """
    p_depol = 1.0 - np.exp(-gamma_depol_per_km * distance_km)
    p_dephase = 1.0 - np.exp(-gamma_dephase_per_km * distance_km)
    return float(np.clip(p_depol, 0.0, 0.99)), float(np.clip(p_dephase, 0.0, 0.99))
