"""Quantum state mathematical integrity checks: Hermiticity, unit trace, and positive semi-definiteness."""

import numpy as np
from quantum.pauli_states import to_density_matrix, quantum_purity


def verify_quantum_state_integrity(rho: np.ndarray, tol: float = 1e-6) -> tuple[bool, str]:
    """Verify that a 2x2 quantum density matrix is mathematically valid.
    
    Checks:
    1. Square 2x2 matrix
    2. Hermiticity: rho == rho^dagger
    3. Unit trace: Tr(rho) == 1.0
    4. Positive semi-definiteness: all eigenvalues >= -tol
    5. Valid purity: 0.5 - tol <= Tr(rho^2) <= 1.0 + tol
    """
    if rho.shape != (2, 2):
        return False, f"Invalid density matrix shape {rho.shape}. Expected (2, 2)."
        
    # Hermiticity
    if not np.allclose(rho, rho.conj().T, atol=tol):
        return False, "Quantum state density matrix is not Hermitian."
        
    # Unit trace
    tr = np.trace(rho)
    if abs(tr - 1.0) > tol:
        return False, f"Density matrix trace is not unity: Tr(rho) = {tr:.6f}."
        
    # Positive semi-definiteness
    eigvals = np.linalg.eigvalsh(rho)
    if np.any(eigvals < -tol):
        return False, f"Density matrix contains negative eigenvalues: {eigvals}."
        
    # Purity
    purity = quantum_purity(rho)
    if purity < 0.5 - tol or purity > 1.0 + tol:
        return False, f"State purity out of physical bounds [0.5, 1.0]: purity = {purity:.6f}."
        
    return True, ""
