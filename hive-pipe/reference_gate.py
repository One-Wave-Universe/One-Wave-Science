"""Fail-closed, one-use reference receipts for Hive Pipe tool execution."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess
import threading
import time

REFERENCE_FILES = ("AGENTS.md", "AI_BRIDGE_START_HERE.md", "BRANCH_STEP_PROJECT_TEMPLATE.md")
MAX_AGE_SECONDS = 300


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def snapshot() -> dict:
    root = Path(os.environ.get("ONE_WAVE_PROJECT_ROOT", Path(__file__).resolve().parent.parent)).resolve()
    if not (root / ".git").exists():
        raise ValueError("reference HOLD: canonical repository checkout is missing")
    head = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, timeout=10)
    status = subprocess.run(["git", "-C", str(root), "status", "--porcelain", "-uno"], capture_output=True, text=True, timeout=10)
    if head.returncode or status.returncode:
        raise ValueError("reference HOLD: cannot verify repository HEAD and working state")
    files = {}
    for relative in REFERENCE_FILES:
        path = root / relative
        if not path.is_file() or path.is_symlink():
            raise ValueError(f"reference HOLD: missing authority {relative}")
        files[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return {"repo": str(root), "head": head.stdout.strip(), "status_sha256": hashlib.sha256(status.stdout.encode()).hexdigest(), "files": files}


def required_text(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > 1024:
        raise ValueError(f"reference HOLD: {name} must be non-empty text <= 1024 characters")
    return value.strip()


class Gate:
    def __init__(self):
        self.lock = threading.Lock()
        self.pending: dict[str, dict] = {}

    @staticmethod
    def record(event: dict) -> None:
        path = Path(os.environ.get("REFERENCE_GATE_LEDGER", Path.home() / ".local/state/one-wave/reference-receipts.jsonl"))
        path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND | os.O_NOFOLLOW, 0o600)
        try:
            with os.fdopen(fd, "a", encoding="utf-8") as stream:
                stream.write(json.dumps(event, sort_keys=True) + "\n")
                stream.flush()
                os.fsync(stream.fileno())
        except Exception:
            raise

    def issue(self, *, intention: object, consequence: object, action: object) -> dict:
        intention = required_text(intention, "intention")
        consequence = required_text(consequence, "consequence")
        if not isinstance(action, dict) or action.get("name") not in {"terminal_run", "python_run", "cpp_compile_run"} or not isinstance(action.get("arguments"), dict):
            raise ValueError("reference HOLD: action must name a supported executable tool and its arguments")
        state = snapshot()
        card = {
            "id": secrets.token_urlsafe(24),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "intention": intention,
            "consequence": consequence,
            "action_sha256": digest(action),
            "reference": state,
        }
        self.record({"phase": "issued", "card": card})
        with self.lock:
            self.pending[card["id"]] = {"issued": time.monotonic(), "card": card}
        return card

    def consume(self, card: object, action: dict) -> dict:
        if not isinstance(card, dict) or not isinstance(card.get("id"), str):
            raise ValueError("reference HOLD: fresh reference card required")
        with self.lock:
            entry = self.pending.pop(card["id"], None)
        if entry is None or entry["card"] != card:
            raise ValueError("reference HOLD: unknown, altered, or already used card")
        if time.monotonic() - entry["issued"] > MAX_AGE_SECONDS:
            raise ValueError("reference HOLD: reference card expired")
        if card["action_sha256"] != digest(action):
            raise ValueError("reference HOLD: action differs from stamped intention")
        if card["reference"] != snapshot():
            raise ValueError("reference HOLD: repository changed since the card was stamped")
        self.record({"phase": "authorized", "card_id": card["id"], "at": datetime.now(timezone.utc).isoformat()})
        return card

    def complete(self, card: dict, result: dict) -> None:
        self.record({"phase": "observed", "card_id": card["id"], "at": datetime.now(timezone.utc).isoformat(), "result": result})
