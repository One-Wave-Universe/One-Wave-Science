#!/usr/bin/env python3
"""Verify the six-around-one CELL_V1 hexagon flower's edge pairing.

cell_v1_hexagon_flower.svg claims: one hexagon cell, translated (never
rotated) into all six neighbor positions of a hex tiling, produces 12
shared edges (6 center<->neighbor, 6 neighbor<->neighbor around the
outer ring), and every one of them lands on the exact same point from
both cells' sides and pairs the same axis letter with opposite polarity
(A+/A-, B+/B-, C+/C-).

This script is the actual check behind that claim, independent of the
SVG's own coordinates -- re-run it any time the flower is edited to
confirm the geometry still holds.
"""
import math
import sys
from collections import defaultdict

def pt(base, angle_deg, r):
    a = math.radians(angle_deg)
    return (base[0] + r * math.cos(a), base[1] - r * math.sin(a))

# Same fixed, unrotated side pattern used by every cell in the flower.
# Each key is the angle (degrees, 0=right, ccw, y-flipped for screen
# coordinates) of a hexagon side's midpoint; each value is that side's
# axis-and-polarity label. axis_pairs records which two angles belong
# to the same axis (so they must always land on the exact-opposite side
# of the cell, per D-411's -d (0) +d).
LABELS = {
    60: "A+", 0: "C-", -60: "B+",
    -120: "A-", 180: "C+", 120: "B-",
}
AXIS_PAIRS = [(60, -120), (-60, 120), (180, 0)]
NEIGHBOR_DIRS = [60, 0, -60, -120, 180, 120]


def build_flower(corner_r=95.0):
    side_r = corner_r * math.cos(math.radians(30))
    neighbor_dist = 2 * side_r
    page_center = (0.0, 0.0)
    centers = {"CENTER": page_center}
    for d in NEIGHBOR_DIRS:
        centers[d] = pt(page_center, d, neighbor_dist)
    return centers, side_r


def check(name, expected, actual, note=""):
    ok = expected == actual
    print(f"{'PASS' if ok else 'FAIL'} [{name}] expected={expected} actual={actual}{' -- ' + note if note else ''}")
    return ok


def main() -> int:
    centers, side_r = build_flower()

    # Every axis pair must be exact opposites (180 degrees apart) --
    # this is what makes one straight coil a real -d (0) +d axis.
    all_ok = True
    for a1, a2 in AXIS_PAIRS:
        all_ok &= check(f"axis-pair-{LABELS[a1]}/{LABELS[a2]}-are-opposite",
                         True, abs((a1 - a2) % 360) in (180,))

    points = []
    for key, c in centers.items():
        for ang, lab in LABELS.items():
            p = pt(c, ang, side_r)
            points.append((key, round(p[0], 6), round(p[1], 6), lab))

    groups = defaultdict(list)
    for key, x, y, lab in points:
        groups[(x, y)].append((key, lab))

    shared = [g for g in groups.values() if len(g) == 2]
    external = [g for g in groups.values() if len(g) == 1]
    other = [g for g in groups.values() if len(g) not in (1, 2)]

    all_ok &= check("shared-edge-count", 12, len(shared))
    all_ok &= check("external-facing-count", 18, len(external))
    all_ok &= check("no-triple-or-more-overlaps", 0, len(other))

    mismatches = []
    for (k1, l1), (k2, l2) in shared:
        same_axis = l1[0] == l2[0]
        opposite_polarity = l1[1] != l2[1]
        if not (same_axis and opposite_polarity):
            mismatches.append(((k1, l1), (k2, l2)))
    all_ok &= check("every-shared-edge-is-same-axis-opposite-polarity", 0, len(mismatches),
                    note=str(mismatches) if mismatches else "")

    print()
    print("PASS: hexagon flower geometry holds" if all_ok else "FAIL: see above")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
