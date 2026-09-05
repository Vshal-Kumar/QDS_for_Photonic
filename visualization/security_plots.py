"""Publication-quality security trade-off curves: ROC, FAR vs FRR, and Shot Scaling."""

import os
import shutil
import matplotlib.pyplot as plt
import numpy as np


def plot_shot_scaling_vs_pd(
    shot_counts: list[int],
    detection_probs: list[float],
    output_path: str = "results/figures/10_measurement_scaling.png"
) -> str:
    """Generate plot of measurement shot count N vs Threat Detection Probability."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    plt.figure(figsize=(9, 5), dpi=300)
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    plt.plot(shot_counts, detection_probs, marker='o', color='#1d3557', linewidth=2.2, label='Empirical $P_D(N)$')
    plt.xscale('log')
    plt.xlabel('Measurement Shot Count $N$ (Log Scale)', fontsize=12, fontweight='bold')
    plt.ylabel('Threat Detection Probability $P_D$', fontsize=12, fontweight='bold')
    plt.title('Statistical Detection Convergence vs Measurement Budget $N$', fontsize=13, fontweight='bold', pad=12)
    plt.ylim(-0.05, 1.05)
    plt.legend(frameon=True, loc='lower right')
    plt.tight_layout()
    plt.savefig(output_path)
    
    alt_path = "results/figures/exp10_shot_scaling.png"
    if output_path != alt_path:
        shutil.copyfile(output_path, alt_path)
        
    plt.close()
    return output_path


def plot_threshold_roc_curve(
    fpr_list: list[float],
    tpr_list: list[float],
    output_path: str = "results/figures/11_threshold_roc_curve.png"
) -> str:
    """Generate ROC curve (True Positive Rate vs False Positive Rate / FAR)."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    plt.figure(figsize=(7, 7), dpi=300)
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    plt.plot(fpr_list, tpr_list, color='#e63946', linewidth=2.5, label='Statistical Threat Detector ROC')
    plt.plot([0, 1], [0, 1], color='#6c757d', linestyle='--', label='Random Classifier (AUC = 0.5)')
    
    plt.xlabel('False Rejection Rate (FRR) / FPR', fontsize=12, fontweight='bold')
    plt.ylabel('True Positive Rate (TPR) / $P_D$', fontsize=12, fontweight='bold')
    plt.title('Receiver Operating Characteristic (ROC) of Statistical Detector', fontsize=13, fontweight='bold', pad=12)
    plt.xlim(-0.02, 1.02)
    plt.ylim(-0.02, 1.02)
    plt.legend(frameon=True, loc='lower right')
    plt.tight_layout()
    plt.savefig(output_path)
    
    alt_path = "results/figures/exp11_threshold_roc.png"
    if output_path != alt_path:
        shutil.copyfile(output_path, alt_path)
        
    plt.close()
    return output_path
