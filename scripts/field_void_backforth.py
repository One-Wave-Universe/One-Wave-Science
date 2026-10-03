#!/usr/bin/env python3
"""Field / Void live back-and-forth.

Field expresses. Void confirms, defers, or denies. They do not swap.
Authority is G-740. G-744 is a wrapper and must not replace it.

Every turn loads the reference files, then reads I-06 front matter for the
nodes in play. A missing metadata block stops the turn. Void is DeepSeek
through the existing web bridge. If that bridge does not answer, Void is
ABSENT and is not a vote.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

ROOT_FILES = (
    "GENERAL_REFERENCE_RULES.md",
    "AI_CANONICAL_START_HERE.md",
    "Governance_I_Series/I-06_Canonical_Node_Metadata_and_Alias_Resolution.md",
)
PAIR_FILES = (
    "Nodes/G-740_Field_Void_Ternary_and_Quadratic_Command_Routing.md",
    "Nodes/G-744_Field_Void_Occupancy_and_Loop_Pickup.md",
)
REQUIRED_META = (
    "node_id",
    "canonical_name",
    "namespace",
    "gate",
    "lifecycle",
    "classification",
    "claim_gate_detail",
    "metadata_standard",
)
ALLOWED_GATES = {"BROWN", "GRAY", "GREEN", "YELLOW", "BRONZE", "SILVER", "GOLD", "RED"}
ALLOWED_LIFE = {
    "ACTIVE",
    "ACTIVE_HYPOTHESIS",
    "PROPOSED_BUILD",
    "HELD",
    "BLOCKED",
    "SUPERSEDED",
    "HISTORY",
}


class LoopError(RuntimeError):
    pass


def repo_root() -> Path:
    proc = subprocess.run(["git", "rev-parse", "--show-toplevel"], text=True, capture_output=True)
    if proc.returncode != 0:
        raise LoopError("Run inside One-Wave-Science.")
    return Path(proc.stdout.strip()).resolve()


def front_matter(text: str, path: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise LoopError(f"I-06 front matter missing: {path}")
    end = text.find("\n---", 4)
    if end < 0:
        raise LoopError(f"I-06 front matter not closed: {path}")
    meta: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.strip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"')
    missing = [key for key in REQUIRED_META if key not in meta]
    if missing:
        raise LoopError(f"{path} missing I-06 fields: {', '.join(missing)}")
    if meta["gate"] not in ALLOWED_GATES:
        raise LoopError(f"{path} gate {meta['gate']} is not an I-06 gate")
    if meta["lifecycle"] not in ALLOWED_LIFE:
        raise LoopError(f"{path} lifecycle {meta['lifecycle']} is not an I-06 lifecycle")
    if meta["metadata_standard"] != "I-06":
        raise LoopError(f"{path} metadata_standard is not I-06")
    return meta


def load_reference(root: Path) -> str:
    chunks = ["FORCED REFERENCE — first. Memory does not outrank it."]
    for name in ROOT_FILES + PAIR_FILES:
        path = root / name
        if not path.is_file():
            raise LoopError(f"Required reference missing: {name}")
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            raise LoopError(f"Required reference empty: {name}")
        if name.startswith("Nodes/"):
            meta = front_matter(text, name)
            chunks.append(
                "METADATA "
                + name
                + " node_id="
                + meta["node_id"]
                + " gate="
                + meta["gate"]
                + " lifecycle="
                + meta["lifecycle"]
                + " classification="
                + meta["classification"]
            )
        chunks.append(f"===== {name} =====\n{text[:12000]}")
    return "\n\n".join(chunks)


def journal_path(root: Path) -> Path:
    out = root / "External_Work" / "brain_buddy" / "journal"
    out.mkdir(parents=True, exist_ok=True)
    return out / f"field-void-{time.strftime('%Y%m%d-%H%M%S')}.md"


def call_void(root: Path, prompt: str, timeout: int) -> tuple[bool, str]:
    cmd = [
        "python3",
        "One_Wave_Bench/hive-pipe/deepseek_web_bridge.py",
        "--max-tool-rounds",
        "12",
        prompt,
    ]
    try:
        proc = subprocess.run(cmd, cwd=root, text=True, capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return False, f"ABSENT timeout after {timeout}s. Not a vote."
    if proc.returncode != 0:
        return False, "ABSENT\n" + (proc.stderr or proc.stdout or f"exit {proc.returncode}") + "\nNot a vote."
    text = proc.stdout.strip()
    if not text:
        return False, "ABSENT empty return. Not a vote."
    return True, text


def field_claim(question: str) -> str:
    return f"""FIELD EXPRESS

G-740: FIELD = active interactions. Ternary is Express / Hold / Compress.
G-744 is a yellow wrapper and does not replace G-740.
Shared reference is the comparison, not a third seat. Sides do not swap.

Claim under test:
{question}

Repo paths used:
- GENERAL_REFERENCE_RULES.md
- AI_CANONICAL_START_HERE.md
- Governance_I_Series/I-06_Canonical_Node_Metadata_and_Alias_Resolution.md
- Nodes/G-740_Field_Void_Ternary_and_Quadratic_Command_Routing.md
- Nodes/G-744_Field_Void_Occupancy_and_Loop_Pickup.md

Void must Confirm, Defer, or Deny this claim against that metadata. A missing front matter is a stop, not a guess.
"""


def main() -> int:
    ap = argparse.ArgumentParser(description="Field/Void back-and-forth with I-06 gate")
    ap.add_argument("question")
    ap.add_argument("--timeout", type=int, default=240)
    args = ap.parse_args()
    question = args.question.strip()
    if not question:
        raise LoopError("Question is empty.")
    root = repo_root()
    reference = load_reference(root)
    path = journal_path(root)
    field = field_claim(question)
    void_prompt = reference + "\n\nVOID TURN\n\nYou are Void. Do not become Field.\nConfirm, Defer, or Deny the Field claim against the forced reference and the I-06 metadata above.\nG-744 must not replace G-740.\nEnd with exactly one of CONFIRM, DEFER, DENY, and the metadata fields you used.\n\n" + field
    ok, void = call_void(root, void_prompt, args.timeout)
    body = [
        "# Field / Void journal",
        "",
        "Reference and I-06 metadata loaded before the Void call.",
        "",
        field,
        "",
        "## VOID",
        "",
        void,
        "",
        "## RESPONSE",
        "",
        "READY WITH ABSENCE" if not ok else "READY",
        "",
    ]
    path.write_text("\n".join(body), encoding="utf-8")
    print(path.read_text(encoding="utf-8"))
    print(f"Journal: {path.relative_to(root)}")
    return 0 if ok else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except LoopError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
