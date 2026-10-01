#!/usr/bin/env python3
"""Unified Gemini + DeepSeek Brain Buddy Council.

Modes:
  gemini
  deepseek
  both
  gemini-deepseek
  deepseek-gemini
  discussion

The council is orchestration only. Each worker still enters through its existing
bounded wrapper and the canonical One-Wave reference rules.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import textwrap
import time
from typing import Any

from brain_buddy_oversight import baseline_zero, field_path, local_turn_prompt, parse_oversight
from brain_buddy_transports import TransportError, run as run_transport

ROOT_FILES = (
    "GENERAL_REFERENCE_RULES.md",
    "AI_CANONICAL_START_HERE.md",
    "Governance_I_Series/I-06_Canonical_Node_Metadata_and_Alias_Resolution.md",
)

MODES = (
    "gemini",
    "deepseek",
    "both",
    "gemini-deepseek",
    "deepseek-gemini",
    "discussion",
)

REFERENCE_PREAMBLE = """BRAIN BUDDY COUNCIL — ONE-WAVE REFERENCE + RESEARCH CONTRACT\n\nBefore answering:\n1. Reference GENERAL_REFERENCE_RULES.md.\n2. Reference AI_CANONICAL_START_HERE.md.\n3. Reference Governance_I_Series/I-06_Canonical_Node_Metadata_and_Alias_Resolution.md.\n4. Read YAML/front-matter metadata for every governed node actually used.\n5. Reference only the exact task-specific repo files needed after those authorities.\n6. Define the exact claim/test before external research.\n7. If current literature, measurements, CERN/LIGO/public data, or outside claims are needed, research them only after the repo claim/test is defined.\n8. Keep external source metadata/provenance distinct from One-Wave node metadata.\n9. Distinguish established external evidence from One-Wave hypotheses.\n10. Bring external findings back to the exact repo claim and classify them as support, contradiction, or inconclusive.\n11. Do not claim any command, experiment, or external lookup ran without a receipt/source.\n12. Do not edit, commit, merge, push, or expose secrets.\n13. Cite exact repo paths and external sources actually used.\n14. Return HOLD with the exact missing reference/evidence if grounding cannot be completed.\n\nReference/research loop:\nREFERENCE GIT -> DEFINE CLAIM/TEST -> I-06 METADATA -> EXTERNAL RESEARCH/DATA AS NEEDED -> VALIDATE -> RETURN TO REFERENCE\n"""


class CouncilError(RuntimeError):
    pass


def repo_root() -> Path:
    p = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        text=True,
        capture_output=True,
        check=False,
    )
    if p.returncode != 0:
        raise CouncilError("Run Brain Buddy Council inside One-Wave-Science.")
    root = Path(p.stdout.strip()).resolve()
    remote = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    ).stdout.strip()
    if "One-Wave-Universe/One-Wave-Science" not in remote:
        raise CouncilError(f"Unexpected repository origin: {remote}")
    for name in ROOT_FILES:
        if not (root / name).exists():
            raise CouncilError(f"Required canonical reference missing: {name}")
    return root


def read_prompt(value: str) -> str:
    p = Path(value)
    if p.is_file():
        data = p.read_text(encoding="utf-8")
        if len(data.encode("utf-8")) > 16000:
            raise CouncilError("Prompt file exceeds 16 KB; reference large repo files by path.")
        return data.strip()
    return value.strip()


def gemini_text(raw: str) -> str:
    """Extract useful text from Gemini CLI JSON while tolerating CLI revisions."""
    value = raw.strip()
    if not value:
        return ""
    try:
        obj = json.loads(value)
    except json.JSONDecodeError:
        return value

    if isinstance(obj, str):
        return obj
    if not isinstance(obj, dict):
        return value

    for key in ("response", "text", "content", "output"):
        v = obj.get(key)
        if isinstance(v, str) and v.strip():
            return v.strip()

    # Gemini CLI commonly returns a nested result/candidates structure.
    result = obj.get("result")
    if isinstance(result, str) and result.strip():
        return result.strip()
    if isinstance(result, dict):
        for key in ("response", "text", "content", "output"):
            v = result.get(key)
            if isinstance(v, str) and v.strip():
                return v.strip()

    candidates = obj.get("candidates")
    if isinstance(candidates, list):
        chunks: list[str] = []
        for candidate in candidates:
            if not isinstance(candidate, dict):
                continue
            content = candidate.get("content")
            if isinstance(content, str):
                chunks.append(content)
            elif isinstance(content, dict):
                parts = content.get("parts")
                if isinstance(parts, list):
                    for part in parts:
                        if isinstance(part, dict) and isinstance(part.get("text"), str):
                            chunks.append(part["text"])
        if chunks:
            return "\n".join(x.strip() for x in chunks if x.strip())

    return value


def run_worker_raw(root: Path, worker: str, prompt: str, timeout: int) -> dict[str, Any]:
    started = time.monotonic()
    try:
        answer = run_transport(root, worker, prompt, timeout)
        return {
            "worker": worker, "ok": True, "exit_code": 0,
            "elapsed_s": round(time.monotonic() - started, 3),
            "answer": answer, "stderr": "",
        }
    except TransportError as exc:
        return {
            "worker": worker, "ok": False, "exit_code": 1,
            "elapsed_s": round(time.monotonic() - started, 3),
            "answer": "", "stderr": str(exc),
        }



def run_worker(root: Path, worker: str, prompt: str, timeout: int) -> dict[str, Any]:
    """Run one worker turn with a local M4 transcript loop; outer Council routing is unchanged."""
    zero = baseline_zero(root)
    path = field_path(prompt)

    # Direct Field is a legitimate fast path: speak/act without a preceding
    # local-dialogue turn. It still returns through the unchanged outer Council.
    if path == "DIRECT":
        field = run_worker_raw(root, worker, prompt, timeout)
        field["local_state"] = {"state": "DIRECT", "reason": "explicit direct Field request"}
        field["local_transcript"] = [
            {"speaker": "field-task", "text": prompt},
            {"speaker": "field-result", "text": field["answer"] if field["ok"] else field["stderr"]},
        ]
        field["baseline_zero"] = zero
        return field

    local_turns: list[dict[str, str]] = [
        {"speaker": "field-task", "text": prompt},
    ]

    # The local loop mirrors Council's transcript pattern at the worker scale.
    # It is intentionally bounded to one explicit Void/self-reference turn per
    # outward Council turn until live testing justifies more autonomous cycling.
    local = run_worker_raw(
        root,
        worker,
        local_turn_prompt(worker, zero, prompt, local_turns),
        timeout,
    )
    if not local["ok"]:
        return local

    local_turns.append({"speaker": "void", "text": local["answer"]})
    decision = parse_oversight(local["answer"])
    if decision["state"] == "HOLD":
        return {
            "worker": worker,
            "ok": True,
            "exit_code": 0,
            "elapsed_s": local["elapsed_s"],
            "answer": "HOLD — local M4 loop: " + decision["reason"],
            "stderr": "",
            "local_state": decision,
            "local_transcript": local_turns,
            "baseline_zero": zero,
        }

    field_prompt = (
        prompt
        + "\n\nLOCAL M4 SELF-REFERENCE (explicit operational state):\n"
        + transcript_text(local_turns)
        + "\n\nSHARED BASELINE ZERO (external project reference):\n"
        + json.dumps(zero, indent=2, sort_keys=True)
        + "\n\nPerform the NEXT action from your local state now. "
          "Re-reference exact repo files when the task requires shared project truth."
    )
    field = run_worker_raw(root, worker, field_prompt, timeout)
    local_turns.append({
        "speaker": "field-result",
        "text": field["answer"] if field["ok"] else field["stderr"],
    })
    field["local_state"] = decision
    field["local_transcript"] = local_turns
    field["baseline_zero"] = zero
    field["elapsed_s"] = round(local["elapsed_s"] + field["elapsed_s"], 3)
    return field

def bounded_prompt(question: str, extra: str = "") -> str:
    blocks = [REFERENCE_PREAMBLE, "USER QUESTION:\n" + question]
    if extra.strip():
        blocks.append(extra.strip())
    return "\n\n".join(blocks)


def print_result(result: dict[str, Any]) -> None:
    name = result["worker"].upper()
    print(f"\n===== {name} =====")
    if result["ok"]:
        print(result["answer"])
    else:
        print(f"HOLD — {name} worker failed (exit {result['exit_code']}).")
        if result["stderr"]:
            print(result["stderr"])


def transcript_text(turns: list[dict[str, str]]) -> str:
    return "\n\n".join(f"{t['speaker'].upper()}:\n{t['text']}" for t in turns)


def run_parallel(root: Path, prompt: str, timeout: int) -> list[dict[str, Any]]:
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:
        futures = {
            ex.submit(run_worker, root, worker, prompt, timeout): worker
            for worker in ("gemini", "deepseek")
        }
        by_name = {}
        for f in concurrent.futures.as_completed(futures):
            result = f.result()
            by_name[result["worker"]] = result
    return [by_name["gemini"], by_name["deepseek"]]


def handoff_prompt(question: str, first_name: str, first_answer: str) -> str:
    return bounded_prompt(
        question,
        f"""PEER HANDOFF

{first_name.upper()} answered first:
---
{first_answer}
---

Review that answer against the canonical repo references. Identify agreements,
disagreements, unsupported claims, and the strongest correction or extension.
Do not merely summarize the peer. Finish with your own current answer.""",
    )


def discussion_turn_prompt(
    question: str,
    turns: list[dict[str, str]],
    worker: str,
    round_no: int,
) -> str:
    peer = "DeepSeek" if worker == "gemini" else "Gemini"
    return bounded_prompt(
        question,
        f"""OPEN COUNCIL DISCUSSION — ROUND {round_no}

Participants are the user, Gemini, and DeepSeek.
You are {worker.title()}. {peer} is a peer reviewer, not an authority.
The user controls the question and may redirect the discussion.

DISCUSSION SO FAR:
---
{transcript_text(turns)}
---

Respond to the latest state of the discussion. Address the other participant's
strongest point directly. Preserve unresolved disagreements instead of forcing
consensus. Check disputed claims against the repository reference chain.
End with either:
- AGREEMENT: <specific point>
- DISAGREEMENT: <specific point>
- OPEN QUESTION: <specific next test>
You may use more than one of those labels.""",
    )


def interactive_user_turn(round_no: int) -> str:
    if not sys.stdin.isatty():
        return ""
    print(
        f"\n[You — after round {round_no}] Enter a reply/redirection, "
        "press Enter to let them continue, or type /stop:"
    )
    try:
        return input("> ").strip()
    except EOFError:
        return ""


def save_transcript(root: Path, mode: str, question: str, turns: list[dict[str, str]]) -> Path:
    out = root / "External_Work" / "brain_buddy" / "outbox"
    out.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    path = out / f"council-{mode}-{stamp}.md"
    body = [
        "# Brain Buddy Council transcript",
        "",
        f"- mode: {mode}",
        f"- repository: One-Wave-Universe/One-Wave-Science",
        "",
        "## User question",
        "",
        question,
        "",
        "## Discussion",
        "",
        transcript_text(turns),
        "",
    ]
    path.write_text("\n".join(body), encoding="utf-8")
    return path


def choose_mode() -> str:
    print("Brain Buddy Council")
    options = [
        ("1", "gemini", "Gemini only"),
        ("2", "deepseek", "DeepSeek only"),
        ("3", "both", "Both independently / parallel"),
        ("4", "gemini-deepseek", "Gemini first, then DeepSeek reviews"),
        ("5", "deepseek-gemini", "DeepSeek first, then Gemini reviews"),
        ("6", "discussion", "Open Gemini + DeepSeek + user discussion"),
    ]
    for n, _, label in options:
        print(f"  {n}. {label}")
    selected = input("Choose 1-6: ").strip()
    for n, mode, _ in options:
        if selected == n:
            return mode
    raise CouncilError("Invalid selection.")


def main() -> int:
    ap = argparse.ArgumentParser(description="Unified Gemini + DeepSeek Brain Buddy Council")
    ap.add_argument("mode", nargs="?", choices=MODES)
    ap.add_argument("question", nargs="?")
    ap.add_argument("--rounds", type=int, default=2, help="Discussion rounds; default 2")
    ap.add_argument("--timeout", type=int, default=240, help="Per-worker timeout in seconds")
    ap.add_argument("--save", action="store_true", help="Save a transcript receipt under External_Work")
    args = ap.parse_args()

    root = repo_root()
    mode = args.mode
    question = args.question

    if mode is None:
        if not sys.stdin.isatty():
            raise CouncilError("Mode required in non-interactive use.")
        mode = choose_mode()
    if not question:
        if not sys.stdin.isatty():
            raise CouncilError("Question required in non-interactive use.")
        question = input("Question / task: ").strip()
    question = read_prompt(question)
    if not question:
        raise CouncilError("Question is empty.")

    turns: list[dict[str, str]] = [{"speaker": "user", "text": question}]
    base = bounded_prompt(question)

    if mode == "gemini":
        r = run_worker(root, "gemini", base, args.timeout)
        print_result(r)
        turns.append({"speaker": "gemini", "text": r["answer"] or r["stderr"]})

    elif mode == "deepseek":
        r = run_worker(root, "deepseek", base, args.timeout)
        print_result(r)
        turns.append({"speaker": "deepseek", "text": r["answer"] or r["stderr"]})

    elif mode == "both":
        for r in run_parallel(root, base, args.timeout):
            print_result(r)
            turns.append({"speaker": r["worker"], "text": r["answer"] or r["stderr"]})

    elif mode in ("gemini-deepseek", "deepseek-gemini"):
        first, second = (
            ("gemini", "deepseek")
            if mode == "gemini-deepseek"
            else ("deepseek", "gemini")
        )
        r1 = run_worker(root, first, base, args.timeout)
        print_result(r1)
        turns.append({"speaker": first, "text": r1["answer"] or r1["stderr"]})
        if r1["ok"]:
            r2 = run_worker(
                root,
                second,
                handoff_prompt(question, first, r1["answer"]),
                args.timeout,
            )
            print_result(r2)
            turns.append({"speaker": second, "text": r2["answer"] or r2["stderr"]})
        else:
            print(f"\nHOLD — sequential handoff stopped because {first} failed.")

    elif mode == "discussion":
        rounds = max(1, min(args.rounds, 12))
        for round_no in range(1, rounds + 1):
            for worker in ("gemini", "deepseek"):
                prompt = discussion_turn_prompt(question, turns, worker, round_no)
                r = run_worker(root, worker, prompt, args.timeout)
                print_result(r)
                turns.append({"speaker": worker, "text": r["answer"] or r["stderr"]})
                if not r["ok"]:
                    print(f"HOLD — {worker} failed; discussion continues with available participants.")
            user_turn = interactive_user_turn(round_no)
            if user_turn == "/stop":
                break
            if user_turn:
                turns.append({"speaker": "user", "text": user_turn})
                question = question + "\n\nUSER REDIRECTION:\n" + user_turn

    if args.save:
        path = save_transcript(root, mode, question, turns)
        print(f"\nTranscript receipt: {path.relative_to(root)}")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except CouncilError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
