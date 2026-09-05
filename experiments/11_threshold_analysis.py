"""Experiment 11: Receiver Operating Characteristic (ROC) and Threshold Trade-Off Analysis."""

import os
import shutil
import csv
import numpy as np
from core.simulator import QDSThreatSimulator
from visualization.security_plots import plot_threshold_roc_curve


def run_experiment_11(trials_per_class: int = 50, distance_km: float = 50.0) -> dict:
    """Execute Experiment 11."""
    print("=" * 60)
    print("Running Experiment 11: ROC Curve and Threshold Trade-off Analysis")
    print("=" * 60)
    
    sim = QDSThreatSimulator()
    
    # 1. Collect Normal TVD samples
    normal_tvds = []
    for seed in range(trials_per_class):
        res = sim.run_simulation(distance_km=distance_km, attack_type="none", seed=seed)
        normal_tvds.append(res.statistics.total_variation_distance)
        
    # 2. Collect Attacked TVD samples (e.g. 20% X attack)
    attacked_tvds = []
    for seed in range(trials_per_class):
        res = sim.run_simulation(distance_km=distance_km, attack_type="X", attack_strength=0.20, seed=1000 + seed)
        attacked_tvds.append(res.statistics.total_variation_distance)
        
    # Sweep threshold tau from min to max
    all_tvds = normal_tvds + attacked_tvds
    tau_sweep = np.linspace(min(all_tvds) * 0.8, max(all_tvds) * 1.2, 50)
    
    fpr_list = []
    tpr_list = []
    records = []
    
    for tau in tau_sweep:
        # False Positives: Normal runs with TVD > tau
        fp = sum(1 for d in normal_tvds if d > tau)
        fpr = fp / len(normal_tvds)
        
        # True Positives: Attacked runs with TVD > tau
        tp = sum(1 for d in attacked_tvds if d > tau)
        tpr = tp / len(attacked_tvds)
        
        fpr_list.append(fpr)
        tpr_list.append(tpr)
        
        records.append({"threshold": float(tau), "fpr_frr": fpr, "tpr_pd": tpr})
        
    # Sort for clean ROC plot
    sorted_pairs = sorted(zip(fpr_list, tpr_list), key=lambda p: (p[0], p[1]))
    sorted_fpr = [p[0] for p in sorted_pairs]
    sorted_tpr = [p[1] for p in sorted_pairs]
    
    # Approximate Area Under Curve (AUC)
    auc = float(np.trapezoid(sorted_tpr, sorted_fpr)) if hasattr(np, 'trapezoid') else float(np.trapz(sorted_tpr, sorted_fpr))
    print(f"Computed ROC Area Under Curve (AUC): {auc:.4f}")
    
    fig_path = plot_threshold_roc_curve(sorted_fpr, sorted_tpr)
    
    csv_path = "results/tables/11_threshold_roc.csv"
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["threshold", "fpr_frr", "tpr_pd"])
        writer.writeheader()
        writer.writerows(records)
        
    alt_csv = "results/tables/exp11_threshold_analysis.csv"
    shutil.copyfile(csv_path, alt_csv)
        
    print(f"Saved figure: {fig_path}")
    print(f"Saved table:  {csv_path}\n")
    return {"auc": auc, "records": records}


if __name__ == "__main__":
    run_experiment_11()
