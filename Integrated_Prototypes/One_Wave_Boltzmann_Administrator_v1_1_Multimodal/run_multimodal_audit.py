#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from multimodal_memory import (
    AllocationProfile,
    EqualReserveHopfieldMemory,
    MemoryModality,
    example_traces,
)

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    traces = example_traces()
    memory = EqualReserveHopfieldMemory(block_width=32, seed=2026)
    memory.store_many(traces)
    profile = AllocationProfile.dialogue_sound_pressure_profile()

    cases = [
        (
            traces[0],
            (
                MemoryModality.DIALOGUE,
                MemoryModality.SOUND,
                MemoryModality.BODY_PRESSURE,
                MemoryModality.MOVEMENT_GAZE,
            ),
            "waking",
        ),
        (
            traces[1],
            (MemoryModality.DIALOGUE, MemoryModality.BODY_PRESSURE),
            "daydream",
        ),
        (
            traces[2],
            (MemoryModality.SOUND, MemoryModality.BODY_PRESSURE, MemoryModality.MOVEMENT_GAZE),
            "dream_sleep",
        ),
    ]

    recalls = []
    for trace, available, mode in cases:
        result = memory.recall(
            expected_memory=trace.memory_id,
            cue=trace,
            available=available,
            profile=profile,
            mode=mode,
        )
        recalls.append(result.to_jsonable())

    memory.save(RESULTS / "multimodal_hopfield_memory.json")

    original_copy = ROOT / "hopfield_original" / "One_Wave_Hopfield_Brain_v2_1_Final.py"
    source_original = ROOT.parent / "hopfield" / "One_Wave_Hopfield_Brain_v2_1_Final" / "One_Wave_Hopfield_Brain_v2_1_Final.py"
    preservation = {
        "copied_source_sha256": sha256(original_copy),
        "source_sha256": sha256(source_original) if source_original.exists() else None,
    }
    preservation["exact_source_preserved"] = (
        preservation["source_sha256"] is not None
        and preservation["copied_source_sha256"] == preservation["source_sha256"]
    )

    summary = {
        "version": "1.1-multimodal",
        "reserved_memory_percent": {m.value: 20.0 for m in MemoryModality},
        "storage_total_percent": 100.0,
        "profile": "dialogue_sound_pressure_heavy_with_faint_image_access",
        "recall_cases": recalls,
        "correct_recalls": sum(1 for r in recalls if r["correct_attractor"]),
        "total_recalls": len(recalls),
        "hopfield_preservation": preservation,
        "architectural_note": (
            "Five equal memory banks are not automatically the same as the five M4 pathways. "
            "M4 will later mix and route these representations into the transmission lanes."
        ),
    }
    (RESULTS / "multimodal_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )

    report = [
        "# One-Wave Multimodal Memory Audit",
        "",
        "## Locked rule",
        "",
        "- Five memory media retain equal 20% reserved capacity.",
        "- Live access can redistribute without deleting any modality.",
        "- Original Hopfield v2.1 source is copied unchanged and hash-checked.",
        "- The companion attractor can recall memories with visual input absent or faint.",
        "- Internal dialogue, sound abstraction, body pressure/breath, movement/gaze, and image/spatial traces remain separate fields of one memory.",
        "",
        "## Audit result",
        "",
        f"- Correct multimodal recalls: {summary['correct_recalls']}/{summary['total_recalls']}",
        f"- Original Hopfield source preserved exactly: {preservation['exact_source_preserved']}",
        "",
        "## Important boundary",
        "",
        "The five equal memory banks are storage/representation allocations. They are not yet declared identical to the five M4 transmission pathways. M4 will later act as the operator that mixes, routes, inhibits, and releases these forms according to State, Scale, Caution, Drive, and the think-before-speaking gate.",
    ]
    (RESULTS / "MULTIMODAL_REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
