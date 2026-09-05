"""Publication-quality plots for photonic optical fiber channel characteristics."""

import os
import shutil
import matplotlib.pyplot as plt
import numpy as np


def plot_distance_vs_transmission_and_fidelity(
    distances_km: list[float],
    transmissions: list[float],
    fidelities: list[float],
    output_path: str = "results/figures/02_photonic_channel_scaling.png"
) -> str:
    """Generate dual-axis plot of fiber distance vs optical transmission and state fidelity."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    fig, ax1 = plt.subplots(figsize=(9, 5.5), dpi=300)
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    color1 = '#1d3557'
    ax1.set_xlabel('Fiber Transmission Distance $L$ (km)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Optical Transmittance $T(L) = 10^{-\\alpha L / 10}$', color=color1, fontsize=12, fontweight='bold')
    line1 = ax1.plot(distances_km, transmissions, color=color1, marker='o', linewidth=2.2, label='Transmission Efficiency $T(L)$')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.set_ylim(-0.05, 1.05)
    
    ax2 = ax1.twinx()
    color2 = '#e63946'
    ax2.set_ylabel('Average Reconstructed Fidelity $F(L)$', color=color2, fontsize=12, fontweight='bold')
    line2 = ax2.plot(distances_km, fidelities, color=color2, marker='s', linestyle='--', linewidth=2.2, label='Quantum State Fidelity $F(L)$')
    ax2.tick_params(axis='y', labelcolor=color2)
    ax2.set_ylim(0.5, 1.05)
    
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='center right', frameon=True)
    
    plt.title('Long-Distance Photonic Channel Degradation ($1550\\text{ nm}$, $\\alpha = 0.2\\text{ dB/km}$)', fontsize=13, fontweight='bold', pad=12)
    plt.tight_layout()
    plt.savefig(output_path)
    
    alt_path = "results/figures/exp02_fiber_transmission.png"
    if output_path != alt_path:
        shutil.copyfile(output_path, alt_path)
        
    plt.close()
    return output_path


def plot_legitimate_baseline_tvd(
    distances_km: list[float],
    mean_tvds: list[float],
    mean_fidelities: list[float],
    output_path: str = "results/figures/03_legitimate_baseline.png"
) -> str:
    """Generate plot of Legitimate Channel Baseline P_{0,L} Total Variation Distance across distances."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    fig, ax1 = plt.subplots(figsize=(9, 5.5), dpi=300)
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    color1 = '#2a9d8f'
    ax1.set_xlabel('Optical Fiber Distance $L$ (km)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Baseline Mean TVD $\\mu_{D_0}(L)$', color=color1, fontsize=12, fontweight='bold')
    line1 = ax1.plot(distances_km, mean_tvds, color=color1, marker='o', linewidth=2.2, label='Baseline Statistical Distance ($D_{TV}$)')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.set_ylim(0.0, 0.15)
    
    ax2 = ax1.twinx()
    color2 = '#457b9d'
    ax2.set_ylabel('Baseline Fidelity $F_0(L)$', color=color2, fontsize=12, fontweight='bold')
    line2 = ax2.plot(distances_km, mean_fidelities, color=color2, marker='^', linestyle=':', linewidth=2.2, label='Baseline Quantum Fidelity')
    ax2.tick_params(axis='y', labelcolor=color2)
    ax2.set_ylim(0.80, 1.02)
    
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='center right', frameon=True)
    
    plt.title('Legitimate Baseline Calibration Profile $P_{0,L}$ vs Distance (10 - 200 km)', fontsize=13, fontweight='bold', pad=12)
    plt.tight_layout()
    plt.savefig(output_path)
    
    alt_path = "results/figures/exp03_legitimate_baseline.png"
    if output_path != alt_path:
        shutil.copyfile(output_path, alt_path)
        
    plt.close()
    return output_path


def plot_distance_sensitivity(
    distances_km: list[float],
    clean_acceptance_rates: list[float],
    attack_detection_rates: list[float],
    output_path: str = "results/figures/09_distance_analysis.png"
) -> str:
    """Generate plot of Clean Signature Acceptance vs Attack Detection across distances."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    plt.figure(figsize=(9, 5.5), dpi=300)
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    plt.plot(distances_km, [r * 100 for r in clean_acceptance_rates], marker='o', color='#2a9d8f', linewidth=2.2, label='Clean Signature Acceptance Rate (%)')
    plt.plot(distances_km, [r * 100 for r in attack_detection_rates], marker='s', color='#e63946', linewidth=2.2, label='Attack Detection Rate ($P_D$) (%)')
    
    plt.axhline(95, color='#6c757d', linestyle=':', label='95% High Performance Mark')
    plt.xlabel('Fiber Distance $L$ (km)', fontsize=12, fontweight='bold')
    plt.ylabel('Rate (%)', fontsize=12, fontweight='bold')
    plt.title('Distance Scaling Sensitivity: Legitimate Acceptance vs Threat Detection', fontsize=13, fontweight='bold', pad=12)
    plt.ylim(0, 105)
    plt.legend(frameon=True, loc='lower left')
    plt.tight_layout()
    plt.savefig(output_path)
    
    alt_path = "results/figures/exp09_distance_sensitivity.png"
    if output_path != alt_path:
        shutil.copyfile(output_path, alt_path)
        
    plt.close()
    return output_path
