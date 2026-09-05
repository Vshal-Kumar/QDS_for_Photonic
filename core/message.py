"""Classical message data structures and cryptographic hashing."""

import hashlib
import time
import uuid
from dataclasses import dataclass, field
from typing import Dict, Any, List


@dataclass
class Message:
    """Represents a classical message to be signed via QDS."""
    
    content: str
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def hash_hex(self) -> str:
        """Compute SHA-256 hex digest of the message content."""
        return hashlib.sha256(self.content.encode('utf-8')).hexdigest()
    
    @property
    def hash_bytes(self) -> bytes:
        """Compute SHA-256 raw bytes of the message content."""
        return hashlib.sha256(self.content.encode('utf-8')).digest()
    
    def to_bit_array(self) -> List[int]:
        """Convert the message hash to a list of bits (256 bits)."""
        bits: List[int] = []
        for byte in self.hash_bytes:
            for bit_idx in range(7, -1, -1):
                bits.append((byte >> bit_idx) & 1)
        return bits
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize message to dictionary representation."""
        return {
            "content": self.content,
            "message_id": self.message_id,
            "timestamp": self.timestamp,
            "hash_hex": self.hash_hex,
            "metadata": self.metadata
        }
