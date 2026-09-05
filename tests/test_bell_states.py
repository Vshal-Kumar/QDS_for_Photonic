"""Unit tests for Bell states and Bell State Measurements."""

import pytest
import numpy as np
from quantum.bell_states import (
    BELL_PHI_PLUS,
    BELL_PHI_MINUS,
    BELL_PSI_PLUS,
    BELL_PSI_MINUS,
    BELL_PROJECTORS,
    create_bell_pair,
    create_bell_density_matrix,
    perform_bell_measurement
)


def test_bell_state_orthonormality():
    """Verify that the 4 Bell states form an orthonormal basis in 4D Hilbert space."""
    bell_states = [BELL_PHI_PLUS, BELL_PHI_MINUS, BELL_PSI_PLUS, BELL_PSI_MINUS]
    for i, b1 in enumerate(bell_states):
        for j, b2 in enumerate(bell_states):
            dot = np.vdot(b1, b2)
            if i == j:
                assert np.isclose(dot, 1.0)
            else:
                assert np.isclose(dot, 0.0)


def test_bell_projectors_completeness():
    """Verify that the sum of the 4 Bell projectors equals the 4x4 identity operator."""
    sum_proj = sum(BELL_PROJECTORS)
    assert np.allclose(sum_proj, np.eye(4, dtype=complex))


def test_bell_measurement_statistics():
    """Verify Bell measurement on a 3-qubit state yields valid probability distributions."""
    rng = np.random.default_rng(42)
    # State: |0> (x) |Phi+>
    input_state = np.array([1.0, 0.0], dtype=complex)
    bell_state = create_bell_pair("Phi+")
    joint_state = np.kron(input_state, bell_state)
    
    outcomes = []
    for _ in range(100):
        outcome_idx, (c1, c2), bob_qubit = perform_bell_measurement(joint_state, rng)
        assert outcome_idx in [0, 1, 2, 3]
        assert c1 in [0, 1]
        assert c2 in [0, 1]
        assert np.isclose(np.linalg.norm(bob_qubit), 1.0)
        outcomes.append(outcome_idx)
        
    # All 4 outcomes should be observed over multiple trials
    assert len(set(outcomes)) == 4
