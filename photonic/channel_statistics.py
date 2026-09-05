"""Statistical calculations for photonic channels: SNR, QBER, and loss profiles."""

import numpy as np
from photonic.fiber_loss import compute_transmission


def calculate_channel_snr_db(
    distance_km: float,
    signal_power_dbm: float = 0.0,
    dark_count_prob: float = 1e-5,
    alpha_db_per_km: float = 0.20
) -> float:
    """Calculate the estimated optical Signal-to-Noise Ratio in dB."""
    loss_db = alpha_db_per_km * distance_km
    rx_power_dbm = signal_power_dbm - loss_db
    noise_power_dbm = 10.0 * np.log10(max(1e-12, dark_count_prob))
    snr_db = rx_power_dbm - noise_power_dbm
    return float(snr_db)


def estimate_channel_qber(
    distance_km: float,
    gamma_depol_per_km: float = 0.001,
    gamma_dephase_per_km: float = 0.0015,
    dark_count_prob: float = 1e-5
) -> float:
    """Estimate the intrinsic channel Quantum Bit Error Rate (QBER) for legitimate transmission."""
    p_depol = 1.0 - np.exp(-gamma_depol_per_km * distance_km)
    p_dephase = 1.0 - np.exp(-gamma_dephase_per_km * distance_km)
    
    # QBER contribution from depolarization: 2/3 * p_depol / 2 = p_depol / 3
    # QBER contribution from dephasing in conjugate basis: p_dephase / 2
    qber = (p_depol / 3.0) + (p_dephase / 4.0) + (dark_count_prob / 2.0)
    return float(np.clip(qber, 0.0, 0.5))
