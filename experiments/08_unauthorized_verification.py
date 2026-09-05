"""Experiment 08: Unauthorized Verifier Access Rejection."""

import os
import shutil
import csv
from core.simulator import QDSThreatSimulator
from visualization.attack_plots import plot_cyber_attack_rejections


def run_experiment_08(trials: int = 30) -> dict:
    """Execute Experiment 08."""
    print("=" * 60)
    print("Running Experiment 08: Unauthorized Verifier Access Defense")
    print("=" * 60)
    
    sim = QDSThreatSimulator()
    unauthorized_blocked = 0
    
    for i in range(trials):
        res = sim.run_simulation(
            verifier_id="Eve_Rogue_Verifier",
            shots=1000,
            seed=i * 71
        )
        if not res.protocol_checks.verifier_authorized or res.final_decision == "REJECT":
            unauthorized_blocked += 1
            
    detection_rate = unauthorized_blocked / trials
    print(f"Total Unauthorized Access Trials: {trials}")
    print(f"Rogue Verifiers Blocked:          {unauthorized_blocked}")
    print(f"Authorization Defense Rate:       {detection_rate * 100:.1f}%\n")
    
    fig_path = plot_cyber_attack_rejections(
        attack_name="Unauthorized Verifier",
        total_trials=trials,
        rejected_trials=unauthorized_blocked,
        detection_rate=detection_rate,
        output_path="results/figures/08_unauthorized_verification.png"
    )
    alt_fig = "results/figures/exp08_unauthorized_verification.png"
    shutil.copyfile(fig_path, alt_fig)
    
    csv_path = "results/tables/08_unauthorized_verification.csv"
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["trials", "blocked", "detection_rate"])
        writer.writerow([trials, unauthorized_blocked, detection_rate])
        
    alt_csv = "results/tables/exp08_unauthorized_verification.csv"
    shutil.copyfile(csv_path, alt_csv)
        
    print(f"Saved figure: {fig_path}")
    print(f"Saved table:  {csv_path}\n")
    return {"detection_rate": detection_rate}


if __name__ == "__main__":
    run_experiment_08()
