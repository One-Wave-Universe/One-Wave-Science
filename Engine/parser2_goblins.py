#!/usr/bin/env python3
"""Two-state parser + loop goblins.

States: HOLD | GO
Dead band: missing intention or consequence => HOLD (Reference Goblin).

Goblins:
  HOLD  — refuse
  RELAY — message only (write packet / inbox)
  ACT   — may invoke a named local wrapper
"""
from __future__ import annotations

import json
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

State = Literal["HOLD", "GO"]
Role = Literal["HOLD", "RELAY", "ACT"]


@dataclass
class Packet:
    text: str
    intention: str = ""
    consequence: str = ""
    role: Role = "RELAY"
    named_files: list | None = None


def parse(raw: dict) -> Packet:
    role = str(raw.get("role") or "RELAY").upper()
    if role not in ("HOLD", "RELAY", "ACT"):
        role = "HOLD"
    return Packet(
        text=str(raw.get("text") or raw.get("goal") or "").strip(),
        intention=str(raw.get("intention") or "").strip(),
        consequence=str(raw.get("consequence") or "").strip(),
        role=role,
        named_files=list(raw.get("named_files") or []),
    )


def state_of(p: Packet) -> State:
    if not p.text or not p.intention or not p.consequence:
        return "HOLD"
    if p.role not in ("HOLD", "RELAY", "ACT"):
        return "HOLD"
    return "GO"


def route(p: Packet) -> Role:
    if state_of(p) == "HOLD":
        return "HOLD"
    if p.role == "ACT":
        return "ACT"
    return "RELAY"


def hold_goblin(p: Packet) -> dict:
    missing = [k for k, v in (("text", p.text), ("intention", p.intention), ("consequence", p.consequence)) if not v]
    return {"goblin": "HOLD", "ok": False, "missing": missing, "msg": "Reference Goblin HOLD"}


def relay_goblin(p: Packet, root: Path) -> dict:
    box = root / "External_Work" / "brain_buddy" / "inbox"
    box.mkdir(parents=True, exist_ok=True)
    dest = box / "relay.md"
    dest.write_text(
        f"# relay\n\n{p.text}\n\nintention: {p.intention}\nconsequence: {p.consequence}\n",
        encoding="utf-8",
    )
    return {"goblin": "RELAY", "ok": True, "wrote": str(dest), "acted": False}


def act_goblin(p: Packet, root: Path) -> dict:
    prover = root / "Engine" / "prove_one_wave.py"
    buddy = root / "scripts" / "brain_buddy.sh"
    if prover.is_file():
        r = subprocess.run(["python3", str(prover)], cwd=str(root), capture_output=True, text=True, timeout=30)
        return {
            "goblin": "ACT",
            "ok": r.returncode == 0,
            "wrapper": str(prover),
            "stdout_tail": (r.stdout or "")[-800:],
        }
    if buddy.is_file():
        return {
            "goblin": "ACT",
            "ok": False,
            "msg": "brain_buddy present; Gemini CLI is a Jetson step",
            "wrapper": str(buddy),
        }
    return {"goblin": "ACT", "ok": False, "msg": "no allowed wrapper on this host"}


def loop_once(raw: dict, root: Path | None = None) -> dict:
    root = root or Path.cwd()
    p = parse(raw)
    who = route(p)
    if who == "HOLD":
        body = hold_goblin(p)
    elif who == "ACT":
        body = act_goblin(p, root)
    else:
        body = relay_goblin(p, root)
    return {"state": state_of(p), "role": who, "packet": asdict(p), **body}


def demo() -> dict:
    cases = [
        {"text": "status", "role": "RELAY"},
        {
            "text": "Does 2N+2m = 2(N+m)?",
            "intention": "check hop identity",
            "consequence": "yes/no plus receipt",
            "role": "RELAY",
        },
        {
            "text": "run prove_one_wave",
            "intention": "algebra receipts",
            "consequence": "all_pass true or listed fails",
            "role": "ACT",
        },
    ]
    return {"brick": "YELLOW", "cases": [loop_once(c) for c in cases]}


if __name__ == "__main__":
    print(json.dumps(demo(), indent=2))
