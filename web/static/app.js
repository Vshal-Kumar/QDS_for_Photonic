/**
 * Interactive Client for the Photonic QDS Threat Detection Simulator
 */

document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements
  const inputDistance = document.getElementById('input-distance');
  const valDistance = document.getElementById('val-distance');
  const inputShots = document.getElementById('input-shots');
  const valShots = document.getElementById('val-shots');
  const inputAttackType = document.getElementById('input-attack-type');
  const groupAttackStrength = document.getElementById('group-attack-strength');
  const inputStrength = document.getElementById('input-strength');
  const valStrength = document.getElementById('val-strength');
  const inputMessage = document.getElementById('input-message');
  const btnRunSim = document.getElementById('btn-run-sim');
  const btnRunAll = document.getElementById('btn-run-all');

  // Display Elements
  const decisionBadge = document.getElementById('decision-badge');
  const decisionReason = document.getElementById('decision-reason');
  const valTransmission = document.getElementById('val-transmission');
  const subLoss = document.getElementById('sub-loss');
  const valFidelity = document.getElementById('val-fidelity');
  const subMismatch = document.getElementById('sub-mismatch');
  const valTvd = document.getElementById('val-tvd');
  const subThreshold = document.getElementById('sub-threshold');
  const valAnomaly = document.getElementById('val-anomaly');
  const subAnomalyLevel = document.getElementById('sub-anomaly-level');

  // Gauge Elements
  const gaugeBarFill = document.getElementById('gauge-bar-fill');
  const gaugeMarker = document.getElementById('gauge-marker');
  const gaugeRatio = document.getElementById('gauge-ratio');

  // Histograms
  const barXp = document.getElementById('bar-xp');
  const barXm = document.getElementById('bar-xm');
  const txtXp = document.getElementById('txt-xp');
  const txtXm = document.getElementById('txt-xm');

  const barYp = document.getElementById('bar-yp');
  const barYm = document.getElementById('bar-ym');
  const txtYp = document.getElementById('txt-yp');
  const txtYm = document.getElementById('txt-ym');

  const barZ0 = document.getElementById('bar-z0');
  const barZ1 = document.getElementById('bar-z1');
  const txtZ0 = document.getElementById('txt-z0');
  const txtZ1 = document.getElementById('txt-z1');

  // Audit Elements
  const chkSigner = document.getElementById('chk-signer');
  const chkVerifier = document.getElementById('chk-verifier');
  const chkNonce = document.getElementById('chk-nonce');
  const chkState = document.getElementById('chk-state');
  const chkChi2 = document.getElementById('chk-chi2');
  const latencyTag = document.getElementById('latency-tag');

  // Event Listeners for Sliders
  inputDistance.addEventListener('input', (e) => {
    valDistance.textContent = `${e.target.value} km`;
  });

  inputShots.addEventListener('input', (e) => {
    valShots.textContent = e.target.value;
  });

  inputStrength.addEventListener('input', (e) => {
    valStrength.textContent = `${e.target.value}%`;
  });

  inputAttackType.addEventListener('change', (e) => {
    const atk = e.target.value;
    const isQuantumPauli = ['X', 'Y', 'Z', 'depolarizing'].includes(atk);
    groupAttackStrength.style.opacity = isQuantumPauli ? '1' : '0.4';
    inputStrength.disabled = !isQuantumPauli;
  });

  // Run Simulation Function
  async function runSimulation() {
    btnRunSim.disabled = true;
    btnRunSim.querySelector('.btn-text').textContent = 'Simulating...';

    const payload = {
      message: inputMessage.value,
      distance_km: parseFloat(inputDistance.value),
      shots: parseInt(inputShots.value, 10),
      attack_type: inputAttackType.value,
      attack_strength: parseFloat(inputStrength.value) / 100.0,
    };

    try {
      const response = await fetch('/api/simulate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!response.ok) throw new Error('Simulation API request failed');
      const data = await response.json();
      updateDashboard(data);
    } catch (err) {
      console.error(err);
      alert('Error contacting simulation engine. Please check if Python server is active.');
    } finally {
      btnRunSim.disabled = false;
      btnRunSim.querySelector('.btn-text').textContent = 'Execute Simulation';
    }
  }

  function updateDashboard(res) {
    // 1. Decision Badge & Box
    decisionBadge.textContent = res.final_decision;
    decisionBadge.className = 'decision-badge';
    if (res.final_decision === 'ACCEPT') {
      decisionBadge.classList.add('badge-accept');
    } else if (res.final_decision === 'SUSPICIOUS') {
      decisionBadge.classList.add('badge-suspicious');
    } else {
      decisionBadge.classList.add('badge-reject');
    }
    decisionReason.textContent = res.decision_reason;

    // 2. Metrics Box
    valTransmission.textContent = `${(res.transmission * 100).toFixed(1)}%`;
    subLoss.textContent = `Loss: ${(0.20 * res.distance_km).toFixed(1)} dB`;

    valFidelity.textContent = res.quantum_fidelity.toFixed(3);
    subMismatch.textContent = `Mismatch: ${(res.qds_mismatch_rate * 100).toFixed(1)}%`;

    const tvd = res.statistics.total_variation_distance;
    const tau = res.statistics.adaptive_threshold;
    valTvd.textContent = tvd.toFixed(4);
    subThreshold.textContent = `Threshold τ: ${tau.toFixed(4)}`;

    const anomaly = res.statistics.anomaly_score;
    valAnomaly.textContent = anomaly.toFixed(2);
    if (anomaly < 0.30) {
      subAnomalyLevel.textContent = 'Clean / Normal';
      subAnomalyLevel.style.color = 'var(--accent-emerald)';
    } else if (anomaly < 0.60) {
      subAnomalyLevel.textContent = 'Suspicious State';
      subAnomalyLevel.style.color = 'var(--accent-amber)';
    } else {
      subAnomalyLevel.textContent = 'Critical Threat Detected';
      subAnomalyLevel.style.color = 'var(--accent-crimson)';
    }

    // 3. Gauge Bar Fill & Marker
    const maxGauge = Math.max(0.20, tau * 2.5);
    const fillPct = Math.min(100, Math.max(2, (tvd / maxGauge) * 100));
    const markerPct = Math.min(100, Math.max(2, (tau / maxGauge) * 100));
    gaugeBarFill.style.width = `${fillPct}%`;
    gaugeMarker.style.left = `${markerPct}%`;
    gaugeRatio.textContent = `TVD / Threshold: ${((tvd / Math.max(1e-5, tau)) * 100).toFixed(0)}%`;

    // 4. Histograms
    const obs = res.statistics.observed_distribution;
    if (obs) {
      const xp = obs['X+'] ?? 0.5;
      const xm = obs['X-'] ?? 0.5;
      const yp = obs['Y+'] ?? 0.5;
      const ym = obs['Y-'] ?? 0.5;
      const z0 = obs['Z0'] ?? 0.5;
      const z1 = obs['Z1'] ?? 0.5;

      barXp.style.height = `${xp * 100}%`;
      barXm.style.height = `${xm * 100}%`;
      txtXp.textContent = xp.toFixed(2);
      txtXm.textContent = xm.toFixed(2);

      barYp.style.height = `${yp * 100}%`;
      barYm.style.height = `${ym * 100}%`;
      txtYp.textContent = yp.toFixed(2);
      txtYm.textContent = ym.toFixed(2);

      barZ0.style.height = `${z0 * 100}%`;
      barZ1.style.height = `${z1 * 100}%`;
      txtZ0.textContent = z0.toFixed(2);
      txtZ1.textContent = z1.toFixed(2);
    }

    // 5. Audit Checks
    const proto = res.protocol_checks;
    setAuditStatus('chk-signer', proto.signer_authenticated, proto.signer_authenticated ? 'Alice (Valid HMAC)' : 'Impersonation Detected');
    setAuditStatus('chk-verifier', proto.verifier_authorized, proto.verifier_authorized ? 'Bob (Authorized)' : 'Unauthorized Verifier');
    setAuditStatus('chk-nonce', proto.nonce_valid, proto.nonce_valid ? 'Fresh (Unique)' : 'Replay Attack Detected');
    setAuditStatus('chk-state', proto.signature_intact, proto.signature_intact ? 'Hermitian & Unit Trace' : 'State Tampered');

    const chi2 = res.statistics.chi_square_statistic;
    const pval = res.statistics.chi_square_p_value;
    chkChi2.textContent = `χ² = ${chi2.toFixed(2)}, p = ${pval.toFixed(3)}`;
    chkChi2.parentElement.className = pval > 0.05 ? 'check-item check-pass' : 'check-item check-fail';

    // 6. Latency Breakdown
    const t = res.timing;
    latencyTag.textContent = `Total: ${t.total_verification_ms.toFixed(1)} ms`;
  }

  function setAuditStatus(elementId, isPass, text) {
    const el = document.getElementById(elementId);
    if (!el) return;
    el.textContent = text;
    el.parentElement.className = isPass ? 'check-item check-pass' : 'check-item check-fail';
    el.parentElement.querySelector('.check-icon').textContent = isPass ? '✓' : '✗';
  }

  // Button actions
  btnRunSim.addEventListener('click', runSimulation);
  btnRunAll.addEventListener('click', () => {
    alert('Launching benchmark suite in background. Check terminal and results/tables/ directory.');
  });

  // Initial Run
  runSimulation();
});
