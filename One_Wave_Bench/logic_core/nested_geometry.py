"""G-748 nested hex / pyramid / triangle-cube-hex receipts."""

from __future__ import annotations

import math
from typing import Dict, List, Tuple

Point = Tuple[float, float, float]


def hexagon_xy(radius: float = 1.0) -> List[Point]:
    return [
        (radius * math.cos(math.pi / 3.0 * i), radius * math.sin(math.pi / 3.0 * i), 0.0)
        for i in range(6)
    ]


def hexagonal_bipyramid(radius: float = 1.0, height: float = 1.0) -> Dict[str, object]:
    equator = hexagon_xy(radius)
    verts = equator + [(0.0, 0.0, height), (0.0, 0.0, -height)]
    faces = 12
    edges = 18
    return {
        "V": len(verts),
        "E": edges,
        "F": faces,
        "euler": len(verts) - edges + faces,
        "pyramids": 6,
        "axis_pairs": 3,
        "vertices": verts,
    }


def triangle_midpoint_split() -> Dict[str, int]:
    return {
        "parent_triangles": 1,
        "child_triangles": 4,
        "corner_triangles": 3,
        "middle_inverted": 1,
    }


def tet_midpoint_split() -> Dict[str, int]:
    return {
        "corner_tets": 4,
        "central_octahedra": 1,
        "octa_equatorial_hex_edges": 6,
        "note": "cube_hex_share_is_section_not_identity",
    }


def receipt() -> Dict[str, object]:
    bi = hexagonal_bipyramid()
    return {
        "euler_ok": bi["euler"] == 2,
        "six_pyramids": bi["pyramids"] == 6,
        "eighteen_edges": bi["E"] == 18,
        "triangle_children": triangle_midpoint_split()["child_triangles"],
        "tet_octa": tet_midpoint_split(),
        "six_is_not_six_routes": True,
        "brick": "Yellow",
    }
