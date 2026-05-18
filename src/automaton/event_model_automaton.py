"""
Perseus — EventModelAutomaton

A single CA process bound to one Event Schema in the Neocortex.

Based on Event Segmentation Theory (EST), each EventModelAutomaton represents
a dynamic, active model of the current event being processed.

Operational Modes
-----------------
PASSIVE_REFLEXIVE : Default resting mode. The CA evolves freely at low
                    frequency, maintaining schema coherence without any
                    external input. The Neocortex passively observes for
                    resonance signals.

HIGH_RES_ACTIVE   : Triggered by an Event Boundary detected by the LLM.
                    The automaton samples at high frequency, "digesting"
                    the incoming seed to integrate it with existing memory.
                    After processing, it transitions back to PASSIVE_REFLEXIVE.
"""

from __future__ import annotations

import math
from enum import Enum, auto

import numpy as np

from automaton.grid import Automaton, AutomatonState


class EventModelMode(Enum):
    """Operational state of an EventModelAutomaton."""
    PASSIVE_REFLEXIVE = auto()   # resting, low-frequency, observing
    HIGH_RES_ACTIVE   = auto()   # triggered by event boundary, high-frequency


class EventModelAutomaton:
    """
    A single CA process bound to one Event Schema in the Neocortex.

    Attributes
    ----------
    schema       : name of the Event Schema (Neocortex region) this model serves.
    mode         : current operational mode (PASSIVE_REFLEXIVE or HIGH_RES_ACTIVE).
    automaton    : the underlying Brian's Brain CA engine.
    mapped       : catalogue of binary seeds (one per registered event boundary).
    occupancy    : log(mapped+1) / log(2^N) — catalogue fill ratio (0→1).
    entropy      : 1 - occupancy — system uncertainty (1→0).
    """

    def __init__(
        self,
        schema: str,
        width: int = 16,
        height: int = 16,
        density: float = 0.20,
        seed: int | None = None,
    ) -> None:
        self.schema    = schema
        self.mode      = EventModelMode.PASSIVE_REFLEXIVE
        self._log_cap  = (width * height) * math.log(2)   # log(2^N)
        self.automaton = Automaton(width, height, density, seed)
        self.mapped: list[np.ndarray] = []

    # ── Metrics ───────────────────────────────────────────────────────────────

    @property
    def occupancy(self) -> float:
        """log(mapped+1) / log(2^N) — grows 0→1 as the catalogue fills."""
        return math.log(len(self.mapped) + 1) / self._log_cap

    @property
    def entropy(self) -> float:
        """1 - occupancy — system uncertainty, decreases as the model learns."""
        return 1.0 - self.occupancy

    # ── Core API ──────────────────────────────────────────────────────────────

    def step(self) -> AutomatonState:
        """Advance one CA tick. Mode does not change here; caller controls it."""
        return self.automaton.step()

    def get_state(self) -> AutomatonState:
        return self.automaton.get_state()

    def activate(self, initial_grid: np.ndarray) -> None:
        """
        Transition to HIGH_RES_ACTIVE and seed the automaton with the
        grid produced by encoding an event boundary.

        This is the entry point for new information entering the system.
        """
        self.mode = EventModelMode.HIGH_RES_ACTIVE
        self.automaton.grid[:] = initial_grid
        self.mapped.append(initial_grid.copy())

    def rest(self) -> None:
        """Transition back to PASSIVE_REFLEXIVE (resting) mode."""
        self.mode = EventModelMode.PASSIVE_REFLEXIVE

    # ── Resonance ─────────────────────────────────────────────────────────────

    def nearest_resonance(self, grid: np.ndarray) -> tuple[float, np.ndarray] | None:
        """
        Return (error, seed) for the mapped seed closest to `grid`,
        or None if the catalogue is empty.
        Error is normalised Hamming distance (0 = identical, 1 = fully different).
        """
        if not self.mapped:
            return None
        total  = grid.size
        errors = [np.sum(grid != m) / total for m in self.mapped]
        idx    = int(np.argmin(errors))
        return errors[idx], self.mapped[idx]
