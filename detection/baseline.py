"""Legitimate baseline generator establishing normal channel distribution P_{0,L} across distances."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import numpy as np

from config.photonic_config import PhotonicConfig
from photonic.optical_channel import PhotonicChannel
from quantum.pauli_states import get_pauli_state, to_density_matrix
from quantum.measurements import measure_all_pauli_bases


@dataclass
class BaselineProfile:
    """Baseline legitimate distribution and variance profile for a specific distance L."""
    distance_km: float
    mean_distribution_vector: np.ndarray  # 6-element: [X+, X-, Y+, Y-, Z0, Z1]
    variance_vector: np.ndarray
    mean_fidelity: float
    mean_tvd: float
    distribution_dict: Dict[str, float] = field(default_factory=dict)


class BaselineGenerator:
    """Generates and maintains calibrated legitimate baseline profiles P_{0,L} without attacks."""
    
    DISTRIBUTION_KEYS = ["X+", "X-", "Y+", "Y-", "Z0", "Z1"]
    
    def __init__(self, photonic_config: Optional[PhotonicConfig] = None) -> None:
        self.photonic_config = photonic_config if photonic_config is not None else PhotonicConfig()
        self.channel = PhotonicChannel(config=self.photonic_config)
        self._cache: Dict[Tuple[float, str], BaselineProfile] = {}
        
    def generate_baseline(
        self,
        distance_km: float,
        expected_state_names: Optional[List[str]] = None,
        monte_carlo_trials: int = 50,
        shots_per_basis: int = 1000,
        seed: Optional[int] = None
    ) -> BaselineProfile:
        """Run simulation of unattacked transmission over distance_km to establish P_{0,L} for the state ensemble."""
        if expected_state_names is None or len(expected_state_names) == 0:
            expected_state_names = ["|0>", "|1>", "|+>", "|+_y>"]
            
        cache_key = (float(distance_km), ",".join(expected_state_names))
        if cache_key in self._cache:
            return self._cache[cache_key]
            
        rng = np.random.default_rng(seed)
        
        # Prepare state vectors for the ensemble
        state_vecs = [get_pauli_state(name) for name in expected_state_names]
        
        collected_distributions: List[np.ndarray] = []
        fidelities: List[float] = []
        
        for _ in range(monte_carlo_trials):
            # Transmit ensemble through legitimate channel
            rhos_out = []
            for s_vec in state_vecs:
                tx_res = self.channel.transmit(s_vec, distance_km=distance_km, rng=rng)
                rhos_out.append(tx_res.output_rho)
                fidelities.append(tx_res.fidelity_with_input)
                
            avg_rho_trial = np.mean(rhos_out, axis=0)
            
            # Measure in X, Y, Z bases
            meas_suite = measure_all_pauli_bases(
                rho=avg_rho_trial,
                shots_per_basis=shots_per_basis,
                seed=int(rng.integers(0, 1000000))
            )
            collected_distributions.append(meas_suite.empirical_distribution_vector)
            
        dist_array = np.array(collected_distributions)  # (trials, 6)
        mean_dist = np.mean(dist_array, axis=0)
        var_dist = np.var(dist_array, axis=0)
        mean_fid = float(np.mean(fidelities))
        
        # Compute baseline intrinsic variation (finite shot fluctuations under H0)
        baseline_tvds = [
            0.5 * float(np.sum(np.abs(d - mean_dist)))
            for d in collected_distributions
        ]
        mean_tvd = float(np.mean(baseline_tvds))
        
        dist_dict = {
            k: float(v) for k, v in zip(self.DISTRIBUTION_KEYS, mean_dist)
        }
        
        profile = BaselineProfile(
            distance_km=distance_km,
            mean_distribution_vector=mean_dist,
            variance_vector=var_dist,
            mean_fidelity=mean_fid,
            mean_tvd=mean_tvd,
            distribution_dict=dist_dict
        )
        
        self._cache[cache_key] = profile
        return profile

    def get_baseline(
        self,
        distance_km: float,
        expected_state_names: Optional[List[str]] = None
    ) -> BaselineProfile:
        """Retrieve baseline profile for distance_km and expected states, generating it if needed."""
        if expected_state_names is None:
            expected_state_names = ["|0>", "|1>", "|+>", "|+_y>"]
        cache_key = (float(distance_km), ",".join(expected_state_names))
        if cache_key not in self._cache:
            return self.generate_baseline(distance_km, expected_state_names)
        return self._cache[cache_key]
