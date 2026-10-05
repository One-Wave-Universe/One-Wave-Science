#!/usr/bin/env python3
"""OW1F geometry: stacked-hex (8-NN) and FCC-12.

D-408 basis. Integers (m,n,p). XYZ derived.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

SQRT3_2 = math.sqrt(3.0) / 2.0
INPLANE = (
    (1, 0, 0),
    (-1, 0, 0),
    (0, 1, 0),
    (0, -1, 0),
    (1, -1, 0),
    (-1, 1, 0),
)
STACKED_VERT = ((0, 0, 1), (0, 0, -1))


def embed(m: int, n: int, p: int, a: float, h: float) -> np.ndarray:
    return np.array(
        [a * (m + 0.5 * n), a * (n * SQRT3_2), p * h],
        dtype=np.float64,
    )


@dataclass
class Lattice:
    Nm: int
    Nn: int
    Np: int
    a: float = 1.0
    h: float = 1.0
    pack: int = 0  # 0 stacked-hex, 1 fcc-12
    m4_pair: int = 0

    def in_bounds(self, m: int, n: int, p: int) -> bool:
        return 0 <= m < self.Nm and 0 <= n < self.Nn and 0 <= p < self.Np

    def id_of(self, m: int, n: int, p: int) -> int:
        return m + self.Nm * (n + self.Nn * p)

    def coords_of(self, i: int) -> tuple[int, int, int]:
        m = i % self.Nm
        t = i // self.Nm
        n = t % self.Nn
        p = t // self.Nn
        return m, n, p

    def xyz(self, m: int, n: int, p: int) -> np.ndarray:
        return embed(m, n, p, self.a, self.h)

    def neighbors(self, m: int, n: int, p: int) -> list[tuple[int, int, int]]:
        out: list[tuple[int, int, int]] = []
        for dm, dn, dp in INPLANE:
            mm, nn, pp = m + dm, n + dn, p + dp
            if self.in_bounds(mm, nn, pp):
                out.append((mm, nn, pp))
        if self.pack == 0:
            for dm, dn, dp in STACKED_VERT:
                mm, nn, pp = m + dm, n + dn, p + dp
                if self.in_bounds(mm, nn, pp):
                    out.append((mm, nn, pp))
            return out
        # fcc-12: keep in-plane six, add any site at distance ~ a
        here = self.xyz(m, n, p)
        seen = set(out)
        for pp in range(self.Np):
            for nn in range(self.Nn):
                for mm in range(self.Nm):
                    if (mm, nn, pp) == (m, n, p) or (mm, nn, pp) in seen:
                        continue
                    d = np.linalg.norm(self.xyz(mm, nn, pp) - here)
                    if abs(d - self.a) <= 0.02 * self.a:
                        out.append((mm, nn, pp))
                        seen.add((mm, nn, pp))
        return out

    def cluster7(self, m: int, n: int, p: int) -> list[tuple[int, int, int]]:
        ring = [(m + dm, n + dn, p) for dm, dn, _ in INPLANE]
        return [(m, n, p)] + [c for c in ring if self.in_bounds(*c)]

    def midline_axes(self) -> list[tuple[int, int]]:
        # pyramid index pairs
        pairs = ((0, 3), (1, 4), (2, 5))
        return [pairs[self.m4_pair]]


def hex_vertices(a: float = 1.0) -> np.ndarray:
    ang = np.linspace(0, 2 * math.pi, 6, endpoint=False)
    return np.stack([a * np.cos(ang), a * np.sin(ang), np.zeros(6)], axis=1)


def demo() -> None:
    print("OW1F both packs")
    for pack, name in ((0, "stacked-hex"), (1, "fcc-12")):
        lat = Lattice(5, 5, 3, a=1.0, h=math.sqrt(2.0 / 3.0) if pack else 1.0, pack=pack)
        c = (2, 2, 1)
        nb = lat.neighbors(*c)
        print(f"  {name} center={c} n_neighbors={len(nb)} cluster7={len(lat.cluster7(*c))}")
        print(f"    xyz={lat.xyz(*c)}")
    print("hex verts r=1")
    for i, v in enumerate(hex_vertices(), 0):
        print(f"  V{i} {np.round(v, 6)}")


if __name__ == "__main__":
    demo()
