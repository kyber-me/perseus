"""
Perseus — Event

A directed sequence of Points representing a single segmented event
(as identified by Event Segmentation Theory via the LLM).

An Event is the unit that:
  - Gets routed to an EventSchema in the Neocortex.
  - Seeds the EventModelAutomaton (via its sparse seed).
  - Defines semantic trajectory (direction + magnitude) for schema comparison.

Events are NOT individual sintagmas — they are composed of Points.
The automaton is fed by the Event's seed, not by any individual Point's seed.
"""

from __future__ import annotations

import time

import numpy as np

from perseus.neocortex.point import Point


# ── DTW helpers (module-level, used by Event.similarity) ─────────────────────

def _cosine_distance(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine distance ∈ [0, 2].  0 = identical direction, 2 = opposite."""
    na = float(np.linalg.norm(a))
    nb = float(np.linalg.norm(b))
    if na < 1e-8 or nb < 1e-8:
        return 1.0
    return 1.0 - float(np.dot(a, b)) / (na * nb)


def _dtw_distance(seq1: list[np.ndarray], seq2: list[np.ndarray]) -> float:
    """
    Dynamic Time Warping over two sequences of embedding vectors.

    Builds an (n+1) x (m+1) cost matrix and finds the minimum-cost
    warping path using three allowed moves: diagonal, down, right.
    Local cost = cosine distance between the two vectors at each cell.

    Returns the total accumulated cost of the optimal path.
    """
    n, m = len(seq1), len(seq2)
    dp = np.full((n + 1, m + 1), np.inf, dtype=np.float64)
    dp[0, 0] = 0.0

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = _cosine_distance(seq1[i - 1], seq2[j - 1])
            dp[i, j] = cost + min(dp[i-1, j], dp[i, j-1], dp[i-1, j-1])

    return float(dp[n, m])


def _dtw_similarity(seq1: list[np.ndarray], seq2: list[np.ndarray]) -> float:
    """
    Convert DTW distance to similarity in [0, 1].

    Normalises by the average sequence length so scores are comparable
    across events with different numbers of Points.
    Formula:  1 / (1 + dtw / avg_len)
    """
    avg_len = (len(seq1) + len(seq2)) / 2.0
    dist = _dtw_distance(seq1, seq2)
    return 1.0 / (1.0 + dist / avg_len)


class Event:
    """
    A directed sequence of Points — one segmented event from EST.

    Attributes
    ----------
    points              : ordered list of constituent Points (sintagmas).
    embedding           : dense embedding vector of the full event text.
    seed                : 16×16 binary grid (sparse projection of embedding)
                          — this is what the EventModelAutomaton receives.
    direction           : normalized vector (last_point.embedding - first_point.embedding).
                          Represents the semantic trajectory of the event.
    magnitude           : ||last_point.embedding - first_point.embedding||.
                          How far the event travels in semantic space.
    neocortex_position  : 2D coordinates in the Neocortex space (from SparseEncoder).
    schema_name         : assigned EventSchema name (None until routed).
    created_at          : creation timestamp.
    """

    def __init__(
        self,
        points: list[Point],
        embedding: np.ndarray,
        seed: np.ndarray,
        neocortex_position: np.ndarray | None = None,
        schema_name: str | None = None,
        resonance_threshold: float = 0.35,
        time_window_ticks: int = 100,
    ) -> None:
        if not points:
            raise ValueError("An Event must have at least one constituent Point.")

        self.points             = points
        self.embedding          = np.asarray(embedding, dtype=np.float32).copy()
        self.seed               = np.asarray(seed, dtype=np.uint8).copy()
        self.neocortex_position = (
            np.asarray(neocortex_position, dtype=np.float32).copy()
            if neocortex_position is not None else None
        )
        self.schema_id: str | None   = None   # set by EventSchema.absorb()
        self.schema_name: str | None = schema_name
        self.resonance_threshold     = resonance_threshold
        self.time_window_ticks       = time_window_ticks
        self.created_at = time.time()

        # Compute semantic trajectory from Point embeddings
        self.direction, self.magnitude = self._compute_trajectory()

    # ── Trajectory ────────────────────────────────────────────────────────────

    def _compute_trajectory(self) -> tuple[np.ndarray, float]:
        """
        Compute the direction vector and magnitude from the first
        to the last Point's embedding.

        For a single-point event, direction is a zero vector and magnitude is 0.
        """
        if len(self.points) == 1:
            dim = self.points[0].embedding.shape[0]
            return np.zeros(dim, dtype=np.float32), 0.0

        start = self.points[0].embedding.astype(np.float32)
        end   = self.points[-1].embedding.astype(np.float32)
        delta = end - start

        magnitude = float(np.linalg.norm(delta))
        direction = (delta / magnitude) if magnitude > 0.0 else np.zeros_like(delta)

        return direction, magnitude

    # ── Comparison ────────────────────────────────────────────────────────────

    def similarity(self, other: Event, alpha: float = 0.5) -> float:
        """
        Compute similarity between two Events.

        Combines:
          - Directional similarity (cosine of trajectory vectors).
          - Proximity (negative cosine distance between embeddings).

        Args
        ----
        other : another Event to compare against.
        alpha : weight for directional similarity (1-alpha for proximity).

        Returns
        -------
        similarity score in [0, 1], higher = more similar.
        """
        # Directional component
        if self.magnitude > 0.0 and other.magnitude > 0.0:
            dir_sim = float(np.dot(self.direction, other.direction))
            dir_sim = (dir_sim + 1.0) / 2.0   # normalize from [-1,1] to [0,1]
        else:
            dir_sim = 0.0

        # Proximity component (cosine similarity between holistic embeddings)
        e1 = self.embedding / (np.linalg.norm(self.embedding) + 1e-8)
        e2 = other.embedding / (np.linalg.norm(other.embedding) + 1e-8)
        prox_sim = float(np.dot(e1, e2))
        prox_sim = (prox_sim + 1.0) / 2.0     # normalize from [-1,1] to [0,1]

        return alpha * dir_sim + (1.0 - alpha) * prox_sim

    def similarity(self, other: Event) -> float:
        """
        Default similarity between two Events — uses DTW over the full
        sequence of Point embeddings.

        DTW (Dynamic Time Warping) aligns the two trajectories and computes
        the minimum cumulative cosine distance along the optimal warping path.
        This captures deviations in intermediate Points, not just start/end.

        Normalised to [0, 1]:  1.0 = identical path,  0.0 = maximally distant.

        Use similarity_direction() for a faster O(1) alternative when only the
        overall displacement vector matters (e.g. quick pre-filtering).
        """
        seq1 = [p.embedding for p in self.points]
        seq2 = [p.embedding for p in other.points]
        return _dtw_similarity(seq1, seq2)

    def similarity_direction(self, other: Event, alpha: float = 0.5) -> float:
        """
        Fast O(1) similarity combining:
          - Directional similarity: cosine of the start→end trajectory vectors.
          - Proximity: cosine similarity between holistic event embeddings.

        Weights:
          alpha     → directional component
          (1-alpha) → proximity component

        Limitation: ignores intermediate Points — two events with the same
        start/end but different midpoints score equally (see similarity()).
        """
        # Directional component
        if self.magnitude > 0.0 and other.magnitude > 0.0:
            dir_sim = float(np.dot(self.direction, other.direction))
            dir_sim = (dir_sim + 1.0) / 2.0
        else:
            dir_sim = 0.0

        # Proximity component
        e1 = self.embedding / (np.linalg.norm(self.embedding) + 1e-8)
        e2 = other.embedding / (np.linalg.norm(other.embedding) + 1e-8)
        prox_sim = float(np.dot(e1, e2))
        prox_sim = (prox_sim + 1.0) / 2.0

        return alpha * dir_sim + (1.0 - alpha) * prox_sim

    # ── Properties ────────────────────────────────────────────────────────────

    @property
    def size(self) -> int:
        """Number of constituent Points."""
        return len(self.points)

    @property
    def quorum(self) -> int:
        """
        Minimum number of constituent Points that must resonate
        in PASSIVE_REFLEXIVE mode to surface this event as a memory.
        """
        return max(1, round(self.size * self.resonance_threshold))

    @property
    def is_routed(self) -> bool:
        """True if this event has been assigned to a schema."""
        return self.schema_id is not None

    def __repr__(self) -> str:
        return (
            f"Event(size={self.size}, "
            f"magnitude={self.magnitude:.3f}, "
            f"schema={self.schema_name!r})"
        )
