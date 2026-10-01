#!/usr/bin/env python3
"""Explicit Brain Buddy Void oversight and Baseline-Zero auto-reference.

This is inspectable runtime state, not hidden model chain-of-thought.
"""
from __future__ import annotations
import json
from pathlib import Path
import subprocess
from typing import Any

GOAL_FILES = (
    "AI_FOREMAN_WORK_REGISTER.md",
    "AI_CANONICAL_START_HERE.md",
    "GENERAL_REFERENCE_RULES.md",
)

def _git(root: Path, *args: str) -> str:
    p = subprocess.run(["git", *args], cwd=root, text=True, capture_output=True, check=False)
    return p.stdout.strip() if p.returncode == 0 else ""

def _head(path: Path, limit: int = 6000) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:limit]
    except OSError:
        return ""

def baseline_zero(root: Path) -> dict[str, Any]:
    """Refresh shared situational reference from the live checkout."""
    return {
        "repository": "One-Wave-Universe/One-Wave-Science",
        "branch": _git(root, "branch", "--show-current"),
        "commit": _git(root, "rev-parse", "HEAD"),
        "working_tree": _git(root, "status", "--short") or "clean",
        "recent_commits": _git(root, "log", "-5", "--oneline"),
        "project_goal_and_work_register": _head(root / "AI_FOREMAN_WORK_REGISTER.md"),
        "canonical_start": _head(root / "AI_CANONICAL_START_HERE.md", 3000),
        "reference_rules": _head(root / "GENERAL_REFERENCE_RULES.md", 3000),
    }

def oversight_prompt(worker: str, zero: dict[str, Any], field_task: str) -> str:
    """Ask the same AI for an explicit oversight state before its Field action."""
    return f"""BRAIN BUDDY VOID OVERSIGHT LOOP
You are {worker}. This is your explicit oversight state, not your outward answer.
Watch the proposed Field task against Baseline Zero and decide whether action is warranted.
Do not expose private chain-of-thought. Return only compact operational state.
There are no menus or option generation.

BASELINE ZERO:
{json.dumps(zero, indent=2, sort_keys=True)}

PROPOSED FIELD TASK:
{field_task}

Return exactly:
STATE: ACT
REASON: <one concise operational reason>
WATCH: <drift, contradiction, stale reference, failure, completion, or none>
NEXT: <single next action>

Use STATE: HOLD instead of ACT when the task should not proceed yet.
"""

def parse_oversight(text: str) -> dict[str, str]:
    state = "HOLD"
    out = {"state": state, "reason": "oversight response was not actionable", "watch": "parse", "next": "refresh reference"}
    for raw in text.splitlines():
        key, sep, value = raw.partition(":")
        if not sep:
            continue
        k = key.strip().upper()
        v = value.strip()
        if k == "STATE" and v.upper() in {"ACT", "HOLD"}:
            out["state"] = v.upper()
        elif k == "REASON":
            out["reason"] = v
        elif k == "WATCH":
            out["watch"] = v
        elif k == "NEXT":
            out["next"] = v
    return out


def local_turn_prompt(
    worker: str,
    zero: dict[str, Any],
    field_task: str,
    local_turns: list[dict[str, str]],
) -> str:
    """Build one explicit self/Void turn using the same accumulated-transcript pattern as Council."""
    transcript = "\n\n".join(
        f"{turn['speaker'].upper()}:\n{turn['text']}" for turn in local_turns
    ) or "(no prior local turns)"
    return f"""BRAIN BUDDY LOCAL M4 LOOP
You are {worker}. This is your explicit local self-reference / Void turn.
This loop is inside your existing Brain Buddy Council turn. The outer Council routing is unchanged.
Use your accumulated LOCAL TRANSCRIPT as your immediate self-reference.
Consult shared Baseline Zero as external project reference; do not confuse it with self-state.
Do not expose private chain-of-thought. Record only compact operational state.

SHARED BASELINE ZERO:
{json.dumps(zero, indent=2, sort_keys=True)}

FIELD TASK:
{field_task}

LOCAL TRANSCRIPT:
---
{transcript}
---

Return exactly:
STATE: ACT
REASON: <one concise operational reason>
WATCH: <current local concern or none>
NEXT: <single next outward action>

Use STATE: HOLD only when outward Field action should not happen on this Council turn.
"""


def field_path(field_task: str) -> str:
    """Select direct Field speech or local-dialogue preparation without exposing private reasoning."""
    task = field_task.lower()
    direct_markers = ("speak direct:", "direct field:", "immediate:")
    return "DIRECT" if any(marker in task for marker in direct_markers) else "M4"
