"""Experiment 09: Long-Distance Detection Sensitivity and Adaptive Threshold Evaluation."""

import os
import shutil
import csv
import numpy as np
from core.simulator import QDSThreatSimulator
from visualization.channel_plots import plot_distance_sensitivity


def run_experiment_09(distances_km: list[float] = None, attack_strength: float = 0.20) -> list[dict]:
    """Execute Experiment 09."""
    print("=" * 60)
    print("Running Experiment 09: Distance Impact on Threat Detection")
    print("=" * 60)
    
    if distances_km is None:
        distances_km = [10.0, 25.0, 50.0, 100.0, 150.0, 200.0]
        
    sim = QDSThreatSimulator()
    records = []
    clean_acc_rates = []
    atk_det_rates = []
    
    for dist in distances_km:
        clean_tvds = []
        clean_accepts = 0
        trials = 25
        for seed in range(trials):
            res_c = sim.run_simulation(distance_km=dist, attack_type="none", seed=seed)
            clean_tvds.append(res_c.statistics.total_variation_distance)
            if res_c.final_decision == "ACCEPT":
                clean_accepts += 1
                
        atk_tvds = []
        atk_detected = 0
        for seed in range(trials):
            res_a = sim.run_simulation(
                distance_km=dist,
                attack_type="X",
                attack_strength=attack_strength,
                seed=500 + seed
            )
            atk_tvds.append(res_a.statistics.total_variation_distance)
            if res_a.final_decision != "ACCEPT":
                atk_detected += 1
                
        c_rate = clean_accepts / trials
        a_rate = atk_detected / trials
        clean_acc_rates.append(c_rate)
        atk_det_rates.append(a_rate)
        
        rec = {
            "distance_km": dist,
            "attack_strength": attack_strength,
            "clean_acceptance_rate": c_rate,
            "attack_detection_rate": a_rate,
            "mean_clean_tvd": float(np.mean(clean_tvds)),
            "mean_attack_tvd": float(np.mean(atk_tvds)),
            "adaptive_threshold": res_c.statistics.adaptive_threshold
        }
        records.append(rec)
        print(f"Dist: {dist:5.1f} km | Clean Acc: {rec['clean_acceptance_rate']*100:5.1f}% | Atk Det (20% X): {rec['attack_detection_rate']*100:5.1f}% | Tau: {rec['adaptive_threshold']:.4f}")
        
    fig_path = plot_distance_sensitivity(distances_km, clean_acc_rates, atk_det_rates)
        
    csv_path = "results/tables/09_distance_analysis.csv"
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        fieldnames = list(records[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
        
    alt_csv = "results/tables/exp09_distance_analysis.csv"
    shutil.copyfile(csv_path, alt_csv)
        
    print(f"Saved figure: {fig_path}")
    print(f"Saved table:  {csv_path}\n")
    return records


if __name__ == "__main__":
    run_experiment_09()
