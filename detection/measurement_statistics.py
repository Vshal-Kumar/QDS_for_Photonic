"""Statistical processing of multi-basis Pauli measurements."""

from dataclasses import dataclass
from typing import Dict
import numpy as np
from quantum.measurements import PauliMeasurementSuiteResult


@dataclass
class MeasurementStatistics:
    """Aggregated statistical properties derived from Pauli measurement outcomes."""
    shots_per_basis: int
    total_shots: int
    empirical_vector: np.ndarray  # [X+, X-, Y+, Y-, Z0, Z1]
    expectation_x: float
    expectation_y: float
    expectation_z: float
    variance_x: float
    variance_y: float
    variance_z: float
    distribution_dict: Dict[str, float]


def process_measurement_suite(suite: PauliMeasurementSuiteResult) -> MeasurementStatistics:
    """Extract full statistical moments and distribution vectors from a measurement suite."""
    emp_vec = suite.empirical_distribution_vector
    
    exp_x = suite.results["X"].expectation_val
    exp_y = suite.results["Y"].expectation_val
    exp_z = suite.results["Z"].expectation_val
    
    shots = suite.shots_per_basis
    # Binomial variance of expectation value <sigma>: Var(X) = (1 - <sigma>^2) / N
    var_x = max(0.0, (1.0 - exp_x**2) / max(1, shots))
    var_y = max(0.0, (1.0 - exp_y**2) / max(1, shots))
    var_z = max(0.0, (1.0 - exp_z**2) / max(1, shots))
    
    dist_dict = {
        "X+": float(emp_vec[0]),
        "X-": float(emp_vec[1]),
        "Y+": float(emp_vec[2]),
        "Y-": float(emp_vec[3]),
        "Z0": float(emp_vec[4]),
        "Z1": float(emp_vec[5]),
    }
    
    return MeasurementStatistics(
        shots_per_basis=shots,
        total_shots=suite.total_shots,
        empirical_vector=emp_vec,
        expectation_x=exp_x,
        expectation_y=exp_y,
        expectation_z=exp_z,
        variance_x=var_x,
        variance_y=var_y,
        variance_z=var_z,
        distribution_dict=dist_dict
    )
