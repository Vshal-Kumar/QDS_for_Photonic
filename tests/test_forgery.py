"""Unit tests for signature forgery generation and verification failure."""

import pytest
from core.message import Message
from core.session import Session
from qds.verifier import Verifier
from qds.verification import verify_qds_signature
from attacks.signature.forgery import generate_forged_signature_random_guess


def test_forgery_random_guessing_fails_verification():
    """Verify that random state guessing by Eve fails QDS signature verification with high mismatch."""
    msg = Message(content="Authentic Contract Terms")
    session = Session(signer_id="Alice", verifier_id="Bob")
    
    forged_sig = generate_forged_signature_random_guess(
        message=msg,
        session=session,
        signature_length=32,
        seed=42
    )
    
    verifier = Verifier("Bob")
    reconstructed_states = verifier.reconstruct_signature_states(forged_sig)
    
    res = verify_qds_signature(msg, forged_sig, reconstructed_states)
    
    # Random guessing yields high mismatch rate (typically ~50% to ~75%)
    assert res.is_valid is False
    assert res.mismatch_rate > 0.30
