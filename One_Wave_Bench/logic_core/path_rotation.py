"""G-769 C3 Path rotation. Kinematics of the ride. Not the point."""

from __future__ import annotations

import math
from typing import Sequence, Tuple

Vec3 = Tuple[float, float, float]


def sub(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dot(a: Vec3, b: Vec3) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def norm(a: Vec3) -> float:
    return math.sqrt(dot(a, a))


def unit(a: Vec3) -> Vec3:
    n = norm(a)
    if n == 0.0:
        raise ValueError("zero edge")
    return (a[0] / n, a[1] / n, a[2] / n)


def turning_angle(a: Vec3, b: Vec3, c: Vec3) -> float:
    """Angle between the incoming edge and the outgoing edge, in radians."""
    t0 = unit(sub(b, a))
    t1 = unit(sub(c, b))
    cth = max(-1.0, min(1.0, dot(t0, t1)))
    return math.acos(cth)


def path_receipt(points: Sequence[Vec3], closed: bool = False) -> dict:
    pts = list(points)
    if len(pts) < 3:
        raise ValueError("a path turn needs three centers")
    seq = pts + [pts[0], pts[1]] if closed else pts
    turns = [turning_angle(seq[i - 1], seq[i], seq[i + 1]) for i in range(1, len(seq) - 1)]
    lengths = [norm(sub(seq[i], seq[i - 1])) for i in range(1, len(seq) - 1)]
    mean_len = sum(lengths) / len(lengths)
    return {
        "turning": sum(turns),
        "n_corners": len(turns),
        "mean_edge": mean_len,
        "curvature": (sum(turns) / len(turns)) / mean_len,
        "L": None,
        "magnetic_gradient_applied": False,
        "gravity_coefficient_on_point": 0.0,
    }


def regular_hex(side: float = 1.0):
    return tuple(
        (side * math.cos(k * math.pi / 3.0), side * math.sin(k * math.pi / 3.0), 0.0)
        for k in range(6)
    )
