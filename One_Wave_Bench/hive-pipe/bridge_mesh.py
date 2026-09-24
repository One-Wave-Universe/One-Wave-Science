#!/usr/bin/env python3
"""Target-neutral self-repairing supervisor for One-Wave bridge services.

Runs on any authorized Linux host. It checks known One-Wave user services,
restarts only those known services when inactive, verifies route-level health,
and records receipts. It does not create credentials, widen allowed roots,
modify repositories, or bypass authentication.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from typing import Callable

SCRIPT_DIR = Path(__file__).resolve().parent
STATE_DIR = Path(os.environ.get(
    "ONE_WAVE_BRIDGE_MESH_STATE",
    str(Path.home() / ".local/state/one-wave-bridge-mesh"),
)).expanduser()

@dataclass
class Receipt:
    route: str
    service: str
    before: str
    repair_attempted: bool
    repair_ok: bool
    after: str
    route_ok: bool
    detail: str
    timestamp: str

def run(argv: list[str], timeout: int = 30) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, text=True, capture_output=True, timeout=timeout, check=False)

def service_state(name: str) -> str:
    r = run(["systemctl", "--user", "is-active", name], timeout=10)
    return r.stdout.strip() or r.stderr.strip() or "unknown"

def restart_service(name: str) -> tuple[bool, str]:
    r = run(["systemctl", "--user", "restart", name], timeout=20)
    return r.returncode == 0, (r.stderr or r.stdout or "").strip()

def doctor(profile: str) -> tuple[bool, str]:
    p = SCRIPT_DIR / "bridge_doctor.py"
    r = run([sys.executable, str(p), "--profile", profile, "--json"], timeout=45)
    text = (r.stdout or r.stderr or "").strip()
    return r.returncode == 0, (text[-1600:] if text else f"{profile} doctor exit={r.returncode}")

ROUTES: tuple[tuple[str, str, Callable[[], tuple[bool, str]]], ...] = (
    ("hive-pipe-mcp", "hive-pipe-gateway.service", lambda: doctor("gateway")),
    ("hive-pipe-queue", "hive-pipe-agent.service", lambda: doctor("gateway")),
    ("chatgpt-pull", "one-wave-chatgpt-terminal-pull.service", lambda: doctor("pull")),
)

def append_receipt(receipt: Receipt) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with (STATE_DIR / "receipts.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(receipt), sort_keys=True) + "\n")

def check(route: str, service: str, probe: Callable[[], tuple[bool, str]], repair: bool) -> Receipt:
    before = service_state(service)
    attempted = False
    repair_ok = False
    repair_detail = ""
    if before != "active" and repair:
        attempted = True
        repair_ok, repair_detail = restart_service(service)
        if repair_ok:
            time.sleep(1)
    after = service_state(service)
    route_ok, detail = probe() if after == "active" else (False, f"service state={after}")
    if repair_detail:
        detail = f"{detail}; repair={repair_detail}" if detail else f"repair={repair_detail}"
    return Receipt(
        route=route,
        service=service,
        before=before,
        repair_attempted=attempted,
        repair_ok=repair_ok,
        after=after,
        route_ok=route_ok,
        detail=detail,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )

def one_pass(repair: bool) -> int:
    receipts = [check(route, service, probe, repair) for route, service, probe in ROUTES]
    for receipt in receipts:
        append_receipt(receipt)
        print(json.dumps(asdict(receipt), sort_keys=True))
    return 0 if any(r.route_ok for r in receipts) else 1

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--watch", action="store_true")
    parser.add_argument("--interval", type=int, default=30)
    parser.add_argument("--no-repair", action="store_true")
    args = parser.parse_args()
    interval = max(10, args.interval)
    if not args.watch:
        return one_pass(not args.no_repair)
    while True:
        try:
            one_pass(not args.no_repair)
        except Exception as exc:
            STATE_DIR.mkdir(parents=True, exist_ok=True)
            with (STATE_DIR / "supervisor-errors.jsonl").open("a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "error": f"{type(exc).__name__}: {exc}",
                }, sort_keys=True) + "\n")
        time.sleep(interval)

if __name__ == "__main__":
    raise SystemExit(main())
