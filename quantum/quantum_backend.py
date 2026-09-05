"""PennyLane and PennyLane-Lightning quantum simulation backend and QNodes."""

from typing import Dict, Tuple, Optional, Any
import numpy as np

# Try importing PennyLane
try:
    import pennylane as qml
    PENNYLANE_AVAILABLE = True
except ImportError:
    qml = None
    PENNYLANE_AVAILABLE = False


class PennyLaneBackend:
    """Manages PennyLane devices (lightning.qubit / default.qubit) and circuit QNodes."""
    
    def __init__(self, prefer_lightning: bool = True) -> None:
        self.prefer_lightning = prefer_lightning
        self.device_name = "default.qubit"
        self._dev_1qubit = None
        self._dev_2qubit = None
        self._dev_3qubit = None
        
        if PENNYLANE_AVAILABLE:
            if prefer_lightning:
                try:
                    # Test if lightning.qubit is available
                    test_dev = qml.device("lightning.qubit", wires=1)
                    self.device_name = "lightning.qubit"
                except Exception:
                    self.device_name = "default.qubit"
            else:
                self.device_name = "default.qubit"
                
            self._dev_1qubit = qml.device(self.device_name, wires=1)
            self._dev_2qubit = qml.device(self.device_name, wires=2)
            self._dev_3qubit = qml.device(self.device_name, wires=3)
            
    @property
    def is_available(self) -> bool:
        return PENNYLANE_AVAILABLE
        
    def prepare_pauli_state_qnode(self, state_name: str) -> np.ndarray:
        """Use PennyLane to prepare a canonical Pauli eigenstate and return its state vector."""
        if not PENNYLANE_AVAILABLE:
            from quantum.pauli_states import get_pauli_state
            return get_pauli_state(state_name)
            
        @qml.qnode(self._dev_1qubit)
        def circuit():
            clean = state_name.strip()
            if clean in ["|0>", "0"]:
                pass
            elif clean in ["|1>", "1"]:
                qml.PauliX(wires=0)
            elif clean in ["|+>", "+"]:
                qml.Hadamard(wires=0)
            elif clean in ["|->", "-"]:
                qml.PauliX(wires=0)
                qml.Hadamard(wires=0)
            elif clean in ["|+_y>", "+y"]:
                qml.Hadamard(wires=0)
                qml.S(wires=0)
            elif clean in ["|-_y>", "-y"]:
                qml.PauliX(wires=0)
                qml.Hadamard(wires=0)
                qml.S(wires=0)
            return qml.state()
            
        return np.array(circuit(), dtype=complex)

    def prepare_bell_pair_qnode(self, bell_type: str = "Phi+") -> np.ndarray:
        """Use PennyLane to generate a maximally entangled Bell pair on wires (0, 1)."""
        if not PENNYLANE_AVAILABLE:
            from quantum.bell_states import create_bell_pair
            return create_bell_pair(bell_type)
            
        @qml.qnode(self._dev_2qubit)
        def circuit():
            # Create |Phi+> = (|00> + |11>) / sqrt(2)
            qml.Hadamard(wires=0)
            qml.CNOT(wires=[0, 1])
            
            if bell_type == "Phi-":
                qml.PauliZ(wires=0)
            elif bell_type == "Psi+":
                qml.PauliX(wires=1)
            elif bell_type == "Psi-":
                qml.PauliZ(wires=0)
                qml.PauliX(wires=1)
                
            return qml.state()
            
        return np.array(circuit(), dtype=complex)

    def execute_teleportation_qnode(
        self,
        input_state_vec: np.ndarray,
        c1: int,
        c2: int
    ) -> np.ndarray:
        """Simulate the 3-qubit teleportation circuit and Bob's Pauli correction in PennyLane.
        
        Wires:
            0: Alice's input state |psi>
            1: Alice's entangled qubit (EPR half)
            2: Bob's entangled qubit (EPR half -> reconstructed output)
        """
        if not PENNYLANE_AVAILABLE:
            from quantum.pauli_correction import apply_pauli_correction
            return apply_pauli_correction(input_state_vec, c1, c2)
            
        @qml.qnode(self._dev_3qubit)
        def circuit():
            # 1. Initialize wire 0 to input state
            if hasattr(qml, "StatePrep"):
                qml.StatePrep(input_state_vec, wires=[0])
            else:
                qml.QubitStateVector(input_state_vec, wires=[0])
            
            # 2. Entangle wires 1 & 2 in Bell state |Phi+>
            qml.Hadamard(wires=1)
            qml.CNOT(wires=[1, 2])
            
            # 3. Alice's Bell State Measurement operations on (0, 1)
            qml.CNOT(wires=[0, 1])
            qml.Hadamard(wires=0)
            
            return qml.state()
            
        st_3qubit = np.array(circuit(), dtype=complex)
        
        # Extract the collapsed state on wire 2 given measurement outcome (c1, c2) on wires (0, 1)
        idx = 4 * c1 + 2 * c2
        raw_b = st_3qubit[idx : idx + 2]
        norm = np.linalg.norm(raw_b)
        if norm > 1e-12:
            raw_b = raw_b / norm
            
        from quantum.pauli_correction import apply_pauli_correction
        reconstructed_vec = apply_pauli_correction(raw_b, c1, c2)
        from quantum.pauli_states import to_density_matrix
        return to_density_matrix(reconstructed_vec)

    def measure_pauli_probabilities_qnode(self, state_vec_or_rho: np.ndarray, basis: str) -> Tuple[float, float]:
        """Compute exact Born rule projection probabilities in Pauli basis using PennyLane."""
        if not PENNYLANE_AVAILABLE:
            from quantum.measurements import measure_pauli_basis
            res = measure_pauli_basis(state_vec_or_rho, basis=basis, shots=1000)
            return res.prob_plus_theoretical, res.prob_minus_theoretical
            
        @qml.qnode(self._dev_1qubit)
        def circuit():
            if state_vec_or_rho.ndim == 1:
                if hasattr(qml, "StatePrep"):
                    qml.StatePrep(state_vec_or_rho, wires=[0])
                else:
                    qml.QubitStateVector(state_vec_or_rho, wires=[0])
            else:
                if hasattr(qml, "StatePrep"):
                    qml.StatePrep(state_vec_or_rho, wires=[0])
                else:
                    qml.QubitDensityMatrix(state_vec_or_rho, wires=[0])
                
            if basis == "X":
                qml.Hadamard(wires=0)
            elif basis == "Y":
                qml.adjoint(qml.S)(wires=0)
                qml.Hadamard(wires=0)
                
            return qml.probs(wires=0)
            
        probs = circuit()
        return float(probs[0]), float(probs[1])


# Global singleton PennyLane backend instance
quantum_backend = PennyLaneBackend(prefer_lightning=True)
