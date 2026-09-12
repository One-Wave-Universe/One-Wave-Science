#!/usr/bin/env python3
"""Validated action registry and queue executor for Hive Pipe."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import uuid


ROOT = Path(__file__).resolve().parent
QUEUE = ROOT / "queue"
PENDING = QUEUE / "pending"
PROCESSING = QUEUE / "processing"
RESULTS = QUEUE / "results"
DONE = QUEUE / "done"
JOB_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,95}$")
REQUEST_KEYS = {"version", "id", "action", "created_utc"}

ACTIONS: dict[str, list[str]] = {
    "health": ["uname", "-a"],
    "inventory_block_devices": [
        "lsblk", "--json", "--bytes",
        "--output", "NAME,KNAME,PATH,TYPE,SIZE,MODEL,SERIAL,TRAN,RM,RO,FSTYPE,LABEL,UUID,MOUNTPOINTS",
    ],
    "repo_status": ["git", "status", "--short", "--branch"],
}


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def ensure_dirs() -> None:
    for directory in (PENDING, PROCESSING, RESULTS, DONE):
        directory.mkdir(parents=True, exist_ok=True)


def atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def validate_request(path: Path) -> dict:
    if path.is_symlink() or not path.is_file():
        raise ValueError("request must be a regular non-symlink file")
    if path.stat().st_size > 4096:
        raise ValueError("request exceeds 4096 bytes")
    request = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(request, dict) or set(request) != REQUEST_KEYS:
        raise ValueError(f"request keys must be exactly {sorted(REQUEST_KEYS)}")
    if request["version"] != 1:
        raise ValueError("unsupported protocol version")
    if not isinstance(request["id"], str) or not JOB_ID.fullmatch(request["id"]):
        raise ValueError("invalid job id")
    if path.name != f'{request["id"]}.json':
        raise ValueError("filename does not match job id")
    if request["action"] not in ACTIONS:
        raise ValueError("unknown or disabled action")
    if not isinstance(request["created_utc"], str) or not request["created_utc"].endswith("Z"):
        raise ValueError("created_utc must be a UTC timestamp ending in Z")
    return request


def enqueue(action: str) -> Path:
    ensure_dirs()
    if action not in ACTIONS:
        raise ValueError(f"unknown action: {action}")
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    job_id = f"{stamp}-{action}-{uuid.uuid4().hex[:8]}"
    path = PENDING / f"{job_id}.json"
    atomic_json(path, {"version": 1, "id": job_id, "action": action, "created_utc": utc_now()})
    return path


def execute(path: Path) -> Path:
    ensure_dirs()
    request = validate_request(path)
    result_path = RESULTS / path.name
    if result_path.exists() or (DONE / path.name).exists():
        raise ValueError("job id already completed")
    command = ACTIONS[request["action"]]
    started_utc = utc_now()
    completed = subprocess.run(
        command,
        cwd=ROOT.parent,
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
        env={"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LANG": "C.UTF-8"},
    )
    result = {
        "version": 1,
        "id": request["id"],
        "action": request["action"],
        "started_utc": started_utc,
        "finished_utc": utc_now(),
        "exit_code": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }
    atomic_json(result_path, result)
    os.replace(path, DONE / path.name)
    return result_path


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("actions")
    enqueue_parser = sub.add_parser("enqueue")
    enqueue_parser.add_argument("action")
    run_parser = sub.add_parser("run")
    run_parser.add_argument("request", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "actions":
            print("\n".join(sorted(ACTIONS)))
        elif args.command == "enqueue":
            print(enqueue(args.action))
        else:
            print(execute(args.request.resolve()))
        return 0
    except (OSError, ValueError, json.JSONDecodeError, subprocess.SubprocessError) as error:
        print(f"HIVE_PIPE_ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
