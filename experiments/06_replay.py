"""Experiment 06: Nonce Replay Attack Detection and Performance."""

import os
import shutil
import csv
from core.simulator import QDSThreatSimulator
from visualization.attack_plots import plot_cyber_attack_rejections


def run_experiment_06(trials: int = 30) -> dict:
    """Execute Experiment 06."""
    print("=" * 60)
    print("Running Experiment 06: Nonce Replay Attack Defense")
    print("=" * 60)
    
    sim = QDSThreatSimulator()
    replays_blocked = 0
    
    for i in range(trials):
        res = sim.run_simulation(
            is_replay=True,
            shots=1000,
            seed=i * 61
        )
        if not res.protocol_checks.nonce_valid or res.final_decision == "REJECT":
            replays_blocked += 1
            
    detection_rate = replays_blocked / trials
    print(f"Total Replay Trials:      {trials}")
    print(f"Replayed Nonces Blocked:  {replays_blocked}")
    print(f"Replay Defense Rate:      {detection_rate * 100:.1f}%\n")
    
    fig_path = plot_cyber_attack_rejections(
        attack_name="Nonce Replay",
        total_trials=trials,
        rejected_trials=replays_blocked,
        detection_rate=detection_rate,
        output_path="results/figures/06_replay_detection.png"
    )
    alt_fig = "results/figures/exp06_replay_detection.png"
    shutil.copyfile(fig_path, alt_fig)
    
    csv_path = "results/tables/06_replay_detection.csv"
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["trials", "blocked", "detection_rate"])
        writer.writerow([trials, replays_blocked, detection_rate])
        
    alt_csv = "results/tables/exp06_replay.csv"
    shutil.copyfile(csv_path, alt_csv)
        
    print(f"Saved figure: {fig_path}")
    print(f"Saved table:  {csv_path}\n")
    return {"detection_rate": detection_rate}


if __name__ == "__main__":
    run_experiment_06()
