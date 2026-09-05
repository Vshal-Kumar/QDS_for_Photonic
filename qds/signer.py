"""Signer entity (Alice) responsible for quantum signature generation and teleportation."""

import hashlib
import hmac
import time
from typing import List, Tuple, Optional
import numpy as np

from config.protocol_config import ProtocolConfig
from core.message import Message
from core.session import Session
from quantum.pauli_states import get_pauli_state
from quantum.teleportation import teleport_quantum_state
from qds.signature import SignatureElement, QuantumDigitalSignature


class Signer:
    """Represents the authentic Signer (Alice) in the QDS protocol."""
    
    def __init__(
        self,
        signer_id: str = "Alice",
        secret_key: str = "alice_sec_key_qds_2026_x89a",
        config: Optional[ProtocolConfig] = None
    ) -> None:
        self.signer_id = signer_id
        self.secret_key = secret_key
        self.config = config if config is not None else ProtocolConfig()
        
    def _map_bits_to_pauli_state(self, b1: int, b2: int) -> Tuple[str, str, np.ndarray]:
        """Map a pair of bits (b1, b2) to a canonical Pauli eigenstate and basis choice."""
        if (b1, b2) == (0, 0):
            return "|0>", "Z", get_pauli_state("|0>")
        elif (b1, b2) == (0, 1):
            return "|1>", "Z", get_pauli_state("|1>")
        elif (b1, b2) == (1, 0):
            return "|+>", "X", get_pauli_state("|+>")
        elif (b1, b2) == (1, 1):
            return "|+_y>", "Y", get_pauli_state("|+_y>")
        else:
            return "|0>", "Z", get_pauli_state("|0>")

    def sign(
        self,
        message: Message,
        session: Session,
        seed: Optional[int] = None
    ) -> QuantumDigitalSignature:
        """Generate a complete Quantum Digital Signature for a given message and session."""
        rng = np.random.default_rng(seed)
        
        # 1. Derive bit sequence from message hash
        message_bits = message.to_bit_array()
        
        elements: List[SignatureElement] = []
        bsm_bit_string = ""
        
        qubit_count = self.config.signature_qubit_count
        for i in range(qubit_count):
            # Select bit pair
            idx1 = (2 * i) % len(message_bits)
            idx2 = (2 * i + 1) % len(message_bits)
            b1 = message_bits[idx1]
            b2 = message_bits[idx2]
            
            state_name, basis, state_vec = self._map_bits_to_pauli_state(b1, b2)
            
            # Teleport state to create the classical correction bits and transmitted quantum state
            tele_res = teleport_quantum_state(
                input_state=state_vec,
                state_name=state_name,
                seed=int(rng.integers(0, 1000000))
            )
            
            c1, c2 = tele_res.classical_bits
            bsm_bit_string += f"{c1}{c2}"
            
            elements.append(
                SignatureElement(
                    qubit_index=i,
                    state_name=state_name,
                    basis_choice=basis,
                    bsm_classical_bits=(c1, c2),
                    quantum_state_vec=tele_res.raw_bob_state_vec,  # Bob's raw qubit before correction
                    reconstructed_density_matrix=None
                )
            )
            
        # 2. Compute cryptographic authentication tag using HMAC-SHA256
        tag_payload = f"{self.signer_id}:{session.session_id}:{session.nonce}:{message.hash_hex}:{bsm_bit_string}"
        auth_tag = hmac.new(
            self.secret_key.encode('utf-8'),
            tag_payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        return QuantumDigitalSignature(
            signer_id=self.signer_id,
            session_id=session.session_id,
            nonce=session.nonce,
            message_hash_hex=message.hash_hex,
            elements=elements,
            auth_tag=auth_tag,
            timestamp=time.time()
        )
