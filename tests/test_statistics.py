"""Unit tests for statistical distance metrics, chi-square test, and hypothesis testing."""

import pytest
import numpy as np
from detection.statistical_distance import (
    compute_total_variation_distance,
    compute_bhattacharyya_distance,
    compute_hellinger_distance,
    compute_kl_divergence
)
from detection.chi_square import compute_chi_square_test
from detection.hypothesis_testing import compute_z_scores, evaluate_hypothesis_test


def test_total_variation_distance():
    """Verify TVD properties: 0 for identical, 1 for disjoint, symmetric, and bounded."""
    p = np.array([0.5, 0.5])
    q = np.array([0.5, 0.5])
    assert np.isclose(compute_total_variation_distance(p, q), 0.0)
    
    # Completely disjoint distributions
    p_disjoint = np.array([1.0, 0.0])
    q_disjoint = np.array([0.0, 1.0])
    assert np.isclose(compute_total_variation_distance(p_disjoint, q_disjoint), 1.0)
    
    # Partial deviation
    p_part = np.array([0.7, 0.3])
    q_part = np.array([0.4, 0.6])
    # TVD = 0.5 * (|0.7-0.4| + |0.3-0.6|) = 0.5 * (0.3 + 0.3) = 0.3
    assert np.isclose(compute_total_variation_distance(p_part, q_part), 0.3)


def test_chi_square_goodness_of_fit():
    """Verify chi-square test yields p~1 for identical distributions and p~0 for significantly perturbed distributions."""
    p = np.array([0.25, 0.25, 0.25, 0.25])
    
    # Identical: chi2 = 0, p_val = 1.0
    chi2, p_val, dof = compute_chi_square_test(p, p, shots=1000)
    assert np.isclose(chi2, 0.0)
    assert np.isclose(p_val, 1.0)
    assert dof == 3
    
    # Heavily perturbed: p ~ 0
    q_attacked = np.array([0.80, 0.10, 0.05, 0.05])
    chi2_atk, p_val_atk, _ = compute_chi_square_test(q_attacked, p, shots=1000)
    assert chi2_atk > 50.0
    assert p_val_atk < 1e-6


def test_hypothesis_z_testing():
    """Verify hypothesis test detects significant statistical deviation."""
    base = np.array([0.5, 0.5])
    
    # Normal fluctuation (e.g. 505 / 1000 vs 500 / 1000)
    normal_obs = np.array([0.505, 0.495])
    res_norm = evaluate_hypothesis_test(normal_obs, base, shots=1000, alpha=0.05)
    assert res_norm.reject_null_h0 is False
    
    # Attack fluctuation (e.g. 700 / 1000 vs 500 / 1000)
    attack_obs = np.array([0.70, 0.30])
    res_atk = evaluate_hypothesis_test(attack_obs, base, shots=1000, alpha=0.05)
    assert res_atk.reject_null_h0 is True
    assert res_atk.max_z_score > 10.0
