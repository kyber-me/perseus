"""
Perseus — SparseEncoder

Dual-purpose encoder derived from BeeBrain's HippocampalEncoder.
Projects a dense embedding into two representations:

  1. encode_seed()       → sparse binary grid (N×N)  for the EventModelAutomaton
  2. encode_neocortex()  → 2D coordinate              for EventSchema positioning

Both projections share the same fixed Gaussian random matrix (fixed seed),
making the mapping fully deterministic: same embedding → same outputs.
"""

from __future__ import annotations

import numpy as np


class SparseEncoder:
    """
    Projects a dense embedding into sparse representations via
    Gaussian Random Projection + Softmax Temperature Sampling.

    Args
    ----
    input_dim   : Dimensionality of the input embedding (e.g. 384, 768).
    grid_size   : Side length of the automaton grid (16 → 16×16 cells).
    density     : Fraction of cells activated in the seed (default 0.05).
    temperature : Softmax temperature — lower = more deterministic.
    seed        : RNG seed for the projection matrix (fixed → deterministic).
    """

    def __init__(
        self,
        input_dim: int,
        grid_shape: int | tuple[int, ...] = (16, 16),
        density: float = 0.05,
        temperature: float = 1.0,
        seed: int = 42,
    ) -> None:
        self.input_dim   = input_dim
        self.density     = density
        self.temperature = temperature
        self.seed        = seed

        self.grid_shape: tuple[int, ...]
        if isinstance(grid_shape, int):
            self.grid_shape = (grid_shape, grid_shape)
        else:
            self.grid_shape = grid_shape

        self._N   = int(np.prod(self.grid_shape))  # total cells in automaton/memory grid
        self._k   = max(1, int(self._N * density)) # active cells per projection
        self._rng = np.random.default_rng(seed + 1)

        # Fixed Gaussian projection matrix: (input_dim, N)  ~ N(0, 1/D)
        rng_proj = np.random.default_rng(seed)
        self._M  = (
            rng_proj.standard_normal((input_dim, self._N)).astype(np.float32)
            / np.sqrt(input_dim)
        )

        # Separate 2D projection matrix for Neocortex positioning: (input_dim, 2)
        rng_nc   = np.random.default_rng(seed + 2)
        self._M2 = (
            rng_nc.standard_normal((input_dim, 2)).astype(np.float32)
            / np.sqrt(input_dim)
        )

    # ── Public API ────────────────────────────────────────────────────────────

    def encode_seed(self, embedding: np.ndarray) -> np.ndarray:
        """
        Project embedding → sparse binary grid (grid_size × grid_size).
        Activates k cells determined by softmax-weighted sampling.

        Returns
        -------
        grid : uint8 ndarray of shape (grid_size, grid_size)
                1 = active (FIRING), 0 = inactive.
        """
        v      = self._normalize(embedding)
        scores = v @ self._M                         # (N,)
        probs  = self._softmax(scores)

        flat_idx = self._rng.choice(
            self._N, size=self._k, replace=False, p=probs.astype(np.float64)
        )

        grid = np.zeros(self._N, dtype=np.uint8)
        grid[flat_idx] = 1
        return grid.reshape(self.grid_shape)

    def encode_neocortex(self, embedding: np.ndarray) -> np.ndarray:
        """
        Project embedding → 2D coordinate in Neocortex space.

        Returns
        -------
        point : float32 ndarray of shape (2,)  — (x, y) in [-1, 1]².
        """
        v = self._normalize(embedding)
        return np.tanh(v @ self._M2).astype(np.float32)   # (2,)

    # ── Private helpers ───────────────────────────────────────────────────────

    def _normalize(self, v: np.ndarray) -> np.ndarray:
        v = np.asarray(v, dtype=np.float32).ravel()
        if v.shape[0] != self.input_dim:
            raise ValueError(
                f"Expected embedding of length {self.input_dim}, got {v.shape[0]}"
            )
        norm = float(np.linalg.norm(v))
        return v / norm if norm > 0.0 else v

    def _softmax(self, x: np.ndarray) -> np.ndarray:
        scaled = x / self.temperature
        scaled -= scaled.max()
        exp_x  = np.exp(scaled)
        return exp_x / exp_x.sum()
