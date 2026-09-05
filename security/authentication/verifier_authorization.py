"""Verifier authorization and rogue verification attempt detection."""

from dataclasses import dataclass
from typing import Optional
from security.authentication.identity import IdentityRegistry


@dataclass
class VerifierAuthResult:
    """Outcome of verifier authorization check."""
    is_authorized: bool
    verifier_id: str
    error_message: str = ""
    is_unauthorized_attempt: bool = False


class VerifierAuthorizer:
    """Checks whether an entity is permitted to perform verification on the QDS channel."""
    
    def __init__(self, registry: Optional[IdentityRegistry] = None) -> None:
        self.registry = registry if registry is not None else IdentityRegistry()
        
    def authorize_verifier(self, verifier_id: str) -> VerifierAuthResult:
        """Verify that the verifier identity has legitimate verification clearance."""
        if not self.registry.is_authorized_verifier(verifier_id):
            return VerifierAuthResult(
                is_authorized=False,
                verifier_id=verifier_id,
                error_message=f"Unauthorized entity '{verifier_id}' attempted to access the verification service.",
                is_unauthorized_attempt=True
            )
            
        return VerifierAuthResult(
            is_authorized=True,
            verifier_id=verifier_id,
            error_message="",
            is_unauthorized_attempt=False
        )
