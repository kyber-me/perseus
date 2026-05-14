"""
Perseus — Episode

A holistic representation of a complete block of input text.

An Episode is composed of:
  - A sequence of constituent EventPoints (the segmented sintagmas).
  - A single EventPoint of type EPISODE, generated from the embedding
    of the full text block (not from any individual segment).

The episode point is NOT routed through the Neocortex schemas directly.
It is surfaced via passive resonance detection (see resonance_check).
"""

from __future__ import annotations

import time

import numpy as np

from perseus.neocortex.point import Point


class Episode:
    """
    Holistic memory unit for a complete block of input text.

    Attributes
    ----------
    points              : ordered list of constituent EventPoints (sintagmas).
    episode_point       : EventPoint of type EPISODE — full-text encoding.
    resonance_threshold : fraction of points that must resonate for recall (0–1).
    time_window_ticks   : max CA ticks between first and last resonance hit.
    created_at          : creation timestamp.
    """

    def __init__(
        self,
        points: list[Point],
        episode_seed: np.ndarray,
        episode_text: str = "",
        resonance_threshold: float = 0.35,
        time_window_ticks: int = 100,
    ) -> None:
        if not points:
            raise ValueError("An Episode must have at least one constituent EventPoint.")

        self.points = points
        self.episode_point = Point(
            text=episode_text,
            seed=episode_seed,
            embedding=np.zeros(1),  # placeholder — full-text embedding
        )
        self.resonance_threshold = resonance_threshold
        self.time_window_ticks   = time_window_ticks
        self.created_at          = time.time()

    # ── Read-only helpers ─────────────────────────────────────────────────────

    @property
    def size(self) -> int:
        """Number of constituent EventPoints."""
        return len(self.points)

    @property
    def quorum(self) -> int:
        """Minimum number of points that must resonate to surface this episode."""
        return max(1, round(self.size * self.resonance_threshold))

    def __repr__(self) -> str:
        return (
            f"Episode(size={self.size}, "
            f"quorum={self.quorum}/{self.size}, "
            f"threshold={self.resonance_threshold:.0%})"
        )
