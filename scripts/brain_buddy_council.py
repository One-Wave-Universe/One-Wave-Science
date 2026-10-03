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
import re
import subprocess
import signal
import sys
import textwrap
import time
from typing import Any

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
    "field-void",
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
    try:
        is_file = p.is_file()
    except OSError:
        is_file = False
    if is_file:
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


def run_worker(root: Path, worker: str, prompt: str, timeout: int, fast: bool = False) -> dict[str, Any]:
    if worker == "gemini":
        cmd = ["python3", "One_Wave_Bench/hive-pipe/gemini_web_bridge.py"]
        if fast:
            cmd.append("--no-tools")
        cmd += ["--max-tool-rounds", "1" if fast else "12", prompt]
    elif worker == "deepseek":
        cmd = ["python3", "One_Wave_Bench/hive-pipe/deepseek_web_bridge.py"]
        if fast:
            cmd += ["--no-deepthink", "--no-tools"]
        cmd += ["--max-tool-rounds", "1" if fast else "12", prompt]
    else:
        raise CouncilError(f"Unknown worker: {worker}")

    started = time.monotonic()
    worker_env = os.environ.copy()
    if worker == "deepseek":
        worker_env.setdefault("DEEPSEEK_WEB_BASE_URL", "http://192.168.55.100:3000")
        worker_env.setdefault("DEEPSEEK_WEB_API_KEY", "usb-local")
    elif worker == "gemini":
        worker_env.setdefault("GEMINI_WEB_BASE_URL", "http://192.168.55.100:3001")

    proc = subprocess.Popen(
        cmd,
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=worker_env,
        start_new_session=True,
    )
    try:
        stdout, stderr = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(proc.pid, signal.SIGTERM)
            stdout, stderr = proc.communicate(timeout=3)
        except (ProcessLookupError, subprocess.TimeoutExpired):
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            stdout, stderr = proc.communicate()
        elapsed = round(time.monotonic() - started, 3)
        return {
            "worker": worker,
            "ok": False,
            "exit_code": 124,
            "elapsed_s": elapsed,
            "answer": "",
            "stderr": f"Timed out after {timeout}s; terminated the provider process group cleanly.",
        }

    elapsed = round(time.monotonic() - started, 3)
    stdout = (stdout or "").strip()
    stderr = (stderr or "").strip()
    answer = stdout

    return {
        "worker": worker,
        "ok": proc.returncode == 0,
        "exit_code": proc.returncode,
        "elapsed_s": elapsed,
        "answer": answer,
        "stderr": stderr,
    }


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




def science_context_packet(root: Path, question: str, max_files: int = 1) -> str:
    """Build a bounded repo-first packet with YAML metadata before provider calls."""
    stop = {"that", "this", "with", "from", "where", "would", "make", "more", "only", "one", "active", "science", "wave", "claim", "small", "change"}
    words = [w.lower() for w in re.findall(r"[A-Za-z0-9_-]{4,}", question) if w.lower() not in stop]
    candidates: list[tuple[int, Path, str]] = []
    for directory in (root / "Nodes", root / "Root_Axioms"):
        if not directory.is_dir():
            continue
        for path in directory.glob("*.md"):
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            hay = (path.name + "\n" + text[:12000]).lower()
            score = sum(hay.count(w) for w in words)
            if score:
                candidates.append((score, path, text))
    candidates.sort(key=lambda x: (-x[0], str(x[1])))
    chosen = candidates[:max_files]
    if not chosen:
        # Deterministic fallback: first governed nodes, still carrying I-06 metadata.
        for path in sorted((root / "Nodes").glob("*.md"))[:max_files]:
            chosen.append((0, path, path.read_text(encoding="utf-8", errors="replace")))
    blocks = [
        "REPO CONTEXT PACKET — extracted locally before provider calls",
        "Metadata authority: Governance_I_Series/I-06_Canonical_Node_Metadata_and_Alias_Resolution.md",
    ]
    for _score, path, text in chosen:
        rel = path.relative_to(root)
        # Keep front matter plus enough body to reason, bounded for relay stability.
        snippet = text[:2200]
        blocks.append(f"FILE: {rel}\n---\n{snippet}\n---")
    return "\n\n".join(blocks)


FIELD_VOID_RULES = """FIELD / VOID SCIENCE PAIR

FIELD = Gemini-Field. VOID = Gemini-Void. These are independent provider calls using opposing roles; do not describe Gemini-Void as DeepSeek.
Both are equal counter-views. Neither is authority.
Both must independently reference the repository and I-06 metadata for every node used.
Use the six-step structure recursively inside any subproblem: reference -> define -> inspect metadata -> reason/test -> counter-check -> return/update.
On confusion, assumption, drift, or contradiction: re-reference before continuing.
Do not change gate or lifecycle unless the evidence for that change is explicitly part of the task.
Do not invent measurements, experiments, citations, or provider actions.
The goal is one small, exact, repo-grounded science improvement, not a broad rewrite. Keep your response under 500 words.
"""


def field_prompt(question: str, context: str, prior: str = "") -> str:
    extra = FIELD_VOID_RULES + "\n\n" + context + """

NO TOOL CALLS ARE NEEDED. Work only from the repo packet above.
You are FIELD. Expand the strongest useful interpretation, but stay inside what the repo and metadata support.
Locate the exact node/chapter/file involved. Read its YAML metadata before reasoning.
Propose the smallest science update that improves clarity, testability, equations, evidence boundaries, or cross-links.
State exact repo paths and preserve established-vs-hypothesis boundaries.
"""
    if prior:
        extra += "\nVOID'S LAST COUNTER-VIEW:\n---\n" + prior + "\n---\nRe-reference every disputed point and either correct it or defend it with exact repo evidence.\n"
    extra += """
End with exactly one line:
FIELD_STATUS: PROPOSED
FIELD_STATUS: HOLD
"""
    return bounded_prompt(question, extra)


def void_prompt(question: str, context: str, field_answer: str, prior: str = "") -> str:
    extra = FIELD_VOID_RULES + "\n\n" + context + f"""

NO TOOL CALLS ARE NEEDED. Work only from the repo packet above.
You are VOID. Compress, challenge, and falsify FIELD's proposal.
Independently reference the repo and metadata; do not trust FIELD's citations without checking them.

FIELD PROPOSAL:
---
{field_answer}
---
"""
    if prior:
        extra += "\nYOUR PRIOR COUNTER-VIEW:\n---\n" + prior + "\n---\nCheck whether FIELD actually resolved it.\n"
    extra += """
Identify unsupported claims, metadata conflicts, missing tests, duplicated nodes, or overstatement.
If the proposal is now a small safe science update, accept it. Otherwise you may either challenge it or submit a better counter-proposal.
A counter-proposal must include the exact correction you want made, the repo path it applies to, and why it is better grounded in the repo/metadata.

End with exactly one line:
VOID_STATUS: ACCEPT
VOID_STATUS: COUNTER_PROPOSE
VOID_STATUS: CHALLENGE
VOID_STATUS: HOLD
"""
    return bounded_prompt(question, extra)


def field_void_status(text: str, role: str) -> str:
    key = role.upper() + "_STATUS:"
    for line in reversed(text.splitlines()):
        line = line.strip().upper()
        if line.startswith(key):
            return line.split(":", 1)[1].strip()
    return "HOLD"


def save_science_packet(root: Path, question: str, turns: list[dict[str, str]], outcome: str) -> Path:
    out = root / "External_Work" / "brain_buddy" / "science_updates"
    out.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    path = out / f"field-void-{stamp}.md"
    body = [
        "# Field / Void science update packet", "",
        f"- outcome: {outcome}",
        "- authority: repository + I-06 metadata",
        "- status: proposal only; canonical science files are unchanged until reviewed/applied on a branch",
        "", "## Question", "", question, "", "## Back-and-forth", "", transcript_text(turns), ""
    ]
    path.write_text("\n".join(body), encoding="utf-8")
    return path


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
        ("7", "field-void", "Field/Void science pair"),
    ]
    for n, _, label in options:
        print(f"  {n}. {label}")
    selected = input("Choose 1-7: ").strip()
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
    ap.add_argument("--max-loops", type=int, default=6, help="Operator safety budget for field-void; reaching it stays unresolved")
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

    elif mode == "field-void":
        context = science_context_packet(root, question)
        print("\n[FIELD/VOID] Repo packet built locally with governed metadata.", flush=True)
        field = run_worker(root, "gemini", field_prompt(question, context), args.timeout, fast=True)
        print_result(field)
        turns.append({"speaker": "field-gemini", "text": field["answer"] or field["stderr"]})
        if not field["ok"] or field_void_status(field["answer"], "field") == "HOLD":
            outcome = "FIELD_HOLD"
        else:
            outcome = "UNRESOLVED"
            previous_void = ""
            for loop_no in range(1, max(1, args.max_loops) + 1):
                void = run_worker(root, "gemini", void_prompt(question, context, field["answer"], previous_void), args.timeout, fast=True)
                print_result(void)
                turns.append({"speaker": "void-gemini", "text": void["answer"] or void["stderr"]})
                if not void["ok"]:
                    outcome = "VOID_UNAVAILABLE"
                    break
                vstatus = field_void_status(void["answer"], "void")
                if vstatus == "ACCEPT":
                    outcome = "UPDATE_READY"
                    break
                if vstatus == "HOLD":
                    outcome = "VOID_HOLD"
                    break
                if vstatus == "COUNTER_PROPOSE":
                    outcome = "COUNTER_PROPOSAL_ACTIVE"
                previous_void = void["answer"]
                field = run_worker(root, "gemini", field_prompt(question, context, previous_void), args.timeout, fast=True)
                print_result(field)
                turns.append({"speaker": "field-gemini", "text": field["answer"] or field["stderr"]})
                if not field["ok"] or field_void_status(field["answer"], "field") == "HOLD":
                    outcome = "FIELD_HOLD"
                    break
            else:
                outcome = "OPERATOR_LIMIT_UNRESOLVED"
        packet = save_science_packet(root, question, turns, outcome)
        print(f"\nFIELD/VOID OUTCOME: {outcome}")
        print(f"Science update packet: {packet.relative_to(root)}")

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