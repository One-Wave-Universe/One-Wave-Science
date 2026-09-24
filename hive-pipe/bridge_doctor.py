#!/usr/bin/env python3
"""Read-only health doctor for One-Wave AI and terminal bridges.

The doctor separates repository/code health from live target health.  It never
claims that a remote route works merely because its source code passes tests.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
DEFAULT_MCP_URL = "http://127.0.0.1:8765/mcp"

PASS = "PASS"
WARN = "WARN"
FAIL = "FAIL"
NOT_CONFIGURED = "NOT_CONFIGURED"
NOT_VERIFIED = "NOT_VERIFIED"


@dataclass
class Check:
    name: str
    status: str
    detail: str
    action: str = ""


def overall_exit(checks: list[Check]) -> int:
    if any(check.status == FAIL for check in checks):
        return 1
    if any(check.status in {WARN, NOT_CONFIGURED, NOT_VERIFIED} for check in checks):
        return 2
    return 0


def run(argv: list[str], *, cwd: Path = REPO_ROOT, timeout: int = 30) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        cwd=cwd,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )


def static_checks() -> list[Check]:
    checks: list[Check] = []
    required = [
        "hive-pipe/gateway.py",
        "hive-pipe/terminal_parser.py",
        "hive-pipe/install_gateway.sh",
        "hive-pipe/chatgpt_terminal_pull.py",
        "hive-pipe/install_chatgpt_terminal_pull.sh",
        "hive-pipe/bootstrap_chatgpt_terminal_pull.sh",
        "hive-pipe/deepseek_bridge.py",
        "hive-pipe/deepseek_web_bridge.py",
        "scripts/jetson_remote.sh",
        "scripts/external_work_bridge.py",
        ".github/workflows/jetson-command.yml",
        ".github/workflows/hive-pipe-terminal.yml",
        ".github/workflows/jetson-ai-access-validate.yml",
        "AI_BRIDGE_START_HERE.md",
    ]
    missing = [path for path in required if not (REPO_ROOT / path).is_file()]
    checks.append(Check(
        "repository bridge files",
        FAIL if missing else PASS,
        "missing: " + ", ".join(missing) if missing else f"{len(required)} required bridge files present",
        "Restore missing bridge files from main." if missing else "",
    ))

    python_files = [
        "hive-pipe/gateway.py",
        "hive-pipe/mudl.py",
        "hive-pipe/terminal_parser.py",
        "hive-pipe/chatgpt_terminal_pull.py",
        "hive-pipe/bridge_doctor.py",
        "hive-pipe/deepseek_bridge.py",
        "hive-pipe/deepseek_web_bridge.py",
        "scripts/external_work_bridge.py",
    ]
    existing_python = [str(REPO_ROOT / path) for path in python_files if (REPO_ROOT / path).is_file()]
    compiled = run([sys.executable, "-m", "py_compile", *existing_python])
    checks.append(Check(
        "bridge Python syntax",
        PASS if compiled.returncode == 0 else FAIL,
        "all bridge Python entry points compile" if compiled.returncode == 0 else compiled.stderr.strip()[-1200:],
        "Repair the reported syntax error before installing or restarting a bridge." if compiled.returncode else "",
    ))

    shell_files = [
        "hive-pipe/agent.sh",
        "hive-pipe/install_gateway.sh",
        "hive-pipe/create_client_token.sh",
        "hive-pipe/install_chatgpt_terminal_pull.sh",
        "hive-pipe/bootstrap_chatgpt_terminal_pull.sh",
        "scripts/jetson_remote.sh",
        "scripts/install_jetson_gateway.sh",
        "scripts/enable_jetson_ssh.sh",
    ]
    existing_shell = [str(REPO_ROOT / path) for path in shell_files if (REPO_ROOT / path).is_file()]
    shelled = run(["bash", "-n", *existing_shell])
    checks.append(Check(
        "bridge shell syntax",
        PASS if shelled.returncode == 0 else FAIL,
        "all bridge shell entry points parse" if shelled.returncode == 0 else shelled.stderr.strip()[-1200:],
        "Repair the reported shell syntax error before installation." if shelled.returncode else "",
    ))

    contracts: list[tuple[str, list[str]]] = [
        (".github/workflows/jetson-command.yml", ['"name": "terminal_run"', ' + "/mcp"']),
        ("hive-pipe/install_chatgpt_terminal_pull.sh", ["chatgpt-terminal", "chatgpt-terminal-backup"]),
        ("hive-pipe/gateway.py", ["terminal_reference", "terminal_run", "python_run", "cpp_compile_run"]),
        ("hive-pipe/deepseek_bridge.py", ["terminal_pwd", "terminal_which", "terminal_run"]),
    ]
    contract_failures: list[str] = []
    for relative, markers in contracts:
        path = REPO_ROOT / relative
        if not path.is_file():
            contract_failures.append(f"{relative}: missing")
            continue
        text = path.read_text(encoding="utf-8")
        absent = [marker for marker in markers if marker not in text]
        if absent:
            contract_failures.append(f"{relative}: missing {absent}")
    checks.append(Check(
        "bridge route contracts",
        FAIL if contract_failures else PASS,
        "; ".join(contract_failures) if contract_failures else "MCP, pull failover, Actions, and DeepSeek adapter contracts present",
        "Restore the missing route marker or update the doctor with the reviewed replacement contract." if contract_failures else "",
    ))
    return checks


def service_check(name: str, *, required: bool) -> Check:
    completed = run(["systemctl", "--user", "is-active", name], timeout=10)
    state = completed.stdout.strip() or completed.stderr.strip() or "unknown"
    if completed.returncode == 0 and state == "active":
        return Check(f"service {name}", PASS, "active")
    return Check(
        f"service {name}",
        FAIL if required else NOT_CONFIGURED,
        state,
        f"Install or restart {name}; then rerun the same doctor profile.",
    )


def load_token() -> str | None:
    direct = os.environ.get("HIVE_PIPE_TOKEN", "").strip()
    if direct:
        return direct
    token_file = Path(os.environ.get(
        "HIVE_PIPE_TOKEN_FILE",
        str(Path.home() / ".config/hive-pipe/tokens/codex.token"),
    )).expanduser()
    try:
        token = token_file.read_text(encoding="utf-8").strip()
    except OSError:
        return None
    return token or None


def post_mcp(url: str, token: str, name: str, arguments: dict[str, Any], timeout: int) -> dict[str, Any]:
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": name, "arguments": arguments},
    }
    request = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=timeout) as response:
        envelope = json.load(response)
    if "error" in envelope:
        raise RuntimeError(json.dumps(envelope["error"], sort_keys=True))
    structured = envelope.get("result", {}).get("structuredContent")
    if not isinstance(structured, dict):
        raise RuntimeError("MCP response lacks structuredContent")
    return structured


def gateway_live_checks(*, required: bool, timeout: int) -> list[Check]:
    checks = [
        service_check("hive-pipe-agent.service", required=required),
        service_check("hive-pipe-gateway.service", required=required),
    ]
    token = load_token()
    if not token:
        checks.append(Check(
            "local Hive Pipe MCP",
            FAIL if required else NOT_CONFIGURED,
            "no local codex token found",
            "Run hive-pipe/create_client_token.sh codex or set HIVE_PIPE_TOKEN_FILE without exposing the token.",
        ))
        return checks
    url = os.environ.get("HIVE_PIPE_MCP_URL", DEFAULT_MCP_URL).rstrip("/")
    if not url.endswith("/mcp"):
        url += "/mcp"
    try:
        smoke_args = {"argv": ["printf", "ONE_WAVE_BRIDGE_OK"], "timeout": timeout}
        reference = post_mcp(url, token, "terminal_reference", {
            "intention": "Verify the local Hive Pipe terminal route",
            "consequence": "Expect ONE_WAVE_BRIDGE_OK and exit zero; do not change repository files.",
            "action": {"name": "terminal_run", "arguments": smoke_args},
        }, timeout)
        smoke = post_mcp(url, token, "terminal_run", {**smoke_args, "reference_card": reference["reference_card"]}, timeout + 5)
        if reference.get("reference", {}).get("contract") != "one-wave-terminal-parser-v2":
            raise RuntimeError("terminal_reference returned the wrong parser contract")
        if not smoke.get("ok") or smoke.get("stdout") != "ONE_WAVE_BRIDGE_OK":
            raise RuntimeError(f"terminal smoke receipt failed: {json.dumps(smoke, sort_keys=True)[:1000]}")
        checks.append(Check("local Hive Pipe MCP", PASS, f"terminal_reference and terminal_run passed at {url}"))
    except (HTTPError, URLError, OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        checks.append(Check(
            "local Hive Pipe MCP",
            FAIL if required else WARN,
            f"{type(exc).__name__}: {exc}",
            "Check the gateway service, local token, parser version, and loopback endpoint before repairing any tunnel.",
        ))
    return checks


def pull_live_checks(*, required: bool) -> list[Check]:
    checks = [service_check("one-wave-chatgpt-terminal-pull.service", required=required)]
    runtime = Path(os.environ.get(
        "CHATGPT_TERMINAL_RUNTIME",
        str(Path.home() / ".local/share/one-wave-chatgpt-terminal-runtime"),
    )).expanduser()
    if not (runtime / ".git").is_dir():
        checks.append(Check(
            "pull bridge runtime",
            FAIL if required else NOT_CONFIGURED,
            f"not installed at {runtime}",
            "Run hive-pipe/install_chatgpt_terminal_pull.sh from the checkout of the machine to control.",
        ))
        return checks

    remote = run([
        "git", "ls-remote", "--heads", "origin",
        "refs/heads/chatgpt-terminal", "refs/heads/chatgpt-terminal-backup",
    ], cwd=runtime, timeout=30)
    found = remote.stdout.count("refs/heads/chatgpt-terminal")
    if remote.returncode == 0 and found >= 2:
        checks.append(Check("pull bridge routes", PASS, "primary and backup transport branches reachable"))
    else:
        checks.append(Check(
            "pull bridge routes",
            FAIL if required else WARN,
            (remote.stderr or remote.stdout or "both route refs were not returned").strip()[-1200:],
            "Repair Git authentication/network or create the missing dedicated transport branch.",
        ))

    state_path = Path(os.environ.get(
        "CHATGPT_TERMINAL_STATE_FILE",
        str(Path.home() / ".local/state/one-wave-chatgpt-terminal/bridge_state.json"),
    )).expanduser()
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
        controller = state.get("controller", {})
        routes = state.get("routes", {})
        open_routes = [name for name, value in routes.items() if value.get("state") == "open"]
        pending = [
            request_id for request_id, value in state.get("requests", {}).items()
            if value.get("phase") not in {"acknowledged"}
        ]
        if open_routes or pending:
            checks.append(Check(
                "pull bridge state machine",
                WARN,
                f"controller={controller.get('state', 'unknown')} open_routes={open_routes} pending={pending}",
                "Read each route/request guidance field; repair the named path and let the worker retry without reissuing completed commands.",
            ))
        else:
            checks.append(Check(
                "pull bridge state machine",
                PASS,
                f"controller={controller.get('state', 'unknown')} no open routes or pending deliveries",
            ))
    except (OSError, json.JSONDecodeError) as exc:
        checks.append(Check(
            "pull bridge state machine",
            WARN if not required else FAIL,
            f"state unavailable: {exc}",
            "Start the pull service and inspect its user journal; it creates the durable state file after cycling.",
        ))
    return checks


def optional_live_checks(timeout: int) -> list[Check]:
    checks: list[Check] = []
    try:
        request = Request("http://127.0.0.1:3000/health", headers={"Accept": "application/json"})
        with urlopen(request, timeout=timeout) as response:
            payload = json.load(response)
        checks.append(Check("DeepSeek web relay", PASS, json.dumps(payload, sort_keys=True)[:600]))
    except Exception as exc:
        checks.append(Check(
            "DeepSeek web relay",
            NOT_CONFIGURED,
            f"{type(exc).__name__}: {exc}",
            "Only if the free-web adapter is wanted: run scripts/bootstrap_deepseek_web_relay.sh and then its relay-health check.",
        ))

    ssh = run(["systemctl", "is-active", "ssh"], timeout=10)
    checks.append(Check(
        "SSH recovery route",
        PASS if ssh.returncode == 0 and ssh.stdout.strip() == "active" else NOT_CONFIGURED,
        ssh.stdout.strip() or ssh.stderr.strip() or "inactive",
        "Enable SSH only on the intended trusted network if this independent recovery route is required." if ssh.returncode else "",
    ))
    checks.append(Check(
        "GitHub Actions command lane live secrets/tunnel",
        NOT_VERIFIED,
        "repository contract is checked; secret and current tunnel health can only be proven by a workflow dispatch receipt",
        "Dispatch Jetson Command Lane with argv_json=[\"printf\",\"GITHUB_MCP_OK\"] and require exit 0.",
    ))
    return checks


def render(checks: list[Check], *, json_output: bool) -> None:
    if json_output:
        print(json.dumps({
            "checks": [asdict(check) for check in checks],
            "exit_code": overall_exit(checks),
            "status": FAIL if any(c.status == FAIL for c in checks) else (WARN if overall_exit(checks) else PASS),
        }, indent=2, sort_keys=True))
        return
    width = max((len(check.name) for check in checks), default=0)
    for check in checks:
        print(f"{check.status:14} {check.name:<{width}}  {check.detail}")
        if check.action:
            print(f"{'':14} {'':<{width}}  next: {check.action}")
    print(f"\nBRIDGE_DOCTOR_EXIT={overall_exit(checks)}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check One-Wave bridge code and live routes without mutating them.")
    parser.add_argument("--profile", choices=("ci", "pull", "gateway", "all"), default="all")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--timeout", type=int, default=10)
    args = parser.parse_args(argv)
    timeout = max(1, min(args.timeout, 30))

    checks = static_checks()
    if args.profile in {"gateway", "all"}:
        checks.extend(gateway_live_checks(required=True, timeout=timeout))
    if args.profile in {"pull", "all"}:
        checks.extend(pull_live_checks(required=True))
    if args.profile == "all":
        checks.extend(optional_live_checks(timeout))
    render(checks, json_output=args.json)
    return overall_exit(checks)


if __name__ == "__main__":
    raise SystemExit(main())
