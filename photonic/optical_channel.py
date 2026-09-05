"""Integrated long-distance photonic optical fiber channel model."""

from dataclasses import dataclass
from typing import Optional
import numpy as np

from quantum.pauli_states import to_density_matrix, quantum_fidelity, quantum_purity
from photonic.fiber_loss import compute_transmission, compute_loss_db
from photonic.channel_noise import (
    apply_depolarizing_channel,
    apply_dephasing_channel,
    compute_distance_noise_parameters
)
from photonic.polarization_noise import apply_polarization_drift
from photonic.detector_model import apply_detector_imperfections
from config.photonic_config import PhotonicConfig


@dataclass
class ChannelTransmissionResult:
    """Outcome of transmitting a quantum state through the photonic optical channel."""
    input_rho: np.ndarray
    output_rho: np.ndarray
    distance_km: float
    transmission_efficiency: float
    loss_db: float
    fidelity_with_input: float
    purity: float
    p_depol: float
    p_dephase: float


class PhotonicChannel:
    """Simulates realistic long-distance optical fiber propagation and detector physics."""
    
    def __init__(self, config: Optional[PhotonicConfig] = None) -> None:
        self.config = config if config is not None else PhotonicConfig()
        
    def transmit(
        self,
        input_state: np.ndarray,
        distance_km: float,
        rng: Optional[np.random.Generator] = None
    ) -> ChannelTransmissionResult:
        """Transmit a quantum state vector or density matrix across distance_km of optical fiber.
        
        Physics Pipeline:
        1. Compute distance-dependent transmission T(L) and total loss (dB)
        2. Compute accumulated depolarizing and dephasing rates
        3. Apply depolarizing channel
        4. Apply dephasing channel (fiber birefringence phase noise)
        5. Apply detector quantum efficiency, dark count mixture & alignment jitter
        6. Compute output state fidelity and purity
        """
        if rng is None:
            rng = np.random.default_rng()
            
        rho_in = to_density_matrix(input_state)
        
        # 1. Attenuation
        transmission = compute_transmission(distance_km, self.config.fiber_loss_db_per_km)
        loss_db = compute_loss_db(distance_km, self.config.fiber_loss_db_per_km)
        
        # 2. Accumulated noise parameters
        p_depol, p_dephase = compute_distance_noise_parameters(
            distance_km=distance_km,
            gamma_depol_per_km=self.config.depolarization_rate_per_km,
            gamma_dephase_per_km=self.config.dephasing_rate_per_km
        )
        
        # 3. Channel transformations
        rho_noisy = apply_depolarizing_channel(rho_in, p_depol)
        rho_noisy = apply_dephasing_channel(rho_noisy, p_dephase)
        rho_noisy = apply_polarization_drift(rho_noisy, distance_km, rng=rng)
        
        # 4. Detector imperfections
        rho_out = apply_detector_imperfections(
            rho=rho_noisy,
            efficiency=self.config.detector_efficiency,
            dark_count_prob=self.config.dark_count_probability,
            alignment_jitter_rad=self.config.alignment_jitter_rad,
            rng=rng
        )
        
        # 5. Metrics
        fidelity = quantum_fidelity(rho_in, rho_out)
        purity = quantum_purity(rho_out)
        
        return ChannelTransmissionResult(
            input_rho=rho_in,
            output_rho=rho_out,
            distance_km=distance_km,
            transmission_efficiency=transmission,
            loss_db=loss_db,
            fidelity_with_input=fidelity,
            purity=purity,
            p_depol=p_depol,
            p_dephase=p_dephase
        )
