"""
Perseus — HippocampalAutomaton

Wraps a Brian's Brain Automaton with the memory catalogue
that belongs to a named Neocortex region.

Initial conditions use only FIRING (ON) and INACTIVE (OFF) states,
so the combinatorial space of possible seeds is 2^N (N = width × height).

occupancy = log(mapped + 1) / (N × log 2)   — how full is the catalogue (0→1)
entropy   = 1 - occupancy                    — true uncertainty of the system (1→0)

Low entropy  (mature system, many memories) → selective  (high retrieval threshold).
High entropy (new system, few memories)     → sensitive  (low retrieval threshold).
"""

from __future__ import annotations

import math
import numpy as np

from perseus.automaton.grid import Automaton, AutomatonState


class HippocampalAutomaton:
    """
    A single CA process bound to one Neocortex context region.

    Attributes:
        region    : name of the Neocortex region this automaton serves.
        automaton : the underlying Brian's Brain CA engine.
        mapped    : catalogue of initial grid seeds (one per registered syntagma).
        occupancy : log(mapped+1) / (N×log2) — catalogue fill ratio (0→1).
        entropy   : 1 - occupancy — system uncertainty (1→0).
    """

    def __init__(
        self,
        region: str,
        width: int = 16,
        height: int = 16,
        density: float = 0.20,
        seed: int | None = None,
    ) -> None:
        self.region   = region
        self._log_cap = (width * height) * math.log(2)   # log(2^N)
        self.automaton = Automaton(width, height, density, seed)
        self.mapped: list[np.ndarray] = []

    # ── Core API ──────────────────────────────────────────────────────────────

    @property
    def occupancy(self) -> float:
        """log(mapped+1) / log(2^N) — grows 0→1 as the catalogue fills."""
        return math.log(len(self.mapped) + 1) / self._log_cap

    @property
    def entropy(self) -> float:
        """1 - occupancy — system uncertainty, decreases as more is known."""
        return 1.0 - self.occupancy

    def step(self) -> AutomatonState:
        """Advance one tick. Does not record — use register() explicitly."""
        return self.automaton.step()

    def get_state(self) -> AutomatonState:
        return self.automaton.get_state()

    # ── Catalogue ─────────────────────────────────────────────────────────────

    def register(self, initial_grid: np.ndarray) -> None:
        """
        Register the initial grid configuration produced by encoding a syntagma.
        Seeds the automaton with that configuration and stores it in the catalogue.
        """
        self.automaton.grid[:] = initial_grid
        self.mapped.append(initial_grid.copy())

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
