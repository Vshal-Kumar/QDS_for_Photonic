"""Unit tests for Pauli physical attacks (X, Y, Z, Depolarization)."""

import pytest
import numpy as np
from quantum.pauli_states import (
    STATE_0,
    STATE_1,
    STATE_PLUS,
    STATE_PLUS_Y,
    to_density_matrix,
    quantum_fidelity
)
from attacks.quantum.bit_flip import apply_bit_flip_attack
from attacks.quantum.phase_flip import apply_phase_flip_attack
from attacks.quantum.bit_phase_flip import apply_bit_phase_flip_attack
from attacks.attack_engine import AttackEngine


def test_bit_flip_x_attack():
    """Verify Pauli X flips |0> to |1> at 100% attack strength."""
    rho_0 = to_density_matrix(STATE_0)
    rho_1 = to_density_matrix(STATE_1)
    
    # 100% X attack: |0><0| -> |1><1|
    attacked_rho = apply_bit_flip_attack(rho_0, attack_strength=1.0)
    assert np.allclose(attacked_rho, rho_1)
    assert np.isclose(quantum_fidelity(rho_0, attacked_rho), 0.0)
    
    # 50% X attack: Fidelity drops to 0.5
    half_attack = apply_bit_flip_attack(rho_0, attack_strength=0.5)
    assert np.isclose(quantum_fidelity(rho_0, half_attack), 0.5)


def test_phase_flip_z_attack():
    """Verify Pauli Z flips |+> to |-> at 100% attack strength."""
    rho_plus = to_density_matrix(STATE_PLUS)
    
    attacked_plus = apply_phase_flip_attack(rho_plus, attack_strength=1.0)
    assert np.isclose(quantum_fidelity(rho_plus, attacked_plus), 0.0)


def test_bit_phase_flip_y_attack():
    """Verify Pauli Y flips |0> to |1> and |+> to |->, while leaving |+_y> invariant (demonstrating need for 3 bases)."""
    rho_0 = to_density_matrix(STATE_0)
    rho_plus = to_density_matrix(STATE_PLUS)
    rho_plus_y = to_density_matrix(STATE_PLUS_Y)
    
    # Y attack flips |0> to |1> (fidelity = 0.0)
    attacked_0 = apply_bit_phase_flip_attack(rho_0, attack_strength=1.0)
    assert np.isclose(quantum_fidelity(rho_0, attacked_0), 0.0)
    
    # Y attack flips |+> to |-> (fidelity = 0.0)
    attacked_plus = apply_bit_phase_flip_attack(rho_plus, attack_strength=1.0)
    assert np.isclose(quantum_fidelity(rho_plus, attacked_plus), 0.0)
    
    # Y attack leaves |+_y> invariant since it is a Y-eigenstate (fidelity = 1.0)
    # This precisely demonstrates why multi-basis measurements (X, Y, Z) are mandatory!
    attacked_y = apply_bit_phase_flip_attack(rho_plus_y, attack_strength=1.0)
    assert np.isclose(quantum_fidelity(rho_plus_y, attacked_y), 1.0)


def test_attack_engine_quantum_dispatch():
    """Verify attack engine correctly routes attack types."""
    engine = AttackEngine()
    states = [to_density_matrix(STATE_0), to_density_matrix(STATE_PLUS)]
    
    # None
    clean = engine.apply_quantum_attack(states, attack_type="none")
    assert np.allclose(clean[0], states[0])
    
    # X attack
    attacked_x = engine.apply_quantum_attack(states, attack_type="X", attack_strength=1.0)
    assert np.allclose(attacked_x[0], to_density_matrix(STATE_1))
