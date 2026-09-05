"""Experiment 04: Pauli Attacks (X, Y, Z) and Detection Probability vs Attack Strength."""

import os
import shutil
import csv
import numpy as np
from core.simulator import QDSThreatSimulator
from visualization.attack_plots import plot_attack_strength_vs_detection_probability


def run_experiment_04(
    distance_km: float = 50.0,
    strengths: list[float] = None,
    trials_per_point: int = 30
) -> dict:
    """Execute Experiment 04."""
    print("=" * 60)
    print("Running Experiment 04: Pauli Physical Attacks (X, Y, Z)")
    print("=" * 60)
    
    if strengths is None:
        strengths = [0.0, 0.05, 0.10, 0.20, 0.30, 0.50, 0.75, 1.00]
        
    sim = QDSThreatSimulator()
    attacks = ["X", "Y", "Z"]
    
    results = {atk: [] for atk in attacks}
    csv_rows = []
    
    for atk in attacks:
        print(f"--- Evaluating Pauli {atk} Attack ---")
        for st in strengths:
            detected_count = 0
            tvds = []
            
            for seed in range(trials_per_point):
                res = sim.run_simulation(
                    distance_km=distance_km,
                    attack_type=atk if st > 0 else "none",
                    attack_strength=st,
                    shots=1000,
                    seed=seed * 31 + int(st * 100)
                )
                if res.final_decision != "ACCEPT":
                    detected_count += 1
                tvds.append(res.statistics.total_variation_distance)
                
            p_d = detected_count / trials_per_point
            mean_tvd = float(np.mean(tvds))
            results[atk].append(p_d)
            
            csv_rows.append({
                "attack": atk,
                "strength": st,
                "detection_probability": p_d,
                "mean_tvd": mean_tvd,
                "trials": trials_per_point
            })
            print(f"  Attack {atk} | Strength: {st*100:4.0f}% | P_D: {p_d:6.2f} | Mean TVD: {mean_tvd:.4f}")
            
    fig_path = plot_attack_strength_vs_detection_probability(
        attack_strengths=strengths,
        pd_x=results["X"],
        pd_y=results["Y"],
        pd_z=results["Z"]
    )
    
    csv_path = "results/tables/04_pauli_attacks.csv"
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["attack", "strength", "detection_probability", "mean_tvd", "trials"])
        writer.writeheader()
        writer.writerows(csv_rows)
        
    alt_csv = "results/tables/exp04_pauli_attacks.csv"
    shutil.copyfile(csv_path, alt_csv)
        
    print(f"Saved figure: {fig_path}")
    print(f"Saved table:  {csv_path}\n")
    return results


if __name__ == "__main__":
    run_experiment_04()
