"""Experiment 07: Signer Identity Impersonation and Spoofing Rejection."""

import os
import shutil
import csv
from core.simulator import QDSThreatSimulator
from visualization.attack_plots import plot_cyber_attack_rejections


def run_experiment_07(trials: int = 30) -> dict:
    """Execute Experiment 07."""
    print("=" * 60)
    print("Running Experiment 07: Signer Impersonation Defense")
    print("=" * 60)
    
    sim = QDSThreatSimulator()
    impersonations_blocked = 0
    
    for i in range(trials):
        res = sim.run_simulation(
            signer_id="Eve_Rogue_Signer",
            shots=1000,
            seed=i * 67
        )
        if not res.protocol_checks.signer_authenticated or res.final_decision == "REJECT":
            impersonations_blocked += 1
            
    detection_rate = impersonations_blocked / trials
    print(f"Total Impersonation Trials: {trials}")
    print(f"Spoofed Signers Blocked:    {impersonations_blocked}")
    print(f"Impersonation Defense Rate: {detection_rate * 100:.1f}%\n")
    
    fig_path = plot_cyber_attack_rejections(
        attack_name="Signer Impersonation",
        total_trials=trials,
        rejected_trials=impersonations_blocked,
        detection_rate=detection_rate,
        output_path="results/figures/07_impersonation_rejection.png"
    )
    alt_fig = "results/figures/exp07_impersonation_rejection.png"
    shutil.copyfile(fig_path, alt_fig)
    
    csv_path = "results/tables/07_impersonation_rejection.csv"
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["trials", "blocked", "detection_rate"])
        writer.writerow([trials, impersonations_blocked, detection_rate])
        
    alt_csv = "results/tables/exp07_impersonation.csv"
    shutil.copyfile(csv_path, alt_csv)
        
    print(f"Saved figure: {fig_path}")
    print(f"Saved table:  {csv_path}\n")
    return {"detection_rate": detection_rate}


if __name__ == "__main__":
    run_experiment_07()
