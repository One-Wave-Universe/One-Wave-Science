#!/usr/bin/env python3
"""Two-AI council. No idle wait.

Gemini and DeepSeek start from the forced reference and work the same problem.
When one finishes a loop, it does not sit. It looks over the repo, plans more
work, and writes the journal until the response is ready.

Response ready means both seats have a real return, or one seat is absent and
the live seat has recorded that absence. Absence is not a vote.
"""
from __future__ import annotations

import sys
import threading
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
MAX_LOOPS = 6


def journal_path(root: Path) -> Path:
    out = root / "External_Work" / "brain_buddy" / "journal"
    out.mkdir(parents=True, exist_ok=True)
    return out / f"pair-{time.strftime('%Y%m%d-%H%M%S')}.md"


class Pair:
    def __init__(self, root: Path, question: str, timeout: int) -> None:
        self.root = root
        self.question = question
        self.timeout = timeout
        self.lock = threading.Lock()
        self.entries: list[str] = []
        self.answers: dict[str, str] = {}
        self.absent: dict[str, str] = {}
        self.loops: dict[str, int] = {name: 0 for name in SEATS}
        self.path = journal_path(root)
        self._write("OPEN", "pair started from forced reference")

    def _write(self, seat: str, text: str) -> None:
        line = f"## {time.strftime('%H:%M:%S')} {seat}\n\n{text.strip()}\n"
        with self.lock:
            self.entries.append(line)
            body = [
                "# Two-AI journal",
                "",
                "Reference first. No idle wait. Journal until the response is ready.",
                "",
                f"- question: {self.question}",
                "",
                *self.entries,
                "",
            ]
            self.path.write_text("\n".join(body), encoding="utf-8")

    def snapshot(self) -> str:
        with self.lock:
            parts = []
            for name in SEATS:
                if name in self.answers:
                    parts.append(f"{name} ANSWER:\n{self.answers[name]}")
                elif name in self.absent:
                    parts.append(f"{name} ABSENT: {self.absent[name]}")
                else:
                    parts.append(f"{name}: still in its loop")
            parts.append("JOURNAL:\n" + "\n".join(self.entries[-6:]))
            return "\n\n".join(parts)

    def ready(self) -> bool:
        with self.lock:
            done = [name for name in SEATS if name in self.answers or name in self.absent]
            return len(done) == 2 and any(name in self.answers for name in SEATS)

    def prompt_for(self, seat: str) -> str:
        other = "deepseek" if seat == "gemini" else "gemini"
        state = self.snapshot()
        if seat not in self.answers and seat not in self.absent:
            extra = f"""FIRST PASS

You are {seat}. The other seat is {other}.
Start from the forced reference above, then the repo files the question needs.
Give your own answer. Do not wait for {other}.
End with PLAN: the next repo check you would run if you finish before {other}.

CURRENT STATE:
{state}
"""
        else:
            extra = f"""NO IDLE

You already finished a loop. Do not wait for {other}.
Look over the repo again. Plan more work. Write what changed in your view.
If {other} has an answer, attack or confirm it against the reference.
If {other} is still out, keep working the claim.
End with PLAN: the next concrete repo pass.

CURRENT STATE:
{state}
"""
        return bounded_prompt(self.root, self.question, extra)

    def one_loop(self, seat: str) -> None:
        self.loops[seat] += 1
        result = run_worker(self.root, seat, self.prompt_for(seat), self.timeout)
        text = (result.get("answer") or result.get("stderr") or "").strip()
        if result.get("ok") and text:
            with self.lock:
                self.answers[seat] = text
            self._write(seat, text)
        else:
            reason = result.get("stderr") or f"exit {result.get('exit_code')}"
            with self.lock:
                self.absent[seat] = reason
            self._write(seat, f"ABSENT\n{reason}")

    def seat_loop(self, seat: str) -> None:
        while self.loops[seat] < MAX_LOOPS and not self.ready():
            self.one_loop(seat)
        if self.answers.get(seat) and not self.ready():
            self._write(seat, "loop cap hit before the other seat returned; not treated as agreement")

    def run(self) -> int:
        threads = [threading.Thread(target=self.seat_loop, args=(seat,), daemon=True) for seat in SEATS]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self._write("RESPONSE", self.best())
        print(self.path.read_text(encoding="utf-8"))
        print(f"\nJournal: {self.path.relative_to(self.root)}")
        return 0 if self.ready() else 2

    def best(self) -> str:
        live = [name for name in SEATS if name in self.answers]
        missing = [name for name in SEATS if name in self.absent]
        if len(live) == 2:
            return (
                "READY\n"
                "Both seats returned. Best answer is the claim that survives the forced reference "
                "and the other seat's objection. Disagreements stay in the journal. "
                "This file does not pick a winner and does not update Baseline Zero."
            )
        if len(live) == 1:
            return (
                f"READY WITH ABSENCE\n{missing[0]} did not return and is not a vote. "
                f"{live[0]} kept looping. Its answer is the only real return. "
                "Do not call that consensus."
            )
        return "NOT READY\nNeither seat returned a real answer."


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(description="Two-AI no-idle council")
    ap.add_argument("question")
    ap.add_argument("--timeout", type=int, default=240)
    args = ap.parse_args()
    question = args.question.strip()
    if not question:
        raise CouncilError("Question is empty.")
    return Pair(repo_root(), question, args.timeout).run()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CouncilError as exc:
        print(f"ERROR: {exc}")
        raise SystemExit(2)
