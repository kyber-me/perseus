"""
Perseus — EventSchema

A named region of the Neocortex that owns one EventModelAutomaton.

In Event Segmentation Theory (EST), a Schema is the stable, long-term
knowledge structure. This minimal implementation simply binds a name to
its active Event Model, delegating all CA dynamics to it.

Seeds are accepted as opaque binary grids (16×16, ON/OFF) produced
externally. The encoding pipeline (text → seed) is not implemented here.
"""

from __future__ import annotations

import numpy as np

from perseus.automaton.event_model_automaton import EventModelAutomaton, EventModelMode
from perseus.neocortex.event_point import EventPoint


class EventSchema:
    """
    A named Neocortex region bound to a single EventModelAutomaton.
    Manages a catalogue of EventPoints.

    Attributes
    ----------
    name   : semantic identifier for this schema region.
    model  : the EventModelAutomaton that processes events for this schema.
    points : list of EventPoint objects (long-term memory).
    """

    def __init__(self, name: str, width: int = 16, height: int = 16) -> None:
        self.name   = name
        self.model  = EventModelAutomaton(schema=name, width=width, height=height)
        self.points: list[EventPoint] = []

    # ── Delegation & Management ───────────────────────────────────────────────

    def activate(self, text: str, seed: np.ndarray) -> EventPoint:
        """
        Process an incoming event boundary.
        Creates a new EventPoint, adds it to the catalogue, and seeds the model.
        """
        point = EventPoint(text=text, seed=seed)
        self.points.append(point)
        
        # Synchronize with the automaton's internal catalogue
        self.model.activate(seed)
        
        return point

    def rest(self) -> None:
        """Return the model to PASSIVE_REFLEXIVE (resting) mode."""
        self.model.rest()

    def step(self):
        """Advance the automaton by one tick."""
        return self.model.step()

    # ── Read-only pass-throughs ───────────────────────────────────────────────

    @property
    def mode(self) -> EventModelMode:
        return self.model.mode

    @property
    def entropy(self) -> float:
        return self.model.entropy

    @property
    def occupancy(self) -> float:
        return self.model.occupancy

    def __repr__(self) -> str:
        return (
            f"EventSchema(name={self.name!r}, "
            f"mode={self.mode.name}, "
            f"points={len(self.points)}, "
            f"entropy={self.entropy:.3f})"
        )
