"""Projective Pauli measurements (X, Y, Z bases) with finite-shot statistics."""

from dataclasses import dataclass, field
from typing import Dict, Tuple, Optional
import numpy as np

from quantum.pauli_states import (
    to_density_matrix,
    PAULI_X,
    PAULI_Y,
    PAULI_Z,
    STATE_0,
    STATE_1,
    STATE_PLUS,
    STATE_MINUS,
    STATE_PLUS_Y,
    STATE_MINUS_Y,
)


# Projectors for each Pauli basis
PROJ_Z_0: np.ndarray = np.outer(STATE_0, STATE_0.conj())
PROJ_Z_1: np.ndarray = np.outer(STATE_1, STATE_1.conj())

PROJ_X_PLUS: np.ndarray = np.outer(STATE_PLUS, STATE_PLUS.conj())
PROJ_X_MINUS: np.ndarray = np.outer(STATE_MINUS, STATE_MINUS.conj())

PROJ_Y_PLUS: np.ndarray = np.outer(STATE_PLUS_Y, STATE_PLUS_Y.conj())
PROJ_Y_MINUS: np.ndarray = np.outer(STATE_MINUS_Y, STATE_MINUS_Y.conj())

BASIS_PROJECTORS = {
    "Z": (PROJ_Z_0, PROJ_Z_1),
    "X": (PROJ_X_PLUS, PROJ_X_MINUS),
    "Y": (PROJ_Y_PLUS, PROJ_Y_MINUS),
}


@dataclass
class BasisMeasurementResult:
    """Outcome of multi-shot measurement in a single Pauli basis."""
    basis: str
    shots: int
    count_plus: int
    count_minus: int
    prob_plus_empirical: float
    prob_minus_empirical: float
    prob_plus_theoretical: float
    prob_minus_theoretical: float
    expectation_val: float


@dataclass
class PauliMeasurementSuiteResult:
    """Outcome of multi-shot measurements across all three Pauli bases (X, Y, Z)."""
    shots_per_basis: int
    total_shots: int
    results: Dict[str, BasisMeasurementResult] = field(default_factory=dict)
    
    @property
    def empirical_distribution_vector(self) -> np.ndarray:
        """Returns 6-element probability vector: [P(X+), P(X-), P(Y+), P(Y-), P(Z0), P(Z1)]."""
        return np.array([
            self.results["X"].prob_plus_empirical,
            self.results["X"].prob_minus_empirical,
            self.results["Y"].prob_plus_empirical,
            self.results["Y"].prob_minus_empirical,
            self.results["Z"].prob_plus_empirical,
            self.results["Z"].prob_minus_empirical,
        ])
        
    @property
    def theoretical_distribution_vector(self) -> np.ndarray:
        """Returns 6-element theoretical probability vector."""
        return np.array([
            self.results["X"].prob_plus_theoretical,
            self.results["X"].prob_minus_theoretical,
            self.results["Y"].prob_plus_theoretical,
            self.results["Y"].prob_minus_theoretical,
            self.results["Z"].prob_plus_theoretical,
            self.results["Z"].prob_minus_theoretical,
        ])


def measure_pauli_basis(
    rho: np.ndarray,
    basis: str,
    shots: int = 1000,
    rng: Optional[np.random.Generator] = None
) -> BasisMeasurementResult:
    """Perform multi-shot projective measurement in a selected Pauli basis ('X', 'Y', or 'Z')."""
    if basis not in BASIS_PROJECTORS:
        raise ValueError(f"Unknown measurement basis '{basis}'. Choose 'X', 'Y', or 'Z'.")
        
    if rng is None:
        rng = np.random.default_rng()
        
    rho = to_density_matrix(rho)
    proj_plus, proj_minus = BASIS_PROJECTORS[basis]
    
    # Born rule probabilities: P(+) = Tr(rho * Pi_+), P(-) = Tr(rho * Pi_-)
    p_plus_theory = float(np.real(np.trace(rho @ proj_plus)))
    p_plus_theory = max(0.0, min(1.0, p_plus_theory))
    p_minus_theory = 1.0 - p_plus_theory
    
    # Simulate finite measurement shots using binomial distribution
    count_plus = int(rng.binomial(shots, p_plus_theory))
    count_minus = shots - count_plus
    
    p_plus_emp = count_plus / shots
    p_minus_emp = count_minus / shots
    
    # Expectation value <sigma> = P(+) - P(-)
    exp_val = p_plus_emp - p_minus_emp
    
    return BasisMeasurementResult(
        basis=basis,
        shots=shots,
        count_plus=count_plus,
        count_minus=count_minus,
        prob_plus_empirical=p_plus_emp,
        prob_minus_empirical=p_minus_emp,
        prob_plus_theoretical=p_plus_theory,
        prob_minus_theoretical=p_minus_theory,
        expectation_val=exp_val
    )


def measure_all_pauli_bases(
    rho: np.ndarray,
    shots_per_basis: int = 1000,
    seed: Optional[int] = None
) -> PauliMeasurementSuiteResult:
    """Measure the quantum state across all three mutually unbiased Pauli bases (X, Y, Z)."""
    rng = np.random.default_rng(seed)
    suite = PauliMeasurementSuiteResult(
        shots_per_basis=shots_per_basis,
        total_shots=shots_per_basis * 3
    )
    
    for basis in ["X", "Y", "Z"]:
        suite.results[basis] = measure_pauli_basis(
            rho=rho,
            basis=basis,
            shots=shots_per_basis,
            rng=rng
        )
        
    return suite
