#!/usr/bin/env python3
"""Deterministic tests for Brain Buddy Baseline-Zero / Void control semantics."""
from __future__ import annotations
import tempfile
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from brain_buddy_oversight import baseline_zero, local_turn_prompt, parse_oversight

def sh(root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True)

def main() -> int:
    assert parse_oversight("STATE: ACT\nREASON: grounded\nWATCH: none\nNEXT: run")["state"] == "ACT"
    assert parse_oversight("STATE: HOLD\nREASON: stale\nWATCH: stale reference\nNEXT: refresh")["state"] == "HOLD"
    assert parse_oversight("free form model chatter")["state"] == "HOLD"
    lp = local_turn_prompt(
        "gemini",
        {"commit": "abc123", "branch": "test"},
        "do the task",
        [
            {"speaker": "field-task", "text": "do the task"},
            {"speaker": "void", "text": "STATE: HOLD"},
        ],
    )
    assert "LOCAL TRANSCRIPT" in lp
    assert "FIELD-TASK:" in lp and "VOID:" in lp
    assert "abc123" in lp
    assert "outer Council routing is unchanged" in lp

    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        sh(root, "init")
        sh(root, "config", "user.email", "test@example.invalid")
        sh(root, "config", "user.name", "Brain Buddy Test")
        for name in ("AI_FOREMAN_WORK_REGISTER.md","AI_CANONICAL_START_HERE.md","GENERAL_REFERENCE_RULES.md"):
            (root / name).write_text(name + "\n", encoding="utf-8")
        sh(root, "add", ".")
        sh(root, "commit", "-m", "zero")
        z1 = baseline_zero(root)
        (root / "state.txt").write_text("changed\n", encoding="utf-8")
        sh(root, "add", ".")
        sh(root, "commit", "-m", "changed")
        z2 = baseline_zero(root)
        assert z1["commit"] != z2["commit"], "Baseline Zero reused stale commit"
        assert "changed" in z2["recent_commits"], "Baseline Zero did not refresh recent state"

    print("PASS: ACT parse")
    print("PASS: HOLD parse")
    print("PASS: fail-closed malformed oversight")
    print("PASS: local M4 prompt accumulates self transcript without replacing shared reference")
    print("PASS: Baseline Zero refreshes after repository state change")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
