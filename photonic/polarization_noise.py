"""Fiber birefringence and polarization rotation noise models."""

from typing import Optional
import numpy as np
from quantum.pauli_states import PAULI_X, PAULI_Y, PAULI_Z, to_density_matrix


def apply_polarization_drift(
    rho: np.ndarray,
    distance_km: float,
    drift_std_per_km: float = 0.0005,
    rng: Optional[np.random.Generator] = None
) -> np.ndarray:
    """Simulate optical fiber birefringence polarization drift.
    
    Models random unitary rotation on the Poincare sphere:
    U(theta, n_vec) = cos(theta/2)*I - i*sin(theta/2)*(n . sigma)
    where theta ~ N(0, (drift_std * sqrt(L))^2) and n is a random 3D unit axis.
    """
    if rng is None:
        rng = np.random.default_rng()
        
    rho = to_density_matrix(rho)
    if distance_km <= 0.0 or drift_std_per_km <= 0.0:
        return rho
        
    # Accumulated angular drift variance scales with fiber propagation length sqrt(L)
    accumulated_sigma = drift_std_per_km * np.sqrt(distance_km)
    theta = rng.normal(0.0, accumulated_sigma)
    
    # Random 3D unit vector on the Poincare / Bloch sphere
    n_vec = rng.normal(0.0, 1.0, size=3)
    norm_n = np.linalg.norm(n_vec)
    if norm_n > 1e-12:
        n_vec = n_vec / norm_n
    else:
        n_vec = np.array([0.0, 0.0, 1.0])
        
    nx, ny, nz = n_vec
    sigma_n = nx * PAULI_X + ny * PAULI_Y + nz * PAULI_Z
    
    c = np.cos(theta / 2.0)
    s = np.sin(theta / 2.0)
    u_biref = c * np.eye(2, dtype=complex) - 1.0j * s * sigma_n
    
    rotated_rho = u_biref @ rho @ u_biref.conj().T
    return to_density_matrix(rotated_rho)
