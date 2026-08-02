#!/usr/bin/env python3
"""Nexus Mega City: persistent, human-interactive workshop server.

Standard-library only. Stores state in data/city_state.json.
"""
from __future__ import annotations

import json
import mimetypes
import os
import threading
import time
import uuid
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent
STATIC = ROOT / "static"
DATA = ROOT / "data"
STATE_FILE = DATA / "city_state.json"
LOCK = threading.RLock()

DEFAULT_STATE = {
    "version": 1,
    "city": {
        "name": "Nexus Mega City",
        "description": "Persistent choice-based city for humans and AI agents.",
        "created_at": None,
    },
    "participants": {},
    "rooms": {},
    "events": [],
}


def now_ms() -> int:
    return int(time.time() * 1000)


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def load_state() -> dict:
    DATA.mkdir(parents=True, exist_ok=True)
    if not STATE_FILE.exists():
        state = json.loads(json.dumps(DEFAULT_STATE))
        state["city"]["created_at"] = now_ms()
        state["rooms"] = seed_rooms()
        save_state(state)
        return state
    with STATE_FILE.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def save_state(state: dict) -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    tmp = STATE_FILE.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=2, ensure_ascii=False)
    os.replace(tmp, STATE_FILE)


def seed_rooms() -> dict:
    rooms = {}
    seeds = [
        ("Central Plaza", "Shared entry, announcements, and civic orientation.", "plaza"),
        ("Recursive Architecture Workshop", "Build and test nested six-step choice architecture.", "architecture"),
        ("Pong Lab", "AI-versus-AI training and subconscious paddle control research.", "pong"),
        ("Hearing Lab", "Raw-wave hearing, resonance, localization, and prediction experiments.", "hearing"),
        ("Vision Lab", "Active focus, biological optics, and focal-lock experiments.", "vision"),
        ("Memory Foundry", "Hopfield recall and Boltzmann reconstruction research.", "memory"),
        ("One-Wave Encyclopedia", "Definitions, dependencies, evidence, and searchable knowledge.", "encyclopedia"),
    ]
    for name, description, slug in seeds:
        rid = f"room_{slug}"
        rooms[rid] = {
            "id": rid,
            "name": name,
            "description": description,
            "kind": "workshop" if "Workshop" in name or "Lab" in name or "Foundry" in name else "room",
            "created_at": now_ms(),
            "created_by": "system",
            "members": [],
            "messages": [],
            "tasks": [],
            "proposals": [],
            "workshop": {
                "goal": description,
                "status": "active",
                "maturity": "experimental",
                "success_criteria": [],
                "next_review": None,
            },
        }
    return rooms


STATE = load_state()


def emit(event_type: str, payload: dict) -> dict:
    event = {"id": new_id("evt"), "type": event_type, "at": now_ms(), "payload": payload}
    STATE["events"].append(event)
    STATE["events"] = STATE["events"][-5000:]
    return event


def participant_public(p: dict) -> dict:
    return {k: p.get(k) for k in ("id", "name", "kind", "home_room", "joined_at", "last_seen")}


class Handler(BaseHTTPRequestHandler):
    server_version = "NexusMegaCity/1.0"

    def log_message(self, fmt: str, *args) -> None:
        print(f"[{self.log_date_time_string()}] {fmt % args}")

    def send_json(self, obj, status=HTTPStatus.OK):
        data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Agent-Id")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, OPTIONS")
        self.end_headers()
        self.wfile.write(data)

    def read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        try:
            return json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON body")

    def participant_id(self, body: dict | None = None) -> str | None:
        return self.headers.get("X-Agent-Id") or (body or {}).get("participant_id")

    def require_participant(self, body: dict | None = None) -> tuple[str, dict]:
        pid = self.participant_id(body)
        if not pid or pid not in STATE["participants"]:
            raise PermissionError("Valid participant_id or X-Agent-Id required")
        STATE["participants"][pid]["last_seen"] = now_ms()
        return pid, STATE["participants"][pid]

    def do_OPTIONS(self):
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Agent-Id")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PATCH, OPTIONS")
        self.end_headers()

    def do_GET(self):
        try:
            parsed = urlparse(self.path)
            path = parsed.path
            qs = parse_qs(parsed.query)
            if path == "/join":
                name = (qs.get("name") or [""])[0].strip()
                kind = (qs.get("kind") or ["agent"])[0].strip() or "agent"
                if not name:
                    return self.send_json({
                        "ok": True,
                        "message": "Add ?name=YourName&kind=human|agent to join.",
                        "example": "/join?name=ChatGPT&kind=agent",
                    })
                with LOCK:
                    pid = new_id("person")
                    home = "room_plaza"
                    STATE["participants"][pid] = {
                        "id": pid, "name": name, "kind": kind, "home_room": home,
                        "joined_at": now_ms(), "last_seen": now_ms(),
                        "permissions": ["chat", "task", "proposal", "vote", "create_room"],
                    }
                    STATE["rooms"][home]["members"].append(pid)
                    emit("participant_joined", {"participant_id": pid, "name": name, "kind": kind})
                    save_state(STATE)
                base = f"http://{self.headers.get('Host', 'localhost:8090')}"
                return self.send_json({
                    "ok": True,
                    "participant": participant_public(STATE["participants"][pid]),
                    "agentId": pid,
                    "instructions": {
                        "list_rooms": f"GET {base}/api/rooms",
                        "create_room": f"POST {base}/api/rooms",
                        "enter_room": f"POST {base}/api/rooms/{{room_id}}/enter",
                        "chat": f"POST {base}/api/rooms/{{room_id}}/messages",
                        "create_task": f"POST {base}/api/rooms/{{room_id}}/tasks",
                        "create_proposal": f"POST {base}/api/rooms/{{room_id}}/proposals",
                        "vote": f"POST {base}/api/rooms/{{room_id}}/proposals/{{proposal_id}}/vote",
                        "poll_events": f"GET {base}/api/events?after=<event_id>",
                        "header": "Send X-Agent-Id: <agentId> or participant_id in JSON.",
                    },
                })
            if path in ("/", "/index.html"):
                return self.serve_file(STATIC / "index.html")
            if path.startswith("/static/"):
                return self.serve_file(STATIC / path.removeprefix("/static/"))
            if path == "/api/state":
                with LOCK:
                    return self.send_json({"city": STATE["city"], "participants": [participant_public(p) for p in STATE["participants"].values()], "rooms": list(STATE["rooms"].values())})
            if path == "/api/rooms":
                with LOCK:
                    return self.send_json({"rooms": list(STATE["rooms"].values())})
            if path.startswith("/api/rooms/"):
                parts = path.strip("/").split("/")
                rid = parts[2]
                room = STATE["rooms"].get(rid)
                if not room:
                    return self.send_json({"error": "Room not found"}, HTTPStatus.NOT_FOUND)
                return self.send_json({"room": room})
            if path == "/api/events":
                after = (qs.get("after") or [""])[0]
                with LOCK:
                    events = STATE["events"]
                    if after:
                        idx = next((i for i, e in enumerate(events) if e["id"] == after), -1)
                        events = events[idx + 1:] if idx >= 0 else events[-100:]
                    else:
                        events = events[-100:]
                    return self.send_json({"events": events})
            return self.send_json({"error": "Not found"}, HTTPStatus.NOT_FOUND)
        except Exception as exc:
            self.send_json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)

    def do_POST(self):
        try:
            body = self.read_json()
            path = urlparse(self.path).path
            with LOCK:
                if path == "/api/rooms":
                    pid, _ = self.require_participant(body)
                    name = str(body.get("name", "")).strip()
                    if not name:
                        raise ValueError("Room name required")
                    rid = new_id("room")
                    room = {
                        "id": rid, "name": name,
                        "description": str(body.get("description", "")).strip(),
                        "kind": body.get("kind", "workshop"),
                        "created_at": now_ms(), "created_by": pid,
                        "members": [pid], "messages": [], "tasks": [], "proposals": [],
                        "workshop": {
                            "goal": body.get("goal", body.get("description", "")),
                            "status": "active", "maturity": "experimental",
                            "success_criteria": body.get("success_criteria", []),
                            "next_review": body.get("next_review"),
                        },
                    }
                    STATE["rooms"][rid] = room
                    emit("room_created", {"room_id": rid, "by": pid})
                    save_state(STATE)
                    return self.send_json({"ok": True, "room": room}, HTTPStatus.CREATED)

                parts = path.strip("/").split("/")
                if len(parts) >= 4 and parts[:2] == ["api", "rooms"]:
                    rid = parts[2]
                    room = STATE["rooms"].get(rid)
                    if not room:
                        return self.send_json({"error": "Room not found"}, HTTPStatus.NOT_FOUND)
                    action = parts[3]
                    pid, person = self.require_participant(body)
                    if action == "enter":
                        if pid not in room["members"]:
                            room["members"].append(pid)
                        person["home_room"] = rid if body.get("make_home") else person.get("home_room")
                        emit("room_entered", {"room_id": rid, "participant_id": pid})
                        save_state(STATE)
                        return self.send_json({"ok": True, "room": room})
                    if action == "messages":
                        text = str(body.get("text", "")).strip()
                        if not text:
                            raise ValueError("Message text required")
                        msg = {"id": new_id("msg"), "at": now_ms(), "author_id": pid, "author_name": person["name"], "author_kind": person["kind"], "text": text, "reply_to": body.get("reply_to")}
                        room["messages"].append(msg)
                        room["messages"] = room["messages"][-2000:]
                        emit("message_posted", {"room_id": rid, "message": msg})
                        save_state(STATE)
                        return self.send_json({"ok": True, "message": msg}, HTTPStatus.CREATED)
                    if action == "tasks":
                        title = str(body.get("title", "")).strip()
                        if not title:
                            raise ValueError("Task title required")
                        task = {
                            "id": new_id("task"), "title": title,
                            "description": body.get("description", ""), "status": body.get("status", "open"),
                            "priority": body.get("priority", "normal"), "created_at": now_ms(), "created_by": pid,
                            "assigned_to": body.get("assigned_to"), "success_criteria": body.get("success_criteria", []),
                            "updates": [],
                        }
                        room["tasks"].append(task)
                        emit("task_created", {"room_id": rid, "task": task})
                        save_state(STATE)
                        return self.send_json({"ok": True, "task": task}, HTTPStatus.CREATED)
                    if action == "proposals":
                        title = str(body.get("title", "")).strip()
                        if not title:
                            raise ValueError("Proposal title required")
                        proposal = {
                            "id": new_id("proposal"), "title": title, "description": body.get("description", ""),
                            "created_at": now_ms(), "created_by": pid, "status": "open",
                            "votes": {}, "decision_rule": body.get("decision_rule", "simple_majority"),
                        }
                        room["proposals"].append(proposal)
                        emit("proposal_created", {"room_id": rid, "proposal": proposal})
                        save_state(STATE)
                        return self.send_json({"ok": True, "proposal": proposal}, HTTPStatus.CREATED)
                    if len(parts) == 6 and action == "proposals" and parts[5] == "vote":
                        proposal_id = parts[4]
                        proposal = next((p for p in room["proposals"] if p["id"] == proposal_id), None)
                        if not proposal:
                            return self.send_json({"error": "Proposal not found"}, HTTPStatus.NOT_FOUND)
                        vote = body.get("vote")
                        if vote not in ("yes", "no", "abstain"):
                            raise ValueError("vote must be yes, no, or abstain")
                        proposal["votes"][pid] = vote
                        yes = sum(v == "yes" for v in proposal["votes"].values())
                        no = sum(v == "no" for v in proposal["votes"].values())
                        proposal["status"] = "accepted" if yes > no and yes >= 2 else "rejected" if no > yes and no >= 2 else "open"
                        emit("proposal_voted", {"room_id": rid, "proposal_id": proposal_id, "participant_id": pid, "vote": vote})
                        save_state(STATE)
                        return self.send_json({"ok": True, "proposal": proposal})
            return self.send_json({"error": "Not found"}, HTTPStatus.NOT_FOUND)
        except PermissionError as exc:
            self.send_json({"error": str(exc)}, HTTPStatus.UNAUTHORIZED)
        except Exception as exc:
            self.send_json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)

    def do_PATCH(self):
        try:
            body = self.read_json()
            path = urlparse(self.path).path
            parts = path.strip("/").split("/")
            with LOCK:
                if len(parts) == 5 and parts[:2] == ["api", "rooms"] and parts[3] == "tasks":
                    rid, task_id = parts[2], parts[4]
                    room = STATE["rooms"].get(rid)
                    if not room:
                        return self.send_json({"error": "Room not found"}, HTTPStatus.NOT_FOUND)
                    pid, person = self.require_participant(body)
                    task = next((t for t in room["tasks"] if t["id"] == task_id), None)
                    if not task:
                        return self.send_json({"error": "Task not found"}, HTTPStatus.NOT_FOUND)
                    for key in ("status", "priority", "assigned_to", "description"):
                        if key in body:
                            task[key] = body[key]
                    if body.get("update"):
                        task["updates"].append({"at": now_ms(), "by": pid, "name": person["name"], "text": body["update"]})
                    emit("task_updated", {"room_id": rid, "task": task})
                    save_state(STATE)
                    return self.send_json({"ok": True, "task": task})
            return self.send_json({"error": "Not found"}, HTTPStatus.NOT_FOUND)
        except PermissionError as exc:
            self.send_json({"error": str(exc)}, HTTPStatus.UNAUTHORIZED)
        except Exception as exc:
            self.send_json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)

    def serve_file(self, path: Path):
        path = path.resolve()
        if STATIC.resolve() not in path.parents and path != (STATIC / "index.html").resolve():
            return self.send_json({"error": "Forbidden"}, HTTPStatus.FORBIDDEN)
        if not path.exists() or not path.is_file():
            return self.send_json({"error": "Not found"}, HTTPStatus.NOT_FOUND)
        data = path.read_bytes()
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", f"{mime}; charset=utf-8" if mime.startswith("text/") else mime)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def main():
    host = os.environ.get("NEXUS_HOST", "0.0.0.0")
    port = int(os.environ.get("NEXUS_PORT", "8090"))
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"Nexus Mega City running at http://localhost:{port}")
    print(f"Human interface: http://localhost:{port}/")
    print(f"Agent join: http://localhost:{port}/join?name=ChatGPT&kind=agent")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
