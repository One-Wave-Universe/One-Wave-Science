#!/usr/bin/env python3
"""Shared Miniverse room runtime.

One persistent world state feeds both the text/AI bridge and the 3D browser view.
The lattice is stationary. Agent bodies move through legal lattice edges.
No language model is embedded here; AI clients are replaceable external participants.
"""
from __future__ import annotations

import argparse
import json
import mimetypes
import os
from pathlib import Path
import re
import threading
import time
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = ROOT / "room_manifest.json"
DEFAULT_STATE = Path.home() / ".local/share/one-wave/miniverse-room/state.json"
MAX_BODY = 32 * 1024
MAX_CHAT = 600
MAX_BODY_PARTS = 32
AGENT_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{0,31}$", re.I)
HEX_COLOR_RE = re.compile(r"^#[0-9a-fA-F]{6}$")
BODY_SHAPES = {"box", "sphere", "cylinder"}


def now_ms() -> int:
    return int(time.time() * 1000)


def _body_triplet(value: object, field: str, low: float, high: float) -> list[float]:
    if not isinstance(value, list) or len(value) != 3:
        raise ValueError(f"{field} must be a 3-number array")
    out: list[float] = []
    for item in value:
        if isinstance(item, bool) or not isinstance(item, (int, float)):
            raise ValueError(f"{field} must contain numbers")
        number = float(item)
        if not low <= number <= high:
            raise ValueError(f"{field} values must be between {low} and {high}")
        out.append(number)
    return out


def validate_body_spec(spec: object, fallback_color: str) -> dict:
    if not isinstance(spec, dict):
        raise ValueError("body must be a JSON object")
    style = spec.get("style", "voxel16")
    if style != "voxel16":
        raise ValueError("body style must be voxel16")
    scale = spec.get("scale", 1.0)
    if isinstance(scale, bool) or not isinstance(scale, (int, float)) or not 0.2 <= float(scale) <= 1.5:
        raise ValueError("body scale must be between 0.2 and 1.5")
    parts = spec.get("parts")
    if not isinstance(parts, list) or not 1 <= len(parts) <= MAX_BODY_PARTS:
        raise ValueError(f"body parts must contain 1-{MAX_BODY_PARTS} entries")

    cleaned = []
    for index, part in enumerate(parts):
        if not isinstance(part, dict):
            raise ValueError(f"body part {index} must be an object")
        shape = part.get("shape", "box")
        if shape not in BODY_SHAPES:
            raise ValueError(f"body part {index} shape must be box, sphere, or cylinder")
        color = part.get("color", fallback_color)
        if not isinstance(color, str) or not HEX_COLOR_RE.fullmatch(color):
            raise ValueError(f"body part {index} color must be #RRGGBB")
        emissive = part.get("emissive", "#000000")
        if not isinstance(emissive, str) or not HEX_COLOR_RE.fullmatch(emissive):
            raise ValueError(f"body part {index} emissive must be #RRGGBB")
        cleaned.append({
            "name": str(part.get("name", f"part-{index}"))[:32],
            "shape": shape,
            "size": _body_triplet(part.get("size", [0.5, 0.5, 0.5]), f"part {index} size", 0.05, 2.5),
            "position": _body_triplet(part.get("position", [0, 0.5, 0]), f"part {index} position", -3.0, 3.0),
            "rotation": _body_triplet(part.get("rotation", [0, 0, 0]), f"part {index} rotation", -6.3, 6.3),
            "color": color,
            "emissive": emissive,
        })
    return {"style": "voxel16", "scale": float(scale), "parts": cleaned}


class WorldStore:
    def __init__(self, state_path: Path | None = None):
        self.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        self.cells = {c["id"]: c for c in self.manifest["cells"]}
        self.zones = {z["id"]: z for z in self.manifest["zones"]}
        configured = os.environ.get("MINIVERSE_ROOM_STATE")
        self.state_path = Path(configured).expanduser() if configured else (state_path or DEFAULT_STATE)
        self.lock = threading.RLock()
        self.state = self._load()

    def _fresh(self) -> dict:
        return {
            "version": "MINIVERSE_ROOM_STATE_V0",
            "seq": 0,
            "baseline_zero": self.manifest["baseline_zero"],
            "agents": {},
            "chat": [],
            "bench_receipts": [],
            "events": [],
            "started_at": now_ms(),
        }

    def _load(self) -> dict:
        if not self.state_path.exists():
            return self._fresh()
        try:
            data = json.loads(self.state_path.read_text(encoding="utf-8"))
            if data.get("version") != "MINIVERSE_ROOM_STATE_V0":
                return self._fresh()
            return data
        except (OSError, ValueError):
            return self._fresh()

    def _save(self) -> None:
        self.state_path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.state_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        os.replace(tmp, self.state_path)

    def _event(self, kind: str, payload: dict) -> dict:
        self.state["seq"] += 1
        event = {"seq": self.state["seq"], "ts": now_ms(), "kind": kind, **payload}
        self.state["events"].append(event)
        self.state["events"] = self.state["events"][-300:]
        return event

    def snapshot(self) -> dict:
        with self.lock:
            return {
                "manifest": self.manifest,
                "state": self.state,
                "server_time": now_ms(),
            }

    def join(self, agent_id: str, name: str, role: str = "AI", color: str = "#62e6ff") -> dict:
        if not AGENT_RE.fullmatch(agent_id or ""):
            raise ValueError("agent_id must be 1-32 letters/numbers/._-")
        name = (name or agent_id).strip()[:40]
        role = (role or "AI").strip()[:40]
        color = color if re.fullmatch(r"#[0-9a-fA-F]{6}", color or "") else "#62e6ff"
        with self.lock:
            current = self.state["agents"].get(agent_id, {})
            agent = {
                "id": agent_id,
                "name": name,
                "role": role,
                "color": color,
                "cell": current.get("cell", self.manifest["baseline_zero"]),
                "facing": current.get("facing", "A+"),
                "mirror_state": current.get("mirror_state", "NORMAL"),
                "scale": current.get("scale", 1),
                "body": current.get("body"),
                "body_version": current.get("body_version", 0),
                "connected": True,
                "last_seen": now_ms(),
            }
            self.state["agents"][agent_id] = agent
            self._event("join", {"agent_id": agent_id, "cell": agent["cell"]})
            self._save()
            return agent

    def ping(self, agent_id: str) -> dict:
        with self.lock:
            agent = self._require_agent(agent_id)
            agent["connected"] = True
            agent["last_seen"] = now_ms()
            self._save()
            return agent

    def _require_agent(self, agent_id: str) -> dict:
        try:
            return self.state["agents"][agent_id]
        except KeyError as exc:
            raise ValueError(f"unknown agent: {agent_id}") from exc

    def move(self, agent_id: str, direction: str) -> dict:
        with self.lock:
            agent = self._require_agent(agent_id)
            cell = self.cells[agent["cell"]]
            if direction not in self.manifest["axes"]:
                raise ValueError(f"unknown direction: {direction}")
            destination = cell["neighbors"].get(direction)
            if destination is None:
                raise ValueError(f"room boundary: no {direction} edge from {cell['id']}")
            before = agent["cell"]
            agent["cell"] = destination
            agent["facing"] = direction
            agent["last_seen"] = now_ms()
            self._event("move", {
                "agent_id": agent_id,
                "from": before,
                "to": destination,
                "direction": direction,
            })
            self._save()
            return agent

    def set_body(self, agent_id: str, spec: object) -> dict:
        with self.lock:
            agent = self._require_agent(agent_id)
            body = validate_body_spec(spec, agent["color"])
            agent["body"] = body
            agent["body_version"] = int(agent.get("body_version", 0)) + 1
            agent["last_seen"] = now_ms()
            self._event("body", {
                "agent_id": agent_id,
                "body_version": agent["body_version"],
                "part_count": len(body["parts"]),
            })
            self._save()
            return agent

    def say(self, agent_id: str, text: str) -> dict:
        text = (text or "").strip()
        if not text:
            raise ValueError("message cannot be empty")
        if len(text) > MAX_CHAT:
            raise ValueError(f"message exceeds {MAX_CHAT} characters")
        with self.lock:
            agent = self._require_agent(agent_id)
            agent["last_seen"] = now_ms()
            msg = {
                "seq": self.state["seq"] + 1,
                "ts": now_ms(),
                "agent_id": agent_id,
                "name": agent["name"],
                "role": agent["role"],
                "text": text,
            }
            self.state["chat"].append(msg)
            self.state["chat"] = self.state["chat"][-120:]
            self._event("chat", {"agent_id": agent_id, "text": text})
            msg["seq"] = self.state["seq"]
            self._save()
            return msg

    def bench(self, agent_id: str, bench_id: str, action: str, summary: str) -> dict:
        if bench_id not in self.zones:
            raise ValueError(f"unknown bench/zone: {bench_id}")
        action = (action or "NOTE").strip()[:50]
        summary = (summary or "").strip()[:1000]
        if not summary:
            raise ValueError("bench summary cannot be empty")
        with self.lock:
            agent = self._require_agent(agent_id)
            receipt = {
                "seq": self.state["seq"] + 1,
                "ts": now_ms(),
                "agent_id": agent_id,
                "bench_id": bench_id,
                "action": action,
                "summary": summary,
                "cell": agent["cell"],
            }
            self.state["bench_receipts"].append(receipt)
            self.state["bench_receipts"] = self.state["bench_receipts"][-120:]
            self._event("bench", {
                "agent_id": agent_id,
                "bench_id": bench_id,
                "action": action,
            })
            receipt["seq"] = self.state["seq"]
            self._save()
            return receipt


class RoomHandler(BaseHTTPRequestHandler):
    server_version = "MiniverseRoom/0.2"

    @property
    def world(self) -> WorldStore:
        return self.server.world  # type: ignore[attr-defined]

    def log_message(self, fmt: str, *args: object) -> None:
        print(f"[miniverse-room] {self.address_string()} {fmt % args}")

    def _json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, separators=(",", ":")).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _body(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if length < 1 or length > MAX_BODY:
            raise ValueError("invalid request size")
        data = json.loads(self.rfile.read(length))
        if not isinstance(data, dict):
            raise ValueError("JSON body must be an object")
        return data

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/api/health":
            self._json(200, {"ok": True, "service": "miniverse-room", "version": "0.2"})
            return
        if path == "/api/state":
            self._json(200, self.world.snapshot())
            return
        self._serve_static(path)

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        try:
            body = self._body()
            if path == "/api/join":
                result = self.world.join(
                    body.get("agent_id", ""),
                    body.get("name", ""),
                    body.get("role", "AI"),
                    body.get("color", "#62e6ff"),
                )
            elif path == "/api/ping":
                result = self.world.ping(body.get("agent_id", ""))
            elif path == "/api/move":
                result = self.world.move(body.get("agent_id", ""), body.get("direction", ""))
            elif path == "/api/say":
                result = self.world.say(body.get("agent_id", ""), body.get("text", ""))
            elif path == "/api/body":
                result = self.world.set_body(body.get("agent_id", ""), body.get("body"))
            elif path == "/api/bench":
                result = self.world.bench(
                    body.get("agent_id", ""),
                    body.get("bench_id", ""),
                    body.get("action", ""),
                    body.get("summary", ""),
                )
            else:
                self._json(404, {"ok": False, "error": "not_found"})
                return
            self._json(200, {"ok": True, "result": result, "seq": self.world.state["seq"]})
        except (ValueError, KeyError, json.JSONDecodeError) as error:
            self._json(400, {"ok": False, "error": str(error)})

    def _serve_static(self, request_path: str) -> None:
        relative = "index.html" if request_path in ("", "/") else request_path.lstrip("/")
        target = (ROOT / relative).resolve()
        try:
            target.relative_to(ROOT)
        except ValueError:
            self.send_error(HTTPStatus.FORBIDDEN)
            return
        if not target.is_file():
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        body = target.read_bytes()
        mime = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


class RoomServer(ThreadingHTTPServer):
    def __init__(self, address: tuple[str, int], world: WorldStore):
        super().__init__(address, RoomHandler)
        self.world = world


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8787)
    parser.add_argument("--state")
    args = parser.parse_args()
    world = WorldStore(Path(args.state).expanduser() if args.state else None)
    server = RoomServer((args.host, args.port), world)
    print(f"MINIVERSE_ROOM http://{args.host}:{args.port} state={world.state_path}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
