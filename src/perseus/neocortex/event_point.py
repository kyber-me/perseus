"""
Perseus — EventPoint

A single atomic unit of memory in the Neocortex.

Each EventPoint represents a registered event boundary, linking
semantic content (text) to a procedural seed (CA grid) and
metabolic state (Ms, timestamp).
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

import numpy as np


@dataclass
class EventPoint:
    """
    A single memory point in an EventSchema.

    Attributes
    ----------
    text        : the original semantic content (sintagma).
    seed        : the 16x16 binary grid configuration for this event.
    ms          : memory strength (0.0 to 1.0+).
    timestamp   : last time this point was activated/reinforced.
    connections : list of IDs of points that follow this one in sequence.
    """
    text: str
    seed: np.ndarray
    ms: float = 0.1
    timestamp: float = field(default_factory=time.time)
    connections: list[str] = field(default_factory=list)

    def __post_init__(self):
        # Ensure seed is a copy to avoid external mutation
        self.seed = self.seed.copy()

    def reinforce(self, energy: float, decay_constant: float = 0.05):
        """
        Apply metabolic reinforcement (LTP) and update timestamp.
        ms = ms + log(1 + energy)
        """
        self.ms += np.log1p(energy)
        self.timestamp = time.time()

    def __repr__(self) -> str:
        return f"EventPoint(text={self.text!r}, ms={self.ms:.3f})"
