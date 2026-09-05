# Simulation-Based Quantum-Inspired Cyber Threat Detection for Long-Distance Photonic Quantum Digital Signatures

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-38%20passed-brightgreen.svg)]()
[![SIH Category](https://img.shields.io/badge/SIH-Cybersecurity%20%26%20Quantum%20Comms-purple.svg)]()
[![Deterministic](https://img.shields.io/badge/Detection-Deterministic%20Statistical%20(No%20AI%2FML)-orange.svg)]()

A research-grade Python simulation framework modeling a **Teleportation-Based Quantum Digital Signature (QDS)** protocol over a **long-distance photonic optical fiber channel** ($10\text{ km} - 200\text{ km}$ at telecom $\lambda = 1550\text{ nm}$). The core contribution is a **deterministic, non-AI three-tier cyber threat detection architecture** combining cryptographic protocol security, discrete-variable QDS verification, Pauli eigenstate measurements ($X, Y, Z$), and distance-aware adaptive statistical hypothesis testing.

---

## 🏛️ System Architecture

```text
Message (M) ──────────► Alice (Signer)
                              │
                    Session ID + Nonce
                              │
                    Quantum Signature State
                              │
                    Pauli Eigenstate Preparation (|0>, |1>, |+>, |->, |+_y>, |-_y>)
                              │
                    Bell Entanglement (|Phi+> = (|00> + |11>)/sqrt(2))
                              │
                    TELEPORTATION (BSM Outcomes c1, c2)
                              │
       ┌──────────────────────┴──────────────────────┐
       ▼                                             ▼
[Clean Photonic Channel]                     [Adversary Eve Attacks]
- Distance L (10 - 200 km)                   - Pauli X (Bit-Flip)
- Attenuation T(L) = 10^(-alpha*L/10)        - Pauli Z (Phase-Flip)
- Depolarizing & Dephasing Noise             - Pauli Y (Bit-Phase Flip)
- Single-Photon Detector Jitter/Dark Counts  - Depolarization Channel
                                             - Signature Forgery
                                             - Nonce Replay Attack
                                             - Signer Impersonation
                                             - Unauthorized Verifier
       └──────────────────────┬──────────────────────┘
                              │
                              ▼
                      Bob (Verifier)
                              │
       ┌──────────────────────┼──────────────────────┐
       ▼                      ▼                      ▼
[Authentication]        [Freshness]           [Authorization]
- Signer Identity       - Nonce Cache         - Verifier Role Clearance
- HMAC-SHA256 Tag       - Session Expiry      - Rogue Inspection Defense
       └──────────────────────┬──────────────────────┘
                              │
                              ▼
                      QDS Verification
                      - Pauli Unitary Correction: U = Z^c1 * X^c2
                      - Quantum State Fidelity & Mismatch Rate
                              │
                              ▼
               Multi-Basis Projective Measurements
               - X-Basis (Diagonal)
               - Y-Basis (Circular)
               - Z-Basis (Computational)
                              │
                              ▼
               Deterministic Statistical Threat Engine
               - Empirical Frequency Vector: P_N
               - Calibrated Legitimate Baseline: P_{0,L}
               - Total Variation Distance: D_TV(P_N, P_{0,L})
               - Pearson's Chi-Square Test (chi2, p-value)
               - Multi-Component Z-Score Hypothesis Testing
               - Adaptive Threshold: tau(L, N, alpha)
                              │
                              ▼
                Tri-State Decision Arbitrator
               ┌──────────────┼──────────────┐
               ▼              ▼              ▼
             ACCEPT       SUSPICIOUS       REJECT
```

---

## 📁 Repository Structure

```text
photonic_qds_security_sim/
│
├── main.py                           # Master CLI entry point (demo, benchmarks, single sim)
├── requirements.txt                  # Lightweight dependencies (numpy, scipy, matplotlib, pytest)
├── pyproject.toml                    # Project configuration and pytest settings
├── README.md                         # Comprehensive project documentation
│
├── config/                           # System and physical configurations
│   ├── protocol_config.py            # QDS signature lengths, hash algorithms, mismatch thresholds
│   ├── photonic_config.py            # Wavelength (1550nm), fiber loss alpha=0.2 dB/km, dark counts, efficiency
│   ├── security_config.py            # Nonce window, registry, anomaly thresholds
│   └── experiment_config.py          # Benchmark sweep parameters
│
├── core/                             # Simulation primitives
│   ├── message.py                    # Classical message structure, SHA-256 hash
│   ├── session.py                    # Session store, nonce cache
│   ├── simulator.py                  # Master simulation orchestrator
│   └── results.py                    # Structured result dataclasses & timing breakdown
│
├── quantum/                          # Quantum mechanics foundation
│   ├── pauli_states.py               # Pauli eigenstates, density matrices, fidelity, purity, Bloch vectors
│   ├── bell_states.py                # 4 Bell states, EPR generation, Bell measurement projectors
│   ├── teleportation.py              # Teleportation engine with BSM
│   ├── pauli_correction.py           # Unitary recovery operations U = Z^c1 X^c2
│   └── measurements.py               # Projective measurements in X, Y, Z bases with shot noise
│
├── photonic/                         # Photonic optical fiber physics
│   ├── polarization.py               # Qubit-to-polarization mapping (|0>->|H>, |1>->|V>, |+>->|D>, |+_y>->|R>)
│   ├── fiber_loss.py                 # Beer-Lambert transmission T(L) = 10^(-alpha*L/10)
│   ├── channel_noise.py              # Depolarizing & dephasing noise models
│   ├── detector_model.py             # Quantum efficiency eta=0.85, dark counts, alignment jitter
│   ├── optical_channel.py            # Integrated optical fiber channel
│   └── channel_statistics.py         # SNR, QBER, loss scaling calculations
│
├── qds/                              # Discrete-variable QDS protocol
│   ├── protocol.py                   # Full signing -> transmission -> verification cycle
│   ├── signer.py                     # Alice: key mapping, state preparation, signature assembly
│   ├── signature.py                  # Quantum digital signature bundle
│   ├── verifier.py                   # Bob: Pauli state reconstruction
│   └── verification.py               # QDS signature validity check (mismatch vs threshold)
│
├── security/                         # First-class protocol security subsystem
│   ├── authentication/               # Identity registry, signer authentication, verifier authorization
│   ├── freshness/                    # Nonce generation, session freshness, replay protection
│   ├── integrity/                    # Message, signature bundle, and quantum state mathematical integrity
│   ├── verification/                 # Quantum & protocol security integration
│   └── security_engine.py            # Central security coordinator
│
├── attacks/                          # Adversary attack subsystem (Eve)
│   ├── quantum/                      # Pauli X, Z, Y, and depolarizing state attacks
│   ├── signature/                    # Signature forgery generator (random state guessing)
│   ├── protocol/                     # Replay, impersonation, and unauthorized verification attacks
│   └── attack_engine.py              # Master adversary controller
│
├── detection/                        # THE CORE CONTRIBUTION: Statistical Threat Detection
│   ├── baseline.py                   # Legitimate baseline generator P_{0,L} across distances
│   ├── probability.py                # Empirical distribution normalization
│   ├── measurement_statistics.py     # Multi-basis statistical moments, variance, covariance
│   ├── statistical_distance.py       # Total Variation Distance (TVD), Bhattacharyya, KL, Hellinger
│   ├── chi_square.py                 # Pearson's Chi-square goodness-of-fit & exact p-value
│   ├── hypothesis_testing.py         # Z-score hypothesis testing & Log-Likelihood Ratio
│   ├── threshold.py                  # Static baseline empirical percentiles
│   ├── adaptive_threshold.py         # Distance- and shot-aware dynamic threshold tau(L, N)
│   ├── anomaly_score.py              # Calibrated composite anomaly index [0.0, 1.0]
│   └── decision_engine.py            # Tri-state arbitrator (ACCEPT / SUSPICIOUS / REJECT)
│
├── experiments/                      # 11 Scientific Benchmark Experiment Suites
│   ├── 01_teleportation_validation.py  # Teleportation correctness across all 6 Pauli states
│   ├── 02_photonic_channel.py          # Fiber attenuation & noise scaling (10 - 200 km)
│   ├── 03_legitimate_baseline.py       # Baseline calibration profiles P_{0,L}
│   ├── 04_pauli_attacks.py             # Pauli X, Y, Z attack detection vs attack strength
│   ├── 05_forgery.py                   # Signature forgery probability vs analytical bounds
│   ├── 06_replay.py                    # Replay attack detection performance
│   ├── 07_impersonation.py             # Signer identity spoofing rejection performance
│   ├── 08_unauthorized_verification.py # Rogue verifier authorization clearance
│   ├── 09_distance_analysis.py         # Distance impact on detection sensitivity
│   ├── 10_measurement_analysis.py      # Shot count scaling N in {100..10000} vs P_D
│   └── 11_threshold_analysis.py        # ROC curve & threshold trade-off analysis
│
├── evaluation/                       # Metric calculators & tabular exporters
│   ├── security_metrics.py           # FAR, FRR, Detection Probability P_D, F1-score
│   ├── performance_metrics.py        # Verification latency, quantum sim runtime, throughput
│   ├── forgery_probability.py        # Analytical & empirical forgery bounds
│   └── experiment_summary.py         # CSV, JSON, and text table exporters
│
├── visualization/                    # Publication-quality plotting & demo server
│   ├── quantum_plots.py              # Teleportation fidelity bar charts
│   ├── channel_plots.py              # Distance vs transmission & fidelity curves
│   ├── attack_plots.py               # Attack strength vs P_D curves (X, Y, Z)
│   ├── security_plots.py             # ROC curves, shot scaling curves
│   └── dashboard.py                  # Lightweight built-in HTTP simulation server
│
├── web/static/                       # Interactive browser demonstration interface
│   ├── index.html                    # Glassmorphic cyber dashboard
│   ├── styles.css                    # Dark mode UI tokens & animations
│   └── app.js                        # Real-time WebSocket/HTTP simulation client
│
├── results/                          # Generated figures and data tables
│   ├── figures/                      # High-resolution publication plots (.png)
│   └── tables/                       # Scientific benchmark data tables (.csv, .json)
│
└── tests/                            # 12 Comprehensive Test Suites (38 unit tests)
```

---

## ⚡ Quick Start Guide

### 1. Environment Setup
```bash
# Clone or navigate to workspace
cd SIH26141

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run All Automated Unit Tests (100% Green)
```bash
pytest tests/ -v
```

### 3. Launch the Interactive Web Demonstration Dashboard
```bash
python main.py --demo
```
Open **`http://localhost:8000`** in your web browser to interact with live simulation controls (Distance slider $0-200\text{ km}$, Attack vectors, Attack strength $0-100\%$, Shots $100-10000$), view live Pauli basis measurement histograms, inspect the TVD vs Adaptive Threshold gauge, and observe real-time tri-state decision arbitration.

### 4. Execute All 11 Scientific Benchmark Experiment Suites
```bash
python main.py --run-all-experiments
```
This automatically executes all 11 scientific benchmarks, populating `results/figures/` with high-resolution plots and `results/tables/` with CSV tables.

### 5. Run a Custom Single Simulation via CLI
```bash
python main.py --simulate --distance 50 --attack X --strength 0.20 --shots 1000
```

---

## 📊 Scientific Benchmark Summary

| Experiment Suite | Metric / Focus | Key Empirical Result | Status |
|---|---|---|---|
| **01. Teleportation Validation** | Fidelity across all 6 Pauli states | $\mathcal{F} = 1.000000 \pm 0.000000$ for all states | **PASS (100%)** |
| **02. Photonic Channel Scaling** | Fiber loss & transmission vs $L$ | $T(50\text{km}) = 10.0\%$, $T(100\text{km}) = 1.0\%$, adhering to $0.2\text{ dB/km}$ | **PASS** |
| **03. Legitimate Baselines** | Mean TVD under $H_0$ across distances | Baseline TVD $\mu_{D_0} \approx 0.035 - 0.038$ | **PASS** |
| **04. Pauli Attacks ($X, Y, Z$)** | Detection Probability $P_D$ vs $p_a$ | $P_D = 100.0\%$ for $p_a \ge 20\%$ across $X, Y, Z$ | **PASS** |
| **05. Signature Forgery** | Empirical vs Theoretical Forgery Bound | Empirical $P_{\text{forge}} = 0.0000 \le P_{\text{theo}} = 0.002090$ | **PASS (0% Accepted)** |
| **06. Nonce Replay Protection** | Replay detection rate | $100.0\%$ replay rejection rate ($30/30$ detected) | **PASS (100%)** |
| **07. Signer Impersonation** | Identity spoofing rejection rate | $100.0\%$ impersonation rejection rate ($30/30$ rejected) | **PASS (100%)** |
| **08. Unauthorized Verifier** | Rogue verifier rejection rate | $100.0\%$ rogue request rejection rate ($30/30$ rejected) | **PASS (100%)** |
| **09. Distance Sensitivity** | Clean acceptance vs Attack detection | Clean acceptance $\ge 96\%$ up to $100\text{ km}$, $P_D = 100\%$ | **PASS** |
| **10. Shot Count Scaling ($N$)** | Detection sensitivity vs budget $N$ | High confidence scaling from $N=100$ to $N=10000$ | **PASS** |
| **11. Threshold ROC Trade-Off** | False Acceptance vs False Rejection | Clear statistical separation under calibrated adaptive threshold | **PASS** |

---

## 🛡️ SIH Problem Statement Alignment

1. **Teleportation-Based QDS Protocol**: Implemented in discrete-variable photon polarization space ($|H\rangle, |V\rangle, |D\rangle, |A\rangle, |R\rangle, |L\rangle$) using Bell pairs $|\Phi^+\rangle$ and Pauli corrections $U = Z^{c_1}X^{c_2}$.
2. **Cyber Threat Coverage**: Explicitly detects **Forgery**, **Impersonation**, **Replay Attacks**, **Unauthorized Verification**, and **Pauli Channel Tampering ($X, Y, Z$)**.
3. **Pauli Eigenstates & Measurements**: Direct multi-basis projective measurements in $X$, $Y$, and $Z$ bases over finite shots $N$.
4. **Deterministic Statistical Threat Detection**: Total Variation Distance ($D_{TV}$), Pearson's $\chi^2$ Goodness-of-Fit, Z-score hypothesis testing, and distance-aware adaptive thresholds $\tau(L, N, \eta, \alpha)$—**strictly without AI/ML black boxes**.
5. **Efficiency & Performance**: Average verification latency $< 30\text{ ms}$, deterministic polynomial time $\mathcal{O}(K \cdot N)$, providing clear experimental proof of efficiency.
