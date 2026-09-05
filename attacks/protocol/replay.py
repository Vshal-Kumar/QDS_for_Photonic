"""Replay attack simulation module."""

from dataclasses import replace
from qds.signature import QuantumDigitalSignature
from core.session import Session


def create_replayed_signature(
    original_signature: QuantumDigitalSignature,
    target_session: Session
) -> QuantumDigitalSignature:
    """Simulate Eve re-transmitting an intercepted signature into a new or existing session.
    
    The signature carries an already used nonce / stale session metadata.
    """
    # Clone signature keeping the original nonce
    replayed = replace(original_signature)
    return replayed
