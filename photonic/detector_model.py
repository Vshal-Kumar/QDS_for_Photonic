"""Single-photon detector physical imperfections: efficiency, dark counts, and basis misalignment."""

import numpy as np
from quantum.pauli_states import to_density_matrix


def apply_detector_imperfections(
    rho: np.ndarray,
    efficiency: float = 0.85,
    dark_count_prob: float = 1e-5,
    alignment_jitter_rad: float = 0.01,
    rng: np.random.Generator = None
) -> np.ndarray:
    """Apply single-photon detector imperfections to the received density matrix.
    
    Models:
    1. Detection efficiency & dark count background (adds a slight identity mixture)
    2. Optical misalignment jitter (rotates polarization by a small Gaussian random angle theta)
    """
    if rng is None:
        rng = np.random.default_rng()
        
    rho = to_density_matrix(rho)
    
    # 1. Basis misalignment rotation around Y/Z axis
    if alignment_jitter_rad > 0.0:
        d_theta = rng.normal(0.0, alignment_jitter_rad)
        # Unitary rotation R_y(theta) = cos(theta/2) I - i sin(theta/2) Y
        c = np.cos(d_theta / 2.0)
        s = np.sin(d_theta / 2.0)
        u_rot = np.array([[c, -s], [s, c]], dtype=complex)
        rho = u_rot @ rho @ u_rot.conj().T
        
    # 2. Dark count mixture
    # Dark counts add uniform unpolarized background noise
    if dark_count_prob > 0.0:
        p_noise = dark_count_prob / max(1e-6, efficiency)
        p_noise = min(0.5, p_noise)
        rho = (1.0 - p_noise) * rho + (p_noise / 2.0) * np.eye(2, dtype=complex)
        
    return to_density_matrix(rho)
