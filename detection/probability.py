"""Empirical probability distribution computation and normalization utilities."""

from typing import Dict, List, Union
import numpy as np


def normalize_distribution(counts_or_weights: Union[List[float], np.ndarray]) -> np.ndarray:
    """Normalize a 1D vector of counts or weights into a valid probability distribution."""
    arr = np.array(counts_or_weights, dtype=float)
    total = np.sum(arr)
    if total <= 0:
        n = len(arr)
        return np.ones(n) / max(1, n)
    return arr / total


def counts_to_empirical_distribution(
    counts_dict: Dict[str, int],
    ordered_keys: List[str]
) -> np.ndarray:
    """Convert a dictionary of outcome counts to a normalized empirical probability vector."""
    counts = [counts_dict.get(k, 0) for k in ordered_keys]
    return normalize_distribution(counts)


def format_distribution_dict(keys: List[str], probs: np.ndarray) -> Dict[str, float]:
    """Convert key names and probability array into a clean dictionary."""
    return {k: float(p) for k, p in zip(keys, probs)}
