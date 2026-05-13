"""
Perseus — Neocortex

The top-level orchestrator that manages a registry of EventSchemas.

Current Capability (KISS):
  Routes events to schemas by name. The caller decides which schema is
  relevant. Semantic distance routing (via embeddings) is deferred until
  the encoder pipeline is available.

Future Capability:
  - Embedding-based routing: compare incoming event to schema centroids.
  - Automatic spawn: create a new EventSchema when distance > threshold τ.
"""

from __future__ import annotations

from perseus.neocortex.event_schema import EventSchema


class Neocortex:
    """
    Registry and lifecycle manager for EventSchemas.

    Attributes
    ----------
    schemas : dict of {name → EventSchema}
    """

    def __init__(self) -> None:
        self._schemas: dict[str, EventSchema] = {}

    def get_or_create(self, name: str) -> EventSchema:
        """
        Return the EventSchema with this name, creating it if absent.
        This is the primary entry point for routing events.
        """
        if name not in self._schemas:
            self._schemas[name] = EventSchema(name)
        return self._schemas[name]

    @property
    def schemas(self) -> list[EventSchema]:
        return list(self._schemas.values())

    def __repr__(self) -> str:
        names = list(self._schemas.keys())
        return f"Neocortex(schemas={names})"
