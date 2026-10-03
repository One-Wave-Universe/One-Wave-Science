#!/usr/bin/env python3
"""One-Wave Lens Gateway.

A provider-neutral gate that forces every AI turn through the canonical
One-Wave repository reference before and after model reasoning.

This program is transport/orchestration, never project authority.
Authority remains in the canonical repository.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
MANDATORY = (
    "GENERAL_REFERENCE_RULES.md",
    "AI_CANONICAL_START_HERE.md",
)

@dataclass(frozen=True)
class Evidence:
    path: str
    text: str

def read_repo(path: str) -> Evidence:
    p = (ROOT / path).resolve()
    if ROOT not in p.parents and p != ROOT:
        raise ValueError("reference escaped canonical repository")
    if not p.is_file():
        raise FileNotFoundError(path)
    return Evidence(path, p.read_text(encoding="utf-8", errors="replace"))

def git_sha() -> str:
    return subprocess.check_output(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True
    ).strip()

def search_repo(question: str, limit: int = 8) -> list[str]:
    """Deterministic local retrieval; returns canonical paths, not copied canon."""
    words = [w.lower() for w in question.split() if len(w) >= 4][:20]
    if not words:
        return []
    scored = []
    for p in ROOT.rglob("*"):
        if not p.is_file() or ".git" in p.parts:
            continue
        if p.suffix.lower() not in {".md", ".txt", ".json", ".yaml", ".yml", ".py"}:
            continue
        rel = str(p.relative_to(ROOT))
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")[:120000].lower()
        except OSError:
            continue
        score = sum(4 * (w in rel.lower()) + (w in text) for w in words)
        if score:
            scored.append((score, rel))
    return [p for _, p in sorted(scored, reverse=True)[:limit]]

def packet(question: str, extra_paths: list[str]) -> dict:
    paths = list(MANDATORY)
    for path in extra_paths + search_repo(question):
        if path not in paths:
            paths.append(path)
    refs = []
    for path in paths:
        try:
            e = read_repo(path)
            refs.append({"path": e.path, "text": e.text[:16000]})
        except (OSError, ValueError):
            pass
    return {
        "repo_sha": git_sha(),
        "question": question,
        "references": refs,
        "law": (
            "Canonical repo is authority. External data/tools are optional evidence. "
            "Do not replace missing evidence with assumptions. Distinguish established, "
            "repo-hypothesis, external evidence, and model inference."
        ),
    }

def render(role: str, pkt: dict, peer: str | None = None) -> str:
    refs = "\n\n".join(
        f"=== REFERENCE: {r['path']} ===\n{r['text']}" for r in pkt["references"]
    )
    peer_block = f"\n\nPEER OUTPUT TO AUDIT:\n{peer}" if peer else ""
    return f"""ONE-WAVE LENS GATE
ROLE: {role}
REPO SHA: {pkt['repo_sha']}
QUESTION: {pkt['question']}
LAW: {pkt['law']}

You MUST reason from the canonical references below as primary authority.
Tools/external data may be used only when useful; they are evidence, not canon.
Name the repo paths supporting project-specific claims.
If the references do not support a claim, mark it as inference or unresolved.
Do not silently import a standard assumption over a conflicting repo authority.

{refs}{peer_block}

Return:
1. answer
2. repo references actually used
3. external evidence/tools used, if any
4. unresolved/conflicting points
"""

def field_void(
    question: str,
    field_ai: Callable[[str], str],
    void_ai: Callable[[str], str],
    final_ai: Callable[[str], str],
    extra_paths: list[str] | None = None,
) -> dict:
    """Field proposes through lens; Void attacks through same lens; final revalidates."""
    pkt = packet(question, extra_paths or [])
    field = field_ai(render("FIELD: construct the strongest repo-grounded answer", pkt))
    void = void_ai(render(
        "VOID: challenge unsupported assumptions, contradictions, and missing controls",
        pkt, field,
    ))
    final_prompt = render(
        "RECOMBINE: resolve Field/Void against the SAME canonical reference",
        pkt,
        "FIELD:\n" + field + "\n\nVOID:\n" + void,
    )
    final = final_ai(final_prompt)
    return {
        "repo_sha": pkt["repo_sha"],
        "question": question,
        "field": field,
        "void": void,
        "final": final,
        "reference_paths": [r["path"] for r in pkt["references"]],
    }

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("question", nargs="+")
    ap.add_argument("--reference", action="append", default=[])
    ap.add_argument("--packet-only", action="store_true")
    args = ap.parse_args()
    pkt = packet(" ".join(args.question), args.reference)
    # Packet-only is intentionally the first runnable boundary. Existing Gemini,
    # DeepSeek, ChatGPT, Hive Pipe, or future adapters consume this same gate.
    print(json.dumps(pkt, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
