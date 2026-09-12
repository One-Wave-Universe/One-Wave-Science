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
import sys
import time

import mudl


JOB_ROUTE = re.compile(r"^/v1/jobs/([A-Za-z0-9][A-Za-z0-9._-]{0,95})$")
MAX_BODY = 4096
MCP_PROTOCOL = "2025-06-18"
MCP_TOOLS = {
    action: {
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
    for action in sorted(mudl.ACTIONS)
}


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
            "serverInfo": {"name": "one-wave-hive-pipe", "version": "2.0"},
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
        if name not in MCP_TOOLS or arguments != {}:
            return mcp_error(request_id, -32602, "Unknown tool or non-empty arguments")
        try:
            queued = mudl.enqueue(name)
            job_id = json.loads(queued.read_text(encoding="utf-8"))["id"]
            result = wait_for_result(job_id)
            failed = result.get("exit_code") != 0
            return {"jsonrpc": "2.0", "id": request_id, "result": {
                "content": [{"type": "text", "text": json.dumps(result, sort_keys=True)}],
                "structuredContent": result,
                "isError": failed,
            }}
        except (OSError, ValueError, TimeoutError, json.JSONDecodeError) as error:
            return {"jsonrpc": "2.0", "id": request_id, "result": {
                "content": [{"type": "text", "text": str(error)}], "isError": True,
            }}
    return mcp_error(request_id, -32601, "Method not found")


class GatewayHandler(BaseHTTPRequestHandler):
    server_version = "HivePipe/2"

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

    def authenticated(self) -> bool:
        header = self.headers.get("Authorization", "")
        supplied = header[7:] if header.startswith("Bearer ") else ""
        return bool(supplied) and any(hmac.compare_digest(supplied, token) for token in self.server.tokens)

    def require_auth(self) -> bool:
        if self.authenticated():
            return True
        self.send_json(HTTPStatus.UNAUTHORIZED, {"error": "unauthorized"})
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
            self.send_json(HTTPStatus.OK, {"status": "ok", "actions": sorted(mudl.ACTIONS), "mcp": "/mcp"})
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
