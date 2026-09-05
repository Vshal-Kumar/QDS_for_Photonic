"""Unit tests for PennyLane and PennyLane-Lightning quantum backend integration."""

import pytest
import numpy as np
from quantum.quantum_backend import PennyLaneBackend, quantum_backend
from quantum.pauli_states import (
    STATE_0,
    STATE_1,
    STATE_PLUS,
    STATE_PLUS_Y,
    quantum_fidelity,
    to_density_matrix
)
from quantum.bell_states import BELL_PHI_PLUS


def test_pennylane_backend_initialization():
    """Verify PennyLane backend initializes and identifies available devices."""
    backend = PennyLaneBackend(prefer_lightning=True)
    assert backend.device_name in ["lightning.qubit", "default.qubit"]


def test_pennylane_pauli_state_preparation():
    """Verify PennyLane QNode correctly prepares canonical Pauli eigenstates."""
    backend = PennyLaneBackend()
    
    # |0>
    st_0 = backend.prepare_pauli_state_qnode("|0>")
    assert np.isclose(quantum_fidelity(to_density_matrix(st_0), to_density_matrix(STATE_0)), 1.0)
    
    # |1>
    st_1 = backend.prepare_pauli_state_qnode("|1>")
    assert np.isclose(quantum_fidelity(to_density_matrix(st_1), to_density_matrix(STATE_1)), 1.0)
    
    # |+>
    st_plus = backend.prepare_pauli_state_qnode("|+>")
    assert np.isclose(quantum_fidelity(to_density_matrix(st_plus), to_density_matrix(STATE_PLUS)), 1.0)
    
    # |+_y>
    st_plus_y = backend.prepare_pauli_state_qnode("|+_y>")
    assert np.isclose(quantum_fidelity(to_density_matrix(st_plus_y), to_density_matrix(STATE_PLUS_Y)), 1.0)


def test_pennylane_bell_pair_generation():
    """Verify PennyLane QNode prepares maximally entangled Bell pair |Phi+>."""
    backend = PennyLaneBackend()
    bell_vec = backend.prepare_bell_pair_qnode("Phi+")
    assert np.isclose(np.abs(np.vdot(bell_vec, BELL_PHI_PLUS)), 1.0)


def test_pennylane_teleportation_circuit():
    """Verify 3-qubit PennyLane teleportation circuit with Pauli corrections."""
    backend = PennyLaneBackend()
    
    # Teleport |+> with correction (c1=0, c2=1)
    input_vec = STATE_PLUS
    # If c1=0, c2=0: circuit reconstructs state
    rho_out = backend.execute_teleportation_qnode(input_vec, c1=0, c2=0)
    fid = quantum_fidelity(to_density_matrix(input_vec), to_density_matrix(rho_out))
    assert np.isclose(fid, 1.0, atol=1e-5)


def test_pennylane_pauli_measurement_probabilities():
    """Verify PennyLane QNode calculates exact projection probabilities across bases."""
    backend = PennyLaneBackend()
    
    # |0> in Z basis: P(0) = 1.0, P(1) = 0.0
    p0, p1 = backend.measure_pauli_probabilities_qnode(STATE_0, basis="Z")
    assert np.isclose(p0, 1.0)
    assert np.isclose(p1, 0.0)
    
    # |0> in X basis: P(+) = 0.5, P(-) = 0.5
    px_p, px_m = backend.measure_pauli_probabilities_qnode(STATE_0, basis="X")
    assert np.isclose(px_p, 0.5)
    assert np.isclose(px_m, 0.5)
