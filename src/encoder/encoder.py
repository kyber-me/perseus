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
    Gaussian Random Projection + Deterministic Top-K Selection.

    Args
    ----
    input_dim   : Dimensionality of the input embedding (e.g. 384, 768).
    grid_size   : Side length of the automaton grid (16 → 16×16 cells).
    density     : Fraction of cells activated in the seed (default 0.05).
    seed        : RNG seed for the projection matrix (fixed → deterministic).
    """

    def __init__(
        self,
        input_dim: int,
        grid_shape: int | tuple[int, ...] = (16, 16),
        density: float = 0.05,
        seed: int = 42,
    ) -> None:
        self.input_dim   = input_dim
        self.density     = density
        self.seed        = seed

        self.grid_shape: tuple[int, ...]
        if isinstance(grid_shape, int):
            self.grid_shape = (grid_shape, grid_shape)
        else:
            self.grid_shape = grid_shape

        self._N   = int(np.prod(self.grid_shape))  # total cells in automaton/memory grid
        self._k   = max(1, int(self._N * density)) # active cells per projection
        self._rng = np.random.default_rng(seed + 1)

        # Fixed Orthogonal Projection Matrix: (input_dim, N)
        # Prevents "blind spots" by forcing projection axes to be as independent as possible.
        rng_proj = np.random.default_rng(seed)
        M  = rng_proj.standard_normal((input_dim, self._N)).astype(np.float32)
        if self._N <= input_dim:
            # Undercompleted/Perfectly completed space: columns are strictly orthonormal.
            Q, _ = np.linalg.qr(M)
            self._M = Q
        else:
            # Overcompleted space: orthonormalize rows to spread projection axes uniformly.
            Q, _ = np.linalg.qr(M.T)
            self._M = Q.T

        # Separate 2D Orthogonal projection matrix for Neocortex positioning: (input_dim, 2)
        rng_nc   = np.random.default_rng(seed + 2)
        M2 = rng_nc.standard_normal((input_dim, 2)).astype(np.float32)
        Q2, _ = np.linalg.qr(M2)
        self._M2 = Q2

    # ── Public API ────────────────────────────────────────────────────────────

    def encode_seed(self, embedding: np.ndarray) -> np.ndarray:
        """
        Project embedding → sparse binary grid (grid_size × grid_size).
        Uses deterministic Top-K selection (k-Winner-Takes-All) to guarantee 
        same embedding → same outputs.

        Returns
        -------
        grid : uint8 ndarray of shape (grid_size, grid_size)
                1 = active (FIRING), 0 = inactive.
        """
        v      = self._normalize(embedding)
        scores = v @ self._M                         # (N,)
        
        # Deterministic Top-K (K-Winner-Takes-All)
        # Garantia absoluta: mesmo embedding -> exata mesma grade
        flat_idx = np.argsort(scores)[-self._k:]

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

