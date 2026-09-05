"""Replay attack detector and nonce/session uniqueness validator."""

from dataclasses import dataclass
from typing import Optional
from core.session import SessionStore


@dataclass
class ReplayCheckResult:
    """Outcome of nonce freshness and replay attack check."""
    is_fresh: bool
    nonce: str
    session_id: str
    error_message: str = ""
    is_replay_detected: bool = False


class ReplayProtector:
    """Detects and prevents replay of previously transmitted signatures and nonces."""
    
    def __init__(self, session_store: Optional[SessionStore] = None) -> None:
        self.session_store = session_store if session_store is not None else SessionStore()
        
    def check_and_record(self, nonce: str, session_id: str) -> ReplayCheckResult:
        """Verify that the nonce has never been used before, then record it as used."""
        if self.session_store.is_nonce_used(nonce):
            return ReplayCheckResult(
                is_fresh=False,
                nonce=nonce,
                session_id=session_id,
                error_message=f"Replay attack detected: Nonce '{nonce}' has already been processed in a prior transmission.",
                is_replay_detected=True
            )
            
        # Record nonce
        self.session_store.record_nonce(nonce)
        
        return ReplayCheckResult(
            is_fresh=True,
            nonce=nonce,
            session_id=session_id,
            error_message="",
            is_replay_detected=False
        )
