"""Pauli operators, eigenstates, density matrices, and quantum state metrics."""

from typing import Dict, Tuple
import numpy as np
import scipy.linalg


# Fundamental 2x2 Pauli Matrices
PAULI_I: np.ndarray = np.array([[1.0, 0.0], [0.0, 1.0]], dtype=complex)
PAULI_X: np.ndarray = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
PAULI_Y: np.ndarray = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
PAULI_Z: np.ndarray = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)

# Standard Pauli Eigenstates (State Vectors)
STATE_0: np.ndarray = np.array([1.0, 0.0], dtype=complex)
STATE_1: np.ndarray = np.array([0.0, 1.0], dtype=complex)

STATE_PLUS: np.ndarray = (STATE_0 + STATE_1) / np.sqrt(2.0)
STATE_MINUS: np.ndarray = (STATE_0 - STATE_1) / np.sqrt(2.0)

STATE_PLUS_Y: np.ndarray = (STATE_0 + 1.0j * STATE_1) / np.sqrt(2.0)
STATE_MINUS_Y: np.ndarray = (STATE_0 - 1.0j * STATE_1) / np.sqrt(2.0)

# Canonical string mapping to state vectors
PAULI_STATE_MAP: Dict[str, np.ndarray] = {
    "|0>": STATE_0,
    "|1>": STATE_1,
    "|+>": STATE_PLUS,
    "|->": STATE_MINUS,
    "|+_y>": STATE_PLUS_Y,
    "|-_y>": STATE_MINUS_Y,
    # Aliases
    "0": STATE_0,
    "1": STATE_1,
    "+": STATE_PLUS,
    "-": STATE_MINUS,
    "+y": STATE_PLUS_Y,
    "-y": STATE_MINUS_Y,
}


def to_density_matrix(state: np.ndarray) -> np.ndarray:
    """Convert a 1D state vector or 2D density matrix into a normalized 2x2 density matrix."""
    if state.ndim == 1:
        v = state.reshape(-1, 1)
        rho = v @ v.conj().T
    elif state.ndim == 2:
        rho = state
    else:
        raise ValueError(f"Invalid state dimension: {state.shape}")
    
    # Normalize trace to 1.0
    tr = np.trace(rho)
    if abs(tr) > 1e-12:
        rho = rho / tr
    return rho


def get_pauli_state(name: str) -> np.ndarray:
    """Retrieve the 1D state vector for a canonical Pauli eigenstate."""
    clean_name = name.strip()
    if clean_name not in PAULI_STATE_MAP:
        raise KeyError(f"Unknown Pauli state '{name}'. Valid states: {list(PAULI_STATE_MAP.keys())}")
    return PAULI_STATE_MAP[clean_name].copy()


def get_pauli_density_matrix(name: str) -> np.ndarray:
    """Retrieve the 2x2 density matrix for a canonical Pauli eigenstate."""
    return to_density_matrix(get_pauli_state(name))


def quantum_fidelity(rho1: np.ndarray, rho2: np.ndarray) -> float:
    """Compute standard quantum state fidelity F(rho1, rho2) = (Tr sqrt(sqrt(rho1) rho2 sqrt(rho1)))^2.
    
    For a pure state rho1 = |psi><psi|, this reduces exactly to Tr(rho1 * rho2) = <psi|rho2|psi>.
    """
    rho1 = to_density_matrix(rho1)
    rho2 = to_density_matrix(rho2)
    
    # Check if either state is pure (Purity Tr(rho^2) ~ 1)
    purity1 = float(np.real(np.trace(rho1 @ rho1)))
    purity2 = float(np.real(np.trace(rho2 @ rho2)))
    
    if abs(purity1 - 1.0) < 1e-5 or abs(purity2 - 1.0) < 1e-5:
        # Optimized pure state formula: Tr(rho1 @ rho2)
        fid = float(np.real(np.trace(rho1 @ rho2)))
        return max(0.0, min(1.0, fid))
    
    # General mixed state fidelity via matrix square roots
    sqrt_rho1 = scipy.linalg.sqrtm(rho1)
    prod = sqrt_rho1 @ rho2 @ sqrt_rho1
    sqrt_prod = scipy.linalg.sqrtm(prod)
    fid = float(np.real(np.trace(sqrt_prod)) ** 2)
    return max(0.0, min(1.0, fid))


def quantum_purity(rho: np.ndarray) -> float:
    """Compute quantum state purity gamma = Tr(rho^2) in [0.5, 1.0]."""
    rho = to_density_matrix(rho)
    return float(np.real(np.trace(rho @ rho)))


def get_bloch_vector(rho: np.ndarray) -> Tuple[float, float, float]:
    """Compute Bloch vector coordinates (rx, ry, rz) where rho = (I + r . sigma) / 2."""
    rho = to_density_matrix(rho)
    rx = float(np.real(np.trace(rho @ PAULI_X)))
    ry = float(np.real(np.trace(rho @ PAULI_Y)))
    rz = float(np.real(np.trace(rho @ PAULI_Z)))
    return (rx, ry, rz)
