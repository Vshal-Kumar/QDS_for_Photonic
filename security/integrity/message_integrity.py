"""Message integrity validation and tamper detection."""

import hashlib
from core.message import Message


def verify_message_integrity(message: Message, expected_hash_hex: str) -> tuple[bool, str]:
    """Verify that the message payload matches the declared SHA-256 hash."""
    actual_hash = hashlib.sha256(message.content.encode('utf-8')).hexdigest()
    if actual_hash != expected_hash_hex:
        return False, f"Message content has been tampered with. Expected hash {expected_hash_hex}, computed {actual_hash}."
    return True, ""
