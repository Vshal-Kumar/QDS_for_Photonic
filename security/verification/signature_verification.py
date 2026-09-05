"""Cryptographic signature and identity verification integration."""

from dataclasses import dataclass
from core.message import Message
from core.session import Session
from qds.signature import QuantumDigitalSignature
from security.authentication.signer_authentication import SignerAuthenticator, SignerAuthResult
from security.freshness.replay_protection import ReplayProtector, ReplayCheckResult


@dataclass
class SignatureSecurityResult:
    """Consolidated signature and protocol authenticity verification result."""
    is_authentic: bool
    auth_result: SignerAuthResult
    replay_result: ReplayCheckResult
    error_message: str = ""


def verify_signature_authenticity(
    signature: QuantumDigitalSignature,
    message: Message,
    session: Session,
    authenticator: SignerAuthenticator,
    replay_protector: ReplayProtector
) -> SignatureSecurityResult:
    """Verify signer authentication and nonce freshness before proceeding to quantum verification."""
    # 1. Authenticate Signer
    auth_res = authenticator.authenticate_signer(signature, message, session)
    if not auth_res.is_authenticated:
        return SignatureSecurityResult(
            is_authentic=False,
            auth_result=auth_res,
            replay_result=ReplayCheckResult(is_fresh=True, nonce=signature.nonce, session_id=signature.session_id),
            error_message=f"Signer authentication failed: {auth_res.error_message}"
        )
        
    # 2. Check Freshness / Replay
    replay_res = replay_protector.check_and_record(signature.nonce, signature.session_id)
    if not replay_res.is_fresh:
        return SignatureSecurityResult(
            is_authentic=False,
            auth_result=auth_res,
            replay_result=replay_res,
            error_message=f"Freshness check failed: {replay_res.error_message}"
        )
        
    return SignatureSecurityResult(
        is_authentic=True,
        auth_result=auth_res,
        replay_result=replay_res,
        error_message=""
    )
