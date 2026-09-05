"""Optical fiber loss and photon transmission models."""

import numpy as np


def compute_transmission(distance_km: float, alpha_db_per_km: float = 0.20) -> float:
    """Compute the optical fiber transmission efficiency T(L) = 10^(-alpha * L / 10).
    
    Args:
        distance_km: Fiber propagation length in kilometers.
        alpha_db_per_km: Attenuation coefficient (standard SMF-28 is 0.20 dB/km at 1550 nm).
        
    Returns:
        Transmittance fraction T in [0.0, 1.0].
    """
    if distance_km < 0.0:
        raise ValueError("Fiber distance cannot be negative.")
    loss_db = alpha_db_per_km * distance_km
    transmittance = 10.0 ** (-loss_db / 10.0)
    return float(np.clip(transmittance, 0.0, 1.0))


def compute_loss_db(distance_km: float, alpha_db_per_km: float = 0.20) -> float:
    """Compute total attenuation in decibels (dB) across distance L."""
    return float(alpha_db_per_km * distance_km)


def simulate_photon_survival(
    initial_photons: int,
    distance_km: float,
    alpha_db_per_km: float = 0.20,
    detector_efficiency: float = 0.85,
    rng: np.random.Generator = None
) -> int:
    """Simulate the number of surviving transmitted photons over fiber distance L."""
    if rng is None:
        rng = np.random.default_rng()
    t = compute_transmission(distance_km, alpha_db_per_km)
    overall_efficiency = t * detector_efficiency
    surviving = int(rng.binomial(initial_photons, overall_efficiency))
    return surviving
