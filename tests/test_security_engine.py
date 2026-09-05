"""Unit tests for the integrated Security Engine."""

import pytest
from core.message import Message
from core.session import Session
from qds.signer import Signer
from qds.verifier import Verifier
from security.security_engine import SecurityEngine


def test_security_engine_full_legitimate_flow():
    """Verify that a legitimate QDS transmission passes all security engine checks."""
    sec_engine = SecurityEngine()
    msg = Message(content="Approved transaction")
    session = Session(signer_id="Alice", verifier_id="Bob")
    
    signer = Signer("Alice", secret_key=sec_engine.config.authorized_signers["Alice"])
    sig = signer.sign(msg, session)
    
    verifier = Verifier("Bob")
    reconstructed_states = verifier.reconstruct_signature_states(sig)
    
    res = sec_engine.evaluate_protocol_security(
        message=msg,
        session=session,
        signature=sig,
        reconstructed_states=reconstructed_states,
        verifier_id="Bob"
    )
    
    assert res.all_passed is True
    assert res.signer_authenticated is True
    assert res.verifier_authorized is True
    assert res.nonce_valid is True
    assert res.message_intact is True
    assert res.signature_intact is True


def test_security_engine_detects_replay_on_second_submission():
    """Verify that submitting the same signature twice triggers immediate replay failure."""
    sec_engine = SecurityEngine()
    msg = Message(content="Single-use payment")
    session = Session(signer_id="Alice", verifier_id="Bob")
    
    signer = Signer("Alice", secret_key=sec_engine.config.authorized_signers["Alice"])
    sig = signer.sign(msg, session)
    verifier = Verifier("Bob")
    reconstructed_states = verifier.reconstruct_signature_states(sig)
    
    # First submission: success
    res1 = sec_engine.evaluate_protocol_security(
        message=msg,
        session=session,
        signature=sig,
        reconstructed_states=reconstructed_states,
        verifier_id="Bob"
    )
    assert res1.all_passed is True
    
    # Replay submission: failure
    res2 = sec_engine.evaluate_protocol_security(
        message=msg,
        session=session,
        signature=sig,
        reconstructed_states=reconstructed_states,
        verifier_id="Bob"
    )
    assert res2.all_passed is False
    assert res2.nonce_valid is False
    assert "Replay attack detected" in res2.nonce_error
