#!/usr/bin/env python3
"""OCTAVE CASCADE

Lock strength from alignment amplitude, spin, and bath.
Not a correction sitting on top of a borrowed g0.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


@dataclass
class Cascade:
    kappa: float = 1.0
    omega: float = 0.0
    bath: float = 0.0  # 0 = room rest, hotter loosens

    def lock(self, align: float) -> float:
        spin = 1.0 + math.tanh(self.omega / 10.0)
        heat = 1.0 / (1.0 + self.bath)
        return self.kappa * (align ** 2) * spin * heat


def hexagon_split_normals() -> np.ndarray:
    angles = np.linspace(0, 2 * math.pi, 6, endpoint=False)
    xy = np.stack([np.cos(angles), np.sin(angles), np.zeros(6)], axis=1)
    z = np.array([0.0, 0.0, 1.0])
    walls = xy + 0.4 * z
    return walls / np.linalg.norm(walls, axis=1, keepdims=True)


def demo() -> None:
    print("GRAV LAB — octave cascade")
    quiet = Cascade(kappa=1.0, omega=0.0, bath=0.0)
    loud = Cascade(kappa=1.0, omega=7.0, bath=0.2)
    aligns = [0.0, 0.2, 0.5, 1.0, 1.4]
    print(f"{'align':>8}  {'lock_quiet':>12}  {'lock_spin+bath':>16}")
    for a in aligns:
        print(f"{a:8.2f}  {quiet.lock(a):12.6f}  {loud.lock(a):16.6f}")
    print()
    print("hexagon → six pyramid normals")
    for i, n in enumerate(hexagon_split_normals(), 1):
        print(f"  P{i}: {n}")


if __name__ == "__main__":
    demo()
