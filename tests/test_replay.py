"""Unit tests for nonce freshness and replay attack protection."""

import pytest
from core.session import SessionStore
from security.freshness.replay_protection import ReplayProtector


def test_nonce_replay_protection():
    """Verify first presentation of a nonce succeeds, while reuse immediately triggers replay detection."""
    store = SessionStore()
    protector = ReplayProtector(store)
    
    nonce = "a1b2c3d4e5f67890"
    session_id = "sess-001"
    
    # First attempt: fresh
    res1 = protector.check_and_record(nonce, session_id)
    assert res1.is_fresh is True
    assert res1.is_replay_detected is False
    
    # Second attempt with same nonce: replay detected
    res2 = protector.check_and_record(nonce, "sess-002")
    assert res2.is_fresh is False
    assert res2.is_replay_detected is True
    assert "Replay attack detected" in res2.error_message


def test_session_store_purge():
    """Verify expired sessions and nonces are correctly purged."""
    store = SessionStore(validity_window_sec=10.0)
    sess = store.create_session("Alice", "Bob", nonce="nonce_123")
    store.record_nonce(sess.nonce, sess.created_at)
    assert store.is_nonce_used("nonce_123") is True
    
    # Purge at current time + 20s
    purged = store.purge_expired(current_time=sess.created_at + 20.0)
    assert purged == 1
    assert store.is_nonce_used("nonce_123") is False
