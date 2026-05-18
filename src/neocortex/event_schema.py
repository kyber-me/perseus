"""
Perseus — EventSchema

A named region of the Neocortex that owns one EventModelAutomaton
and accumulates Events to build an emergent conceptual description.

In Event Segmentation Theory (EST), a Schema is the stable, long-term
knowledge structure. Here it is NOT pre-defined — it emerges bottom-up
from the patterns of Events assigned to it.

The schema's `concept` field starts empty and evolves over time as
the LLM synthesises a description from the accumulated events.
"""

from __future__ import annotations

import uuid

import numpy as np

from automaton.event_model_automaton import EventModelAutomaton, EventModelMode
from neocortex.event import Event


class EventSchema:
    """
    A named Neocortex region bound to a single EventModelAutomaton.
    Accumulates Events and maintains an emergent conceptual description.

    Attributes
    ----------
    name     : semantic identifier (arbitrary, assigned at spawn time).
    model    : the EventModelAutomaton — seeded by each incoming Event.
    events   : ordered list of Events assigned to this schema.
    concept  : evolving textual description, synthesised by the LLM.
    centroid : mean of all event embeddings assigned so far.
               Used for schema-level routing (Neocortex distance calculation).
    """

    def __init__(self, name: str, width: int = 16, height: int = 16) -> None:
        self.schema_id: str       = str(uuid.uuid4())
        self.name    = name
        self.model   = EventModelAutomaton(schema=name, width=width, height=height)
        self.events: list[Event] = []
        self.concept: str        = ""
        self.centroid: np.ndarray | None = None

    # ── Core API ──────────────────────────────────────────────────────────────

    def absorb(self, event: Event) -> None:
        """
        Assign an Event to this schema.

        - Tags the event with this schema's name.
        - Seeds the automaton (High-Res Active mode).
        - Updates the running centroid of event embeddings.
        """
        event.schema_id   = self.schema_id
        event.schema_name  = self.name
        self.events.append(event)
        self.model.activate(event.seed)
        self._update_centroid(event.embedding)

    def rest(self) -> None:
        """Return the automaton to PASSIVE_REFLEXIVE (resting) mode."""
        self.model.rest()

    def step(self):
        """Advance the automaton by one tick."""
        return self.model.step()

    # ── Concept Evolution ─────────────────────────────────────────────────────

    def update_concept(self, description: str) -> None:
        """
        Update the schema's concept description.
        Called externally by the LLM pipeline after each new event is absorbed.
        """
        self.concept = description

    # ── Centroid ──────────────────────────────────────────────────────────────

    def _update_centroid(self, embedding: np.ndarray) -> None:
        """Running mean of event embeddings (online update)."""
        n = len(self.events)
        if self.centroid is None:
            self.centroid = embedding.copy().astype(np.float32)
        else:
            # Welford-style online mean
            self.centroid += (embedding.astype(np.float32) - self.centroid) / n

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
        concept_preview = (self.concept[:40] + "…") if len(self.concept) > 40 else self.concept
        return (
            f"EventSchema(id={self.schema_id[:8]}…, "
            f"name={self.name!r}, "
            f"mode={self.mode.name}, "
            f"events={len(self.events)}, "
            f"concept={concept_preview!r})"
        )
