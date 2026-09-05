"""Integrated protocol security validator executing identity, authorization, freshness, and integrity."""

from typing import Optional, List
import numpy as np

from core.message import Message
from core.session import Session
from core.results import ProtocolCheckResult
from qds.signature import QuantumDigitalSignature
from security.authentication.identity import IdentityRegistry
from security.authentication.signer_authentication import SignerAuthenticator
from security.authentication.verifier_authorization import VerifierAuthorizer
from security.freshness.replay_protection import ReplayProtector
from security.freshness.session_id import validate_session_freshness
from security.integrity.message_integrity import verify_message_integrity
from security.integrity.signature_integrity import verify_signature_bundle_integrity
from security.integrity.state_integrity import verify_quantum_state_integrity


def run_comprehensive_protocol_checks(
    message: Message,
    session: Session,
    signature: QuantumDigitalSignature,
    reconstructed_states: List[np.ndarray],
    verifier_id: str,
    identity_registry: IdentityRegistry,
    replay_protector: ReplayProtector,
    max_session_age_sec: float = 300.0
) -> ProtocolCheckResult:
    """Execute all classical protocol-level security checks prior to quantum measurement."""
    result = ProtocolCheckResult()
    
    # 1. Verifier Authorization Check
    authorizer = VerifierAuthorizer(identity_registry)
    v_auth = authorizer.authorize_verifier(verifier_id)
    result.verifier_authorized = v_auth.is_authorized
    result.verifier_error = v_auth.error_message if not v_auth.is_authorized else None
    
    # 2. Signer Authentication Check
    authenticator = SignerAuthenticator(identity_registry)
    s_auth = authenticator.authenticate_signer(signature, message, session)
    result.signer_authenticated = s_auth.is_authenticated
    result.signer_error = s_auth.error_message if not s_auth.is_authenticated else None
    
    # 3. Nonce Freshness & Replay Check
    replay_res = replay_protector.check_and_record(signature.nonce, session.session_id)
    result.nonce_valid = replay_res.is_fresh
    result.nonce_error = replay_res.error_message if not replay_res.is_fresh else None
    
    # 4. Session Validity Check
    sess_valid, sess_err = validate_session_freshness(session, max_age_sec=max_session_age_sec)
    result.session_valid = sess_valid
    result.session_error = sess_err if not sess_valid else None
    
    # 5. Message Integrity Check
    msg_valid, msg_err = verify_message_integrity(message, signature.message_hash_hex)
    result.message_intact = msg_valid
    result.message_error = msg_err if not msg_valid else None
    
    # 6. Signature Bundle Integrity Check
    sig_valid, sig_err = verify_signature_bundle_integrity(signature)
    result.signature_intact = sig_valid
    result.signature_error = sig_err if not sig_valid else None
    
    # 7. Quantum State Physical Integrity Check
    for i, rho in enumerate(reconstructed_states):
        st_valid, st_err = verify_quantum_state_integrity(rho)
        if not st_valid:
            result.signature_intact = False
            result.signature_error = f"Physical state integrity failed at qubit {i}: {st_err}"
            break
            
    return result
