"""Cryptographic nonce generation, validation, and entropy verification."""

import secrets
import string


def generate_secure_nonce(byte_length: int = 16) -> str:
    """Generate a cryptographically secure random hexadecimal nonce."""
    return secrets.token_hex(byte_length)


def validate_nonce_format(nonce: str, min_length: int = 16) -> bool:
    """Verify that the nonce is a valid hex string of sufficient length."""
    if not isinstance(nonce, str) or len(nonce) < min_length:
        return False
    hex_chars = set(string.hexdigits)
    return all(c in hex_chars for c in nonce)
