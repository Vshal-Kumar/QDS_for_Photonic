"""Unit tests for Pauli eigenstates, density matrices, and fidelity."""

import pytest
import numpy as np
from quantum.pauli_states import (
    PAULI_I,
    PAULI_X,
    PAULI_Y,
    PAULI_Z,
    STATE_0,
    STATE_1,
    STATE_PLUS,
    STATE_MINUS,
    STATE_PLUS_Y,
    STATE_MINUS_Y,
    get_pauli_state,
    get_pauli_density_matrix,
    to_density_matrix,
    quantum_fidelity,
    quantum_purity,
    get_bloch_vector
)


def test_pauli_algebra():
    """Verify standard Pauli matrix commutation and identity relations."""
    # X^2 = Y^2 = Z^2 = I
    assert np.allclose(PAULI_X @ PAULI_X, PAULI_I)
    assert np.allclose(PAULI_Y @ PAULI_Y, PAULI_I)
    assert np.allclose(PAULI_Z @ PAULI_Z, PAULI_I)
    # X Y = i Z
    assert np.allclose(PAULI_X @ PAULI_Y, 1.0j * PAULI_Z)
    # Y Z = i X
    assert np.allclose(PAULI_Y @ PAULI_Z, 1.0j * PAULI_X)
    # Z X = i Y
    assert np.allclose(PAULI_Z @ PAULI_X, 1.0j * PAULI_Y)


def test_pauli_eigenstates_normalization():
    """Verify all 6 Pauli eigenstates are normalized unit vectors."""
    states = [STATE_0, STATE_1, STATE_PLUS, STATE_MINUS, STATE_PLUS_Y, STATE_MINUS_Y]
    for s in states:
        assert np.isclose(np.linalg.norm(s), 1.0)


def test_pauli_eigenvalues():
    """Verify that each state is an exact eigenstate of its corresponding Pauli operator."""
    # Z-basis
    assert np.allclose(PAULI_Z @ STATE_0, +1.0 * STATE_0)
    assert np.allclose(PAULI_Z @ STATE_1, -1.0 * STATE_1)
    # X-basis
    assert np.allclose(PAULI_X @ STATE_PLUS, +1.0 * STATE_PLUS)
    assert np.allclose(PAULI_X @ STATE_MINUS, -1.0 * STATE_MINUS)
    # Y-basis
    assert np.allclose(PAULI_Y @ STATE_PLUS_Y, +1.0 * STATE_PLUS_Y)
    assert np.allclose(PAULI_Y @ STATE_MINUS_Y, -1.0 * STATE_MINUS_Y)


def test_fidelity_and_purity():
    """Verify fidelity of identical states is 1.0, orthogonal states is 0.0, and purity is 1.0 for pure states."""
    rho_0 = to_density_matrix(STATE_0)
    rho_1 = to_density_matrix(STATE_1)
    rho_plus = to_density_matrix(STATE_PLUS)
    
    assert np.isclose(quantum_fidelity(rho_0, rho_0), 1.0)
    assert np.isclose(quantum_fidelity(rho_0, rho_1), 0.0)
    assert np.isclose(quantum_fidelity(rho_0, rho_plus), 0.5)
    
    assert np.isclose(quantum_purity(rho_0), 1.0)
    
    # Completely mixed state I / 2 has purity 0.5
    rho_mixed = PAULI_I / 2.0
    assert np.isclose(quantum_purity(rho_mixed), 0.5)


def test_bloch_vectors():
    """Verify Bloch sphere coordinates for Pauli eigenstates."""
    rx, ry, rz = get_bloch_vector(to_density_matrix(STATE_0))
    assert np.allclose([rx, ry, rz], [0.0, 0.0, 1.0], atol=1e-7)
    
    rx, ry, rz = get_bloch_vector(to_density_matrix(STATE_PLUS))
    assert np.allclose([rx, ry, rz], [1.0, 0.0, 0.0], atol=1e-7)
    
    rx, ry, rz = get_bloch_vector(to_density_matrix(STATE_PLUS_Y))
    assert np.allclose([rx, ry, rz], [0.0, 1.0, 0.0], atol=1e-7)
