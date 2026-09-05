"""Deterministic statistical distance measures for quantum measurement distributions."""

import numpy as np


def compute_total_variation_distance(p: np.ndarray, q: np.ndarray) -> float:
    """Compute Total Variation Distance (TVD): D_TV(P, Q) = 0.5 * sum_i |P_i - Q_i|.
    
    Properties:
    - In [0.0, 1.0] for probability distributions
    - D_TV = 0 for identical distributions
    - D_TV = 1 for completely disjoint distributions
    """
    p = np.asarray(p, dtype=float)
    q = np.asarray(q, dtype=float)
    if p.shape != q.shape:
        raise ValueError(f"Shape mismatch: {p.shape} vs {q.shape}")
    tvd = 0.5 * np.sum(np.abs(p - q))
    return float(np.clip(tvd, 0.0, 1.0))


def compute_bhattacharyya_distance(p: np.ndarray, q: np.ndarray, eps: float = 1e-12) -> float:
    """Compute Bhattacharyya Distance: D_B(P, Q) = -ln(sum_i sqrt(P_i * Q_i))."""
    p = np.asarray(p, dtype=float)
    q = np.asarray(q, dtype=float)
    bc = np.sum(np.sqrt(np.clip(p * q, 0.0, None)))
    bc = max(eps, min(1.0, bc))
    return float(-np.log(bc))


def compute_hellinger_distance(p: np.ndarray, q: np.ndarray) -> float:
    """Compute Hellinger Distance: H(P, Q) = (1/sqrt(2)) * sqrt(sum_i (sqrt(P_i) - sqrt(Q_i))^2)."""
    p = np.asarray(p, dtype=float)
    q = np.asarray(q, dtype=float)
    h_sq = 0.5 * np.sum((np.sqrt(np.clip(p, 0.0, None)) - np.sqrt(np.clip(q, 0.0, None))) ** 2)
    return float(np.sqrt(max(0.0, h_sq)))


def compute_kl_divergence(p: np.ndarray, q: np.ndarray, eps: float = 1e-12) -> float:
    """Compute Kullback-Leibler divergence D_KL(P || Q) = sum_i P_i * ln(P_i / Q_i)."""
    p = np.asarray(p, dtype=float) + eps
    q = np.asarray(q, dtype=float) + eps
    p = p / np.sum(p)
    q = q / np.sum(q)
    return float(np.sum(p * np.log(p / q)))
