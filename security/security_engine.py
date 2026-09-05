"""Master Security Engine managing authentication, authorization, freshness, and integrity."""

from typing import List, Optional
import numpy as np

from config.security_config import SecurityConfig
from core.message import Message
from core.session import Session, SessionStore
from core.results import ProtocolCheckResult
from qds.signature import QuantumDigitalSignature
from security.authentication.identity import IdentityRegistry
from security.authentication.signer_authentication import SignerAuthenticator
from security.authentication.verifier_authorization import VerifierAuthorizer
from security.freshness.replay_protection import ReplayProtector
from security.verification.security_verification import run_comprehensive_protocol_checks


class SecurityEngine:
    """Central Security Coordinator governing protocol security and access control."""
    
    def __init__(self, config: Optional[SecurityConfig] = None) -> None:
        self.config = config if config is not None else SecurityConfig()
        self.identity_registry = IdentityRegistry(
            signers=self.config.authorized_signers,
            verifiers=self.config.authorized_verifiers
        )
        self.session_store = SessionStore(
            validity_window_sec=self.config.nonce_validity_window_sec
        )
        self.replay_protector = ReplayProtector(session_store=self.session_store)
        self.signer_authenticator = SignerAuthenticator(self.identity_registry)
        self.verifier_authorizer = VerifierAuthorizer(self.identity_registry)
        
    def evaluate_protocol_security(
        self,
        message: Message,
        session: Session,
        signature: QuantumDigitalSignature,
        reconstructed_states: List[np.ndarray],
        verifier_id: str = "Bob"
    ) -> ProtocolCheckResult:
        """Execute all multi-tier security checks on an incoming signature request."""
        return run_comprehensive_protocol_checks(
            message=message,
            session=session,
            signature=signature,
            reconstructed_states=reconstructed_states,
            verifier_id=verifier_id,
            identity_registry=self.identity_registry,
            replay_protector=self.replay_protector,
            max_session_age_sec=self.config.nonce_validity_window_sec
        )
