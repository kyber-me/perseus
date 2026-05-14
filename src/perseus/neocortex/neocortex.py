"""
Perseus — Neocortex

Top-level orchestrator. Manages a registry of EventSchemas and routes
incoming Events to the most structurally similar schema.

Routing Algorithm (current — linear scan):
  For each new Event E:
    1. Compute score(S_i) = max similarity(E, e_j) for all e_j in S_i.events
    2. winner = argmax score(S_i)
    3. If score(winner) > τ(H)  → absorb into winner
       Else                     → spawn a new EventSchema

Threshold τ(H):
  τ(H) = τ_max · H^α
  H    = system entropy (1 - occupancy), averaged across all schemas.
  High H (sparse Neocortex) → generous threshold (few schemas, absorb more).
  Low  H (dense Neocortex)  → strict threshold (many schemas, discriminate more).

Future (search algorithm roadmap):
  - Ball Tree  : O(log N), works with custom metrics. Good entry point.
  - HNSW       : O(log N), state of the art, used in FAISS/hnswlib.
  - LSH        : probabilistic, natural for cosine similarity.
  - IVF        : cluster-based, scales to very large schema counts.
"""

from __future__ import annotations

import uuid

import numpy as np

from perseus.neocortex.event import Event
from perseus.neocortex.event_schema import EventSchema


class Neocortex:
    """
    Registry and router for EventSchemas.

    Attributes
    ----------
    tau_max : maximum similarity threshold (used when Neocortex is empty).
    alpha   : controls how fast τ shrinks as entropy falls. Default 1.0 (linear).
    """

    def __init__(
        self,
        tau_max: float = 0.75,
        alpha: float = 1.0,
    ) -> None:
        self._schemas: dict[str, EventSchema] = {}   # name → schema
        self._by_id:   dict[str, EventSchema] = {}   # schema_id → schema
        self.tau_max = tau_max
        self.alpha   = alpha

    # ── Core routing ──────────────────────────────────────────────────────────

    def route(self, event: Event) -> EventSchema:
        """
        Route an incoming Event to the most similar schema, or spawn a new one.

        Uses max-similarity (nearest-neighbour) per schema:
            score(S_i) = max(event.similarity(e_j) for e_j in S_i.events)

        Returns the EventSchema that absorbed the event.
        """
        if not self._schemas:
            return self._spawn_and_absorb(event)

        winner, best_score = self._find_best_schema(event)
        tau = self._threshold()

        if best_score >= tau:
            winner.absorb(event)
            return winner
        else:
            return self._spawn_and_absorb(event)

    # ── Manual / demo access ──────────────────────────────────────────────────

    def get_or_create(self, name: str) -> EventSchema:
        """
        Return the named schema, creating it if absent.
        Intended for manual/demo use — production routing goes via route().
        """
        if name not in self._schemas:
            self._register(EventSchema(name))
        return self._schemas[name]

    def get_by_id(self, schema_id: str) -> EventSchema | None:
        """Look up a schema by its UUID."""
        return self._by_id.get(schema_id)

    # ── Properties ────────────────────────────────────────────────────────────

    @property
    def schemas(self) -> list[EventSchema]:
        return list(self._schemas.values())

    @property
    def entropy(self) -> float:
        """Mean entropy across all schemas. H ∈ [0, 1]."""
        if not self._schemas:
            return 1.0
        return float(np.mean([s.entropy for s in self._schemas.values()]))

    @property
    def threshold(self) -> float:
        """Current dynamic routing threshold τ(H) = tau_max · H^alpha."""
        return self._threshold()

    # ── Private helpers ───────────────────────────────────────────────────────

    def _threshold(self) -> float:
        return self.tau_max * (self.entropy ** self.alpha)

    def _find_best_schema(self, event: Event) -> tuple[EventSchema, float]:
        """
        Linear scan: for each schema, compute the max similarity between
        the new event and any event already in that schema.
        Returns (best_schema, best_score).
        """
        best_schema: EventSchema | None = None
        best_score: float = -1.0

        for schema in self._schemas.values():
            if not schema.events:
                # Empty schema (manually created) — treat as score 0
                score = 0.0
            else:
                score = max(event.similarity(e) for e in schema.events)

            if score > best_score:
                best_score = score
                best_schema = schema

        return best_schema, best_score  # type: ignore[return-value]

    def _spawn_and_absorb(self, event: Event) -> EventSchema:
        """Create a new EventSchema with an auto-generated name and absorb event."""
        name   = f"schema_{uuid.uuid4().hex[:8]}"
        schema = EventSchema(name)
        self._register(schema)
        schema.absorb(event)
        return schema

    def _register(self, schema: EventSchema) -> None:
        self._schemas[schema.name]      = schema
        self._by_id[schema.schema_id]   = schema

    def __repr__(self) -> str:
        return (
            f"Neocortex(schemas={len(self._schemas)}, "
            f"H={self.entropy:.3f}, "
            f"τ={self.threshold:.3f})"
        )
