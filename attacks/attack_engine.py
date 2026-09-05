"""Master Attack Engine (Adversary Eve) controlling physical and protocol attacks."""

from typing import List, Optional
import numpy as np

from attacks.quantum.bit_flip import apply_bit_flip_attack
from attacks.quantum.phase_flip import apply_phase_flip_attack
from attacks.quantum.bit_phase_flip import apply_bit_phase_flip_attack
from attacks.quantum.depolarizing import apply_adversarial_depolarizing_attack
from attacks.signature.forgery import generate_forged_signature_random_guess
from attacks.protocol.replay import create_replayed_signature
from attacks.protocol.impersonation import create_impersonated_signature
from core.message import Message
from core.session import Session
from qds.signature import QuantumDigitalSignature


class AttackEngine:
    """Simulates adversary Eve intercepting, tampering, and attacking the QDS channel."""
    
    def __init__(self) -> None:
        pass
        
    def apply_quantum_attack(
        self,
        quantum_states: List[np.ndarray],
        attack_type: str = "none",
        attack_strength: float = 0.0,
        rng: Optional[np.random.Generator] = None
    ) -> List[np.ndarray]:
        """Apply quantum physical manipulation to a list of quantum states/density matrices.
        
        Supported attacks:
        - "none": pass through unchanged
        - "bit_flip" / "X": Pauli X bit flip
        - "phase_flip" / "Z": Pauli Z phase flip
        - "bit_phase_flip" / "Y": Pauli Y bit and phase flip
        - "depolarizing": Pauli depolarizing channel
        """
        if rng is None:
            rng = np.random.default_rng()
            
        atk = attack_type.lower().strip()
        if atk in ["none", "clean", ""]:
            return [st.copy() for st in quantum_states]
            
        attacked_states: List[np.ndarray] = []
        for rho in quantum_states:
            if atk in ["bit_flip", "x"]:
                res_rho = apply_bit_flip_attack(rho, attack_strength)
            elif atk in ["phase_flip", "z"]:
                res_rho = apply_phase_flip_attack(rho, attack_strength)
            elif atk in ["bit_phase_flip", "y"]:
                res_rho = apply_bit_phase_flip_attack(rho, attack_strength)
            elif atk in ["depolarizing", "depol"]:
                res_rho = apply_adversarial_depolarizing_attack(rho, attack_strength)
            else:
                res_rho = rho.copy()
            attacked_states.append(res_rho)
            
        return attacked_states

    def generate_forgery(
        self,
        message: Message,
        session: Session,
        signature_length: int = 16,
        seed: Optional[int] = None
    ) -> QuantumDigitalSignature:
        """Generate a forged signature bundle."""
        return generate_forged_signature_random_guess(
            message=message,
            session=session,
            signature_length=signature_length,
            seed=seed
        )

    def generate_replay(
        self,
        original_signature: QuantumDigitalSignature,
        target_session: Session
    ) -> QuantumDigitalSignature:
        """Generate a replayed signature bundle."""
        return create_replayed_signature(original_signature, target_session)

    def generate_impersonation(
        self,
        original_signature: QuantumDigitalSignature,
        fake_signer_id: str = "Eve_Pretending_Alice"
    ) -> QuantumDigitalSignature:
        """Generate an impersonated signature bundle."""
        return create_impersonated_signature(original_signature, fake_signer_id)
