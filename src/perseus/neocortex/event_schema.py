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
from perseus.neocortex.point import Point


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
        self.points: list[Point] = []

    # ── Delegation & Management ───────────────────────────────────────────────

    def activate(self, text: str, embedding: np.ndarray) -> Point:
        """
        [PLACEHOLDER — will be replaced by Event-based activation in Subtarefa 3]
        Creates a new Point and adds it to the catalogue.
        """
        point = Point(text=text, embedding=embedding)
        self.points.append(point)
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
