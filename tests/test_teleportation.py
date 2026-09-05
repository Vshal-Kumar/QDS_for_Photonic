"""Unit tests for ideal quantum teleportation across all 6 Pauli eigenstates."""

import pytest
import numpy as np
from quantum.pauli_states import (
    STATE_0,
    STATE_1,
    STATE_PLUS,
    STATE_MINUS,
    STATE_PLUS_Y,
    STATE_MINUS_Y,
    to_density_matrix,
    quantum_fidelity
)
from quantum.teleportation import teleport_quantum_state


@pytest.mark.parametrize("state_vec, state_name", [
    (STATE_0, "|0>"),
    (STATE_1, "|1>"),
    (STATE_PLUS, "|+>"),
    (STATE_MINUS, "|->"),
    (STATE_PLUS_Y, "|+_y>"),
    (STATE_MINUS_Y, "|-_y>"),
])
def test_ideal_teleportation_fidelity(state_vec: np.ndarray, state_name: str):
    """Verify that ideal quantum teleportation achieves unity fidelity (F=1.0) for all Pauli states."""
    # Test across multiple random seeds to sample different Bell measurement outcomes
    for seed in [10, 42, 99, 123, 777]:
        result = teleport_quantum_state(
            input_state=state_vec,
            state_name=state_name,
            seed=seed
        )
        
        # Verify perfect fidelity
        assert np.isclose(result.ideal_fidelity, 1.0, atol=1e-7), (
            f"Teleportation failed for state {state_name} with seed {seed}: "
            f"Fidelity = {result.ideal_fidelity}"
        )
        
        # Verify output state matches input density matrix
        input_rho = to_density_matrix(state_vec)
        assert np.allclose(result.reconstructed_density_matrix, input_rho, atol=1e-7)
        
        # Verify purity is 1.0
        assert np.isclose(result.purity, 1.0, atol=1e-7)
