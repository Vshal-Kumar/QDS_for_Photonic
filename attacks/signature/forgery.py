"""Quantum Digital Signature forgery attack generators."""

from typing import List, Optional
import numpy as np
import secrets
import time

from core.message import Message
from core.session import Session
from quantum.pauli_states import get_pauli_state
from qds.signature import SignatureElement, QuantumDigitalSignature


def generate_forged_signature_random_guess(
    message: Message,
    session: Session,
    signature_length: int = 16,
    signer_id: str = "Alice",
    seed: Optional[int] = None
) -> QuantumDigitalSignature:
    """Generate a forged signature where Eve randomly guesses Pauli eigenstates and BSM bits."""
    rng = np.random.default_rng(seed)
    allowed_states = ["|0>", "|1>", "|+>", "|->", "|+_y>", "|-_y>"]
    state_to_basis = {
        "|0>": "Z", "|1>": "Z",
        "|+>": "X", "|->": "X",
        "|+_y>": "Y", "|-_y>": "Y",
    }
    
    elements: List[SignatureElement] = []
    for i in range(signature_length):
        st_name = str(rng.choice(allowed_states))
        basis = state_to_basis[st_name]
        vec = get_pauli_state(st_name)
        c1 = int(rng.choice([0, 1]))
        c2 = int(rng.choice([0, 1]))
        
        elements.append(
            SignatureElement(
                qubit_index=i,
                state_name=st_name,
                basis_choice=basis,
                bsm_classical_bits=(c1, c2),
                quantum_state_vec=vec
            )
        )
        
    # Eve creates a fake HMAC tag
    fake_tag = secrets.token_hex(32)
    
    return QuantumDigitalSignature(
        signer_id=signer_id,
        session_id=session.session_id,
        nonce=session.nonce,
        message_hash_hex=message.hash_hex,
        elements=elements,
        auth_tag=fake_tag,
        timestamp=time.time()
    )
