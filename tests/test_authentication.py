"""Unit tests for signer authentication and verifier authorization."""

import pytest
from core.message import Message
from core.session import Session
from qds.signer import Signer
from security.authentication.identity import IdentityRegistry
from security.authentication.signer_authentication import SignerAuthenticator
from security.authentication.verifier_authorization import VerifierAuthorizer


def test_signer_authentication_legitimate():
    """Verify authentic Alice signature passes authentication."""
    registry = IdentityRegistry()
    authenticator = SignerAuthenticator(registry)
    
    msg = Message(content="Valid Message")
    session = Session(signer_id="Alice")
    signer = Signer("Alice", secret_key=registry.get_signer_secret("Alice"))
    signature = signer.sign(msg, session)
    
    res = authenticator.authenticate_signer(signature, msg, session)
    assert res.is_authenticated is True
    assert res.is_impersonation_attack is False


def test_impersonation_attack_unknown_signer():
    """Verify unknown signer identity 'Eve' is flagged as an impersonation attack."""
    registry = IdentityRegistry()
    authenticator = SignerAuthenticator(registry)
    
    msg = Message(content="Malicious Message")
    session = Session(signer_id="Eve")
    signer = Signer("Eve", secret_key="fake_key")
    signature = signer.sign(msg, session)
    
    res = authenticator.authenticate_signer(signature, msg, session)
    assert res.is_authenticated is False
    assert res.is_impersonation_attack is True


def test_impersonation_attack_spoofed_alice_tag():
    """Verify attacker trying to sign as Alice with wrong key fails HMAC tag verification."""
    registry = IdentityRegistry()
    authenticator = SignerAuthenticator(registry)
    
    msg = Message(content="Spoofed Message")
    session = Session(signer_id="Alice")
    # Eve attempts to sign claiming to be Alice using a wrong secret key
    attacker_signer = Signer("Alice", secret_key="eve_guessed_key")
    signature = attacker_signer.sign(msg, session)
    
    res = authenticator.authenticate_signer(signature, msg, session)
    assert res.is_authenticated is False
    assert res.is_impersonation_attack is True


def test_verifier_authorization_authorized_and_unauthorized():
    """Verify verifier authorization clearance for Bob vs rogue Eve."""
    registry = IdentityRegistry()
    authorizer = VerifierAuthorizer(registry)
    
    # Authorized Bob
    res_bob = authorizer.authorize_verifier("Bob")
    assert res_bob.is_authorized is True
    assert res_bob.is_unauthorized_attempt is False
    
    # Unauthorized Eve
    res_eve = authorizer.authorize_verifier("Eve_Rogue")
    assert res_eve.is_authorized is False
    assert res_eve.is_unauthorized_attempt is True
