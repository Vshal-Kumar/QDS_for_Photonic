"""Photonic optical fiber channel and detector physical parameters."""

from dataclasses import dataclass


@dataclass
class PhotonicConfig:
    """Parameters governing the photonic optical channel and single-photon detection."""
    
    # Optical wavelength in nanometers (standard telecom C-band)
    wavelength_nm: float = 1550.0
    
    # Standard single-mode fiber (SMF-28) attenuation coefficient in dB/km
    fiber_loss_db_per_km: float = 0.20
    
    # Base depolarizing noise parameter per km (gamma_depol)
    depolarization_rate_per_km: float = 0.001
    
    # Base phase damping (dephasing) rate per km due to fiber birefringence fluctuations
    dephasing_rate_per_km: float = 0.0015
    
    # Single-photon detector quantum efficiency (e.g. SNSPD / InGaAs APD)
    detector_efficiency: float = 0.85
    
    # Dark count probability per measurement gate window
    dark_count_probability: float = 1e-5
    
    # Measurement basis alignment angular error standard deviation (radians)
    alignment_jitter_rad: float = 0.01
