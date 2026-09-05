"""Experiment benchmarks and parameter sweep configurations."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class ExperimentConfig:
    """Parameters for running the 11 scientific benchmark suites."""
    
    # Distance benchmarks in km
    distances_km: List[float] = field(
        default_factory=lambda: [10.0, 25.0, 50.0, 100.0, 150.0, 200.0]
    )
    
    # Measurement shot counts for scaling analysis
    shot_counts: List[int] = field(
        default_factory=lambda: [100, 500, 1000, 5000, 10000]
    )
    
    # Default measurement shot count for standard experiments
    default_shots: int = 1000
    
    # Attack strengths (probability of Pauli manipulation pa)
    attack_strengths: List[float] = field(
        default_factory=lambda: [0.0, 0.05, 0.10, 0.20, 0.30, 0.50, 0.75, 1.00]
    )
    
    # Number of Monte Carlo repetitions per experiment point
    monte_carlo_runs: int = 200
    
    # Output directories
    figures_dir: str = "results/figures"
    tables_dir: str = "results/tables"
    raw_dir: str = "results/raw"
    processed_dir: str = "results/processed"
