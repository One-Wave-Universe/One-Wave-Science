#!/usr/bin/env python3
"""Android reference-first execution gate.

This module sits in front of the existing Hive Pipe terminal parser for Android
clients.  It enforces one fresh reference receipt per action:

    Field reference -> Void test -> Field act -> Void confirm/deny

A reference receipt is one-shot.  Missing, stale, reused, cwd-mismatched, or
pre-action-drifted receipts HOLD instead of executing.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import secrets
import time
from typing import Any

import terminal_parser

ANDROID_REFERENCE_CONTRACT = "one-wave-android-reference-gate-v1"
REFERENCE_TTL_SECONDS = 120


@dataclass
class _IssuedReference:
    issued_monotonic: float
    snapshot: dict[str, Any]


_REFERENCES: dict[str, _IssuedReference] = {}


def _git_read(argv: list[str], cwd: str) -> str | None:
    result = terminal_parser.run(["git", *argv], cwd=cwd, timeout=15)
    if not result.get("ok"):
        return None
    return result.get("stdout", "").strip()


def _snapshot(cwd: str | None = None) -> dict[str, Any]:
    validated = terminal_parser.pwd(cwd)
    target = validated["cwd"]

    repo_root = _git_read(["rev-parse", "--show-toplevel"], target)
    branch = _git_read(["branch", "--show-current"], target) if repo_root else None
    head = _git_read(["rev-parse", "HEAD"], target) if repo_root else None
    status = _git_read(["status", "--short", "--branch"], target) if repo_root else None

    return {
        "cwd": target,
        "repo_root": repo_root,
        "branch": branch,
        "head": head,
        "status": status,
        "git_repo": bool(repo_root),
    }


def _void_test(snapshot: dict[str, Any]) -> dict[str, Any]:
    problems: list[str] = []
    if not snapshot.get("cwd"):
        problems.append("missing_cwd")
    if snapshot.get("git_repo"):
        for key in ("repo_root", "head", "status"):
            if snapshot.get(key) is None:
                problems.append(f"missing_{key}")

    return {
        "decision": "ALLOW" if not problems else "HOLD",
        "problems": problems,
        "same_snapshot_required": True,
    }


def reference(cwd: str | None = None) -> dict[str, Any]:
    """Issue one fresh reference token for exactly one subsequent Android action."""
    snapshot = _snapshot(cwd)
    void = _void_test(snapshot)
    if void["decision"] != "ALLOW":
        return {
            "ok": False,
            "contract": ANDROID_REFERENCE_CONTRACT,
            "cycle": {
                "field_reference": snapshot,
                "void_test": void,
                "field_act": "BLOCKED",
                "void_confirm": "HOLD",
            },
        }

    token = secrets.token_urlsafe(24)
    _REFERENCES[token] = _IssuedReference(time.monotonic(), snapshot)
    return {
        "ok": True,
        "contract": ANDROID_REFERENCE_CONTRACT,
        "reference_token": token,
        "expires_in_seconds": REFERENCE_TTL_SECONDS,
        "one_shot": True,
        "cycle": {
            "field_reference": snapshot,
            "void_test": void,
            "field_act": "PENDING",
            "void_confirm": "PENDING",
        },
    }


def _hold(code: str, explanation: str, *, snapshot: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "ok": False,
        "contract": ANDROID_REFERENCE_CONTRACT,
        "decision": "HOLD",
        "code": code,
        "explanation": explanation,
        "current_reference": snapshot,
        "next_action": "Call android_reference again before any action.",
    }


def run(reference_token: str, argv: Any, cwd: str | None = None, timeout: int | float = 60) -> dict[str, Any]:
    """Consume a fresh reference token and execute exactly one bounded action."""
    if not isinstance(reference_token, str) or not reference_token:
        return _hold("REFERENCE_REQUIRED", "Android actions require a fresh reference token.")

    issued = _REFERENCES.pop(reference_token, None)
    if issued is None:
        return _hold("REFERENCE_UNKNOWN_OR_REUSED", "Reference token is missing, invalid, or already consumed.")

    age = time.monotonic() - issued.issued_monotonic
    if age > REFERENCE_TTL_SECONDS:
        return _hold("REFERENCE_STALE", "Reference token expired before the action.")

    current = _snapshot(cwd)
    if current["cwd"] != issued.snapshot["cwd"]:
        return _hold("REFERENCE_CWD_MISMATCH", "Action cwd differs from the referenced cwd.", snapshot=current)

    if current != issued.snapshot:
        return _hold(
            "REFERENCE_DRIFT",
            "Repository or working state changed after reference; action was not executed.",
            snapshot=current,
        )

    result = terminal_parser.run(argv, cwd=current["cwd"], timeout=timeout)
    post = _snapshot(current["cwd"])
    confirmation = {
        "decision": "CONFIRM" if result.get("ok") else "DENY",
        "command_ok": bool(result.get("ok")),
        "state_changed": post != current,
        "pre_reference": current,
        "post_reference": post,
        "next_action_requires_new_reference": True,
    }

    return {
        "ok": bool(result.get("ok")),
        "contract": ANDROID_REFERENCE_CONTRACT,
        "decision": confirmation["decision"],
        "cycle": {
            "field_reference": current,
            "void_test": {"decision": "ALLOW", "problems": [], "same_snapshot_required": True},
            "field_act": result,
            "void_confirm": confirmation,
        },
    }


def clear_reference_tokens() -> None:
    """Test helper; production callers should never need to clear the registry."""
    _REFERENCES.clear()
