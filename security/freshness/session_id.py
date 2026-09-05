"""Session ID lifecycle management and session state verification."""

import time
import uuid
from typing import Optional
from core.session import Session


def create_session_id() -> str:
    """Generate a globally unique session identifier."""
    return str(uuid.uuid4())


def validate_session_freshness(
    session: Session,
    max_age_sec: float = 300.0,
    current_time: Optional[float] = None
) -> tuple[bool, str]:
    """Verify that the session timestamp is within the allowable freshness window."""
    now = current_time if current_time is not None else time.time()
    
    if session.created_at > now + 5.0:
        return False, "Session created_at timestamp is in the future (clock skew anomaly)."
        
    age = now - session.created_at
    if age > max_age_sec:
        return False, f"Session expired. Age {age:.1f}s exceeds maximum freshness window of {max_age_sec}s."
        
    if not session.is_active:
        return False, "Session is marked inactive or terminated."
        
    return True, ""
