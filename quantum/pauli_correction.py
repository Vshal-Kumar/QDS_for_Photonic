"""Pauli unitary correction operators for quantum teleportation reconstruction."""

from typing import Tuple
import numpy as np
from quantum.pauli_states import PAULI_I, PAULI_X, PAULI_Y, PAULI_Z, to_density_matrix


def get_correction_unitary(c1: int, c2: int) -> np.ndarray:
    """Return the single-qubit unitary correction operator U = Z^c1 * X^c2.
    
    Mapping based on Alice's Bell State Measurement (BSM) outcome:
    - (c1=0, c2=0) [Phi+] -> U = I
    - (c1=1, c2=0) [Phi-] -> U = Z
    - (c1=0, c2=1) [Psi+] -> U = X
    - (c1=1, c2=1) [Psi-] -> U = Z @ X = -i Y
    """
    if (c1, c2) == (0, 0):
        return PAULI_I.copy()
    elif (c1, c2) == (1, 0):
        return PAULI_Z.copy()
    elif (c1, c2) == (0, 1):
        return PAULI_X.copy()
    elif (c1, c2) == (1, 1):
        return PAULI_Z @ PAULI_X
    else:
        raise ValueError(f"Invalid BSM classical bit pair: ({c1}, {c2})")


def apply_pauli_correction(state_vec: np.ndarray, c1: int, c2: int) -> np.ndarray:
    """Apply unitary correction U(c1, c2) to a state vector |psi>."""
    unitary = get_correction_unitary(c1, c2)
    corrected_vec = unitary @ state_vec
    norm = np.linalg.norm(corrected_vec)
    if norm > 1e-12:
        corrected_vec = corrected_vec / norm
    return corrected_vec


def apply_pauli_correction_density(rho: np.ndarray, c1: int, c2: int) -> np.ndarray:
    """Apply unitary correction U(c1, c2) rho U(c1, c2)^dagger to a density matrix."""
    unitary = get_correction_unitary(c1, c2)
    corrected_rho = unitary @ rho @ unitary.conj().T
    return to_density_matrix(corrected_rho)
