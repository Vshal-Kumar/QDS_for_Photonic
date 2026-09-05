"""Unauthorized verification request generator."""

from dataclasses import dataclass


@dataclass
class RogueVerificationRequest:
    """Represents an unauthorized verifier querying the QDS verification service."""
    verifier_id: str = "Eve_Rogue_Verifier"
    session_id: str = "fake-sess-999"
    requested_signature_id: str = "sig-target-001"
