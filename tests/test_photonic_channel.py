"""Unit tests for the photonic optical channel, fiber loss, and noise models."""

import pytest
import numpy as np
from photonic.fiber_loss import compute_transmission, compute_loss_db
from photonic.channel_noise import apply_depolarizing_channel, apply_dephasing_channel
from photonic.optical_channel import PhotonicChannel
from quantum.pauli_states import STATE_0, STATE_PLUS, to_density_matrix, quantum_fidelity, quantum_purity


def test_fiber_loss_attenuation():
    """Verify Beer-Lambert transmission T(L) matches standard telecom 0.2 dB/km."""
    # 0 km -> T = 1.0 (0 dB loss)
    assert np.isclose(compute_transmission(0.0), 1.0)
    assert np.isclose(compute_loss_db(0.0), 0.0)
    
    # 50 km -> 10 dB loss -> T = 10^(-1.0) = 0.10
    assert np.isclose(compute_loss_db(50.0), 10.0)
    assert np.isclose(compute_transmission(50.0), 0.10, atol=1e-5)
    
    # 100 km -> 20 dB loss -> T = 10^(-2.0) = 0.01
    assert np.isclose(compute_loss_db(100.0), 20.0)
    assert np.isclose(compute_transmission(100.0), 0.01, atol=1e-5)


def test_channel_noise_trace_preservation():
    """Verify depolarizing and dephasing channels preserve trace = 1.0."""
    rho = to_density_matrix(STATE_0)
    
    noisy_depol = apply_depolarizing_channel(rho, p_depol=0.3)
    assert np.isclose(np.trace(noisy_depol), 1.0)
    assert np.all(np.linalg.eigvals(noisy_depol) >= -1e-10)
    
    noisy_dephase = apply_dephasing_channel(rho, p_dephase=0.4)
    assert np.isclose(np.trace(noisy_dephase), 1.0)
    assert np.all(np.linalg.eigvals(noisy_dephase) >= -1e-10)


def test_optical_channel_propagation():
    """Verify full optical channel simulation across 50 km and 100 km."""
    channel = PhotonicChannel()
    rho_in = to_density_matrix(STATE_PLUS)
    
    # 10 km transmission
    res_10km = channel.transmit(rho_in, distance_km=10.0)
    assert res_10km.transmission_efficiency > 0.60
    assert res_10km.fidelity_with_input > 0.95
    assert np.isclose(np.trace(res_10km.output_rho), 1.0)
    
    # 100 km transmission
    res_100km = channel.transmit(rho_in, distance_km=100.0)
    assert res_100km.transmission_efficiency < res_10km.transmission_efficiency
    assert res_100km.fidelity_with_input < res_10km.fidelity_with_input
    assert res_100km.loss_db == 20.0
