"""Signer authentication and identity spoofing / impersonation detection."""

import hashlib
import hmac
from dataclasses import dataclass
from typing import Optional

from core.message import Message
from core.session import Session
from qds.signature import QuantumDigitalSignature
from security.authentication.identity import IdentityRegistry


@dataclass
class SignerAuthResult:
    """Outcome of signer identity verification."""
    is_authenticated: bool
    signer_id: str
    error_message: str = ""
    is_impersonation_attack: bool = False


class SignerAuthenticator:
    """Verifies Alice's identity and detects impersonation attempts."""
    
    def __init__(self, registry: Optional[IdentityRegistry] = None) -> None:
        self.registry = registry if registry is not None else IdentityRegistry()
        
    def authenticate_signer(
        self,
        signature: QuantumDigitalSignature,
        message: Message,
        session: Session
    ) -> SignerAuthResult:
        """Verify the signer's identity and validate the cryptographic authentication tag.
        
        Checks:
        1. Signer exists in the authorized identity registry.
        2. Signer identity is not revoked.
        3. HMAC tag correctly verifies against the message hash and session parameters.
        """
        signer_id = signature.signer_id
        
        # 1. Identity existence check
        if not self.registry.is_known_signer(signer_id):
            return SignerAuthResult(
                is_authenticated=False,
                signer_id=signer_id,
                error_message=f"Unknown or unauthorized signer identity '{signer_id}'.",
                is_impersonation_attack=True
            )
            
        secret_key = self.registry.get_signer_secret(signer_id)
        if not secret_key:
            return SignerAuthResult(
                is_authenticated=False,
                signer_id=signer_id,
                error_message=f"No secret key available for signer '{signer_id}'.",
                is_impersonation_attack=True
            )
            
        # 2. Re-compute HMAC auth tag
        bsm_bit_string = "".join(f"{el.bsm_classical_bits[0]}{el.bsm_classical_bits[1]}" for el in signature.elements)
        tag_payload = f"{signer_id}:{session.session_id}:{session.nonce}:{message.hash_hex}:{bsm_bit_string}"
        
        expected_tag = hmac.new(
            secret_key.encode('utf-8'),
            tag_payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(expected_tag, signature.auth_tag):
            return SignerAuthResult(
                is_authenticated=False,
                signer_id=signer_id,
                error_message="Invalid cryptographic authentication tag. Possible identity forgery or impersonation.",
                is_impersonation_attack=True
            )
            
        return SignerAuthResult(
            is_authenticated=True,
            signer_id=signer_id,
            error_message="",
            is_impersonation_attack=False
        )
