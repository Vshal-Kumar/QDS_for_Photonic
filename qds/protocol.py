"""QDS protocol orchestrator executing complete signing, transmission, and verification cycles."""

from typing import Tuple, List, Optional
import numpy as np

from config.protocol_config import ProtocolConfig
from config.photonic_config import PhotonicConfig
from core.message import Message
from core.session import Session
from photonic.optical_channel import PhotonicChannel
from qds.signer import Signer
from qds.verifier import Verifier
from qds.verification import verify_qds_signature, QDSVerificationResult
from qds.signature import QuantumDigitalSignature


class QDSProtocol:
    """Orchestrates the entire Teleportation-based Quantum Digital Signature workflow."""
    
    def __init__(
        self,
        protocol_config: Optional[ProtocolConfig] = None,
        photonic_config: Optional[PhotonicConfig] = None
    ) -> None:
        self.protocol_config = protocol_config if protocol_config is not None else ProtocolConfig()
        self.photonic_config = photonic_config if photonic_config is not None else PhotonicConfig()
        self.signer = Signer("Alice", config=self.protocol_config)
        self.verifier = Verifier("Bob")
        self.channel = PhotonicChannel(config=self.photonic_config)
        
    def execute_cycle(
        self,
        message: Message,
        session: Session,
        distance_km: float = 0.0,
        seed: Optional[int] = None
    ) -> Tuple[QuantumDigitalSignature, List[np.ndarray], QDSVerificationResult]:
        """Execute a full QDS protocol cycle:
        1. Alice generates signature & teleports states
        2. States propagate through optical channel of distance_km
        3. Bob applies Pauli correction and verifies the signature
        """
        rng = np.random.default_rng(seed)
        
        # 1. Sign
        signature = self.signer.sign(message, session, seed=int(rng.integers(0, 1000000)))
        
        # 2. Transmit each qubit through the photonic channel
        received_states: List[np.ndarray] = []
        for el in signature.elements:
            res = self.channel.transmit(
                input_state=el.quantum_state_vec,
                distance_km=distance_km,
                rng=rng
            )
            received_states.append(res.output_rho)
            
        # 3. Bob reconstructs states
        reconstructed_rhos = self.verifier.reconstruct_signature_states(
            signature=signature,
            received_quantum_states=received_states
        )
        
        # 4. Verify
        verif_result = verify_qds_signature(
            message=message,
            signature=signature,
            reconstructed_states=reconstructed_rhos,
            config=self.protocol_config
        )
        
        return signature, reconstructed_rhos, verif_result
