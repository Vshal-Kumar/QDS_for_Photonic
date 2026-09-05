"""Quantum teleportation protocol execution engine."""

from dataclasses import dataclass
from typing import Tuple, Optional
import numpy as np

from quantum.pauli_states import (
    get_pauli_state,
    to_density_matrix,
    quantum_fidelity,
    quantum_purity
)
from quantum.bell_states import create_bell_pair, perform_bell_measurement
from quantum.pauli_correction import apply_pauli_correction, apply_pauli_correction_density


@dataclass
class TeleportationResult:
    """Outcome of a single quantum teleportation execution."""
    input_state_name: str
    input_state_vec: np.ndarray
    bsm_outcome_idx: int
    classical_bits: Tuple[int, int]
    raw_bob_state_vec: np.ndarray
    reconstructed_state_vec: np.ndarray
    reconstructed_density_matrix: np.ndarray
    ideal_fidelity: float
    purity: float


def teleport_quantum_state(
    input_state: np.ndarray,
    state_name: str = "custom",
    seed: Optional[int] = None
) -> TeleportationResult:
    """Execute standard quantum teleportation for a single qubit state vector.
    
    Circuit Steps:
    1. Form 3-qubit product state |psi>_S (x) |Phi+>_AB
    2. Perform Bell State Measurement (BSM) on qubits (S, A)
    3. Transmit 2 classical bits (c1, c2)
    4. Apply Bob's Pauli unitary correction U = Z^c1 X^c2 on qubit B
    5. Evaluate output state and state fidelity
    """
    rng = np.random.default_rng(seed)
    
    # 1. Normalize input state
    norm = np.linalg.norm(input_state)
    if norm < 1e-12:
        raise ValueError("Input state cannot be zero vector.")
    norm_input = input_state / norm
    
    # 2. Generate EPR pair |Phi+>_AB
    bell_ab = create_bell_pair("Phi+")
    
    # 3. Form 3-qubit joint state |psi>_S (x) |Phi+>_AB
    joint_3qubit = np.kron(norm_input, bell_ab)
    
    # 4. Perform BSM on qubits (S, A)
    bsm_idx, (c1, c2), bob_raw_qubit = perform_bell_measurement(joint_3qubit, rng)
    
    # 5. Apply Pauli unitary correction on Bob's qubit
    reconstructed_vec = apply_pauli_correction(bob_raw_qubit, c1, c2)
    reconstructed_rho = to_density_matrix(reconstructed_vec)
    
    # 6. Compute fidelity with ideal input
    input_rho = to_density_matrix(norm_input)
    fid = quantum_fidelity(input_rho, reconstructed_rho)
    purity = quantum_purity(reconstructed_rho)
    
    return TeleportationResult(
        input_state_name=state_name,
        input_state_vec=norm_input,
        bsm_outcome_idx=bsm_idx,
        classical_bits=(c1, c2),
        raw_bob_state_vec=bob_raw_qubit,
        reconstructed_state_vec=reconstructed_vec,
        reconstructed_density_matrix=reconstructed_rho,
        ideal_fidelity=fid,
        purity=purity
    )
