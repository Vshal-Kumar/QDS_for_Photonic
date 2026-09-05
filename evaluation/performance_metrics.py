"""Performance and runtime efficiency metrics for QDS verification."""

from dataclasses import dataclass
from typing import List
import numpy as np
from core.results import SimulationResult


@dataclass
class PerformanceSummary:
    """Consolidated runtime efficiency and latency metrics."""
    total_runs: int
    mean_total_verification_ms: float
    std_total_verification_ms: float
    mean_quantum_sim_ms: float
    mean_channel_sim_ms: float
    mean_teleportation_ms: float
    mean_measurement_ms: float
    mean_statistical_analysis_ms: float
    mean_protocol_checks_ms: float
    throughput_verifications_per_sec: float


def compute_performance_metrics(results: List[SimulationResult]) -> PerformanceSummary:
    """Analyze latency profile and computational efficiency across simulation runs."""
    n = len(results)
    if n == 0:
        return PerformanceSummary(0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        
    totals = [r.timing.total_verification_ms for r in results]
    q_sims = [r.timing.quantum_sim_ms for r in results]
    ch_sims = [r.timing.channel_sim_ms for r in results]
    teleports = [r.timing.teleportation_ms for r in results]
    meass = [r.timing.measurement_ms for r in results]
    stats = [r.timing.statistical_analysis_ms for r in results]
    protos = [r.timing.protocol_checks_ms for r in results]
    
    mean_total = float(np.mean(totals))
    std_total = float(np.std(totals))
    
    tps = 1000.0 / max(1e-3, mean_total) if mean_total > 0 else 0.0
    
    return PerformanceSummary(
        total_runs=n,
        mean_total_verification_ms=mean_total,
        std_total_verification_ms=std_total,
        mean_quantum_sim_ms=float(np.mean(q_sims)),
        mean_channel_sim_ms=float(np.mean(ch_sims)),
        mean_teleportation_ms=float(np.mean(teleports)),
        mean_measurement_ms=float(np.mean(meass)),
        mean_statistical_analysis_ms=float(np.mean(stats)),
        mean_protocol_checks_ms=float(np.mean(protos)),
        throughput_verifications_per_sec=tps
    )
