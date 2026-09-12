#!/usr/bin/env python3
"""Authenticated HTTP gateway for the bounded Hive Pipe action queue."""

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

import mudl


JOB_ROUTE = re.compile(r"^/v1/jobs/([A-Za-z0-9][A-Za-z0-9._-]{0,95})$")
MAX_BODY = 4096


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
            mode = path.stat().st_mode & 0o777
            if mode & 0o077:
                raise RuntimeError(f"token file permissions must be 0600: {path}")
            value = path.read_text(encoding="utf-8").strip()
            if value:
                tokens.append(value)
    if not tokens:
        raise RuntimeError("no gateway tokens configured")
    return tokens


class GatewayHandler(BaseHTTPRequestHandler):
    server_version = "HivePipe/1"

    def log_message(self, message: str, *args: object) -> None:
        print(f"{self.address_string()} - {message % args}", file=sys.stderr)

    def json_response(self, status: HTTPStatus, payload: dict) -> None:
        body = json.dumps(payload, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def authenticated(self) -> bool:
        header = self.headers.get("Authorization", "")
        if not header.startswith("Bearer "):
            return False
        supplied = header[7:]
        return any(hmac.compare_digest(supplied, token) for token in self.server.tokens)

    def require_auth(self) -> bool:
        if self.authenticated():
            return True
        self.json_response(HTTPStatus.UNAUTHORIZED, {"error": "unauthorized"})
        return False

    def do_GET(self) -> None:
        if not self.require_auth():
            return
        if self.path == "/v1/health":
            self.json_response(HTTPStatus.OK, {"status": "ok", "actions": sorted(mudl.ACTIONS)})
            return
        match = JOB_ROUTE.fullmatch(self.path)
        if not match:
            self.json_response(HTTPStatus.NOT_FOUND, {"error": "not_found"})
            return
        job_id = match.group(1)
        result = mudl.RESULTS / f"{job_id}.json"
        if result.is_file() and not result.is_symlink():
            self.json_response(HTTPStatus.OK, json.loads(result.read_text(encoding="utf-8")))
            return
        for state, directory in (("pending", mudl.PENDING), ("processing", mudl.PROCESSING)):
            if (directory / f"{job_id}.json").is_file():
                self.json_response(HTTPStatus.ACCEPTED, {"id": job_id, "state": state})
                return
        self.json_response(HTTPStatus.NOT_FOUND, {"error": "unknown_job", "id": job_id})

    def do_POST(self) -> None:
        if not self.require_auth():
            return
        if self.path != "/v1/jobs":
            self.json_response(HTTPStatus.NOT_FOUND, {"error": "not_found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length < 1 or length > MAX_BODY:
                raise ValueError("invalid request size")
            payload = json.loads(self.rfile.read(length))
            if not isinstance(payload, dict) or set(payload) != {"action"}:
                raise ValueError("body must contain exactly one action")
            path = mudl.enqueue(payload["action"])
            request = json.loads(path.read_text(encoding="utf-8"))
            self.json_response(HTTPStatus.ACCEPTED, {
                "id": request["id"], "action": request["action"], "state": "pending"
            })
        except (ValueError, TypeError, json.JSONDecodeError) as error:
            self.json_response(HTTPStatus.BAD_REQUEST, {"error": str(error)})


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
