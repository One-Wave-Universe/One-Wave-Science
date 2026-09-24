#!/usr/bin/env python3
"""Authenticated localhost command gateway for the Jetson.

Designed to sit behind a Cloudflare tunnel or another HTTPS reverse proxy.
It intentionally binds to loopback by default and runs commands as the
unprivileged account that launches the service.
"""

from __future__ import annotations

import hmac
import json
import os
import subprocess
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

HOST = os.environ.get("HIVE_GATEWAY_HOST", "127.0.0.1")
PORT = int(os.environ.get("HIVE_GATEWAY_PORT", "8765"))
TOKEN_FILE = Path(
    os.environ.get(
        "HIVE_GATEWAY_TOKEN_FILE",
        str(Path.home() / ".config/hive-pipe/gateway.token"),
    )
)
DISABLE_FILE = Path(
    os.environ.get(
        "HIVE_GATEWAY_DISABLE_FILE",
        str(Path.home() / ".config/hive-pipe/DISABLED"),
    )
)
MAX_TIMEOUT = int(os.environ.get("HIVE_GATEWAY_MAX_TIMEOUT", "600"))
MAX_BODY = int(os.environ.get("HIVE_GATEWAY_MAX_BODY", "65536"))
MAX_OUTPUT = int(os.environ.get("HIVE_GATEWAY_MAX_OUTPUT", str(1024 * 1024)))


def load_token() -> str:
    try:
        token = TOKEN_FILE.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        raise SystemExit(f"missing gateway token: {TOKEN_FILE}")
    if len(token) < 32:
        raise SystemExit("gateway token is too short; run install_jetson_gateway.sh")
    return token


TOKEN = load_token()


def clipped(text: str) -> tuple[str, bool]:
    raw = text.encode("utf-8", errors="replace")
    if len(raw) <= MAX_OUTPUT:
        return text, False
    cut = raw[:MAX_OUTPUT].decode("utf-8", errors="replace")
    return cut + "\n[output clipped]\n", True


class Handler(BaseHTTPRequestHandler):
    server_version = "HivePipeGateway/1"

    def log_message(self, fmt: str, *args: object) -> None:
        sys.stderr.write(
            f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} "
            f"{self.client_address[0]} {fmt % args}\n"
        )

    def send_json(self, code: int, payload: dict) -> None:
        data = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def authorized(self) -> bool:
        auth = self.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return False
        supplied = auth[7:].strip()
        return hmac.compare_digest(supplied, TOKEN)

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/healthz":
            self.send_json(
                200,
                {
                    "ok": True,
                    "disabled": DISABLE_FILE.exists(),
                    "uid": os.getuid(),
                    "cwd": os.getcwd(),
                },
            )
            return
        self.send_json(404, {"ok": False, "error": "not found"})

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        if path != "/v1/exec":
            self.send_json(404, {"ok": False, "error": "not found"})
            return
        if not self.authorized():
            self.send_json(401, {"ok": False, "error": "unauthorized"})
            return
        if DISABLE_FILE.exists():
            self.send_json(503, {"ok": False, "error": "gateway disabled"})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self.send_json(400, {"ok": False, "error": "bad content length"})
            return
        if length <= 0 or length > MAX_BODY:
            self.send_json(413, {"ok": False, "error": "request too large"})
            return

        try:
            body = json.loads(self.rfile.read(length))
        except (json.JSONDecodeError, UnicodeDecodeError):
            self.send_json(400, {"ok": False, "error": "invalid json"})
            return

        command = body.get("command")
        if not isinstance(command, str) or not command.strip():
            self.send_json(400, {"ok": False, "error": "command is required"})
            return

        requested_timeout = body.get("timeout", 120)
        try:
            timeout = max(1, min(int(requested_timeout), MAX_TIMEOUT))
        except (TypeError, ValueError):
            self.send_json(400, {"ok": False, "error": "timeout must be an integer"})
            return

        cwd = body.get("cwd")
        if cwd is not None and not isinstance(cwd, str):
            self.send_json(400, {"ok": False, "error": "cwd must be a string"})
            return
        if cwd:
            cwd_path = Path(cwd).expanduser().resolve()
            if not cwd_path.is_dir():
                self.send_json(400, {"ok": False, "error": "cwd does not exist"})
                return
            cwd = str(cwd_path)

        started = time.time()
        audit = {
            "event": "exec",
            "command": command,
            "cwd": cwd or os.getcwd(),
            "timeout": timeout,
        }
        self.log_message("AUDIT %s", json.dumps(audit, separators=(",", ":")))

        try:
            proc = subprocess.run(
                ["bash", "-lc", command],
                cwd=cwd,
                text=True,
                capture_output=True,
                timeout=timeout,
                env=os.environ.copy(),
            )
            stdout, stdout_clipped = clipped(proc.stdout)
            stderr, stderr_clipped = clipped(proc.stderr)
            self.send_json(
                200,
                {
                    "ok": proc.returncode == 0,
                    "exit_code": proc.returncode,
                    "stdout": stdout,
                    "stderr": stderr,
                    "output_clipped": stdout_clipped or stderr_clipped,
                    "duration_ms": int((time.time() - started) * 1000),
                },
            )
        except subprocess.TimeoutExpired as exc:
            out = exc.stdout or ""
            err = exc.stderr or ""
            if isinstance(out, bytes):
                out = out.decode("utf-8", errors="replace")
            if isinstance(err, bytes):
                err = err.decode("utf-8", errors="replace")
            stdout, _ = clipped(out)
            stderr, _ = clipped(err)
            self.send_json(
                504,
                {
                    "ok": False,
                    "error": "timeout",
                    "stdout": stdout,
                    "stderr": stderr,
                    "duration_ms": int((time.time() - started) * 1000),
                },
            )

    def do_PUT(self) -> None:
        self.send_json(405, {"ok": False, "error": "method not allowed"})

    do_DELETE = do_PUT
    do_PATCH = do_PUT


def main() -> None:
    if os.geteuid() == 0:
        raise SystemExit("refusing to run gateway as root")
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(
        f"hive-pipe gateway listening on http://{HOST}:{PORT} "
        f"as uid={os.getuid()}",
        flush=True,
    )
    server.serve_forever()


if __name__ == "__main__":
    main()
