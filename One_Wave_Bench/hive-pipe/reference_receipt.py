"""Durable original receipts for the fail-closed reference goblin."""

from __future__ import annotations

import json
import os
from pathlib import Path


def required_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > 1024:
        raise ValueError(f"Reference Goblin HOLD: {label} must be non-empty text <= 1024 characters")
    return value.strip()


def record(event: dict) -> None:
    path = Path(os.environ.get("REFERENCE_GATE_LEDGER", Path.home() / ".local/state/one-wave/reference-receipts.jsonl"))
    path.parent.mkdir(parents=True, mode=0o700, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, "a", encoding="utf-8") as output:
        output.write(json.dumps(event, sort_keys=True) + "\n")
        output.flush()
        os.fsync(output.fileno())
