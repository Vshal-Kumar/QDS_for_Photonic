"""Master Simulation Pipeline executing complete end-to-end Photonic QDS runs with threat detection."""

import time
import uuid
from typing import Optional, List
import numpy as np

from config.protocol_config import ProtocolConfig
from config.photonic_config import PhotonicConfig
from config.security_config import SecurityConfig
from core.message import Message
from core.session import Session
from core.results import SimulationResult, StatisticalResult, TimingBreakdown
from qds.signer import Signer
from qds.verifier import Verifier
from qds.verification import verify_qds_signature
from photonic.optical_channel import PhotonicChannel
from attacks.attack_engine import AttackEngine
from security.security_engine import SecurityEngine
from detection.baseline import BaselineGenerator
from quantum.measurements import measure_all_pauli_bases
from detection.measurement_statistics import process_measurement_suite
from detection.statistical_distance import compute_total_variation_distance
from detection.chi_square import compute_chi_square_test
from detection.hypothesis_testing import compute_z_scores
from detection.adaptive_threshold import compute_adaptive_threshold
from detection.anomaly_score import compute_composite_anomaly_score
from detection.decision_engine import DecisionEngine


class QDSThreatSimulator:
    """End-to-end master simulator combining Quantum Mechanics, Photonics, Protocols, and Threat Detection."""
    
    def __init__(
        self,
        protocol_config: Optional[ProtocolConfig] = None,
        photonic_config: Optional[PhotonicConfig] = None,
        security_config: Optional[SecurityConfig] = None,
    ) -> None:
        self.protocol_config = protocol_config if protocol_config is not None else ProtocolConfig()
        self.photonic_config = photonic_config if photonic_config is not None else PhotonicConfig()
        self.security_config = security_config if security_config is not None else SecurityConfig()
        
        # Subsystems
        self.signer = Signer("Alice", config=self.protocol_config)
        self.verifier = Verifier("Bob")
        self.channel = PhotonicChannel(config=self.photonic_config)
        self.attack_engine = AttackEngine()
        self.security_engine = SecurityEngine(config=self.security_config)
        self.baseline_generator = BaselineGenerator(photonic_config=self.photonic_config)
        self.decision_engine = DecisionEngine(
            suspicious_anomaly_threshold=self.security_config.suspicious_anomaly_threshold,
            critical_anomaly_threshold=self.security_config.critical_anomaly_threshold
        )
        
    def run_simulation(
        self,
        message_text: str = "Transfer 100 Quantum Tokens",
        distance_km: float = 50.0,
        attack_type: str = "none",
        attack_strength: float = 0.0,
        shots: int = 1000,
        signer_id: str = "Alice",
        verifier_id: str = "Bob",
        is_replay: bool = False,
        seed: Optional[int] = None
    ) -> SimulationResult:
        """Execute one complete end-to-end simulation run.
        
        Pipeline:
        1. Setup Message & Session
        2. Alice generates QDS signature & teleports states
        3. Photonic optical channel propagation over distance_km
        4. Eve applies selected attack (Quantum, Forgery, Replay, Impersonation)
        5. Bob performs Pauli corrections & reconstructs states
        6. Security Engine evaluates protocol security
        7. Bob performs projective measurements (X, Y, Z)
        8. Statistical Engine computes TVD, Chi-square, Z-scores vs baseline P_{0,L}
        9. Adaptive threshold tau(L, N) evaluated
        10. Decision engine renders tri-state outcome
        """
        rng = np.random.default_rng(seed)
        t_start = time.perf_counter()
        
        # 1. Message and Session initialization
        t_proto_start = time.perf_counter()
        message = Message(content=message_text)
        session = self.security_engine.session_store.create_session(
            signer_id=signer_id,
            verifier_id=verifier_id
        )
        
        if is_replay:
            # Simulate replay by generating a duplicate session with an already used nonce
            replayed_nonce = "replayed_stale_nonce_001"
            self.security_engine.replay_protector.check_and_record(replayed_nonce, session.session_id)
            session.nonce = replayed_nonce
            
        t_proto_init = (time.perf_counter() - t_proto_start) * 1000.0
        
        # 2. Quantum Signature Generation & Teleportation (Alice)
        t_q_start = time.perf_counter()
        if attack_type.lower() == "forgery":
            signature = self.attack_engine.generate_forgery(
                message=message,
                session=session,
                signature_length=self.protocol_config.signature_qubit_count,
                seed=int(rng.integers(0, 1000000))
            )
        elif attack_type.lower() == "impersonation":
            raw_sig = self.signer.sign(message, session, seed=int(rng.integers(0, 1000000)))
            signature = self.attack_engine.generate_impersonation(raw_sig, fake_signer_id="Eve_Pretending_Alice")
        else:
            # Legitimate Alice signing with correct secret key
            signer_key = self.security_engine.identity_registry.get_signer_secret(signer_id) or "key_fallback"
            alice_signer = Signer(signer_id, secret_key=signer_key, config=self.protocol_config)
            signature = alice_signer.sign(message, session, seed=int(rng.integers(0, 1000000)))
            
        t_q_ms = (time.perf_counter() - t_q_start) * 1000.0
        
        # 3. Photonic Channel Propagation
        t_ch_start = time.perf_counter()
        channel_results = []
        transmitted_states: List[np.ndarray] = []
        for el in signature.elements:
            res = self.channel.transmit(
                input_state=el.quantum_state_vec,
                distance_km=distance_km,
                rng=rng
            )
            channel_results.append(res)
            transmitted_states.append(res.output_rho)
            
        avg_transmission = float(np.mean([r.transmission_efficiency for r in channel_results]))
        t_ch_ms = (time.perf_counter() - t_ch_start) * 1000.0
        
        # 4. Quantum Attack Injection (Eve)
        if attack_type.lower() in ["bit_flip", "x", "phase_flip", "z", "bit_phase_flip", "y", "depolarizing", "depol"]:
            received_states = self.attack_engine.apply_quantum_attack(
                quantum_states=transmitted_states,
                attack_type=attack_type,
                attack_strength=attack_strength,
                rng=rng
            )
        else:
            received_states = transmitted_states
            
        # 5. Bob Reconstructs States via Pauli Corrections
        t_recon_start = time.perf_counter()
        reconstructed_rhos = self.verifier.reconstruct_signature_states(
            signature=signature,
            received_quantum_states=received_states
        )
        t_recon_ms = (time.perf_counter() - t_recon_start) * 1000.0
        
        # 6. Protocol Security Checks
        t_sec_start = time.perf_counter()
        proto_check_res = self.security_engine.evaluate_protocol_security(
            message=message,
            session=session,
            signature=signature,
            reconstructed_states=reconstructed_rhos,
            verifier_id=verifier_id
        )
        
        # QDS Signature Verification
        qds_verif_res = verify_qds_signature(
            message=message,
            signature=signature,
            reconstructed_states=reconstructed_rhos,
            config=self.protocol_config
        )
        t_sec_ms = (time.perf_counter() - t_sec_start) * 1000.0
        
        # 7. Quantum Measurement across X, Y, Z bases
        t_meas_start = time.perf_counter()
        # Measure ensemble average state
        avg_rho = np.mean(reconstructed_rhos, axis=0)
        meas_suite = measure_all_pauli_bases(
            rho=avg_rho,
            shots_per_basis=max(10, shots // 3),
            seed=int(rng.integers(0, 1000000))
        )
        meas_stats = process_measurement_suite(meas_suite)
        t_meas_ms = (time.perf_counter() - t_meas_start) * 1000.0
        
        # 8. Statistical Threat Analysis vs Legitimate Baseline
        t_stat_start = time.perf_counter()
        expected_state_names = [el.state_name for el in signature.elements]
        baseline_profile = self.baseline_generator.get_baseline(distance_km, expected_state_names)
        base_dist = baseline_profile.mean_distribution_vector
        obs_dist = meas_stats.empirical_vector
        
        # Total Variation Distance
        tvd = compute_total_variation_distance(obs_dist, base_dist)
        
        # Chi-Square Test
        shots_basis = max(10, shots // 3)
        chi2_stat, chi2_pval, _ = compute_chi_square_test(
            observed_distribution=obs_dist,
            expected_distribution=base_dist,
            shots=shots_basis
        )
        
        # Z-Scores
        z_scores, max_z = compute_z_scores(
            observed_probs=obs_dist,
            baseline_probs=base_dist,
            shots=shots_basis,
            keys=BaselineGenerator.DISTRIBUTION_KEYS
        )
        
        # Adaptive Thresholds
        tau, tau_crit = compute_adaptive_threshold(
            baseline_profile=baseline_profile,
            shots=shots,
            significance_level_alpha=self.security_config.significance_level_alpha
        )
        
        # Composite Anomaly Score
        anomaly_score = compute_composite_anomaly_score(
            total_variation_distance=tvd,
            adaptive_threshold=tau,
            critical_threshold=tau_crit,
            chi_square_p_value=chi2_pval,
            max_z_score=max_z,
            qds_mismatch_rate=qds_verif_res.mismatch_rate,
            significance_alpha=self.security_config.significance_level_alpha
        )
        
        stat_result = StatisticalResult(
            shots=shots,
            observed_distribution=meas_stats.distribution_dict,
            baseline_distribution=baseline_profile.distribution_dict,
            total_variation_distance=tvd,
            chi_square_statistic=chi2_stat,
            chi_square_p_value=chi2_pval,
            z_scores=z_scores,
            adaptive_threshold=tau,
            critical_threshold=tau_crit,
            anomaly_score=anomaly_score,
            statistical_threat_detected=(tvd > tau or anomaly_score >= self.security_config.suspicious_anomaly_threshold)
        )
        t_stat_ms = (time.perf_counter() - t_stat_start) * 1000.0
        
        # 9. Final Decision Arbitration
        decision_outcome = self.decision_engine.arbitrate_decision(
            protocol_checks=proto_check_res,
            qds_verification=qds_verif_res,
            statistical_result=stat_result
        )
        
        t_total_ms = (time.perf_counter() - t_start) * 1000.0
        
        timing = TimingBreakdown(
            quantum_sim_ms=t_q_ms,
            channel_sim_ms=t_ch_ms,
            teleportation_ms=t_recon_ms,
            measurement_ms=t_meas_ms,
            statistical_analysis_ms=t_stat_ms,
            protocol_checks_ms=t_sec_ms + t_proto_init,
            total_verification_ms=t_total_ms
        )
        
        return SimulationResult(
            run_id=str(uuid.uuid4()),
            session_id=session.session_id,
            message_text=message_text,
            distance_km=distance_km,
            attack_type=attack_type,
            attack_strength=attack_strength,
            shots=shots,
            transmission=avg_transmission,
            quantum_fidelity=qds_verif_res.average_fidelity,
            quantum_purity=float(np.real(np.trace(avg_rho @ avg_rho))),
            qds_mismatch_rate=qds_verif_res.mismatch_rate,
            qds_signature_valid=qds_verif_res.is_valid,
            protocol_checks=proto_check_res,
            statistics=stat_result,
            final_decision=decision_outcome.decision,
            decision_reason=decision_outcome.reason,
            threat_detected=decision_outcome.threat_detected,
            timing=timing
        )
