#!/usr/bin/env python3
"""Synchronize the canonical discovery surfaces for locked node-graph additions.

This script is deliberately narrow and idempotent.  It does not regenerate the
whole master index or rewrite prose.  It owns only the exact rows/section needed
for the C-319/C-320/D-416 bridge.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "00_MASTER_INDEX.md"
AI_START = ROOT / "AI_CANONICAL_START_HERE.md"

C319_ROW = "| C-319 | Magnetic Lattice Reorganization | Rotational magnetic state reorganizes directional lattice path accessibility without automatically inserting scalar compression. | GREEN |"
C320_ROW = "| C-320 | Magnetic-Compression Path Coupling | Canonical hypothesis: C-319 path reorganization weights the A-115 compression/restoring response; magnetism reorganizes the lattice rather than becoming gravity. | GREEN |"
D416_ROW = "| D-416 | Planetary Rotation-Magnetic Coupling Test Matrix | Joint Moon/Mercury/Venus/Uranus/Neptune falsification set for C-319/C-320, with locking required to emerge rather than be initialized. | GREEN |"

AI_BRIDGE = """## Magnetism / Gravity canonical bridge\n\nBefore any AI connects magnetism, lattice reorganization, gravity/compression, orbital response, tidal/spin locking, or planetary magnetic anomalies, read this chain in order:\n\n1. `Nodes/C-311_Electric_Magnetic_Duality.md` — magnetic field is the rotational field view used by the framework.\n2. `Nodes/D-408_Sixfold_2D_Triangular_Hexagonal_Lattice.md` — planar control geometry only.\n3. `Nodes/D-409_Twelvefold_3D_Close_Packed_Coordination.md` — required native 3D geometry before planetary interpretation.\n4. `Nodes/C-319_Magnetic_Lattice_Reorganization.md` — magnetic rotation reorganizes directional lattice path accessibility.\n5. `Nodes/A-115_Unified_Compression_Field.md` — gravity remains the compression-gradient/restoring field source.\n6. `Nodes/C-320_Magnetic_Compression_Path_Coupling.md` — candidate coupling `g_OW = -alpha_g K_L grad(chi)` with mandatory `K_L -> I` recovery.\n7. `Nodes/D-413_Ground_Lattice_Orbital_Restoring_Simulation.md` — reduced lab; source-derived A-115 baseline must pass before magnetic coupling is enabled.\n8. `Nodes/D-416_Planetary_Rotation_Magnetic_Coupling_Test_Matrix.md` — Moon/Mercury/Venus/Uranus/Neptune joint falsification matrix.\n\nLocked interpretation:\n\n```text\nmagnetic rotational state\n-> reorganizes lattice pathways\n-> changes directional accessibility of an existing compression/restoring field\n-> can alter distributed restoring response and torque if the coupling survives tests\n```\n\nDo **not** collapse this to `magnetism = gravity`.  Do **not** use a present global lunar dipole as an explanation for lunar synchronous rotation; the Moon has no present global magnetic field.  Do **not** call Mercury 1:1 tidally locked; its control state is 3:2 spin-orbit resonance.  Venus, Uranus, and Neptune remain mandatory awkward-body controls rather than exceptions.\n\n"""


def require_once(text: str, needle: str, label: str) -> None:
    count = text.count(needle)
    if count != 1:
        raise RuntimeError(f"expected exactly one {label}; found {count}")


def sync_master(text: str) -> str:
    if "| C-319 |" not in text:
        anchor = "| C-318 | Four-Interaction Mass-Effect Response | Permanently removes the false speed-ceiling shortcut and scalar-gap import; defines Mass Effect as the carried-pattern response of the coupled knot, electrical shell, Mirror relation, Boundary-Tension Weave, and cross-terms. | GREEN |"
        require_once(text, anchor, "C-318 master-index row")
        text = text.replace(anchor, anchor + "\n" + C319_ROW + "\n" + C320_ROW)
    if "| D-416 |" not in text:
        anchor = "| D-415 | Nonlocal Three-Excitation One-Field Bench | Runnable six-neighbor triangular-lattice bench evolving one globally connected nonlinear Field and measuring three extended excitations with origin-free relational receipts; candidate kernel and potential remain underived. | YELLOW |"
        require_once(text, anchor, "D-415 master-index row")
        text = text.replace(anchor, anchor + "\n" + D416_ROW)

    text = text.replace(
        "### Appendix C — Applied Mechanics & Conflict-Resolution (20 active files)",
        "### Appendix C — Applied Mechanics & Conflict-Resolution (22 active files)",
    )
    text = text.replace(
        "### Appendix D — Resonance, Modal & Dimensional Structure (15 nodes)",
        "### Appendix D — Resonance, Modal & Dimensional Structure (16 nodes)",
    )
    return text


def sync_ai_start(text: str) -> str:
    if "## Magnetism / Gravity canonical bridge" in text:
        return text
    marker = "## Current update handoff"
    require_once(text, marker, "AI current-update marker")
    return text.replace(marker, AI_BRIDGE + marker)


def sync_file(path: Path, transform, check: bool) -> bool:
    original = path.read_text(encoding="utf-8")
    updated = transform(original)
    changed = updated != original
    if changed and not check:
        path.write_text(updated, encoding="utf-8")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if synchronization would change files")
    args = parser.parse_args()

    changed = []
    if sync_file(MASTER, sync_master, args.check):
        changed.append(str(MASTER.relative_to(ROOT)))
    if sync_file(AI_START, sync_ai_start, args.check):
        changed.append(str(AI_START.relative_to(ROOT)))

    if args.check and changed:
        print("node graph discovery surfaces are stale:")
        for path in changed:
            print(f"- {path}")
        return 1

    if changed:
        print("updated:")
        for path in changed:
            print(f"- {path}")
    else:
        print("node graph discovery surfaces already synchronized")
    return 0


if __name__ == "__main__":
    sys.exit(main())
