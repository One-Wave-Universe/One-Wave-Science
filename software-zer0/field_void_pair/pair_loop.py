"""Field/Void pair loop — two AIs, one repo lens, Algorythm-Zer0 as the referee.

SOFTWARE ONLY. Routes, compares, and rebases numbers (software-zer0/SEPARATE.md).
It does not claim the cell, the core, or any body remembered anything.

One turn:

    REPO LENS (shared reference, same for both)
         |
    FIELD AI  -> one bounded proposal, must cite repo paths
         |
    VOID AI   -> VERDICT ALLOW|CORRECT|OVERRIDE|HOLD|ESCALATE
                 REFERENCE -1..+1   GOAL -1..+1
         |
    Zer0 branches (simulations/zer0_first_cycle.py, imported, not copied)
        X = grounding   deterministic: cited paths that exist in the repo
        Y = reference   Void verdict + reference score
        Z = goal        Void goal score
        T = timing      turn / max_turns (closure, does not vote)
         |
    shared_event(ref, X/Y/Z/T) -> resolved -, 0, +  and bounded new ref
         |
    +  confirmed: proposal becomes the reference state
    -  denied:    Void note goes back to Field as override
    0  HOLD:      nothing advances

Because each branch is classified against the moving reference, the bar
rises after every confirmation: the next proposal has to beat the new zero.

Stops (AGENTS.md):
    ESCALATE verdict          -> ESCALATE
    3 denials in a row        -> THREE_STRIKES
    2 HOLDs in a row          -> SETTLED
    turn == max_turns         -> HARD_STOP
"""

from __future__ import annotations

import json
import re
import sys
import time
import types
from dataclasses import dataclass, field
from pathlib import Path

try:
    from .providers import Provider, ProviderError
    from .repo_lens import RepoLens
except ImportError:  # run as a plain script
    from providers import Provider, ProviderError
    from repo_lens import RepoLens


def _load_zer0(lens: RepoLens):
    """Import the Algorythm-Zer0 harness from the repo the lens reads. Never a copy."""
    if not lens.bundle:
        sim = str(lens.root / "simulations")
        if sim not in sys.path:
            sys.path.insert(0, sim)
        import zer0_first_cycle  # noqa: E402

        return zer0_first_cycle
    # Bundle: run the same file's source from the snapshot.
    # Own module name, so it never shadows a checkout's zer0_first_cycle.
    name = "zer0_first_cycle__bundle"
    mod = types.ModuleType(name)
    mod.__file__ = f"{lens.root}!repo/simulations/zer0_first_cycle.py"
    sys.modules[name] = mod  # dataclasses look the module up by name
    exec(compile(lens.source("simulations/zer0_first_cycle.py"), mod.__file__, "exec"), mod.__dict__)
    return mod


VERDICT_VALUE = {"ALLOW": 1.0, "CORRECT": 0.4, "HOLD": 0.0, "OVERRIDE": -0.6, "ESCALATE": -1.0}
VERDICTS = tuple(VERDICT_VALUE)

FIELD_ROLE = """You are FIELD in a One-Wave Field/Void pair.
FIELD = expressive side: propose, expand, explore one continuation (AGENTS.md, UPDATED_34 s3, G-740).
You see the One-Wave repository through the REPO LENS below. That lens is your only authority.

Rules:
- Propose exactly ONE bounded next step toward the GOAL. Do not approve yourself.
- Ground every claim in repo files. Cite exact repo paths in backticks.
- Separate established fact, derived result, simulation result, proposal, and speculation.
- If the lens does not hold what you need, say HOLD and name the missing file.
- If VOID overrode or corrected you, answer that note first.
- End with one line: CITES: `path`, `path`
"""

VOID_ROLE = """You are VOID in a One-Wave Field/Void pair.
VOID = compressive side: compare, constrain against the reference, reject, stabilize, redirect.
You are the oversight override mechanism (AGENTS.md), not a generic reviewer.
You see the same REPO LENS as FIELD. Judge FIELD's proposal only against that repo reference
and the confirmed reference state.

Reply with exactly these four lines first, then optional detail:
VERDICT: ALLOW | CORRECT | OVERRIDE | HOLD | ESCALATE
REFERENCE: <number -1..+1>   consistency with repo canon and the confirmed state
GOAL: <number -1..+1>        real progress toward the GOAL (0 = none)
NOTE: <one line: the correction, override, or reason>

Score low when FIELD cites files that do not exist, contradicts canon, or invents architecture
the repo already has. Unsupported confidence is not progress.
"""


def parse_void(text: str) -> dict:
    """Missing or malformed fields read as HOLD/0. No hidden pass."""

    def num(tag: str) -> float:
        m = re.search(rf"^\s*{tag}\s*:\s*([+-]?\d*\.?\d+)", text, re.I | re.M)
        if not m:
            return 0.0
        return max(-1.0, min(1.0, float(m.group(1))))

    m = re.search(r"^\s*VERDICT\s*:\s*([A-Za-z]+)", text, re.I | re.M)
    verdict = m.group(1).upper() if m and m.group(1).upper() in VERDICTS else "HOLD"
    note = re.search(r"^\s*NOTE\s*:\s*(.+)$", text, re.I | re.M)
    return {
        "verdict": verdict,
        "reference": num("REFERENCE"),
        "goal": num("GOAL"),
        "note": note.group(1).strip() if note else "",
        "parsed": bool(m),
    }


def grounding_score(good: list[str], bad: list[str]) -> float:
    if not good and not bad:
        return -1.0  # no citations is ungrounded, not neutral
    return 2.0 * len(good) / (len(good) + len(bad)) - 1.0


@dataclass
class FieldVoidPair:
    goal: str
    field_ai: Provider
    void_ai: Provider
    lens: RepoLens
    max_turns: int = 8
    ref: float = 0.0
    turn: int = 0
    confirmed: str = ""
    last_void: dict = field(default_factory=dict)
    holds: int = 0
    denials: int = 0
    stop: str = ""
    history: list = field(default_factory=list)
    snapshot: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.field_ai.role = "field"
        self.void_ai.role = "void"
        self.zer0 = _load_zer0(self.lens)
        if not self.snapshot:
            self.snapshot = self.lens.snapshot()

    def _state_block(self) -> str:
        last = self.last_void
        return (
            f"GOAL: {self.goal}\n"
            f"TURN: {self.turn} of {self.max_turns}\n"
            f"ZER0 REFERENCE r = {self.ref:+.3f}  (moving zero, bounded [-1,1]; HOLD band ±{self.zer0.DEAD})\n"
            f"CONFIRMED REFERENCE STATE:\n{self.confirmed or '(none yet)'}\n"
            f"LAST VOID: {last.get('verdict', '-')} — {last.get('note', '')}\n"
        )

    def step(self) -> dict:
        if self.stop:
            raise RuntimeError(f"loop already stopped: {self.stop}")
        self.turn += 1
        t0 = time.time()
        query = " ".join([self.goal, self.last_void.get("note", ""), self.confirmed[-600:]])
        lens_txt = self.lens.render(query)

        field_text = self.field_ai.complete(FIELD_ROLE + "\n" + lens_txt, self._state_block())
        good, bad = self.lens.cited_paths(field_text)

        void_user = (self._state_block() + "\nFIELD PROPOSAL:\n" + field_text +
                     f"\n\nDETERMINISTIC CITATION CHECK: exist={good} missing={bad}\n")
        void_text = self.void_ai.complete(VOID_ROLE + "\n" + lens_txt, void_user)
        v = parse_void(void_text)

        x = grounding_score(good, bad)
        y = 0.5 * (VERDICT_VALUE[v["verdict"]] + v["reference"])
        z = v["goal"]
        t = self.turn / self.max_turns
        ref_in = self.ref
        ev = self.zer0.shared_event(ref_in, {"X": x, "Y": y, "Z": z, "T": t})
        resolved = ev["resolved"]
        self.ref = ev["new_ref"]

        if resolved == "+":
            self.confirmed = field_text.strip()
            self.holds, self.denials = 0, 0
        elif resolved == "-":
            self.denials += 1
            self.holds = 0
        else:
            self.holds += 1

        if v["verdict"] == "ESCALATE":
            self.stop = "ESCALATE"
        elif self.denials >= 3:
            self.stop = "THREE_STRIKES"
        elif self.holds >= 2:
            self.stop = "SETTLED"
        elif self.turn >= self.max_turns:
            self.stop = "HARD_STOP"
        self.last_void = v

        rec = {
            "kind": "software-field-void-pair",
            "turn": self.turn,
            "field": {"provider": self.field_ai.name, "model": self.field_ai.model, "text": field_text},
            "void": {"provider": self.void_ai.name, "model": self.void_ai.model, "text": void_text, **v},
            "citations": {"exist": good, "missing": bad},
            "zer0": {
                "inputs": {"X": round(x, 4), "Y": round(y, 4), "Z": round(z, 4), "T": round(t, 4)},
                "choices": ev["choices"],
                "resolved": resolved,
                "ref_in": ref_in,
                "ref_out": self.ref,
            },
            "stop": self.stop,
            "seconds": round(time.time() - t0, 2),
        }
        self.history.append(rec)
        return rec

    def run(self, on_turn=None) -> list:
        while not self.stop:
            try:
                rec = self.step()
            except ProviderError as e:
                self.stop = "PROVIDER_ERROR"
                rec = {"kind": "software-field-void-pair", "turn": self.turn,
                       "error": str(e), "stop": self.stop}
                self.history.append(rec)
            if on_turn:
                on_turn(rec)
        return self.history

    def summary(self) -> dict:
        return {
            "kind": "software-field-void-pair-summary",
            "label": "SOFTWARE_ONLY",
            "goal": self.goal,
            "reference_point_zero": self.snapshot,
            "field": f"{self.field_ai.name}:{self.field_ai.model}",
            "void": f"{self.void_ai.name}:{self.void_ai.model}",
            "turns": self.turn,
            "stop": self.stop,
            "final_ref": self.ref,
            "confirmed": self.confirmed,
        }

    def write_ledger(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            for rec in self.history:
                f.write(json.dumps(rec) + "\n")
            f.write(json.dumps(self.summary()) + "\n")
        return path
