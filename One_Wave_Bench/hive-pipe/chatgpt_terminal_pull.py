#!/usr/bin/env python3
"""Resilient pull bridge for bounded ChatGPT terminal requests.

Two small state machines keep transport failure separate from command execution:

* TransportStateMachine rotates across configured Git remote/branch routes,
  rewards successful routes, and quarantines failing routes with backoff.
* RequestStateMachine journals accepted/executing/completed/acknowledged phases so
  a crash cannot silently execute the same request twice.

All commands still pass through terminal_parser.  Transport redundancy never
widens the parser's command or filesystem boundary.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from typing import Any, Iterable

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = Path(os.environ.get("CHATGPT_TERMINAL_REPO", os.environ.get("ONE_WAVE_PROJECT_ROOT", str(SCRIPT_DIR.parent.parent)))).expanduser().resolve()
sys.path.insert(0, str(SCRIPT_DIR))
import terminal_parser  # noqa: E402
import reference_receipt  # noqa: E402

REQUEST_PATH = ".chatgpt-terminal/request.json"
RESULT_PATH = ".chatgpt-terminal/result.json"
STATE_DIR = Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local/state")) / "one-wave-chatgpt-terminal"
STATE_FILE = STATE_DIR / "bridge_state.json"
OUTBOX_DIR = STATE_DIR / "outbox"
POLL_SECONDS = max(5, int(os.environ.get("CHATGPT_TERMINAL_POLL_SECONDS", "15")))
MAX_REQUEST_BYTES = 8192
MAX_JOURNAL_REQUESTS = 256
MAX_BACKOFF_SECONDS = 300


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def explain_transport_failure(error: Exception | str) -> dict[str, Any]:
    text = str(error).lower()
    if any(marker in text for marker in ("authentication failed", "could not read username", "publickey", "repository not found")):
        return {
            "code": "TRANSPORT_AUTHENTICATION_REQUIRED",
            "level": "authentication",
            "higher_level_required": True,
            "next_action": "Repair the configured Git remote identity outside request payloads; do not copy credentials into the bridge journal.",
        }
    if any(marker in text for marker in ("couldn't find remote ref", "remote ref does not exist", "invalid refspec")):
        return {
            "code": "TRANSPORT_BRANCH_CREATION_REQUIRED",
            "level": "path_authorization",
            "higher_level_required": True,
            "next_action": "Create the named dedicated transport branch from the current main commit, then let the route leave backoff naturally.",
        }
    if any(marker in text for marker in ("could not resolve host", "network is unreachable", "timed out", "connection reset")):
        return {
            "code": "TRANSPORT_ROUTE_FAILOVER_ACTIVE",
            "level": "ai_correction",
            "higher_level_required": False,
            "next_action": "Continue through the next healthy route while this route waits in exponential backoff.",
        }
    return {
        "code": "TRANSPORT_REPAIR_REQUIRED",
        "level": "path_authorization",
        "higher_level_required": True,
        "next_action": "Inspect the recorded route error and repair or add a configured remote/branch path without weakening parser boundaries.",
    }


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(REPO_ROOT), *args],
        text=True,
        capture_output=True,
        check=check,
    )


@dataclass(frozen=True)
class Route:
    name: str
    remote: str
    branch: str

    @property
    def key(self) -> str:
        return f"{self.remote}:{self.branch}"

    @property
    def ref(self) -> str:
        return f"refs/remotes/{self.remote}/{self.branch}"


def parse_routes(raw: str | None = None) -> list[Route]:
    """Parse NAME=REMOTE:BRANCH entries, preserving order and removing duplicates."""
    if raw is None:
        raw = os.environ.get(
            "CHATGPT_TERMINAL_ROUTES",
            "primary=origin:chatgpt-terminal,backup=origin:chatgpt-terminal-backup",
        )
    routes: list[Route] = []
    seen: set[str] = set()
    for index, item in enumerate(raw.split(","), start=1):
        item = item.strip()
        if not item:
            continue
        if "=" in item:
            name, target = item.split("=", 1)
        else:
            name, target = f"route-{index}", item
        if ":" not in target:
            raise ValueError(f"route must be NAME=REMOTE:BRANCH: {item}")
        remote, branch = target.split(":", 1)
        name, remote, branch = name.strip(), remote.strip(), branch.strip()
        if not name or not remote or not branch or any(char.isspace() for char in remote + branch):
            raise ValueError(f"invalid route: {item}")
        route = Route(name=name, remote=remote, branch=branch)
        if route.key not in seen:
            routes.append(route)
            seen.add(route.key)
    if not routes:
        raise ValueError("at least one terminal bridge route is required")
    return routes


class StateStore:
    def __init__(self, path: Path = STATE_FILE):
        self.path = path
        self.data: dict[str, Any] = self._load()

    def _load(self) -> dict[str, Any]:
        try:
            loaded = json.loads(self.path.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                return loaded
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            pass
        return {"version": 2, "routes": {}, "requests": {}, "controller": {}}

    def save(self) -> None:
        self.data["version"] = 2
        self.data["updated_at"] = utc_now()
        atomic_write(self.path, json.dumps(self.data, indent=2, sort_keys=True) + "\n")

    def trim_requests(self) -> None:
        requests = self.data.setdefault("requests", {})
        if len(requests) <= MAX_JOURNAL_REQUESTS:
            return
        ranked = sorted(
            requests.items(),
            key=lambda item: item[1].get("updated_at", ""),
            reverse=True,
        )
        self.data["requests"] = dict(ranked[:MAX_JOURNAL_REQUESTS])


class TransportStateMachine:
    """Circuit breaker and route scorer for inbound and outbound Git paths."""

    def __init__(self, routes: list[Route], store: StateStore, clock=time.time):
        self.routes = routes
        self.store = store
        self.clock = clock
        state = self.store.data.setdefault("routes", {})
        for route in routes:
            state.setdefault(route.key, {
                "state": "closed",
                "failures": 0,
                "successes": 0,
                "retry_at": 0.0,
            })

    def health(self, route: Route) -> dict[str, Any]:
        return self.store.data["routes"][route.key]

    def ordered(self, preferred: Route | None = None) -> list[Route]:
        now = self.clock()

        def rank(route: Route) -> tuple[int, int, int, int]:
            health = self.health(route)
            available = float(health.get("retry_at", 0)) <= now
            preferred_rank = 0 if preferred and route.key == preferred.key else 1
            return (
                0 if available else 1,
                preferred_rank,
                int(health.get("failures", 0)),
                -int(health.get("successes", 0)),
            )

        ordered = sorted(self.routes, key=rank)
        return [route for route in ordered if float(self.health(route).get("retry_at", 0)) <= now]

    def success(self, route: Route) -> None:
        health = self.health(route)
        health.update({
            "state": "closed",
            "failures": 0,
            "successes": int(health.get("successes", 0)) + 1,
            "retry_at": 0.0,
            "last_success_at": utc_now(),
            "last_error": None,
        })
        self.store.save()

    def failure(self, route: Route, error: Exception | str) -> None:
        health = self.health(route)
        failures = int(health.get("failures", 0)) + 1
        backoff = min(MAX_BACKOFF_SECONDS, 5 * (2 ** min(failures - 1, 6)))
        health.update({
            "state": "open",
            "failures": failures,
            "retry_at": self.clock() + backoff,
            "last_failure_at": utc_now(),
            "last_error": str(error)[-1000:],
            "guidance": explain_transport_failure(error),
        })
        self.store.save()

    def next_delay(self) -> float:
        now = self.clock()
        waits = [max(0.0, float(self.health(route).get("retry_at", 0)) - now) for route in self.routes]
        available = [wait for wait in waits if wait == 0]
        return float(POLL_SECONDS if available else max(1.0, min(waits, default=POLL_SECONDS)))


def fetch_route(route: Route) -> None:
    run_git(
        "fetch", "--quiet", route.remote,
        f"+refs/heads/{route.branch}:{route.ref}",
    )


def read_request(route: Route) -> tuple[str, str] | None:
    fetch_route(route)
    commit = run_git("rev-parse", route.ref).stdout.strip()
    shown = run_git("show", f"{route.ref}:{REQUEST_PATH}", check=False)
    if shown.returncode != 0:
        return None
    if len(shown.stdout.encode("utf-8")) > MAX_REQUEST_BYTES:
        raise ValueError(f"{route.key}:{REQUEST_PATH} exceeds {MAX_REQUEST_BYTES} bytes")
    return commit, shown.stdout


def validate_request(raw: str) -> dict[str, Any]:
    request = json.loads(raw)
    request_id = request.get("id")
    argv = request.get("argv")
    default_cwd = os.environ.get("CHATGPT_TERMINAL_DEFAULT_CWD", str(REPO_ROOT))
    cwd = request.get("cwd", default_cwd)
    timeout = request.get("timeout", 120)
    intention = reference_receipt.required_text(request.get("intention"), "intention")
    consequence = reference_receipt.required_text(request.get("consequence"), "consequence")

    if not isinstance(request_id, str) or not request_id.strip() or len(request_id) > 128:
        raise ValueError("id must be a non-empty string <= 128 characters")
    if not isinstance(argv, list) or not argv or not all(isinstance(x, str) and x for x in argv):
        raise ValueError("argv must be a non-empty JSON array of non-empty strings")
    if len(argv) > terminal_parser.MAX_ARGS or sum(len(x) for x in argv) > MAX_REQUEST_BYTES:
        raise ValueError("argv exceeds bridge size limits")
    if not isinstance(cwd, str) or not cwd.startswith("/") or len(cwd) > 1024:
        raise ValueError("cwd must be an absolute path <= 1024 characters")
    if not isinstance(timeout, int) or not 1 <= timeout <= terminal_parser.MAX_TIMEOUT:
        raise ValueError(f"timeout must be an integer from 1 to {terminal_parser.MAX_TIMEOUT}")
    normalized = {"id": request_id.strip(), "argv": argv, "cwd": cwd, "timeout": timeout,
                  "intention": intention, "consequence": consequence}
    encoded = json.dumps(normalized, sort_keys=True, separators=(",", ":")).encode("utf-8")
    normalized["digest"] = hashlib.sha256(encoded).hexdigest()
    return normalized


def result_path(request_id: str) -> Path:
    safe_id = hashlib.sha256(request_id.encode("utf-8")).hexdigest()
    return OUTBOX_DIR / f"{safe_id}.json"


def write_result(result: dict[str, Any]) -> Path:
    path = result_path(str(result["id"]))
    atomic_write(path, json.dumps(result, indent=2, sort_keys=True) + "\n")
    return path


def load_result(request_id: str) -> dict[str, Any] | None:
    try:
        return json.loads(result_path(request_id).read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def execute_request(request: dict[str, Any], commit: str, source: Route) -> dict[str, Any]:
    try:
        reference_receipt.record({"phase": "issued", "request_id": request["id"],
                                  "intention": request["intention"], "consequence": request["consequence"],
                                  "request_digest": request["digest"], "reference": terminal_parser._project_reference(),
                                  "at": utc_now()})
        parsed = terminal_parser.run(request["argv"], cwd=request["cwd"], timeout=request["timeout"])
        result = {
            "id": request["id"],
            "request_digest": request["digest"],
            "request_commit": commit,
            "source_route": source.key,
            "completed_at": utc_now(),
            **parsed,
        }
        try:
            reference_receipt.record({"phase": "observed", "request_id": request["id"],
                                      "result": result, "at": utc_now()})
        except OSError as error:
            result["ok"] = False
            result["error"] = f"Reference Goblin HOLD: command may have run, but observed receipt could not be stored: {error}"
        return result
    except Exception as exc:
        return {
            "id": request["id"],
            "request_digest": request["digest"],
            "request_commit": commit,
            "source_route": source.key,
            "completed_at": utc_now(),
            "ok": False,
            "exit_code": None,
            "stdout": "",
            "stderr": "",
            "error": f"{type(exc).__name__}: {exc}",
            "guidance": terminal_parser.explain_exception(exc),
            "reference": {"tool": "terminal_reference", "contract": terminal_parser.PARSER_CONTRACT},
        }


def publish_result(result: dict[str, Any], route: Route) -> None:
    """Publish through one route without touching the user's active checkout."""
    fetch_route(route)
    with tempfile.TemporaryDirectory(prefix="one-wave-chatgpt-terminal-") as td:
        worktree = Path(td) / "bridge"
        subprocess.run(
            ["git", "-C", str(REPO_ROOT), "worktree", "add", "--detach", str(worktree), route.ref],
            text=True, capture_output=True, check=True,
        )
        try:
            destination = worktree / RESULT_PATH
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(worktree), "add", RESULT_PATH], check=True)
            changed = subprocess.run(
                ["git", "-C", str(worktree), "diff", "--cached", "--quiet"], check=False,
            ).returncode != 0
            if not changed:
                return
            subprocess.run(["git", "-C", str(worktree), "config", "user.name", "one-wave-terminal-bridge"], check=True)
            subprocess.run(["git", "-C", str(worktree), "config", "user.email", "terminal-bridge@users.noreply.github.com"], check=True)
            subprocess.run(
                ["git", "-C", str(worktree), "commit", "-m", f"terminal: result {result.get('id', 'unknown')} [skip ci]"],
                text=True, capture_output=True, check=True,
            )
            for attempt in range(2):
                pushed = subprocess.run(
                    ["git", "-C", str(worktree), "push", route.remote, f"HEAD:refs/heads/{route.branch}"],
                    text=True, capture_output=True, check=False,
                )
                if pushed.returncode == 0:
                    return
                if attempt == 0:
                    subprocess.run(["git", "-C", str(worktree), "fetch", route.remote, route.branch], check=True)
                    subprocess.run(["git", "-C", str(worktree), "rebase", "FETCH_HEAD"], check=True)
            raise RuntimeError(pushed.stderr.strip() or f"push failed for {route.key}")
        finally:
            subprocess.run(
                ["git", "-C", str(REPO_ROOT), "worktree", "remove", "--force", str(worktree)],
                text=True, capture_output=True, check=False,
            )


class RequestStateMachine:
    """Durable at-most-once execution loop with retryable result delivery."""

    def __init__(self, store: StateStore, transport: TransportStateMachine):
        self.store = store
        self.transport = transport

    def _entry(self, request_id: str) -> dict[str, Any] | None:
        return self.store.data.setdefault("requests", {}).get(request_id)

    def _set(self, request_id: str, **fields: Any) -> dict[str, Any]:
        entry = self.store.data.setdefault("requests", {}).setdefault(request_id, {})
        entry.update(fields, updated_at=utc_now())
        self.store.trim_requests()
        self.store.save()
        return entry

    def recover(self) -> None:
        for request_id, entry in list(self.store.data.setdefault("requests", {}).items()):
            if entry.get("phase") == "executing":
                result = {
                    "id": request_id,
                    "request_digest": entry.get("digest"),
                    "request_commit": entry.get("request_commit"),
                    "source_route": entry.get("source_route"),
                    "completed_at": utc_now(),
                    "ok": False,
                    "exit_code": None,
                    "stdout": "",
                    "stderr": "",
                    "error": "bridge restarted during execution; command was not repeated because its completion is uncertain",
                    "execution_state": "uncertain_after_restart",
                    "guidance": {
                        "code": "EXECUTION_RECONCILIATION_REQUIRED",
                        "level": "privileged_operator",
                        "higher_level_required": True,
                        "explanation": "The bridge restarted after launch but before a durable completion receipt.",
                        "next_action": "Inspect the target state before issuing a new uniquely identified request; the bridge will not guess or repeat the command.",
                    },
                    "reference": {"tool": "terminal_reference", "contract": terminal_parser.PARSER_CONTRACT},
                }
                write_result(result)
                self._set(request_id, phase="completed", recovery="at_most_once_hold")

    def deliver(self, request_id: str, preferred: Route | None = None) -> bool:
        result = load_result(request_id)
        if result is None:
            self._set(request_id, phase="delivery_blocked", error="durable result missing")
            return False
        attempts: list[dict[str, str]] = []
        for route in self.transport.ordered(preferred):
            try:
                publish_result(result, route)
                self.transport.success(route)
                attempts.append({"route": route.key, "status": "delivered"})
                self._set(request_id, phase="acknowledged", delivered_route=route.key, delivery_attempts=attempts)
                try:
                    result_path(request_id).unlink()
                except FileNotFoundError:
                    pass
                return True
            except Exception as exc:
                self.transport.failure(route, exc)
                attempts.append({"route": route.key, "status": "failed", "error": str(exc)[-500:]})
        self._set(request_id, phase="completed", delivery_attempts=attempts)
        return False

    def retry_pending(self) -> None:
        for request_id, entry in list(self.store.data.setdefault("requests", {}).items()):
            if entry.get("phase") in {"completed", "delivery_blocked"}:
                preferred = next((r for r in self.transport.routes if r.key == entry.get("source_route")), None)
                self.deliver(request_id, preferred)

    def accept(self, route: Route, commit: str, raw: str) -> bool:
        try:
            request = validate_request(raw)
        except Exception as exc:
            digest = hashlib.sha256(raw.encode("utf-8", errors="replace")).hexdigest()
            request_id = f"invalid-{digest[:16]}"
            if self._entry(request_id):
                return False
            result = {
                "id": request_id,
                "request_commit": commit,
                "source_route": route.key,
                "completed_at": utc_now(),
                "ok": False,
                "exit_code": None,
                "stdout": "",
                "stderr": "",
                "error": f"invalid request: {type(exc).__name__}: {exc}",
                "guidance": terminal_parser.explain_exception(exc),
                "reference": {"tool": "terminal_reference", "contract": terminal_parser.PARSER_CONTRACT},
            }
            write_result(result)
            self._set(request_id, phase="completed", digest=digest, request_commit=commit, source_route=route.key)
            return self.deliver(request_id, route)

        previous = self._entry(request["id"])
        if previous:
            if previous.get("digest") != request["digest"]:
                # Reusing an id for a different command is rejected; it is never executed.
                conflict_id = f"conflict-{request['id']}-{request['digest'][:12]}"
                if not self._entry(conflict_id):
                    result = {
                        "id": conflict_id,
                        "conflicting_request_id": request["id"],
                        "request_digest": request["digest"],
                        "request_commit": commit,
                        "source_route": route.key,
                        "completed_at": utc_now(),
                        "ok": False,
                        "exit_code": None,
                        "stdout": "",
                        "stderr": "",
                        "error": "request id was already used with different content; choose a new id",
                        "guidance": {
                            "code": "UNIQUE_REQUEST_ID_REQUIRED",
                            "level": "ai_correction",
                            "higher_level_required": False,
                            "explanation": "A stable request id is the at-most-once execution key and cannot name different commands.",
                            "next_action": "Issue the corrected command with a new request id.",
                        },
                        "reference": {"tool": "terminal_reference", "contract": terminal_parser.PARSER_CONTRACT},
                    }
                    write_result(result)
                    self._set(conflict_id, phase="completed", digest=request["digest"], source_route=route.key)
                    return self.deliver(conflict_id, route)
            elif previous.get("phase") in {"completed", "delivery_blocked"}:
                return self.deliver(request["id"], route)
            return False

        self._set(
            request["id"], phase="accepted", digest=request["digest"],
            request_commit=commit, source_route=route.key,
        )
        # The executing journal entry is fsynced logically (atomic replace) before
        # command launch.  After a crash, recovery reports uncertainty and refuses
        # to repeat the command automatically.
        self._set(request["id"], phase="executing", started_at=utc_now())
        result = execute_request(request, commit, route)
        write_result(result)
        self._set(request["id"], phase="completed", completed_at=result["completed_at"])
        return self.deliver(request["id"], route)


class BridgeController:
    def __init__(self, routes: list[Route], store: StateStore | None = None):
        self.store = store or StateStore()
        self.transport = TransportStateMachine(routes, self.store)
        self.requests = RequestStateMachine(self.store, self.transport)

    def cycle(self) -> bool:
        self.store.data.setdefault("controller", {}).update({"state": "recovering", "cycle_at": utc_now()})
        self.store.save()
        self.requests.recover()
        self.requests.retry_pending()
        activity = False
        self.store.data["controller"]["state"] = "polling"
        self.store.save()
        for route in self.transport.ordered():
            try:
                found = read_request(route)
                self.transport.success(route)
                if found is not None:
                    commit, raw = found
                    activity = self.requests.accept(route, commit, raw) or activity
            except Exception as exc:
                self.transport.failure(route, exc)
        self.store.data["controller"].update({
            "state": "idle",
            "last_cycle_completed_at": utc_now(),
            "activity": activity,
        })
        self.store.save()
        return activity


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="run one recovery/poll/delivery cycle")
    parser.add_argument("--watch", action="store_true", help="run continuously (default)")
    parser.add_argument("--status", action="store_true", help="print durable controller state and exit")
    args = parser.parse_args()

    if not (REPO_ROOT / ".git").exists():
        raise SystemExit(f"not a git checkout: {REPO_ROOT}")
    if args.status:
        print(json.dumps(StateStore().data, indent=2, sort_keys=True))
        return 0

    routes = parse_routes()
    controller = BridgeController(routes)
    if args.once:
        controller.cycle()
        return 0

    print("CHATGPT_TERMINAL_BRIDGE routes=" + ",".join(route.key for route in routes))
    while True:
        try:
            controller.cycle()
        except Exception as exc:
            print(f"CHATGPT_TERMINAL_BRIDGE_ERROR {type(exc).__name__}: {exc}", file=sys.stderr)
        time.sleep(controller.transport.next_delay())


if __name__ == "__main__":
    raise SystemExit(main())
