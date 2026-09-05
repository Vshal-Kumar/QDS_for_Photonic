"""Signature structure and metadata integrity verification."""

from qds.signature import QuantumDigitalSignature


def verify_signature_bundle_integrity(signature: QuantumDigitalSignature) -> tuple[bool, str]:
    """Verify that all signature elements, classical bit pairs, and indices are well-formed."""
    if not signature.elements:
        return False, "Signature element list is empty."
        
    for i, el in enumerate(signature.elements):
        if el.qubit_index != i:
            return False, f"Signature element index mismatch at position {i}: found {el.qubit_index}."
        if el.bsm_classical_bits not in [(0, 0), (0, 1), (1, 0), (1, 1)]:
            return False, f"Invalid BSM classical bits {el.bsm_classical_bits} at index {i}."
        if el.basis_choice not in ["Z", "X", "Y"]:
            return False, f"Invalid basis choice '{el.basis_choice}' at index {i}."
            
    return True, ""
