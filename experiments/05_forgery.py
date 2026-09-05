"""Experiment 05: Signature Forgery Probability and False Acceptance Rate."""

import os
import shutil
import csv
from core.simulator import QDSThreatSimulator
from evaluation.forgery_probability import compute_theoretical_forgery_bound, evaluate_empirical_forgery
from visualization.attack_plots import plot_forgery_probability_comparison


def run_experiment_05(trials: int = 50, distance_km: float = 50.0) -> dict:
    """Execute Experiment 05."""
    print("=" * 60)
    print("Running Experiment 05: Signature Forgery Analysis")
    print("=" * 60)
    
    sim = QDSThreatSimulator()
    forgery_results = []
    
    for i in range(trials):
        res = sim.run_simulation(
            distance_km=distance_km,
            attack_type="forgery",
            shots=1000,
            seed=i * 53
        )
        forgery_results.append(res)
        
    analysis = evaluate_empirical_forgery(forgery_results)
    
    print(f"Total Forgery Trials:            {analysis.empirical_forgery_trials}")
    print(f"Forged Signatures Accepted:      {analysis.forged_signatures_accepted}")
    print(f"Empirical Forgery Probability:   {analysis.empirical_forgery_probability:.4f}")
    print(f"Theoretical Upper Bound:         {analysis.theoretical_forgery_upper_bound:.6f}")
    
    fig_path = plot_forgery_probability_comparison(
        theoretical_bound=analysis.theoretical_forgery_upper_bound,
        empirical_prob=analysis.empirical_forgery_probability,
        trials=analysis.empirical_forgery_trials
    )
    
    csv_path = "results/tables/05_forgery_analysis.csv"
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        writer.writerow(["signature_qubit_count", analysis.signature_qubit_count])
        writer.writerow(["mismatch_threshold", analysis.mismatch_threshold])
        writer.writerow(["theoretical_bound", analysis.theoretical_forgery_upper_bound])
        writer.writerow(["empirical_trials", analysis.empirical_forgery_trials])
        writer.writerow(["forged_accepted", analysis.forged_signatures_accepted])
        writer.writerow(["empirical_forgery_prob", analysis.empirical_forgery_probability])
        
    alt_csv = "results/tables/exp05_forgery.csv"
    shutil.copyfile(csv_path, alt_csv)
        
    print(f"Saved figure: {fig_path}")
    print(f"Saved table:  {csv_path}\n")
    return {
        "empirical_forgery_prob": analysis.empirical_forgery_probability,
        "theoretical_bound": analysis.theoretical_forgery_upper_bound
    }


if __name__ == "__main__":
    run_experiment_05()
