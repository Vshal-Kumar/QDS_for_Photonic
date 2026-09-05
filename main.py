"""Master Entry Point for the Photonic QDS Security Simulator.

Usage:
  # 1. Run Interactive SIH Demonstration Web UI:
  python main.py --demo

  # 2. Execute all 11 scientific benchmark experiment suites:
  python main.py --run-all-experiments

  # 3. Run a custom single simulation:
  python main.py --simulate --distance 50 --attack X --strength 0.20 --shots 1000
"""

import argparse
import sys
from core.simulator import QDSThreatSimulator
from evaluation.experiment_summary import format_results_table
from visualization.dashboard import start_demo_server

import importlib

def _get_exp(mod_name: str, func_name: str):
    mod = importlib.import_module(f"experiments.{mod_name}")
    return getattr(mod, func_name)

def run_all_experiments() -> None:
    """Execute all 11 scientific benchmark suites sequentially."""
    print("\n" + "=" * 75)
    print("EXECUTING ALL 11 SCIENTIFIC BENCHMARK EXPERIMENT SUITES")
    print("=" * 75 + "\n")
    
    _get_exp("01_teleportation_validation", "run_experiment_01")()
    _get_exp("02_photonic_channel", "run_experiment_02")()
    _get_exp("03_legitimate_baseline", "run_experiment_03")()
    _get_exp("04_pauli_attacks", "run_experiment_04")()
    _get_exp("05_forgery", "run_experiment_05")()
    _get_exp("06_replay", "run_experiment_06")()
    _get_exp("07_impersonation", "run_experiment_07")()
    _get_exp("08_unauthorized_verification", "run_experiment_08")()
    _get_exp("09_distance_analysis", "run_experiment_09")()
    _get_exp("10_measurement_analysis", "run_experiment_10")()
    _get_exp("11_threshold_analysis", "run_experiment_11")()
    
    print("=" * 75)
    print("✓ All 11 experiments completed successfully!")
    print("  Publication plots saved in: results/figures/")
    print("  Summary data tables saved in: results/tables/")
    print("=" * 75 + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Simulation-Based Quantum-Inspired Cyber Threat Detection for Photonic QDS."
    )
    
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Launch interactive web demonstration dashboard on http://localhost:8000"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for the demo web server (default: 8000)"
    )
    parser.add_argument(
        "--run-all-experiments",
        action="store_true",
        help="Execute all 11 scientific benchmark suites and generate publication figures"
    )
    parser.add_argument(
        "--simulate",
        action="store_true",
        help="Execute a single customized simulation run"
    )
    parser.add_argument(
        "--distance",
        type=float,
        default=50.0,
        help="Optical fiber distance in km (default: 50.0)"
    )
    parser.add_argument(
        "--attack",
        type=str,
        default="none",
        help="Attack vector (none, X, Y, Z, depolarizing, forgery, replay, impersonation, unauthorized_verification)"
    )
    parser.add_argument(
        "--strength",
        type=float,
        default=0.0,
        help="Attack strength pa in [0.0, 1.0] (default: 0.0)"
    )
    parser.add_argument(
        "--shots",
        type=int,
        default=1000,
        help="Measurement shot count N (default: 1000)"
    )
    parser.add_argument(
        "--message",
        type=str,
        default="Transfer 1000 Quantum Credits to Bob",
        help="Classical message to sign"
    )
    
    args = parser.parse_args()
    
    if args.demo:
        start_demo_server(port=args.port)
    elif args.run_all_experiments:
        run_all_experiments()
    elif args.simulate or len(sys.argv) > 1:
        sim = QDSThreatSimulator()
        
        signer_id = "Alice"
        verifier_id = "Bob"
        is_replay = False
        
        if args.attack.lower() == "impersonation":
            signer_id = "Eve_Pretending_Alice"
        elif args.attack.lower() == "unauthorized_verification":
            verifier_id = "Eve_Rogue_Verifier"
        elif args.attack.lower() == "replay":
            is_replay = True
            
        res = sim.run_simulation(
            message_text=args.message,
            distance_km=args.distance,
            attack_type=args.attack,
            attack_strength=args.strength,
            shots=args.shots,
            signer_id=signer_id,
            verifier_id=verifier_id,
            is_replay=is_replay
        )
        
        print("\n" + "=" * 65)
        print("                 SIMULATION EXECUTION RESULT")
        print("=" * 65)
        print(f"Message:               {res.message_text}")
        print(f"Distance:              {res.distance_km:.1f} km")
        print(f"Attack Type:           {res.attack_type}")
        print(f"Attack Strength:       {res.attack_strength * 100:.0f}%")
        print(f"Measurement Shots:     {res.shots}")
        print("-" * 65)
        print(f"Optical Transmission:  {res.transmission * 100:.2f}% (Loss: {0.20 * res.distance_km:.1f} dB)")
        print(f"Quantum State Fidelity:{res.quantum_fidelity:.4f}")
        print(f"Total Variation Dist:  {res.statistics.total_variation_distance:.4f}")
        print(f"Adaptive Threshold:    {res.statistics.adaptive_threshold:.4f}")
        print(f"Critical Threshold:    {res.statistics.critical_threshold:.4f}")
        print(f"Pearson Chi-Square:    chi2 = {res.statistics.chi_square_statistic:.2f} (p = {res.statistics.chi_square_p_value:.4f})")
        print(f"Composite Anomaly Score: {res.statistics.anomaly_score:.3f}")
        print("-" * 65)
        print(f"Threat Detected:       {res.threat_detected}")
        print(f"FINAL DECISION:        {res.final_decision}")
        print(f"Decision Reason:       {res.decision_reason}")
        print(f"Total Latency:         {res.timing.total_verification_ms:.2f} ms")
        print("=" * 65 + "\n")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
