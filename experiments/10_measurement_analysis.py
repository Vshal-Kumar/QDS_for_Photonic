"""Experiment 10: Measurement Count Scaling (N = 100 to 10000) vs Detection Sensitivity."""

import os
import shutil
import csv
from core.simulator import QDSThreatSimulator
from visualization.security_plots import plot_shot_scaling_vs_pd


def run_experiment_10(
    shot_counts: list[int] = None,
    distance_km: float = 50.0,
    attack_strength: float = 0.15,
    trials_per_point: int = 30
) -> dict:
    """Execute Experiment 10."""
    print("=" * 60)
    print("Running Experiment 10: Measurement Count (Shots) Scaling Analysis")
    print("=" * 60)
    
    if shot_counts is None:
        shot_counts = [100, 500, 1000, 5000, 10000]
        
    sim = QDSThreatSimulator()
    detection_probs = []
    records = []
    
    for shots in shot_counts:
        detected_count = 0
        for seed in range(trials_per_point):
            res = sim.run_simulation(
                distance_km=distance_km,
                attack_type="X",
                attack_strength=attack_strength,
                shots=shots,
                seed=seed * 71
            )
            if res.final_decision != "ACCEPT":
                detected_count += 1
                
        p_d = detected_count / trials_per_point
        detection_probs.append(p_d)
        
        rec = {
            "shots": shots,
            "attack_strength": attack_strength,
            "detection_probability": p_d,
            "trials": trials_per_point
        }
        records.append(rec)
        print(f"Shots: {shots:6d} | Detection Probability P_D: {p_d:6.2f} (Attack: {attack_strength*100:.0f}% X)")
        
    fig_path = plot_shot_scaling_vs_pd(shot_counts, detection_probs)
    
    csv_path = "results/tables/10_measurement_scaling.csv"
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["shots", "attack_strength", "detection_probability", "trials"])
        writer.writeheader()
        writer.writerows(records)
        
    alt_csv = "results/tables/exp10_measurement_analysis.csv"
    shutil.copyfile(csv_path, alt_csv)
        
    print(f"Saved figure: {fig_path}")
    print(f"Saved table:  {csv_path}\n")
    return records


if __name__ == "__main__":
    run_experiment_10()
