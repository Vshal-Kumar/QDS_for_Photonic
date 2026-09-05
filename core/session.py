"""Session management, nonce tracking, and communication state."""

import secrets
import time
import uuid
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Set


@dataclass
class Session:
    """Represents a QDS transmission session between a signer and verifier."""
    
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    signer_id: str = "Alice"
    verifier_id: str = "Bob"
    nonce: str = field(default_factory=lambda: secrets.token_hex(16))
    created_at: float = field(default_factory=time.time)
    expires_at: Optional[float] = None
    is_active: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_expired(self, current_time: Optional[float] = None) -> bool:
        """Check if the session has expired."""
        now = current_time if current_time is not None else time.time()
        if self.expires_at is not None:
            return now > self.expires_at
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize session state to dictionary."""
        return {
            "session_id": self.session_id,
            "signer_id": self.signer_id,
            "verifier_id": self.verifier_id,
            "nonce": self.nonce,
            "created_at": self.created_at,
            "expires_at": self.expires_at,
            "is_active": self.is_active,
            "metadata": self.metadata
        }


class SessionStore:
    """Thread-safe session repository and nonce cache for replay prevention."""
    
    def __init__(self, validity_window_sec: float = 300.0) -> None:
        self.validity_window_sec = validity_window_sec
        self._sessions: Dict[str, Session] = {}
        self._used_nonces: Set[str] = set()
        self._nonce_timestamps: Dict[str, float] = {}
    
    def create_session(
        self,
        signer_id: str = "Alice",
        verifier_id: str = "Bob",
        nonce: Optional[str] = None
    ) -> Session:
        """Create and store a new active session."""
        now = time.time()
        session_nonce = nonce if nonce is not None else secrets.token_hex(16)
        session = Session(
            session_id=str(uuid.uuid4()),
            signer_id=signer_id,
            verifier_id=verifier_id,
            nonce=session_nonce,
            created_at=now,
            expires_at=now + self.validity_window_sec
        )
        self._sessions[session.session_id] = session
        return session
    
    def get_session(self, session_id: str) -> Optional[Session]:
        """Retrieve a session by ID."""
        return self._sessions.get(session_id)
    
    def is_nonce_used(self, nonce: str) -> bool:
        """Check if a nonce has been registered previously."""
        return nonce in self._used_nonces
    
    def record_nonce(self, nonce: str, timestamp: Optional[float] = None) -> None:
        """Register a nonce as used with timestamp."""
        ts = timestamp if timestamp is not None else time.time()
        self._used_nonces.add(nonce)
        self._nonce_timestamps[nonce] = ts
    
    def purge_expired(self, current_time: Optional[float] = None) -> int:
        """Purge sessions and nonces older than the validity window."""
        now = current_time if current_time is not None else time.time()
        expired_sessions = [
            sid for sid, s in self._sessions.items()
            if s.is_expired(now)
        ]
        for sid in expired_sessions:
            del self._sessions[sid]
        
        expired_nonces = [
            n for n, ts in self._nonce_timestamps.items()
            if now - ts > self.validity_window_sec
        ]
        for n in expired_nonces:
            self._used_nonces.discard(n)
            del self._nonce_timestamps[n]
            
        return len(expired_sessions)
