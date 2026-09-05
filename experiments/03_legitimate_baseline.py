"""Experiment 03: Legitimate Baseline Calibration P_{0,L} Across Distances."""

import os
import shutil
import csv
from detection.baseline import BaselineGenerator
from visualization.channel_plots import plot_legitimate_baseline_tvd


def run_experiment_03(distances_km: list[float] = None) -> list[dict]:
    """Execute Experiment 03."""
    print("=" * 60)
    print("Running Experiment 03: Legitimate Baseline Generator P_{0,L}")
    print("=" * 60)
    
    if distances_km is None:
        distances_km = [10.0, 25.0, 50.0, 100.0, 150.0, 200.0]
        
    generator = BaselineGenerator()
    records = []
    mean_tvds = []
    mean_fidelities = []
    
    for dist in distances_km:
        profile = generator.generate_baseline(dist, monte_carlo_trials=100, shots_per_basis=1000)
        rec = {
            "distance_km": dist,
            "mean_tvd": profile.mean_tvd,
            "mean_fidelity": profile.mean_fidelity,
            "prob_X_plus": profile.mean_distribution_vector[0],
            "prob_X_minus": profile.mean_distribution_vector[1],
            "prob_Y_plus": profile.mean_distribution_vector[2],
            "prob_Y_minus": profile.mean_distribution_vector[3],
            "prob_Z_0": profile.mean_distribution_vector[4],
            "prob_Z_1": profile.mean_distribution_vector[5],
        }
        records.append(rec)
        mean_tvds.append(profile.mean_tvd)
        mean_fidelities.append(profile.mean_fidelity)
        print(f"Baseline {dist:5.1f} km | Baseline TVD: {profile.mean_tvd:.4f} | Fidelity: {profile.mean_fidelity:.4f}")
        
    fig_path = plot_legitimate_baseline_tvd(distances_km, mean_tvds, mean_fidelities)
        
    csv_path = "results/tables/03_legitimate_baselines.csv"
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        fieldnames = list(records[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
        
    alt_csv = "results/tables/exp03_legitimate_baseline.csv"
    shutil.copyfile(csv_path, alt_csv)
        
    print(f"Saved figure: {fig_path}")
    print(f"Saved baseline table: {csv_path}\n")
    return records


if __name__ == "__main__":
    run_experiment_03()
