"""Experimental associative-memory helper for symbolic melody cells.

This module is intentionally small and dependency-light. It does not implement
CELL_V1 physics and must not be treated as evidence for the One-Wave model.
"""

from __future__ import annotations

from typing import Iterable, Sequence


def bipolar(values: Iterable[float]) -> list[int]:
    """Map numeric inputs to {-1, +1}; zero resolves to +1 deterministically."""
    return [1 if float(v) >= 0.0 else -1 for v in values]


def train(patterns: Sequence[Sequence[int]]) -> list[list[float]]:
    """Hebbian Hopfield weight matrix with zero diagonal."""
    if not patterns:
        raise ValueError("at least one pattern is required")
    n = len(patterns[0])
    if n == 0 or any(len(p) != n for p in patterns):
        raise ValueError("all patterns must have the same non-zero length")

    pats = [bipolar(p) for p in patterns]
    weights = [[0.0 for _ in range(n)] for _ in range(n)]
    scale = float(n)
    for p in pats:
        for i in range(n):
            for j in range(n):
                if i != j:
                    weights[i][j] += (p[i] * p[j]) / scale
    return weights


def recall(
    state: Sequence[int],
    weights: Sequence[Sequence[float]],
    max_sweeps: int = 16,
) -> list[int]:
    """Deterministic asynchronous recall until stable or max_sweeps reached."""
    x = bipolar(state)
    n = len(x)
    if len(weights) != n or any(len(row) != n for row in weights):
        raise ValueError("weight matrix shape must match state length")

    for _ in range(max_sweeps):
        changed = False
        for i in range(n):
            field = sum(float(weights[i][j]) * x[j] for j in range(n))
            new_value = 1 if field >= 0.0 else -1
            if new_value != x[i]:
                x[i] = new_value
                changed = True
        if not changed:
            break
    return x


def energy(state: Sequence[int], weights: Sequence[Sequence[float]]) -> float:
    """Return standard Hopfield energy for inspection/debugging."""
    x = bipolar(state)
    n = len(x)
    if len(weights) != n or any(len(row) != n for row in weights):
        raise ValueError("weight matrix shape must match state length")
    return -0.5 * sum(
        float(weights[i][j]) * x[i] * x[j]
        for i in range(n)
        for j in range(n)
    )
