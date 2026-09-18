#!/usr/bin/env python3
"""Lock the canonical logical six-step receipt without inventing six physical gates.

Logical/receipt cycle:
    M1 -> A1 -> M2 -> A2 -> M3 -> A3
Process labels:
    BEGIN -> BUILD -> HOLD -> BUILD -> BREAK -> LOOP

Physical CELL_V1 primitive:
    3 bidirectional A/B/C mirrors = 6 directed edge interfaces
    Views travel UP and Actions/conditioning travel DOWN through the same mirrors.

Permanent CI is read-only. ``--write`` is only an explicit migration aid for
Books/Repository_Operations/AI_CANONICAL_START_HERE.md; the permanent workflow never writes repository
content.
"""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AI_START = ROOT / "Books" / "Repository_Operations" / "AI_CANONICAL_START_HERE.md"
MASTER = ROOT / "Nodes" / "Reference" / "00_MASTER_INDEX.md"

REPLACEMENTS = {
    "6 measured oscillator gates": "6 process steps = 6 gates = 3 Mirror gates + 3 Action gates",
    "- The current VTC physical interpretation uses three physical Mirror Gates traversed in two orientations to realize the six logical positions.": "- The six logical positions are the six process gates: three Mirror gates and three Action gates, alternating `M1 -> A1 -> M2 -> A2 -> M3 -> A3`.",
    "- The six process steps are **Begin -> Build -> Hold -> Build -> Break -> Loop**; G-739 constrains them as measured stability regions around a bidirectional oscillator.": "- The six process steps are the six gates: **BEGIN/M1 -> BUILD/A1 -> HOLD/M2 -> BUILD/A2 -> BREAK/M3 -> LOOP/A3**; G-739 measures behavior at those same positions rather than defining another gate set.",
    "BEGIN is the active shared center/reference region. The six recursive labels are stability gates observed around a bidirectional oscillator, not a universal one-way conveyor.": "BEGIN/M1 is the first Mirror-gate relation at the active shared center/reference region. The six recursive labels are the same six gate positions: three Mirror gates alternating with three Action gates, not a separate measured-gate layer or a universal one-way conveyor.",
    "- `-` is the Mirror Gate return/crossover through the shared `(0)` reference.": "- `-` is the handoff from one canonical gate position to the next; Mirror behavior occurs only at M1, M2, and M3.",
    "- Four Actions are **Inward, Outward, Across, Over**.": "- Four Action **modes** are **Inward, Outward, Across, Over**; they describe what an Action gate may do and are not four primitive Action gates.",
    "If removing a domain vocabulary changes the six-pair oscillator, that domain representation has leaked into the kernel.": "If removing a domain vocabulary changes the six-step/six-gate Mirror-Action oscillator, that domain representation has leaked into the kernel.",
}

AI_REQUIRED = (
    "THREE PHYSICAL BIDIRECTIONAL MIRRORS:",
    "A+ <-> A-",
    "B+ <-> B-",
    "C+ <-> C-",
    "There are six directed edge interfaces, not six separate physical Mirror/Action gates.",
    "Views/state travel UP and Actions/conditioning travel DOWN through the same mirrors.",
)

AI_FORBIDDEN = (
    "3 physical Mirror gates + 3 physical Action gates = 6 physical gates",
)


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
    ROOT / "Nodes" / "Archive" / "Updated" / "UPDATED_33_INVARIANT_ENGINE_VTC_BUILD_AND_VIEW_ACTION_CORRECTION.md",
)


def patch_ai_start(write: bool) -> bool:
    text = AI_START.read_text(encoding="utf-8")
    updated = text
    for old, new in REPLACEMENTS.items():
        updated = updated.replace(old, new)
    changed = updated != text
    if changed and write:
        AI_START.write_text(updated, encoding="utf-8")
    return changed


def check() -> list[str]:
    errors: list[str] = []

    ai = AI_START.read_text(encoding="utf-8")
    for phrase in AI_REQUIRED:
        if phrase not in ai:
            errors.append(f"AI_CANONICAL_START_HERE.md missing canonical phrase: {phrase}")
    for phrase in AI_FORBIDDEN:
        if phrase in ai:
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
        if path.name in {
            "G-740_Field_Void_Ternary_and_Quadratic_Command_Routing.md",
            "UPDATED_33_INVARIANT_ENGINE_VTC_BUILD_AND_VIEW_ACTION_CORRECTION.md",
        }:
            lower = text.lower()
            if "three physical bidirectional" not in lower and "3 physical bidirectional" not in lower:
                errors.append(f"{path.relative_to(ROOT)} must anchor the three-bidirectional-mirror physical primitive")
            if "six directed" not in lower and "6 directed" not in lower:
                errors.append(f"{path.relative_to(ROOT)} must preserve six directed interfaces as interface count, not six devices")
            if "views" not in lower or "actions" not in lower or "same" not in lower:
                errors.append(f"{path.relative_to(ROOT)} must keep Views/Actions on the same physical mirrors")
            continue

        # Logical timing/receipt nodes may retain the six-position M/A sequence.
        lower = text.lower()
        if path.name in {
            "B-221a_Six_Step_Oscillator_Program.md",
            "G-739_Six_Gate_Trajectory_Extraction.md",
        }:
            if "six" not in lower:
                errors.append(f"{path.relative_to(ROOT)} must preserve the logical six-position recurrence")
        # Mirror-definition nodes must not be interpreted as creating six physical devices.
        if path.name in {
            "C-301_Mirror_Gate.md",
            "G-729_Mirror_as_Continuous_Phase_with_Six_Route_Projection.md",
        }:
            if "mirror" not in lower:
                errors.append(f"{path.relative_to(ROOT)} must retain the Mirror relation")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    changed = patch_ai_start(args.write)
    if changed and not args.write:
        print("AI canonical start requires six-gate synchronization")
        return 1

    errors = check()
    if errors:
        print("SIX-GATE CANON FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS: logical six-step receipt preserved; physical CELL_V1 = 3 bidirectional A/B/C mirrors, 6 directed interfaces; Views/Actions share those mirrors; no internal Gate 7")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
