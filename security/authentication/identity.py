"""Identity models, credential registries, and key management."""

from dataclasses import dataclass
from typing import Dict, Set, Optional


@dataclass
class EntityIdentity:
    """Represents an entity participating in the QDS network."""
    entity_id: str
    role: str  # "signer", "verifier", "auditor", "untrusted"
    public_key_or_cert: str
    is_revoked: bool = False


class IdentityRegistry:
    """Registry maintaining authorized signers and verifiers."""
    
    def __init__(
        self,
        signers: Optional[Dict[str, str]] = None,
        verifiers: Optional[Set[str]] = None
    ) -> None:
        # Default authorized signers with their pre-shared key/cert
        self._signers: Dict[str, str] = signers if signers is not None else {
            "Alice": "alice_sec_key_qds_2026_x89a",
            "Alice_Backup": "alice_backup_key_qds_77c1",
        }
        
        # Default authorized verifiers
        self._verifiers: Set[str] = verifiers if verifiers is not None else {
            "Bob",
            "Charlie_Auditor",
            "Bob_Secondary",
        }
        
        self._revoked_entities: Set[str] = set()
        
    def register_signer(self, signer_id: str, secret_key: str) -> None:
        """Register a new authorized signer."""
        self._signers[signer_id] = secret_key
        
    def register_verifier(self, verifier_id: str) -> None:
        """Register a new authorized verifier."""
        self._verifiers.add(verifier_id)
        
    def revoke_entity(self, entity_id: str) -> None:
        """Revoke authorization for an entity."""
        self._revoked_entities.add(entity_id)
        
    def is_known_signer(self, signer_id: str) -> bool:
        """Check if signer exists in the registry."""
        return signer_id in self._signers and signer_id not in self._revoked_entities
        
    def is_authorized_verifier(self, verifier_id: str) -> bool:
        """Check if verifier is permitted to perform verification."""
        return verifier_id in self._verifiers and verifier_id not in self._revoked_entities
        
    def get_signer_secret(self, signer_id: str) -> Optional[str]:
        """Retrieve signer secret for HMAC validation."""
        if self.is_known_signer(signer_id):
            return self._signers.get(signer_id)
        return None
