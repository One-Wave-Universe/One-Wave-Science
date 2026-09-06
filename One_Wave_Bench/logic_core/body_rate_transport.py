"""G-750 body-rate transport."""

from __future__ import annotations

import math
from typing import Tuple

Vec3 = Tuple[float, float, float]
Mat3 = Tuple[Vec3, Vec3, Vec3]


def transpose(R: Mat3) -> Mat3:
    return tuple(tuple(R[j][i] for j in range(3)) for i in range(3))  # type: ignore


def matvec(R: Mat3, v: Vec3) -> Vec3:
    return tuple(sum(R[i][j] * v[j] for j in range(3)) for i in range(3))  # type: ignore


def add(a: Vec3, b: Vec3) -> Vec3:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def rot_z(theta: float) -> Mat3:
    c, s = math.cos(theta), math.sin(theta)
    return ((c, -s, 0.0), (s, c, 0.0), (0.0, 0.0, 1.0))


def rot_x(theta: float) -> Mat3:
    c, s = math.cos(theta), math.sin(theta)
    return ((1.0, 0.0, 0.0), (0.0, c, -s), (0.0, s, c))


def compose_omega_body(omega_parent_body: Vec3, omega_child_body: Vec3, R_child_in_parent: Mat3) -> Vec3:
    """Child-body chart: omega_c + R_c^T omega_p."""
    return add(omega_child_body, matvec(transpose(R_child_in_parent), omega_parent_body))


def compose_omega_ground(omega_parent_body: Vec3, omega_child_body: Vec3, R_parent: Mat3, R_child_in_parent: Mat3) -> Vec3:
    """Ground chart: R_p omega_p + R_p R_c omega_c."""
    R_child_ground = (
        tuple(sum(R_parent[i][k] * R_child_in_parent[k][j] for k in range(3)) for j in range(3))
        for i in range(3)
    )
    R_g = tuple(R_child_ground)  # type: ignore
    return add(matvec(R_parent, omega_parent_body), matvec(R_g, omega_child_body))
