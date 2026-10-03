#!/usr/bin/env python3
"""Unified Gemini + DeepSeek Brain Buddy Council.

Modes:
  gemini
  deepseek
  both
  gemini-deepseek
  deepseek-gemini
  discussion
  lead

The council is orchestration only. Each worker still enters through its existing
bounded wrapper and the canonical One-Wave reference rules.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import subprocess
import sys
import textwrap
import time
from typing import Any, Callable

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
    "lead",
)

# Seats this script can call directly today. ChatGPT/Claude adapters come later.
SEATS = ("gemini", "deepseek")

# Provider states (BRAIN_BUDDY_CANONICAL_RULES.md rules 15, 16, 45).
PENDING = "PENDING"
ACTIVE = "ACTIVE"
OFFLINE = "OFFLINE"
AUTH_FAILURE = "AUTH FAILURE"
INVALID_RETURN = "INVALID RETURN"
OUT_TO_LUNCH = "OUT TO LUNCH"

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


def run_worker(root: Path, worker: str, prompt: str, timeout: int) -> dict[str, Any]:
    if worker == "gemini":
        cmd = ["python3", "One_Wave_Bench/hive-pipe/gemini_web_bridge.py", "--max-tool-rounds", "12", prompt]
    elif worker == "deepseek":
        cmd = ["python3", "One_Wave_Bench/hive-pipe/deepseek_web_bridge.py", "--max-tool-rounds", "12", prompt]
    else:
        raise CouncilError(f"Unknown worker: {worker}")

    started = time.monotonic()
    worker_env = os.environ.copy()
    if worker == "deepseek":
        worker_env.setdefault("DEEPSEEK_WEB_BASE_URL", "http://192.168.55.100:3000")
        worker_env.setdefault("DEEPSEEK_WEB_API_KEY", "usb-local")
    elif worker == "gemini":
        worker_env.setdefault("GEMINI_WEB_BASE_URL", "http://192.168.55.100:3001")

    try:
        p = subprocess.run(
            cmd,
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout,
            env=worker_env,
        )
    except subprocess.TimeoutExpired as exc:
        elapsed = round(time.monotonic() - started, 3)
        return {
            "worker": worker,
            "ok": False,
            "exit_code": 124,
            "elapsed_s": elapsed,
            "answer": "",
            "stderr": f"Timed out after {timeout}s while preserving the other Council participant.",
            "timed_out": True,
        }

    elapsed = round(time.monotonic() - started, 3)
    stdout = p.stdout.strip()
    stderr = p.stderr.strip()
    answer = stdout

    return {
        "worker": worker,
        "ok": p.returncode == 0,
        "exit_code": p.returncode,
        "elapsed_s": elapsed,
        "answer": answer,
        "stderr": stderr,
        "timed_out": False,
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


# ---------------------------------------------------------------------------
# Lead mode: the Rule 50 core.
#
# Whichever seat received the question leads. The lead answers from the repo,
# the other seats review, and the lead refines while a material objection is
# still active. There is no fixed round count: the loop returns when no active
# objection remains, when it stops making progress, when the lead or every
# reviewer is unavailable, or when the user stops it. A transport timeout only
# marks a provider state; it never completes the deliberation.
# ---------------------------------------------------------------------------

RETURN_ID_RE = re.compile(r"^[ \t`*_]*RETURN_ID:[ \t]*`?([A-Za-z0-9-]+)`?[ \t`*_]*$", re.MULTILINE)
VERDICT_RE = re.compile(
    r"^[ \t>*_-]*VERDICT:[ \t*_]*(NO MATERIAL OBJECTION|OBJECTION)\b",
    re.MULTILINE | re.IGNORECASE,
)

FAILURE_PATTERNS = (
    (AUTH_FAILURE, re.compile(r"HTTP(?: Error)? (?:401|403)\b|unauthori[sz]ed|forbidden|not allowed|invalid api key|key is empty|key file|token not found|missing token", re.IGNORECASE)),
    (OUT_TO_LUNCH, re.compile(r"HTTP(?: Error)? 429\b|quota|rate.?limit|usage limit|subscription", re.IGNORECASE)),
    (OFFLINE, re.compile(r"Unable to reach|Connection refused|No route to host|Name or service not known|Temporary failure in name resolution|urlopen error|Network is unreachable", re.IGNORECASE)),
    (INVALID_RETURN, re.compile(r"missing choices|missing message|missing assistant message|non-object JSON|Non-JSON|malformed", re.IGNORECASE)),
)


def classify_failure(result: dict[str, Any], transport_timeout: int) -> tuple[str, str]:
    """Map a failed worker call to an explicit provider state and reason."""
    if result.get("timed_out"):
        return OUT_TO_LUNCH, f"no transport response within {transport_timeout}s"
    stderr = result.get("stderr", "") or ""
    tail = stderr.strip().splitlines()[-1] if stderr.strip() else ""
    for state, pattern in FAILURE_PATTERNS:
        if pattern.search(stderr):
            return state, tail or state.lower()
    return OUT_TO_LUNCH, f"bridge failure (exit {result.get('exit_code')}): {tail}".rstrip(": ")


def new_request_id() -> str:
    return time.strftime("bb-%Y%m%d-%H%M%S-") + secrets.token_hex(3)


def baseline_identity(root: Path) -> str:
    p = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root, text=True, capture_output=True, check=False
    )
    return p.stdout.strip() or "unknown"


def tag_prompt(prompt: str, request_id: str, baseline: str, return_id: str) -> str:
    return (
        f"REQUEST_ID: {request_id}\n"
        f"BASELINE: {baseline}\n"
        "RETURN PATH REQUIREMENT: this reply is not accepted unless it ends with the exact RETURN_ID line supplied below.\n\n"
        f"{prompt}\n\n"
        "RETURN PATH CHECK\n"
        "End your reply with this exact line on its own, unchanged:\n"
        f"RETURN_ID: {return_id}"
    )


def return_repair_prompt(answer: str, return_id: str) -> str:
    return (
        "RETURN PATH REPAIR ONLY. Your previous response reached Brain Buddy, but it omitted the required return marker.\n"
        "Do not redo the task, use tools, add commentary, or change the substance. Re-emit the response below, then end with the exact marker line.\n\n"
        "PREVIOUS RESPONSE:\n---\n" + answer.strip() + "\n---\n\n"
        "End with exactly:\n"
        f"RETURN_ID: {return_id}"
    )


def check_return(answer: str, return_id: str) -> tuple[bool, str]:
    """Verify the reply carries this turn's RETURN_ID; strip the tag line."""
    ids = RETURN_ID_RE.findall(answer)
    body = RETURN_ID_RE.sub("", answer).strip()
    return return_id in ids, body


def parse_verdict(review: str) -> str:
    """Return OBJECTION, NO MATERIAL OBJECTION, or UNCLEAR.

    UNCLEAR counts as unresolved: agreement is never assumed.
    """
    found = VERDICT_RE.findall(review)
    if not found:
        return "UNCLEAR"
    return found[-1].upper()


def normalized(text: str) -> str:
    return " ".join(text.split()).lower()


def lead_answer_prompt(question: str, lead: str) -> str:
    return bounded_prompt(
        question,
        f"""LEAD SEAT

You are {lead.title()}, the lead seat for this request because the user asked
you. Reference the repository first, then give your own complete answer.
Your answer will be reviewed by the other available Council seats.""",
    )


def review_prompt(question: str, lead: str, reviewer: str, answer: str, prior: str) -> str:
    history = ""
    if prior.strip():
        history = f"""
YOUR PREVIOUS REVIEW OF AN EARLIER VERSION:
---
{prior}
---
Check whether the lead's new answer resolves it. Do not repeat an objection the
answer now handles.
"""
    return bounded_prompt(
        question,
        f"""COUNCIL REVIEW

You are {reviewer.title()}. {lead.title()} is the lead seat for this request.
Independently reference the repository; do not rely on the lead's summary of it.

LEAD ANSWER:
---
{answer}
---
{history}
Determine what is supported, unsupported, in conflict with the references,
unclear, improvable, or in need of a test. A material objection must name the
repo path, evidence, or test that the answer gets wrong or omits. Style and
wording preferences are not material.

End with exactly one verdict line:
VERDICT: OBJECTION
or
VERDICT: NO MATERIAL OBJECTION
If OBJECTION, list each one above the verdict as `OBJECTION: <specific point>`.""",
    )


def refine_prompt(question: str, lead: str, answer: str, reviews: dict[str, str], user_note: str) -> str:
    blocks = "\n\n".join(f"{seat.upper()} REVIEW:\n---\n{text}\n---" for seat, text in reviews.items())
    note = f"\nUSER REDIRECTION:\n{user_note}\n" if user_note else ""
    return bounded_prompt(
        question,
        f"""LEAD REFINEMENT

You are {lead.title()}, the lead seat. Your previous answer:
---
{answer}
---

Council reviews with active objections:

{blocks}
{note}
Re-reference the repository on every disputed point. For each objection, either
accept it and correct the answer, or reject it with the specific repo path or
evidence. Agreement is not truth: do not concede a point only because a peer
raised it. Then give your full refined answer.""",
    )


def emit_state(seat: str, state: str, reason: str = "") -> None:
    line = f"[STATE] {seat}: {state}"
    if reason:
        line += f" — {reason}"
    print(line, flush=True)


def run_lead(
    question: str,
    lead: str,
    call: Callable[[str, str], dict[str, Any]],
    *,
    request_id: str,
    baseline: str,
    transport_timeout: int,
    max_loops: int | None = None,
    user_turn: Callable[[int], str] = lambda _n: "",
) -> dict[str, Any]:
    """Run the lead-seat Council loop and return a receipt dict.

    `call(seat, prompt)` must perform a real provider call and return a
    run_worker-shaped result. No answer is ever synthesized here.
    """
    if lead not in SEATS:
        raise CouncilError(f"Lead seat must be one of {', '.join(SEATS)}; got {lead!r}.")

    seats: dict[str, dict[str, Any]] = {
        s: {"role": "lead" if s == lead else "reviewer", "state": "WAITING", "history": []}
        for s in SEATS
    }
    turns: list[dict[str, Any]] = []
    counter = {"n": 0}

    def set_state(seat: str, state: str, turn_id: str, reason: str = "") -> None:
        seats[seat]["state"] = state
        seats[seat]["history"].append({"state": state, "turn": turn_id, "reason": reason})
        emit_state(seat, state, reason)

    def ask(seat: str, kind: str, prompt: str) -> tuple[bool, str]:
        counter["n"] += 1
        turn_id = f"{request_id}-{counter['n']:02d}-{seat}"
        return_id = f"{turn_id}-{secrets.token_hex(3)}"
        set_state(seat, PENDING, turn_id, kind)
        result = call(seat, tag_prompt(prompt, request_id, baseline, return_id))
        record: dict[str, Any] = {
            "turn": turn_id,
            "seat": seat,
            "kind": kind,
            "exit_code": result.get("exit_code"),
            "elapsed_s": result.get("elapsed_s"),
            "return_id": return_id,
            "return_verified": False,
        }
        text = ""
        if not result.get("ok"):
            state, reason = classify_failure(result, transport_timeout)
        elif not (result.get("answer") or "").strip():
            state, reason = INVALID_RETURN, "empty response"
        else:
            verified, text = check_return(result["answer"], return_id)
            record["return_verified"] = verified
            record["return_repair_attempted"] = False
            if not verified:
                # A real provider answer arrived, so make one bounded repair call that only
                # asks that provider to re-emit its answer with the same return marker.
                # The first unverified answer still does not count as participation.
                record["return_repair_attempted"] = True
                repair = call(seat, return_repair_prompt(result["answer"], return_id))
                record["return_repair_exit_code"] = repair.get("exit_code")
                record["return_repair_elapsed_s"] = repair.get("elapsed_s")
                if repair.get("ok") and (repair.get("answer") or "").strip():
                    verified, text = check_return(repair["answer"], return_id)
                    record["return_verified"] = verified
                elif not repair.get("ok"):
                    repair_state, repair_reason = classify_failure(repair, transport_timeout)
                    record["return_repair_state"] = repair_state
                    record["return_repair_reason"] = repair_reason
            if verified:
                state, reason = ACTIVE, kind
            else:
                state, reason = INVALID_RETURN, "reply did not carry this turn's RETURN_ID after one repair attempt"
        record["state"] = state
        record["reason"] = reason
        if state == ACTIVE:
            record["sha256"] = hashlib.sha256(text.encode("utf-8")).hexdigest()
            record["text"] = text
        else:
            # Kept for diagnosis only; never treated as participation.
            record["raw_excerpt"] = ((result.get("answer") or "") + "\n" + (result.get("stderr") or "")).strip()[-800:]
        turns.append(record)
        set_state(seat, state, turn_id, reason)
        return state == ACTIVE, text

    receipt: dict[str, Any] = {
        "request_id": request_id,
        "baseline": baseline,
        "question": question,
        "lead": lead,
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "transport_timeout_s": transport_timeout,
        "max_loops": max_loops,
        "seats": seats,
        "turns": turns,
    }

    def finish(outcome: str, answer: str, open_objections: dict[str, str]) -> dict[str, Any]:
        receipt["outcome"] = outcome
        receipt["final_answer"] = answer
        receipt["open_objections"] = open_objections
        receipt["loops"] = loop
        receipt["refinements"] = sum(1 for t in turns if t["kind"] == "refinement" and t["state"] == ACTIVE)
        receipt["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        return receipt

    loop = 0
    for s in SEATS:
        if s != lead:
            set_state(s, "LISTENING", f"{request_id}-00-{s}")

    ok, answer = ask(lead, "lead_answer", lead_answer_prompt(question, lead))
    if not ok:
        return finish("LEAD_UNAVAILABLE", "", {})

    available = [s for s in SEATS if s != lead]
    prior_review: dict[str, str] = {}
    prior_objection: dict[str, str] = {}
    previous_answer = answer

    while True:
        loop += 1
        reviews: dict[str, str] = {}
        for reviewer in list(available):
            ok, review = ask(
                reviewer,
                "review",
                review_prompt(question, lead, reviewer, answer, prior_review.get(reviewer, "")),
            )
            if ok:
                reviews[reviewer] = review
                prior_review[reviewer] = review
            else:
                available.remove(reviewer)

        if not reviews:
            return finish("NO_REVIEWERS_AVAILABLE", answer, {})

        objections = {s: r for s, r in reviews.items() if parse_verdict(r) != "NO MATERIAL OBJECTION"}
        if not objections:
            return finish("NO_ACTIVE_OBJECTION", answer, {})

        if prior_objection and all(
            normalized(objections[s]) == normalized(prior_objection.get(s, "")) for s in objections
        ):
            return finish("STALLED_UNRESOLVED", answer, objections)
        prior_objection = dict(objections)

        if max_loops is not None and loop >= max_loops:
            return finish("OPERATOR_LIMIT_UNRESOLVED", answer, objections)

        note = user_turn(loop)
        if note == "/stop":
            return finish("USER_STOPPED", answer, objections)

        ok, refined = ask(lead, "refinement", refine_prompt(question, lead, answer, objections, note))
        if not ok:
            return finish("LEAD_UNAVAILABLE", answer, objections)
        if normalized(refined) == normalized(previous_answer):
            return finish("STALLED_UNRESOLVED", refined, objections)
        previous_answer = answer = refined


def save_receipt(root: Path, receipt: dict[str, Any]) -> Path:
    out = root / "External_Work" / "brain_buddy" / "outbox"
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{receipt['request_id']}.json"
    path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def print_lead_summary(receipt: dict[str, Any]) -> None:
    print(f"\n===== BRAIN BUDDY — {receipt['request_id']} =====")
    print(f"Lead seat: {receipt['lead']}")
    for seat, info in receipt["seats"].items():
        last = info["history"][-1]["reason"] if info["history"] else ""
        print(f"  {seat:<9} {info['role']:<9} {info['state']}" + (f" — {last}" if last else ""))
    print(f"Outcome: {receipt['outcome']}  (loops: {receipt['loops']}, refinements: {receipt['refinements']})")
    if receipt["final_answer"]:
        print(f"\n===== {receipt['lead'].upper()} (LEAD) =====")
        print(receipt["final_answer"])
    for seat, text in receipt["open_objections"].items():
        print(f"\n===== OPEN OBJECTION — {seat.upper()} =====")
        print(text)


def choose_mode() -> str:
    print("Brain Buddy Council")
    options = [
        ("1", "gemini", "Gemini only"),
        ("2", "deepseek", "DeepSeek only"),
        ("3", "both", "Both independently / parallel"),
        ("4", "gemini-deepseek", "Gemini first, then DeepSeek reviews"),
        ("5", "deepseek-gemini", "DeepSeek first, then Gemini reviews"),
        ("6", "discussion", "Open Gemini + DeepSeek + user discussion"),
        ("7", "lead", "Lead seat answers, Council reviews until no active objection"),
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
    ap.add_argument(
        "--timeout",
        type=int,
        default=240,
        help="Per-call transport timeout in seconds. In lead mode it only marks the provider OUT TO LUNCH.",
    )
    ap.add_argument("--save", action="store_true", help="Save a transcript receipt under External_Work")
    ap.add_argument("--seat", choices=SEATS, help="Lead mode: the seat the user asked (it leads this request)")
    ap.add_argument(
        "--max-loops",
        type=int,
        default=None,
        help="Lead mode: optional operator budget. Reaching it records OPERATOR_LIMIT_UNRESOLVED, never agreement.",
    )
    args = ap.parse_intermixed_args()

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

    if mode == "lead":
        seat = args.seat
        if seat is None:
            if not sys.stdin.isatty():
                raise CouncilError("Lead mode requires --seat in non-interactive use.")
            seat = input(f"Which seat are you asking ({'/'.join(SEATS)})? ").strip().lower()
        if args.max_loops is not None and args.max_loops < 1:
            raise CouncilError("--max-loops must be at least 1.")
        receipt = run_lead(
            question,
            seat,
            lambda s, prompt: run_worker(root, s, prompt, args.timeout),
            request_id=new_request_id(),
            baseline=baseline_identity(root),
            transport_timeout=args.timeout,
            max_loops=args.max_loops,
            user_turn=interactive_user_turn,
        )
        print_lead_summary(receipt)
        path = save_receipt(root, receipt)
        print(f"\nReceipt: {path.relative_to(root)}")
        return 0 if receipt["outcome"] != "LEAD_UNAVAILABLE" else 1

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