"""Mapping between abstract qubit eigenstates and physical photon polarization modes."""

from typing import Dict
import numpy as np
from quantum.pauli_states import (
    STATE_0,
    STATE_1,
    STATE_PLUS,
    STATE_MINUS,
    STATE_PLUS_Y,
    STATE_MINUS_Y,
)


# Physical Polarization Modes
POLARIZATION_H: np.ndarray = STATE_0.copy()        # |H> Horizontal
POLARIZATION_V: np.ndarray = STATE_1.copy()        # |V> Vertical
POLARIZATION_D: np.ndarray = STATE_PLUS.copy()     # |D> Diagonal (+45 deg)
POLARIZATION_A: np.ndarray = STATE_MINUS.copy()    # |A> Anti-diagonal (-45 deg)
POLARIZATION_R: np.ndarray = STATE_PLUS_Y.copy()   # |R> Right Circular
POLARIZATION_L: np.ndarray = STATE_MINUS_Y.copy()  # |L> Left Circular

QUBIT_TO_POLARIZATION_MAP: Dict[str, str] = {
    "|0>": "|H>",
    "|1>": "|V>",
    "|+>": "|D>",
    "|->": "|A>",
    "|+_y>": "|R>",
    "|-_y>": "|L>",
    "0": "H",
    "1": "V",
    "+": "D",
    "-": "A",
    "+y": "R",
    "-y": "L",
}

POLARIZATION_TO_QUBIT_MAP: Dict[str, str] = {
    "|H>": "|0>",
    "|V>": "|1>",
    "|D>": "|+>",
    "|A>": "|->",
    "|R>": "|+_y>",
    "|L>": "|-_y>",
    "H": "0",
    "V": "1",
    "D": "+",
    "A": "-",
    "R": "+y",
    "L": "-y",
}


def qubit_to_polarization_label(qubit_label: str) -> str:
    """Convert abstract qubit label (e.g. '|0>') to photonic polarization label ('|H>')."""
    return QUBIT_TO_POLARIZATION_MAP.get(qubit_label.strip(), qubit_label)


def polarization_to_qubit_label(pol_label: str) -> str:
    """Convert photonic polarization label (e.g. '|H>') to abstract qubit label ('|0>')."""
    return POLARIZATION_TO_QUBIT_MAP.get(pol_label.strip(), pol_label)
