"""Unit tests for the Quantum Digital Signature (QDS) protocol."""

import pytest
import numpy as np
from core.message import Message
from core.session import Session
from qds.signer import Signer
from qds.verifier import Verifier
from qds.verification import verify_qds_signature
from qds.protocol import QDSProtocol


def test_qds_signing_and_verification_ideal():
    """Verify that a legitimate signature produced by Alice passes Bob's verification with 0% mismatch."""
    message = Message(content="Transfer 500 Quantum Credits to Bob")
    session = Session(signer_id="Alice", verifier_id="Bob")
    
    signer = Signer("Alice")
    signature = signer.sign(message, session, seed=42)
    
    verifier = Verifier("Bob")
    reconstructed_states = verifier.reconstruct_signature_states(signature)
    
    result = verify_qds_signature(message, signature, reconstructed_states)
    
    assert result.is_valid is True
    assert result.mismatch_rate == 0.0
    assert result.average_fidelity > 0.999
    assert len(signature.elements) == 16


def test_qds_tampered_message_fails():
    """Verify that if the message content is altered, verification fails immediately due to hash mismatch."""
    original_message = Message(content="Original contract text")
    tampered_message = Message(content="Tampered contract text")
    session = Session()
    
    signer = Signer("Alice")
    signature = signer.sign(original_message, session)
    
    verifier = Verifier("Bob")
    reconstructed_states = verifier.reconstruct_signature_states(signature)
    
    result = verify_qds_signature(tampered_message, signature, reconstructed_states)
    assert result.is_valid is False
    assert result.mismatch_rate == 1.0


def test_qds_protocol_cycle_across_distance():
    """Verify end-to-end QDS protocol cycle across 10 km optical fiber."""
    protocol = QDSProtocol()
    message = Message(content="Confidential Quantum Message")
    session = Session()
    
    sig, recon_states, verif_res = protocol.execute_cycle(
        message=message,
        session=session,
        distance_km=10.0,
        seed=123
    )
    
    assert verif_res.is_valid is True
    assert verif_res.average_fidelity > 0.90
