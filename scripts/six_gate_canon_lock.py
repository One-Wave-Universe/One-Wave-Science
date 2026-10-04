#!/usr/bin/env python3
"""Lock current CELL_V1 physical architecture and legacy logical-role separation.

Primitive cycle:
    M1 -> A1 -> M2 -> A2 -> M3 -> A3
Process labels:
    BEGIN -> BUILD -> HOLD -> BUILD -> BREAK -> LOOP

M/A positions are logical/receipt vocabulary, not six physical gate devices.
Updated 33 and the current AI start supersede the previous physical reading.
This checker is read-only. The old --write migration is retired.
"""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AI_START = ROOT / "AI_CANONICAL_START_HERE.md"
MASTER = ROOT / "00_MASTER_INDEX.md"

AI_REQUIRED = (
    "three physical bidirectional mirrors",
    "six hex interfaces are directed ends of those three mirrors",
    "logical/receipt notation",
    "not another hardware gate count",
    "no internal Gate 7",
)
AI_FORBIDDEN = (
    "6 process steps = 6 gates = 3 Mirror gates + 3 Action gates",
    "Mirror behavior occurs only at M1, M2, and M3",
)
CURRENT_PHYSICAL_REQUIRED = {
    "G-740_Field_Void_Ternary_and_Quadratic_Command_Routing.md": (
        "exactly three physical bidirectional Mirror axes",
        "six directed edge interfaces, not six separate physical gates",
        "logical/receipt sequence only",
        "no separate Action-gate hardware layer",
        "no Field/Void identity swap",
    ),
    "UPDATED_33_INVARIANT_ENGINE_VTC_BUILD_AND_VIEW_ACTION_CORRECTION.md": (
        "three bidirectional Mirror axes",
        "logical/receipt positions, not six physical gates",
        "Views travel UP and Actions travel DOWN",
        "A Mirror operation does not swap their ontology",
    ),
}

def normalized(text: str) -> str:
    return text.replace("**", "").casefold()

MASTER_REQUIRED = (
    "| G-711 | Namika — Inter-System Relation (No Internal Gate 7) |",
    "| B-206b | Four Views — Direction, Phase, Strength, Reference |",
    "| B-206c | Four Action Modes — Inward, Outward, Across, Over |",
    "| B-221a | Six-Step / Six-Gate Mirror-Action Oscillator |",
    "| G-729 | Mirror Operator for the Three Mirror Gates |",
    "| G-739 | Six-Gate Mirror-Action Trajectory Extraction |",
)

MASTER_FORBIDDEN = (
    "| G-711 | Gate 7 |",
    "| B-206c | Four Actions — Inward, Outward, Across, Over |",
    "| B-221a | Six-Step Oscillator Program — Begin Build Hold Build Break Loop |",
    "| G-729 | Mirror as Continuous Phase with Six-Route Projection |",
    "| G-739 | Six-Gate Trajectory Extraction |",
)

CANON_FILES = (
    ROOT / "Nodes" / "B-206b_Four_Views.md",
    ROOT / "Nodes" / "B-206c_Four_Actions.md",
    ROOT / "Nodes" / "B-221a_Six_Step_Oscillator_Program.md",
    ROOT / "Nodes" / "C-301_Mirror_Gate.md",
    ROOT / "Nodes" / "G-711_Gate_7.md",
    ROOT / "Nodes" / "G-729_Mirror_as_Continuous_Phase_with_Six_Route_Projection.md",
    ROOT / "Nodes" / "G-739_Six_Gate_Trajectory_Extraction.md",
    ROOT / "Nodes" / "G-740_Field_Void_Ternary_and_Quadratic_Command_Routing.md",
    ROOT / "UPDATED_33_INVARIANT_ENGINE_VTC_BUILD_AND_VIEW_ACTION_CORRECTION.md",
)


def check() -> list[str]:
    errors: list[str] = []

    ai = normalized(AI_START.read_text(encoding="utf-8"))
    for phrase in AI_REQUIRED:
        if normalized(phrase) not in ai:
            errors.append(f"AI_CANONICAL_START_HERE.md missing canonical phrase: {phrase}")
    for phrase in AI_FORBIDDEN:
        if normalized(phrase) in ai:
            errors.append(f"AI_CANONICAL_START_HERE.md contains superseded phrase: {phrase}")

    master = MASTER.read_text(encoding="utf-8")
    for phrase in MASTER_REQUIRED:
        if phrase not in master:
            errors.append(f"00_MASTER_INDEX.md missing canonical row: {phrase}")
    for phrase in MASTER_FORBIDDEN:
        if phrase in master:
            errors.append(f"00_MASTER_INDEX.md contains superseded row: {phrase}")

    for path in CANON_FILES:
        if not path.exists():
            errors.append(f"missing canonical architecture file: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        if path.name in CURRENT_PHYSICAL_REQUIRED:
            for phrase in CURRENT_PHYSICAL_REQUIRED[path.name]:
                if normalized(phrase) not in normalized(text):
                    errors.append(f"{path.relative_to(ROOT)} missing current physical rule: {phrase}")
            continue
        if path.name == "G-711_Gate_7.md":
            if "No Internal Gate 7" not in text or "six" not in text.lower():
                errors.append("G-711 must remain Namika/no-internal-Gate-7")
            continue
        if path.name == "B-206b_Four_Views.md":
            if "not four Mirror gates" not in text:
                errors.append("B-206b must keep Four Views subordinate to the primitive gate count")
            continue
        if path.name == "B-206c_Four_Actions.md":
            if "not four primitive Action gates" not in text:
                errors.append("B-206c must define four Action modes, not four primitive Action gates")
            continue
        if "3 Mirror" not in text or "3 Action" not in text:
            errors.append(f"{path.relative_to(ROOT)} does not declare 3 Mirror + 3 Action roles")
        if "6 gates" not in text and "six-gate" not in text.lower():
            errors.append(f"{path.relative_to(ROOT)} does not anchor the six-gate primitive")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    if args.write:
        parser.error("--write is retired: this checker is read-only and must not restore superseded physical gates")

    errors = check()
    if errors:
        print("SIX-GATE CANON FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS: three physical bidirectional mirrors; six directed interfaces; logical roles and physical gates separate; no internal Gate 7")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
