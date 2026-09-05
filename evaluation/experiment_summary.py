"""Aggregation, formatting, and saving of scientific benchmark results to CSV, JSON, Markdown, and LaTeX tables."""

import csv
import json
import os
from typing import List, Dict, Any
from core.results import SimulationResult


def format_results_table(results: List[SimulationResult]) -> str:
    """Format a batch of simulation results into a clean text/markdown table."""
    headers = ["Distance", "Condition", "Attack", "Strength", "Shots", "TVD", "Threshold", "Decision", "Reason"]
    rows = []
    
    for r in results:
        cond = "Normal" if r.attack_type in ["none", "clean", ""] else "Attack"
        atk = r.attack_type if r.attack_type else "None"
        strength_str = f"{r.attack_strength * 100:.0f}%" if r.attack_strength > 0 else "-"
        tvd_str = f"{r.statistics.total_variation_distance:.4f}"
        tau_str = f"{r.statistics.adaptive_threshold:.4f}"
        
        rows.append([
            f"{r.distance_km:.0f} km",
            cond,
            atk,
            strength_str,
            str(r.shots),
            tvd_str,
            tau_str,
            r.final_decision,
            r.decision_reason[:40] + ("..." if len(r.decision_reason) > 40 else "")
        ])
        
    col_widths = [max(len(str(item)) for item in [h] + [row[i] for row in rows]) for i, h in enumerate(headers)]
    
    header_line = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
    sep_line = "-|-".join("-" * col_widths[i] for i in range(len(headers)))
    
    body_lines = [
        " | ".join(str(val).ljust(col_widths[i]) for i, val in enumerate(row))
        for row in rows
    ]
    
    return "\n".join([header_line, sep_line] + body_lines)


def export_results_csv(results: List[SimulationResult], filepath: str) -> None:
    """Export simulation results to a CSV file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    fieldnames = [
        "run_id", "session_id", "distance_km", "attack_type", "attack_strength",
        "shots", "transmission", "quantum_fidelity", "qds_mismatch_rate",
        "tvd", "chi2_stat", "chi2_pval", "adaptive_threshold", "critical_threshold",
        "anomaly_score", "threat_detected", "final_decision", "total_verification_ms"
    ]
    
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow({
                "run_id": r.run_id,
                "session_id": r.session_id,
                "distance_km": r.distance_km,
                "attack_type": r.attack_type,
                "attack_strength": r.attack_strength,
                "shots": r.shots,
                "transmission": r.transmission,
                "quantum_fidelity": r.quantum_fidelity,
                "qds_mismatch_rate": r.qds_mismatch_rate,
                "tvd": r.statistics.total_variation_distance,
                "chi2_stat": r.statistics.chi_square_statistic,
                "chi2_pval": r.statistics.chi_square_p_value,
                "adaptive_threshold": r.statistics.adaptive_threshold,
                "critical_threshold": r.statistics.critical_threshold,
                "anomaly_score": r.statistics.anomaly_score,
                "threat_detected": r.threat_detected,
                "final_decision": r.final_decision,
                "total_verification_ms": r.timing.total_verification_ms,
            })


def export_results_json(results: List[SimulationResult], filepath: str) -> None:
    """Export simulation results to a JSON file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    data = [r.to_dict() for r in results]
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def export_results_latex(results: List[SimulationResult], filepath: str, caption: str = "Photonic QDS Threat Detection Benchmark Results") -> None:
    """Export simulation results to a publication-ready LaTeX table."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    lines = [
        "\\begin{table}[htbp]",
        "\\centering",
        f"\\caption{{{caption}}}",
        "\\label{tab:qds_threat_results}",
        "\\begin{tabular}{rcccccc}",
        "\\hline\\hline",
        "\\textbf{Distance} & \\textbf{Attack} & \\textbf{Strength} & \\textbf{$D_{TV}$} & \\textbf{Threshold $\\tau$} & \\textbf{Anomaly Score} & \\textbf{Decision} \\\\",
        "\\hline"
    ]
    
    for r in results:
        dist_str = f"{r.distance_km:.0f}~km"
        atk_str = r.attack_type if r.attack_type not in ["none", "clean", ""] else "None"
        strength_str = f"{r.attack_strength * 100:.0f}\\%" if r.attack_strength > 0 else "---"
        tvd_str = f"{r.statistics.total_variation_distance:.4f}"
        tau_str = f"{r.statistics.adaptive_threshold:.4f}"
        anomaly_str = f"{r.statistics.anomaly_score:.2f}"
        dec_str = f"\\textbf{{{r.final_decision}}}"
        
        lines.append(f"{dist_str} & {atk_str} & {strength_str} & {tvd_str} & {tau_str} & {anomaly_str} & {dec_str} \\\\")
        
    lines.extend([
        "\\hline\\hline",
        "\\end{tabular}",
        "\\end{table}"
    ])
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
