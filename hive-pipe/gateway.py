#!/usr/bin/env python3
"""Authenticated REST and MCP gateway for the bounded Hive Pipe queue."""

from __future__ import annotations

import argparse
import hmac
import json
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re
import subprocess
import sys
import time

import mudl
import terminal_parser


JOB_ROUTE = re.compile(r"^/v1/jobs/([A-Za-z0-9][A-Za-z0-9._-]{0,95})$")
MAX_BODY = 16384
MCP_PROTOCOL = "2025-06-18"


def action_tool(action: str) -> dict:
    return {
        "name": action,
        "title": action.replace("_", " ").title(),
        "description": {
            "health": "Read the Jetson kernel and system identity.",
            "inventory_block_devices": "Read-only inventory of attached disks, filesystems, and mount points.",
            "repo_status": "Read the local One-Wave-Science git working-tree status.",
        }.get(action, f"Run the bounded Hive Pipe action {action}."),
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False},
    }


MCP_TOOLS = {action: action_tool(action) for action in sorted(mudl.ACTIONS)}
MCP_TOOLS.update({
    "terminal_pwd": {
        "name": "terminal_pwd",
        "title": "Terminal Pwd",
        "description": "Return the Jetson terminal working directory available to the AI parser.",
        "inputSchema": {
            "type": "object",
            "properties": {"cwd": {"type": "string"}},
            "additionalProperties": False,
        },
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False},
    },
    "terminal_which": {
        "name": "terminal_which",
        "title": "Terminal Which",
        "description": "Find an executable on the Jetson PATH.",
        "inputSchema": {
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"],
            "additionalProperties": False,
        },
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "openWorldHint": False},
    },
    "terminal_run": {
        "name": "terminal_run",
        "title": "Terminal Run",
        "description": "Run a structured argv command on the Jetson and return stdout, stderr, exit code, cwd, and timing. Runs as the normal unprivileged Jetson user; sudo/raw-disk/power commands and shell -c strings are blocked.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "argv": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                    "maxItems": 128,
                },
                "cwd": {"type": "string"},
                "timeout": {"type": "integer", "minimum": 1, "maximum": 300},
            },
            "required": ["argv"],
            "additionalProperties": False,
        },
        "annotations": {"readOnlyHint": False, "destructiveHint": True, "openWorldHint": False},
    },
})


def load_tokens() -> list[str]:
    tokens: list[str] = []
    single = os.environ.get("HIVE_PIPE_TOKEN")
    if single:
        tokens.append(single.strip())
    token_dir = Path(os.environ.get("HIVE_PIPE_TOKEN_DIR", Path.home() / ".config/hive-pipe/tokens"))
    if token_dir.is_dir():
        for path in sorted(token_dir.glob("*.token")):
            if path.is_symlink() or not path.is_file():
                continue
            if path.stat().st_mode & 0o077:
                raise RuntimeError(f"token file permissions must be 0600: {path}")
            value = path.read_text(encoding="utf-8").strip()
            if value:
                tokens.append(value)
    if not tokens:
        raise RuntimeError("no gateway tokens configured")
    return tokens


def wait_for_result(job_id: str, timeout: float = 35.0) -> dict:
    deadline = time.monotonic() + timeout
    path = mudl.RESULTS / f"{job_id}.json"
    while time.monotonic() < deadline:
        if path.is_file() and not path.is_symlink():
            return json.loads(path.read_text(encoding="utf-8"))
        time.sleep(0.1)
    raise TimeoutError(f"job {job_id} did not finish within {timeout:g} seconds")


def mcp_error(request_id: object, code: int, message: str) -> dict:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def tool_result(request_id: object, result: dict, *, failed: bool = False) -> dict:
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {
            "content": [{"type": "text", "text": json.dumps(result, sort_keys=True)}],
            "structuredContent": result,
            "isError": failed,
        },
    }


def handle_terminal_tool(request_id: object, name: str, arguments: object) -> dict:
    if not isinstance(arguments, dict):
        return mcp_error(request_id, -32602, "Terminal arguments must be an object")
    try:
        if name == "terminal_pwd":
            if set(arguments) - {"cwd"}:
                raise ValueError("terminal_pwd accepts only cwd")
            result = terminal_parser.pwd(arguments.get("cwd"))
        elif name == "terminal_which":
            if set(arguments) != {"name"}:
                raise ValueError("terminal_which requires exactly name")
            result = terminal_parser.which(arguments["name"])
        elif name == "terminal_run":
            if not set(arguments).issubset({"argv", "cwd", "timeout"}) or "argv" not in arguments:
                raise ValueError("terminal_run requires argv and accepts optional cwd/timeout")
            result = terminal_parser.run(
                arguments["argv"],
                cwd=arguments.get("cwd"),
                timeout=arguments.get("timeout", 60),
            )
        else:
            return mcp_error(request_id, -32602, "Unknown terminal tool")
        return tool_result(request_id, result, failed=not result.get("ok", False))
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        return tool_result(request_id, {"ok": False, "error": str(error)}, failed=True)


def handle_mcp(payload: object) -> dict | None:
    if not isinstance(payload, dict) or payload.get("jsonrpc") != "2.0":
        return mcp_error(None, -32600, "Invalid Request")
    request_id = payload.get("id")
    method = payload.get("method")
    params = payload.get("params", {})
    if method and method.startswith("notifications/"):
        return None
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": request_id, "result": {
            "protocolVersion": MCP_PROTOCOL,
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": "one-wave-hive-pipe", "version": "3.1"},
        }}
    if method == "ping":
        return {"jsonrpc": "2.0", "id": request_id, "result": {}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": request_id, "result": {"tools": list(MCP_TOOLS.values())}}
    if method == "tools/call":
        if not isinstance(params, dict):
            return mcp_error(request_id, -32602, "Invalid params")
        name = params.get("name")
        arguments = params.get("arguments", {})
        if name in {"terminal_pwd", "terminal_which", "terminal_run"}:
            return handle_terminal_tool(request_id, name, arguments)
        if name not in MCP_TOOLS or arguments != {}:
            return mcp_error(request_id, -32602, "Unknown tool or non-empty arguments")
        try:
            queued = mudl.enqueue(name)
            job_id = json.loads(queued.read_text(encoding="utf-8"))["id"]
            result = wait_for_result(job_id)
            return tool_result(request_id, result, failed=result.get("exit_code") != 0)
        except (OSError, ValueError, TimeoutError, json.JSONDecodeError) as error:
            return tool_result(request_id, {"ok": False, "error": str(error)}, failed=True)
    return mcp_error(request_id, -32601, "Method not found")


class GatewayHandler(BaseHTTPRequestHandler):
    server_version = "HivePipe/3.1"

    def log_message(self, message: str, *args: object) -> None:
        print(f"{self.address_string()} - {message % args}", file=sys.stderr)

    def send_json(self, status: HTTPStatus, payload: dict | None) -> None:
        body = b"" if payload is None else json.dumps(payload, sort_keys=True).encode("utf-8")
        self.send_response(status)
        if payload is not None:
            self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if body:
            self.wfile.write(body)

    def supplied_token(self) -> str:
        """Accept common MCP/API-key auth forms without weakening token checks."""
        authorization = self.headers.get("Authorization", "").strip()
        for prefix in ("Bearer ", "ApiKey ", "API-Key "):
            if authorization.lower().startswith(prefix.lower()):
                return authorization[len(prefix):].strip()
        for header_name in ("X-API-Key", "Api-Key"):
            value = self.headers.get(header_name, "").strip()
            if value:
                return value
        return ""

    def authenticated(self) -> bool:
        supplied = self.supplied_token()
        return bool(supplied) and any(hmac.compare_digest(supplied, token) for token in self.server.tokens)

    def require_auth(self) -> bool:
        if self.authenticated():
            return True
        self.send_json(HTTPStatus.UNAUTHORIZED, {
            "error": "unauthorized",
            "accepted_auth": ["Authorization: Bearer", "X-API-Key", "Api-Key"],
        })
        return False

    def read_payload(self) -> object:
        length = int(self.headers.get("Content-Length", "0"))
        if length < 1 or length > MAX_BODY:
            raise ValueError("invalid request size")
        return json.loads(self.rfile.read(length))

    def do_GET(self) -> None:
        if not self.require_auth():
            return
        if self.path == "/v1/health":
            self.send_json(HTTPStatus.OK, {
                "status": "ok",
                "actions": sorted(mudl.ACTIONS),
                "terminal_tools": ["terminal_pwd", "terminal_which", "terminal_run"],
                "mcp": "/mcp",
            })
            return
        match = JOB_ROUTE.fullmatch(self.path)
        if not match:
            self.send_json(HTTPStatus.NOT_FOUND, {"error": "not_found"})
            return
        job_id = match.group(1)
        result = mudl.RESULTS / f"{job_id}.json"
        if result.is_file() and not result.is_symlink():
            self.send_json(HTTPStatus.OK, json.loads(result.read_text(encoding="utf-8")))
            return
        for state, directory in (("pending", mudl.PENDING), ("processing", mudl.PROCESSING)):
            if (directory / f"{job_id}.json").is_file():
                self.send_json(HTTPStatus.ACCEPTED, {"id": job_id, "state": state})
                return
        self.send_json(HTTPStatus.NOT_FOUND, {"error": "unknown_job", "id": job_id})

    def do_POST(self) -> None:
        if not self.require_auth():
            return
        try:
            payload = self.read_payload()
            if self.path == "/mcp":
                response = handle_mcp(payload)
                self.send_json(HTTPStatus.ACCEPTED if response is None else HTTPStatus.OK, response)
                return
            if self.path != "/v1/jobs":
                self.send_json(HTTPStatus.NOT_FOUND, {"error": "not_found"})
                return
            if not isinstance(payload, dict) or set(payload) != {"action"}:
                raise ValueError("body must contain exactly one action")
            path = mudl.enqueue(payload["action"])
            request = json.loads(path.read_text(encoding="utf-8"))
            self.send_json(HTTPStatus.ACCEPTED, {"id": request["id"], "action": request["action"], "state": "pending"})
        except (ValueError, TypeError, json.JSONDecodeError) as error:
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": str(error)})


class GatewayServer(ThreadingHTTPServer):
    def __init__(self, address: tuple[str, int], tokens: list[str]):
        super().__init__(address, GatewayHandler)
        self.tokens = tokens


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    try:
        server = GatewayServer((args.host, args.port), load_tokens())
    except (OSError, RuntimeError) as error:
        print(f"HIVE_PIPE_GATEWAY_ERROR: {error}", file=sys.stderr)
        return 2
    print(f"HIVE_PIPE_GATEWAY http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
