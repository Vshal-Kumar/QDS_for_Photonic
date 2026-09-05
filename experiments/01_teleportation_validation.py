"""Experiment 01: Quantum Teleportation Correctness Validation across all 6 Pauli Eigenstates."""

import os
import shutil
import numpy as np
from quantum.pauli_states import get_pauli_state
from quantum.teleportation import teleport_quantum_state
from visualization.quantum_plots import plot_teleportation_fidelity_bar
import csv


def run_experiment_01(trials_per_state: int = 50) -> dict:
    """Execute Experiment 01."""
    print("=" * 60)
    print("Running Experiment 01: Teleportation Correctness Validation")
    print("=" * 60)
    
    states = ["|0>", "|1>", "|+>", "|->", "|+_y>", "|-_y>"]
    results = {}
    fidelities_mean = []
    
    for st_name in states:
        vec = get_pauli_state(st_name)
        fids = []
        for i in range(trials_per_state):
            res = teleport_quantum_state(vec, state_name=st_name, seed=i * 17)
            fids.append(res.ideal_fidelity)
            
        mean_fid = float(np.mean(fids))
        std_fid = float(np.std(fids))
        fidelities_mean.append(mean_fid)
        results[st_name] = {"mean_fidelity": mean_fid, "std_fidelity": std_fid}
        print(f"State {st_name.ljust(6)}: Mean Fidelity = {mean_fid:.6f} +/- {std_fid:.6f}")
        
    fig_path = plot_teleportation_fidelity_bar(states, fidelities_mean)
    
    # Save CSV
    csv_path = "results/tables/01_teleportation_validation.csv"
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["state", "mean_fidelity", "std_fidelity"])
        for st, data in results.items():
            writer.writerow([st, data["mean_fidelity"], data["std_fidelity"]])
            
    alt_csv = "results/tables/exp01_teleportation_validation.csv"
    shutil.copyfile(csv_path, alt_csv)
            
    print(f"Saved figure: {fig_path}")
    print(f"Saved table:  {csv_path}\n")
    return results


if __name__ == "__main__":
    run_experiment_01()
