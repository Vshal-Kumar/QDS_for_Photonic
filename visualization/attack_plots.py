"""Publication-quality plots for attack detection curves (X, Y, Z), forgery, and cyber attacks."""

import os
import shutil
import matplotlib.pyplot as plt
import numpy as np


def plot_attack_strength_vs_detection_probability(
    attack_strengths: list[float],
    pd_x: list[float],
    pd_y: list[float],
    pd_z: list[float],
    output_path: str = "results/figures/04_attack_strength_vs_detection.png"
) -> str:
    """Generate multi-curve plot comparing Detection Probability P_D for X, Y, and Z Pauli attacks."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    plt.figure(figsize=(9, 5.5), dpi=300)
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    strengths_pct = [s * 100 for s in attack_strengths]
    
    plt.plot(strengths_pct, pd_x, marker='o', color='#e63946', linewidth=2.2, label='Pauli $X$ (Bit-Flip) Attack')
    plt.plot(strengths_pct, pd_y, marker='^', color='#457b9d', linewidth=2.2, label='Pauli $Y$ (Bit-Phase-Flip) Attack')
    plt.plot(strengths_pct, pd_z, marker='s', color='#2a9d8f', linewidth=2.2, label='Pauli $Z$ (Phase-Flip) Attack')
    
    plt.axhline(0.95, color='#6c757d', linestyle=':', label='95% High-Confidence Detection Threshold')
    plt.xlabel('Adversary Attack Strength $p_a$ (%)', fontsize=12, fontweight='bold')
    plt.ylabel('Detection Probability $P_D$', fontsize=12, fontweight='bold')
    plt.title('Threat Detection Probability vs Adversarial Attack Strength', fontsize=13, fontweight='bold', pad=12)
    plt.ylim(-0.05, 1.05)
    plt.legend(frameon=True, loc='lower right')
    plt.tight_layout()
    plt.savefig(output_path)
    
    alt_path = "results/figures/exp04_pauli_attacks_pd.png"
    if output_path != alt_path:
        shutil.copyfile(output_path, alt_path)
        
    plt.close()
    return output_path


def plot_forgery_probability_comparison(
    theoretical_bound: float,
    empirical_prob: float,
    trials: int,
    output_path: str = "results/figures/05_forgery_analysis.png"
) -> str:
    """Generate plot comparing analytical vs empirical signature forgery bounds."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    plt.figure(figsize=(8, 5), dpi=300)
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    categories = ['Theoretical Bound\n(Information-Theoretic)', f'Empirical Result\n({trials} Simulated Trials)']
    values = [theoretical_bound, empirical_prob]
    colors = ['#457b9d', '#2a9d8f']
    
    bars = plt.bar(categories, values, color=colors, width=0.45, edgecolor='#1d3557', linewidth=1.2)
    plt.ylabel('Forgery Probability $P_{\\text{forge}}$', fontsize=12, fontweight='bold')
    plt.title('Signature Forgery Resistance: Theoretical Upper Bound vs Empirical Trials', fontsize=13, fontweight='bold', pad=12)
    plt.ylim(0, max(0.005, theoretical_bound * 1.5))
    
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.0001, f"{yval:.6f}", ha='center', va='bottom', fontsize=11, fontweight='bold')
        
    plt.tight_layout()
    plt.savefig(output_path)
    
    alt_path = "results/figures/exp05_forgery_probability.png"
    if output_path != alt_path:
        shutil.copyfile(output_path, alt_path)
        
    plt.close()
    return output_path


def plot_cyber_attack_rejections(
    attack_name: str,
    total_trials: int,
    rejected_trials: int,
    detection_rate: float,
    output_path: str
) -> str:
    """Generate bar plot showing cyber threat rejection performance."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    plt.figure(figsize=(7.5, 5), dpi=300)
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    categories = ['Total Attack Trials', 'Detected & Blocked']
    values = [total_trials, rejected_trials]
    colors = ['#6c757d', '#2a9d8f']
    
    bars = plt.bar(categories, values, color=colors, width=0.45, edgecolor='#1d3557', linewidth=1.2)
    plt.ylabel('Count', fontsize=12, fontweight='bold')
    plt.title(f'{attack_name} Defense Performance ({detection_rate*100:.1f}% Defense Rate)', fontsize=13, fontweight='bold', pad=12)
    plt.ylim(0, total_trials * 1.2)
    
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 1, f"{int(yval)}", ha='center', va='bottom', fontsize=11, fontweight='bold')
        
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    return output_path
