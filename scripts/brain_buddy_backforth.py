#!/usr/bin/env python3
"""Live two-AI back and forth.

Gemini and DeepSeek. Reference is forced in front of every turn.
One seat speaks. The other answers that turn, not a private monologue.
A finished seat does not idle: it writes the journal and takes the next handoff.
Stop when the latest turn has no open objection, missing repo file, or next test.
A loop cap is a stop, not agreement. An absent seat is not a vote.
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from brain_buddy_council import (  # noqa: E402
    CouncilError,
    bounded_prompt,
    repo_root,
    run_worker,
)

SEATS = ("gemini", "deepseek")
MAX_TURNS = 8


def journal_path(root: Path) -> Path:
    out = root / "External_Work" / "brain_buddy" / "journal"
    out.mkdir(parents=True, exist_ok=True)
    return out / f"backforth-{time.strftime('%Y%m%d-%H%M%S')}.md"


def other(seat: str) -> str:
    return "deepseek" if seat == "gemini" else "gemini"


def still_open(text: str) -> bool:
    upper = text.upper()
    markers = (
        "DISAGREEMENT:",
        "OPEN QUESTION:",
        "MISSING REFERENCE:",
        "NEXT TEST:",
        "PLAN:",
    )
    return any(marker in upper for marker in markers)


class BackForth:
    def __init__(self, root: Path, question: str, timeout: int, first: str) -> None:
        self.root = root
        self.question = question
        self.timeout = timeout
        self.first = first
        self.turns: list[dict[str, str]] = []
        self.absent: dict[str, str] = {}
        self.path = journal_path(root)
        self._flush("OPEN", "live back-and-forth started from forced reference")

    def _flush(self, seat: str, text: str) -> None:
        self.turns.append({"speaker": seat, "text": text.strip()})
        body = [
            "# Live back-and-forth journal",
            "",
            "Reference first. One speaker, then the other answers that turn.",
            "",
            f"- question: {self.question}",
            f"- first seat: {self.first}",
            "",
        ]
        for turn in self.turns:
            body.append(f"## {turn['speaker']}\n\n{turn['text']}\n")
        self.path.write_text("\n".join(body) + "\n", encoding="utf-8")

    def transcript(self) -> str:
        lines = []
        for turn in self.turns:
            if turn["speaker"] == "OPEN":
                continue
            lines.append(f"{turn['speaker'].upper()}:\n{turn['text']}")
        return "\n\n".join(lines)

    def prompt_for(self, seat: str, turn_no: int) -> str:
        peer = other(seat)
        if not any(turn["speaker"] in SEATS for turn in self.turns):
            task = f"""FIRST TURN

You are {seat}. {peer} has not spoken.
Start from the forced reference, then the repo files this question needs.
Give your answer. Name the exact repo paths you used.
End with one of:
- DISAGREEMENT: <claim the other seat should attack>
- OPEN QUESTION: <unresolved point>
- MISSING REFERENCE: <path>
- NEXT TEST: <concrete check>
- CLOSED: <claim that already survives the reference>
"""
        else:
            task = f"""HANDOFF {turn_no}

You are {seat}. Answer {peer}'s latest turn. Do not restart from scratch.
The forced reference outranks the transcript.
Attack or confirm the latest claim against the repo.
If you finish this turn and {peer} is not back yet, say what repo pass you will run next.
Do not idle and do not invent {peer}'s agreement.
End with one of DISAGREEMENT, OPEN QUESTION, MISSING REFERENCE, NEXT TEST, or CLOSED.

TRANSCRIPT:
---
{self.transcript()}
---
"""
        return bounded_prompt(self.root, self.question, task)

    def speak(self, seat: str, turn_no: int) -> bool:
        if seat in self.absent:
            self._flush(seat, f"ABSENT\n{self.absent[seat]}\nNot a vote.")
            return False
        result = run_worker(self.root, seat, self.prompt_for(seat, turn_no), self.timeout)
        text = (result.get("answer") or "").strip()
        if result.get("ok") and text:
            self._flush(seat, text)
            print(f"\n===== {seat.upper()} {turn_no} =====\n{text}")
            return True
        reason = result.get("stderr") or f"exit {result.get('exit_code')}"
        self.absent[seat] = reason
        self._flush(seat, f"ABSENT\n{reason}\nNot a vote.")
        print(f"\n===== {seat.upper()} ABSENT =====\n{reason}")
        return False

    def run(self) -> int:
        seat = self.first
        for turn_no in range(1, MAX_TURNS + 1):
            ok = self.speak(seat, turn_no)
            spoken = [turn for turn in self.turns if turn["speaker"] in SEATS and not turn["text"].startswith("ABSENT")]
            if len(self.absent) == 2:
                self._flush("RESPONSE", "NOT READY\nNeither seat returned.")
                break
            if spoken and not still_open(spoken[-1]["text"]) and len(spoken) >= 2:
                self._flush(
                    "RESPONSE",
                    "READY\nLatest turn closed and the other seat had a real return. "
                    "Journal is the record. This script does not update the repo or Baseline Zero.",
                )
                break
            if not ok and len(spoken) >= 1:
                self._flush(
                    "RESPONSE",
                    f"READY WITH ABSENCE\n{seat} did not return and is not a vote. "
                    "The live seat keeps the last real answer. Not consensus.",
                )
                break
            if turn_no == MAX_TURNS:
                self._flush(
                    "RESPONSE",
                    "STOP\nTurn cap hit. Not agreement. Open markers stay open.",
                )
                break
            seat = other(seat)
        print(f"\nJournal: {self.path.relative_to(self.root)}")
        return 0 if any(turn["speaker"] == "RESPONSE" and turn["text"].startswith("READY") for turn in self.turns) else 2


def main() -> int:
    ap = argparse.ArgumentParser(description="Live Gemini <-> DeepSeek back and forth")
    ap.add_argument("question")
    ap.add_argument("--first", choices=SEATS, default="gemini")
    ap.add_argument("--timeout", type=int, default=240)
    args = ap.parse_args()
    question = args.question.strip()
    if not question:
        raise CouncilError("Question is empty.")
    return BackForth(repo_root(), question, args.timeout, args.first).run()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CouncilError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
