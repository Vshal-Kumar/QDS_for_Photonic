"""Publication-quality plots for quantum state fidelity and Bloch coordinates."""

import os
import shutil
import matplotlib.pyplot as plt
import numpy as np


def plot_teleportation_fidelity_bar(
    states: list[str],
    fidelities: list[float],
    output_path: str = "results/figures/01_teleportation_validation.png"
) -> str:
    """Generate bar plot of teleportation fidelity across all 6 Pauli eigenstates."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    plt.figure(figsize=(9, 5), dpi=300)
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    
    colors = ['#2b5c8f', '#3b7ea1', '#4ba3b3', '#5cc8c5', '#6edec6', '#80f4c7']
    bars = plt.bar(states, fidelities, color=colors[:len(states)], width=0.55, edgecolor='#1b3a5c', linewidth=1.2)
    
    plt.axhline(1.0, color='#e63946', linestyle='--', linewidth=1.5, label='Ideal Unity Fidelity ($F = 1.0$)')
    plt.ylim(0.0, 1.15)
    plt.xlabel('Pauli Signature Eigenstates', fontsize=12, fontweight='bold')
    plt.ylabel('Reconstructed State Fidelity ($F$)', fontsize=12, fontweight='bold')
    plt.title('Quantum Teleportation Correctness Validation Across Pauli Eigenstates', fontsize=13, fontweight='bold', pad=12)
    
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.02, f"{yval:.4f}", ha='center', va='bottom', fontsize=10, fontweight='bold')
        
    plt.legend(frameon=True, loc='lower right')
    plt.tight_layout()
    plt.savefig(output_path)
    
    # Also save with alternative naming
    alt_path = "results/figures/exp01_teleportation_fidelity.png"
    if output_path != alt_path:
        shutil.copyfile(output_path, alt_path)
        
    plt.close()
    return output_path
