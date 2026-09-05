"""Bell states, EPR pairs, and Bell measurement projectors."""

from typing import Dict, List, Tuple
import numpy as np
from quantum.pauli_states import STATE_0, STATE_1


# 4-dimensional basis states (|00>, |01>, |10>, |11>)
STATE_00: np.ndarray = np.kron(STATE_0, STATE_0)
STATE_01: np.ndarray = np.kron(STATE_0, STATE_1)
STATE_10: np.ndarray = np.kron(STATE_1, STATE_0)
STATE_11: np.ndarray = np.kron(STATE_1, STATE_1)

# Four Maximally Entangled Bell States (2-qubit state vectors)
BELL_PHI_PLUS: np.ndarray = (STATE_00 + STATE_11) / np.sqrt(2.0)   # |Phi+> = (|00> + |11>) / sqrt(2)
BELL_PHI_MINUS: np.ndarray = (STATE_00 - STATE_11) / np.sqrt(2.0)  # |Phi-> = (|00> - |11>) / sqrt(2)
BELL_PSI_PLUS: np.ndarray = (STATE_01 + STATE_10) / np.sqrt(2.0)   # |Psi+> = (|01> + |10>) / sqrt(2)
BELL_PSI_MINUS: np.ndarray = (STATE_01 - STATE_10) / np.sqrt(2.0)  # |Psi-> = (|01> - |10>) / sqrt(2)

BELL_STATE_DICT: Dict[str, np.ndarray] = {
    "Phi+": BELL_PHI_PLUS,
    "Phi-": BELL_PHI_MINUS,
    "Psi+": BELL_PSI_PLUS,
    "Psi-": BELL_PSI_MINUS,
}

BELL_INDEX_TO_STATE: Dict[int, str] = {
    0: "Phi+",
    1: "Phi-",
    2: "Psi+",
    3: "Psi-",
}

# 4x4 Bell Projectors Pi_i = |Bell_i><Bell_i|
PROJECTOR_PHI_PLUS: np.ndarray = np.outer(BELL_PHI_PLUS, BELL_PHI_PLUS.conj())
PROJECTOR_PHI_MINUS: np.ndarray = np.outer(BELL_PHI_MINUS, BELL_PHI_MINUS.conj())
PROJECTOR_PSI_PLUS: np.ndarray = np.outer(BELL_PSI_PLUS, BELL_PSI_PLUS.conj())
PROJECTOR_PSI_MINUS: np.ndarray = np.outer(BELL_PSI_MINUS, BELL_PSI_MINUS.conj())

BELL_PROJECTORS: List[np.ndarray] = [
    PROJECTOR_PHI_PLUS,
    PROJECTOR_PHI_MINUS,
    PROJECTOR_PSI_PLUS,
    PROJECTOR_PSI_MINUS,
]


def create_bell_pair(bell_type: str = "Phi+") -> np.ndarray:
    """Create a 4-dimensional Bell state vector."""
    if bell_type not in BELL_STATE_DICT:
        raise ValueError(f"Unknown Bell state type '{bell_type}'. Choose from {list(BELL_STATE_DICT.keys())}")
    return BELL_STATE_DICT[bell_type].copy()


def create_bell_density_matrix(bell_type: str = "Phi+") -> np.ndarray:
    """Create a 4x4 density matrix for a Bell pair."""
    state = create_bell_pair(bell_type)
    return np.outer(state, state.conj())


def perform_bell_measurement(
    state_3qubit: np.ndarray,
    rng: np.random.Generator
) -> Tuple[int, Tuple[int, int], np.ndarray]:
    """Perform a Bell-state measurement (BSM) on the first two qubits of a 3-qubit joint state.
    
    Returns:
        outcome_idx (int): 0 for Phi+, 1 for Phi-, 2 for Psi+, 3 for Psi-
        classical_bits (Tuple[int, int]): (c1, c2) corresponding to (00, 01, 10, 11)
        post_measurement_qubit_3 (np.ndarray): Collapsed 2D state vector for qubit 3 (Bob's qubit)
    """
    # Classical bit mappings:
    # 0 -> Phi+ -> (0, 0)
    # 1 -> Phi- -> (1, 0)
    # 2 -> Psi+ -> (0, 1)
    # 3 -> Psi- -> (1, 1)
    bit_map = {
        0: (0, 0),
        1: (1, 0),
        2: (0, 1),
        3: (1, 1),
    }
    
    # Calculate projection probabilities onto each Bell basis state for qubits 1 & 2
    probabilities = []
    projected_states = []
    
    for proj in BELL_PROJECTORS:
        # Full 8x8 projector: Pi_Bell (qubits 1,2) (x) I_2 (qubit 3)
        full_proj = np.kron(proj, np.eye(2, dtype=complex))
        projected = full_proj @ state_3qubit
        prob = float(np.real(np.vdot(projected, projected)))
        probabilities.append(prob)
        projected_states.append(projected)
    
    prob_sum = sum(probabilities)
    if prob_sum > 0:
        normalized_probs = [p / prob_sum for p in probabilities]
    else:
        normalized_probs = [0.25, 0.25, 0.25, 0.25]
        
    outcome_idx = int(rng.choice(4, p=normalized_probs))
    selected_state_8d = projected_states[outcome_idx]
    
    # Partial trace over qubits 1 & 2 to extract the single-qubit state of qubit 3
    norm = np.linalg.norm(selected_state_8d)
    if norm > 1e-12:
        selected_state_8d = selected_state_8d / norm
        
    # State representation in 8D basis |b1 b2 b3>
    # Since qubits 1 & 2 are in a definite Bell state, qubit 3 vector is extracted:
    # Reshape 8D to (4, 2) where row corresponds to Bell state index
    bell_basis_matrix = np.column_stack([
        BELL_PHI_PLUS,
        BELL_PHI_MINUS,
        BELL_PSI_PLUS,
        BELL_PSI_MINUS
    ]) # 4x4
    
    # Reshape state_3qubit 8D to (4, 2)
    state_4x2 = selected_state_8d.reshape(4, 2)
    qubit_3_vec = bell_basis_matrix[:, outcome_idx].conj() @ state_4x2
    q3_norm = np.linalg.norm(qubit_3_vec)
    if q3_norm > 1e-12:
        qubit_3_vec = qubit_3_vec / q3_norm
    else:
        qubit_3_vec = STATE_0.copy()
        
    return outcome_idx, bit_map[outcome_idx], qubit_3_vec
