"""Signer impersonation and identity spoofing attack generator."""

from dataclasses import replace
from qds.signature import QuantumDigitalSignature


def create_impersonated_signature(
    original_signature: QuantumDigitalSignature,
    fake_signer_id: str = "Eve_Pretending_Alice"
) -> QuantumDigitalSignature:
    """Create a signature bundle with a modified or spoofed signer identity."""
    spoofed = replace(original_signature, signer_id=fake_signer_id)
    return spoofed
