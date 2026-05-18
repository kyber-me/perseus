"""
Perseus — Point

A single atomic semantic unit in the Neocortex.

A Point represents the embedding of one sintagma (a segment identified
by the LLM via Event Segmentation Theory). Points are the elementary
building blocks from which Events are composed.

Points are never holistic or episodic — that role belongs to Event.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

import numpy as np


@dataclass
class Point:
    """
    Atomic semantic unit — the embedding of a single sintagma.

    Attributes
    ----------
    text        : the original sintagma text.
    embedding   : dense embedding vector of the sintagma.
    ms          : memory strength (0.0 to 1.0+), grows via LTP reinforcement.
    timestamp   : last time this point was activated/reinforced.
    connections : IDs of Points that follow this one in sequence (within an Event).
    """
    text: str
    embedding: np.ndarray
    memory_strength: float = 0.1
    timestamp: float = field(default_factory=time.time)
    connections: list[str] = field(default_factory=list)

    def __post_init__(self):
        self.embedding = self.embedding.copy()

    def reinforce(self, energy: float) -> None:
        """
        Apply LTP reinforcement: memory_strength += log(1 + energy).
        Updates timestamp to now.
        """
        self.memory_strength += float(np.log1p(energy))
        self.timestamp        = time.time()

    def __repr__(self) -> str:
        return f"Point(text={self.text!r}, memory_strength={self.memory_strength:.3f})"
