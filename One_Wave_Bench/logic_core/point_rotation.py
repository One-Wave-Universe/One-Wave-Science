"""G-749 C2 Point rotation receipts."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Tuple

Vec3 = Tuple[float, float, float]


def hat(omega: Vec3):
    x, y, z = omega
    return ((0.0, -z, y), (z, 0.0, -x), (-y, x, 0.0))


def matmul(a, b):
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3))
        for i in range(3)
    )


def matvec(a, v: Vec3) -> Vec3:
    return tuple(sum(a[i][j] * v[j] for j in range(3)) for i in range(3))  # type: ignore


def rot_z(theta: float):
    c, s = math.cos(theta), math.sin(theta)
    return ((c, -s, 0.0), (s, c, 0.0), (0.0, 0.0, 1.0))


def identity():
    return ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0))


def det3(m) -> float:
    return (
        m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
        - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
        + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    )


@dataclass(frozen=True)
class PointAttitude:
    R: Tuple[Tuple[float, float, float], Tuple[float, float, float], Tuple[float, float, float]]
    omega_body: Vec3
    inertia_diag: Vec3 = (1.0, 1.0, 1.0)

    def L_body(self) -> Vec3:
        return (
            self.inertia_diag[0] * self.omega_body[0],
            self.inertia_diag[1] * self.omega_body[1],
            self.inertia_diag[2] * self.omega_body[2],
        )

    def L_ground(self) -> Vec3:
        return matvec(self.R, self.L_body())


def compose(parent: PointAttitude, child_in_parent: PointAttitude) -> PointAttitude:
    R = matmul(parent.R, child_in_parent.R)
    # transport child omega into parent body, then to the composed body = child body
    omega = child_in_parent.omega_body
    return PointAttitude(R=R, omega_body=omega, inertia_diag=child_in_parent.inertia_diag)


def receipt_planar_spin(theta: float, omega_z: float) -> dict:
    att = PointAttitude(R=rot_z(theta), omega_body=(0.0, 0.0, omega_z))
    return {
        "detR": det3(att.R),
        "L_body": att.L_body(),
        "L_ground": att.L_ground(),
        "path_circulation_stolen": False,
        "field_curl_stolen": False,
        "brick_algebra": "GREEN",
        "brick_inertia_origin": "YELLOW",
    }
