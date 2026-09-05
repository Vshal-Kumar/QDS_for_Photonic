"""Experiment 02: Long-Distance Photonic Channel Loss and Noise Scaling."""

import os
import shutil
import csv
import numpy as np
from photonic.optical_channel import PhotonicChannel
from quantum.pauli_states import get_pauli_state
from visualization.channel_plots import plot_distance_vs_transmission_and_fidelity


def run_experiment_02(distances_km: list[float] = None) -> list[dict]:
    """Execute Experiment 02."""
    print("=" * 60)
    print("Running Experiment 02: Photonic Optical Channel Scaling")
    print("=" * 60)
    
    if distances_km is None:
        distances_km = [10.0, 25.0, 50.0, 100.0, 150.0, 200.0]
        
    channel = PhotonicChannel()
    base_state = get_pauli_state("|+>")
    
    records = []
    transmissions = []
    fidelities = []
    
    for dist in distances_km:
        tx_fids = []
        for seed in range(30):
            res = channel.transmit(base_state, distance_km=dist, rng=np.random.default_rng(seed))
            tx_fids.append(res.fidelity_with_input)
            
        mean_fid = float(np.mean(tx_fids))
        trans = res.transmission_efficiency
        loss_db = res.loss_db
        
        transmissions.append(trans)
        fidelities.append(mean_fid)
        
        rec = {
            "distance_km": dist,
            "transmittance": trans,
            "loss_db": loss_db,
            "mean_fidelity": mean_fid
        }
        records.append(rec)
        print(f"Distance {dist:5.1f} km | Loss: {loss_db:5.1f} dB | Transmittance: {trans:8.4f} | Fidelity: {mean_fid:.4f}")
        
    fig_path = plot_distance_vs_transmission_and_fidelity(distances_km, transmissions, fidelities)
    
    csv_path = "results/tables/02_photonic_channel_scaling.csv"
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["distance_km", "transmittance", "loss_db", "mean_fidelity"])
        writer.writeheader()
        writer.writerows(records)
        
    alt_csv = "results/tables/exp02_photonic_channel.csv"
    shutil.copyfile(csv_path, alt_csv)
        
    print(f"Saved figure: {fig_path}")
    print(f"Saved table:  {csv_path}\n")
    return records


if __name__ == "__main__":
    run_experiment_02()
