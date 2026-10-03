"""Local app server. Same core as the CLI; the browser is only a view.

Binds 127.0.0.1 by default. API keys stay in this process's environment and
never reach the page.

GET  /                 app.html
GET  /api/providers    provider names, default models, key present yes/no
GET  /api/reference    Reference Point Zero snapshot of the checkout
POST /api/start        {goal, field:{provider,model}, void:{provider,model}, max_turns}
POST /api/step         {id}  -> one Field/Void turn record
GET  /api/ledger?id=   JSONL ledger for a session
"""

from __future__ import annotations

import json
import threading
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

try:
    from .pair_loop import FieldVoidPair
    from .providers import PRESETS, Provider, ProviderError, available
    from .repo_lens import RepoLens, reference_snapshot
except ImportError:
    from pair_loop import FieldVoidPair
    from providers import PRESETS, Provider, ProviderError, available
    from repo_lens import RepoLens, reference_snapshot

APP_HTML = Path(__file__).with_name("app.html")
MAX_SESSIONS = 32


def make_provider(spec: dict) -> Provider:
    name = (spec or {}).get("provider", "offline")
    if name not in PRESETS:
        raise ValueError(f"unknown provider {name!r}")
    model = (spec or {}).get("model") or PRESETS[name]["model"]
    return Provider(name=name, model=str(model))


class App:
    def __init__(self, lens: RepoLens) -> None:
        self.lens = lens
        self.sessions: dict[str, FieldVoidPair] = {}
        self.locks: dict[str, threading.Lock] = {}
        self.guard = threading.Lock()

    def start(self, body: dict) -> dict:
        goal = str(body.get("goal", "")).strip()
        if not goal:
            raise ValueError("goal is required")
        turns = int(body.get("max_turns", 8))
        if not 1 <= turns <= 50:
            raise ValueError("max_turns must be 1..50")
        pair = FieldVoidPair(goal=goal, field_ai=make_provider(body.get("field")),
                             void_ai=make_provider(body.get("void")),
                             lens=self.lens, max_turns=turns)
        sid = uuid.uuid4().hex[:12]
        with self.guard:
            if len(self.sessions) >= MAX_SESSIONS:
                oldest = next(iter(self.sessions))
                self.sessions.pop(oldest)
                self.locks.pop(oldest, None)
            self.sessions[sid] = pair
            self.locks[sid] = threading.Lock()
        return {"id": sid, "summary": pair.summary()}

    def step(self, body: dict) -> dict:
        sid = str(body.get("id", ""))
        pair = self.sessions.get(sid)
        if pair is None:
            raise KeyError("unknown session")
        with self.locks[sid]:
            if pair.stop:
                return {"record": None, "summary": pair.summary()}
            try:
                rec = pair.step()
            except ProviderError as e:
                pair.stop = "PROVIDER_ERROR"
                rec = {"turn": pair.turn, "error": str(e), "stop": pair.stop}
                pair.history.append(rec)
            return {"record": rec, "summary": pair.summary()}

    def ledger(self, sid: str) -> str:
        pair = self.sessions.get(sid)
        if pair is None:
            raise KeyError("unknown session")
        lines = [json.dumps(r) for r in pair.history] + [json.dumps(pair.summary())]
        return "\n".join(lines) + "\n"


def handler_for(app: App):
    class Handler(BaseHTTPRequestHandler):
        server_version = "fvpair/1"

        def log_message(self, fmt, *args):  # quiet; ledger is the record
            pass

        def _send(self, code: int, payload, ctype="application/json") -> None:
            data = payload if isinstance(payload, bytes) else (
                payload.encode() if isinstance(payload, str) else json.dumps(payload).encode())
            self.send_response(code)
            self.send_header("content-type", ctype + "; charset=utf-8")
            self.send_header("content-length", str(len(data)))
            self.send_header("cache-control", "no-store")
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            u = urlparse(self.path)
            try:
                if u.path in ("/", "/index.html"):
                    return self._send(200, APP_HTML.read_bytes(), "text/html")
                if u.path == "/api/providers":
                    return self._send(200, {"providers": available()})
                if u.path == "/api/reference":
                    return self._send(200, reference_snapshot(app.lens.root) |
                                      {"files": len(app.lens.files)})
                if u.path == "/api/ledger":
                    sid = parse_qs(u.query).get("id", [""])[0]
                    return self._send(200, app.ledger(sid), "application/x-ndjson")
                self._send(404, {"error": "not found"})
            except KeyError as e:
                self._send(404, {"error": str(e)})

        def do_POST(self):
            u = urlparse(self.path)
            try:
                n = int(self.headers.get("content-length") or 0)
                if n > 1_000_000:
                    return self._send(413, {"error": "body too large"})
                body = json.loads(self.rfile.read(n) or b"{}")
                if u.path == "/api/start":
                    return self._send(200, app.start(body))
                if u.path == "/api/step":
                    return self._send(200, app.step(body))
                self._send(404, {"error": "not found"})
            except (ValueError, json.JSONDecodeError) as e:
                self._send(400, {"error": str(e)})
            except KeyError as e:
                self._send(404, {"error": str(e)})

    return Handler


def serve(host: str = "127.0.0.1", port: int = 8742, lens: RepoLens | None = None,
          ready=None) -> ThreadingHTTPServer:
    app = App(lens or RepoLens.build())
    httpd = ThreadingHTTPServer((host, port), handler_for(app))
    if ready:
        ready(httpd)
    return httpd
