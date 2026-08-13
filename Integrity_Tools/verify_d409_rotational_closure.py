#!/usr/bin/env python3
"""Verify the discrete rotational symmetry group of D-409's twelve-neighbor
shell (RELATIONAL_MECHANICS_NODE_BACKLOG.md, D-417 Evidence Dossier).

D-409 defines N_12 = (a/sqrt2) * {(+-1,+-1,0), (+-1,0,+-1), (0,+-1,+-1)}.
This script checks, by direct numerical construction (not by citing a
textbook result), which rotations map this exact 12-point set onto itself,
what the closure order of the resulting group is, and whether any single
rotation has order 6 or 12 (the numbers the D-417 title implies but that
this shell's actual geometry does not produce).

No physical claim is made by this script. It answers a pure geometry
question about the point set D-409 already defines.
"""
import itertools
from collections import Counter

import numpy as np


def build_n12():
    pts = set()
    for s in itertools.product([1, -1], repeat=2):
        pts.add((s[0], s[1], 0))
        pts.add((s[0], 0, s[1]))
        pts.add((0, s[0], s[1]))
    return np.array(sorted(pts), dtype=float)


def rot_axis(axis, theta):
    axis = axis / np.linalg.norm(axis)
    x, y, z = axis
    k = np.array([[0, -z, y], [z, 0, -x], [-y, x, 0]])
    return np.eye(3) + np.sin(theta) * k + (1 - np.cos(theta)) * (k @ k)


def preserves_set(r, pts, tol=1e-6):
    transformed = pts @ r.T
    return all(any(np.allclose(p, q, atol=tol) for q in pts) for p in transformed)


def element_order(r, max_check=12, tol=1e-6):
    m = np.eye(3)
    for k in range(1, max_check + 1):
        m = m @ r
        if np.allclose(m, np.eye(3), atol=tol):
            return k
    return None


def generate_group(generators):
    group = [np.eye(3)]

    def in_group(m):
        return any(np.allclose(m, g, atol=1e-6) for g in group)

    frontier = [np.eye(3)]
    while frontier:
        nxt = []
        for g in frontier:
            for gen in generators:
                for cand in (g @ gen, gen @ g):
                    if not in_group(cand):
                        group.append(cand)
                        nxt.append(cand)
        frontier = nxt
    return group


def main():
    pts = build_n12()
    assert len(pts) == 12, f"expected 12 points, got {len(pts)}"

    r4 = rot_axis(np.array([0.0, 0.0, 1.0]), np.pi / 2)  # face (4-fold) axis
    r3 = rot_axis(np.array([1.0, 1.0, 1.0]), 2 * np.pi / 3)  # vertex (3-fold) axis
    assert preserves_set(r4, pts), "R4 does not preserve N_12"
    assert preserves_set(r3, pts), "R3 does not preserve N_12"
    assert element_order(r4) == 4
    assert element_order(r3) == 3

    group = generate_group([r4, r3])
    assert all(preserves_set(g, pts) for g in group), "generated group leaves N_12"

    orders = [element_order(g) for g in group]
    order_counts = Counter(orders)

    # Direct check that no order-6 or order-12 rotation about the 4-fold
    # (z) axis preserves the set -- the specific claim this script exists
    # to test, since "12 neighbors" invites the assumption of 12-fold
    # symmetry.
    surviving_z_angles = [
        deg for deg in range(1, 360)
        if preserves_set(rot_axis(np.array([0.0, 0.0, 1.0]), np.deg2rad(deg)), pts)
    ]

    report = {
        "n12_point_count": len(pts),
        "full_rotation_group_order": len(group),
        "element_order_distribution": dict(sorted(order_counts.items())),
        "max_single_element_order": max(orders),
        "order_6_element_exists": 6 in orders,
        "order_12_element_exists": 12 in orders,
        "z_axis_surviving_angles_deg": surviving_z_angles,
    }
    for k, v in report.items():
        print(f"{k}: {v}")

    assert len(group) == 24, "expected the chiral octahedral group, order 24"
    assert 6 not in orders and 12 not in orders, (
        "no order-6 or order-12 rotation exists for this shell -- the naive "
        "12-fold-closure reading of D-417's title is not supported by the "
        "geometry D-409 actually defines"
    )
    assert surviving_z_angles == [90, 180, 270]
    print("\nPASS: N_12's rotation symmetry group is order 24 (chiral "
          "octahedral, isomorphic to S_4); individual element orders are "
          "only 1, 2, 3, or 4. No 6-fold or 12-fold rotational closure "
          "exists for this shell.")


if __name__ == "__main__":
    main()
