"""
Perseus — Brian's Brain Cellular Automaton Engine

3-state CA grid:
  OFF   (0): resting neuron
  ON    (1): firing neuron  → transitions to DYING
  DYING (2): refractory     → transitions to OFF
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass
class AutomatonState:
    """Per-tick metrics extracted from the CA grid state."""
    generation: int
    activation: float    # Fraction of ON cells (0–1)
    refractory: float    # Fraction of DYING cells (0–1)
    momentum: float      # Δactivation vs previous tick (−1 to 1)
    cost: float          # Transition cost this tick (0–1, normalised by grid size)


class Automaton:
    """
    Brian's Brain CA — 16×16 toroidal grid.

    Designed as the core processing unit of Perseus:
    each Automaton is owned by a single context region
    in the Neocortex.
    """

    OFF   = 0
    ON    = 1
    DYING = 2

    def __init__(
        self,
        width: int = 16,
        height: int = 16,
        density: float = 0.20,
        seed: int | None = None,
    ) -> None:
        self.width  = width
        self.height = height
        self.rng    = np.random.default_rng(seed)

        self.grid: np.ndarray = np.zeros((height, width), dtype=np.uint8)
        self._previous_activation: float = 0.0
        self._generation: int = 0

        self._seed_random(density)

    # ── Initialisation ────────────────────────────────────────────────────────

    def _seed_random(self, density: float) -> None:
        """Seed grid with random ON cells at the given density."""
        total = self.width * self.height
        n_on  = int(total * density)
        indices = self.rng.choice(total, n_on, replace=False)
        self.grid.flat[indices] = self.ON

    def seed_from_coords(self, coords: list[tuple[int, int]]) -> None:
        """Inject a sparse pattern (list of (x, y) positions) as the initial state."""
        self.grid[:] = self.OFF
        for x, y in coords:
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y, x] = self.ON

    # ── CA Step ───────────────────────────────────────────────────────────────

    def step(self) -> AutomatonState:
        """Evolve one generation and return the resulting AutomatonState."""
        prev_grid = self.grid.copy()
        new_grid  = np.zeros_like(self.grid)

        # Count ON neighbours (Moore, toroidal wrapping)
        on_mask = (self.grid == self.ON).astype(np.uint8)
        on_neighbours = np.zeros_like(self.grid, dtype=np.uint8)
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dy == 0 and dx == 0:
                    continue
                on_neighbours += np.roll(np.roll(on_mask, dy, axis=0), dx, axis=1)

        # Rules
        new_grid[self.grid == self.ON]                               = self.DYING
        new_grid[self.grid == self.DYING]                            = self.OFF
        new_grid[(self.grid == self.OFF) & (on_neighbours == 2)]    = self.ON

        self.grid = new_grid
        self._generation += 1

        return self._compute_state(prev_grid)

    # ── State / Metrics ───────────────────────────────────────────────────────

    def _compute_state(self, prev_grid: np.ndarray) -> AutomatonState:
        total = self.width * self.height

        on_count    = int(np.sum(self.grid == self.ON))
        dying_count = int(np.sum(self.grid == self.DYING))

        activation = on_count / total
        refractory = dying_count / total

        # Momentum: Δactivation
        momentum = activation - self._previous_activation
        self._previous_activation = activation

        # Cost: cells that changed state, normalised
        changed = int(np.sum(prev_grid != self.grid))
        cost    = changed / total

        return AutomatonState(
            generation = self._generation,
            activation = activation,
            refractory = refractory,
            momentum   = momentum,
            cost       = cost,
        )

    def get_state(self) -> AutomatonState:
        """Return metrics for the current grid without stepping."""
        return self._compute_state(self.grid.copy())

    def reset(self, density: float = 0.20, seed: int | None = None) -> None:
        """Re-initialise the grid."""
        if seed is not None:
            self.rng = np.random.default_rng(seed)
        self.grid[:] = self.OFF
        self._previous_activation = 0.0
        self._generation = 0
        self._seed_random(density)

    def toggle_cell(self, x: int, y: int) -> None:
        """Flip a cell between OFF and ON (for interactive use)."""
        if self.grid[y, x] == self.OFF:
            self.grid[y, x] = self.ON
        else:
            self.grid[y, x] = self.OFF

    # ── Internals ─────────────────────────────────────────────────────────────

    def _flood_fill(self, mask, visited, i, j) -> int:
        """BFS flood-fill — kept for future use (e.g. cluster-based features)."""
        stack, size = [(i, j)], 0
        while stack:
            y, x = stack.pop()
            if y < 0 or y >= self.height or x < 0 or x >= self.width:
                continue
            if visited[y, x] or not mask[y, x]:
                continue
            visited[y, x] = True
            size += 1
            stack.extend([(y-1, x), (y+1, x), (y, x-1), (y, x+1)])
        return size
