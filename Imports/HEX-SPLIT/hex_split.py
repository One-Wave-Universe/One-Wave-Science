#!/usr/bin/env python3
"""Hexagon → six triangles → six pyramids.

Coordinates in a plane of radius 1. Apex height is a free knob (default 1).
Two modes:
  shared  — one apex above the hex center (one mountain, six faces)
  tents   — each triangle gets its own apex above its centroid
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


def hex_vertices(radius: float = 1.0) -> np.ndarray:
    angles = np.linspace(0, 2 * math.pi, 6, endpoint=False)
    return np.stack([radius * np.cos(angles), radius * np.sin(angles), np.zeros(6)], axis=1)


def triangles_from_hex(verts: np.ndarray) -> list[np.ndarray]:
    center = verts.mean(axis=0)
    tris = []
    for i in range(6):
        tris.append(np.stack([center, verts[i], verts[(i + 1) % 6]]))
    return tris


def pyramid_shared(tris: list[np.ndarray], height: float = 1.0) -> list[np.ndarray]:
    apex = np.array([0.0, 0.0, height])
    out = []
    for tri in tris:
        # replace center (tri[0]) role: faces are apex + outer edge
        out.append(np.stack([apex, tri[1], tri[2]]))
    return out


def pyramid_tents(tris: list[np.ndarray], height: float = 1.0) -> list[np.ndarray]:
    out = []
    for tri in tris:
        c = tri.mean(axis=0) + np.array([0.0, 0.0, height])
        out.append(np.stack([c, tri[0], tri[1], tri[2]]))
    return out


def face_normal(face: np.ndarray) -> np.ndarray:
    n = np.cross(face[1] - face[0], face[2] - face[0])
    norm = np.linalg.norm(n)
    return n / norm if norm else n


def area(face: np.ndarray) -> float:
    return 0.5 * np.linalg.norm(np.cross(face[1] - face[0], face[2] - face[0]))


@dataclass
class SplitReceipt:
    mode: str
    height: float
    n_faces: int
    total_area: float
    normals: list[list[float]]


def run(mode: str = "shared", height: float = 1.0) -> SplitReceipt:
    verts = hex_vertices()
    tris = triangles_from_hex(verts)
    faces = pyramid_shared(tris, height) if mode == "shared" else pyramid_tents(tris, height)
    # tents include the original triangle as a base; report only the three walls for normals
    if mode == "tents":
        walls = []
        for pyr in faces:
            apex, a, b, c = pyr
            walls.extend([np.stack([apex, a, b]), np.stack([apex, b, c]), np.stack([apex, c, a])])
        faces_for_n = walls
    else:
        faces_for_n = faces
    normals = [face_normal(f).tolist() for f in faces_for_n]
    total = float(sum(area(f) for f in faces_for_n))
    return SplitReceipt(mode=mode, height=height, n_faces=len(faces_for_n), total_area=total, normals=normals)


def main() -> None:
    print("HEX-SPLIT receipts")
    for mode in ("shared", "tents"):
        r = run(mode=mode, height=1.0)
        print(f"\nmode={r.mode} height={r.height} faces={r.n_faces} area={r.total_area:.6f}")
        for i, n in enumerate(r.normals, 1):
            print(f"  n{i:02d} {[round(x, 6) for x in n]}")
    print("\nhex vertices (r=1)")
    for i, v in enumerate(hex_vertices(), 1):
        print(f"  V{i} {v}")


if __name__ == "__main__":
    main()
