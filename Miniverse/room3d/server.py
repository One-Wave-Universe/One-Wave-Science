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
EXPERIMENT_TYPES = {
    "lattice_pulse": {
        "label": "Lattice Pulse Spread",
        "description": "Abstract signal spread over the stationary 37-cell lattice. Software model only.",
        "defaults": {"amplitude": 1.0, "coupling": 0.22, "retention": 0.96, "steps": 18},
    },
    "reference_recovery": {
        "label": "Reference Recovery",
        "description": "Scalar perturbation relaxing toward Baseline Zero. Software model only.",
        "defaults": {"perturbation": 1.0, "retention": 0.82, "steps": 24, "tolerance": 0.05},
    },
}
EXPERIMENT_ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{0,47}$", re.I)
MAX_EXPERIMENTS = 120
MAX_EXPERIMENT_RUNS = 80
MAX_MEASUREMENTS = 48


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


def _number(value: object, field: str, low: float, high: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field} must be numeric")
    number = float(value)
    if not low <= number <= high:
        raise ValueError(f"{field} must be between {low} and {high}")
    return number


def _integer(value: object, field: str, low: int, high: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{field} must be an integer")
    if not low <= value <= high:
        raise ValueError(f"{field} must be between {low} and {high}")
    return value


def validate_experiment_parameters(kind: str, supplied: object) -> dict:
    if kind not in EXPERIMENT_TYPES:
        raise ValueError(f"unknown experiment type: {kind}")
    if supplied is None:
        supplied = {}
    if not isinstance(supplied, dict):
        raise ValueError("experiment parameters must be an object")
    params = dict(EXPERIMENT_TYPES[kind]["defaults"])
    params.update(supplied)
    if kind == "lattice_pulse":
        return {
            "amplitude": _number(params["amplitude"], "amplitude", -10.0, 10.0),
            "coupling": _number(params["coupling"], "coupling", 0.0, 0.49),
            "retention": _number(params["retention"], "retention", 0.0, 1.0),
            "steps": _integer(params["steps"], "steps", 1, 120),
        }
    return {
        "perturbation": _number(params["perturbation"], "perturbation", -10.0, 10.0),
        "retention": _number(params["retention"], "retention", 0.0, 1.0),
        "steps": _integer(params["steps"], "steps", 1, 240),
        "tolerance": _number(params["tolerance"], "tolerance", 0.000001, 2.0),
    }


def validate_measurements(value: object) -> dict:
    if value is None:
        return {}
    if not isinstance(value, dict) or len(value) > MAX_MEASUREMENTS:
        raise ValueError(f"measurements must be an object with at most {MAX_MEASUREMENTS} entries")
    cleaned = {}
    for key, item in value.items():
        name = str(key)[:48]
        if isinstance(item, bool) or item is None:
            cleaned[name] = item
        elif isinstance(item, (int, float)):
            cleaned[name] = float(item)
        elif isinstance(item, str):
            cleaned[name] = item[:240]
        else:
            raise ValueError(f"measurement {name} must be scalar/string/bool/null")
    return cleaned


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
            "experiments": {},
            "experiment_order": [],
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
            data.setdefault("experiments", {})
            data.setdefault("experiment_order", [])
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

    def experiment_catalog(self) -> dict:
        return EXPERIMENT_TYPES

    def _new_experiment_id(self) -> str:
        return f"exp-{self.state['seq'] + 1:06d}"

    def create_experiment(
        self,
        agent_id: str,
        kind: str,
        title: str = "",
        hypothesis: str = "",
        parameters: object = None,
        experiment_id: str = "",
    ) -> dict:
        with self.lock:
            agent = self._require_agent(agent_id)
            if len(self.state["experiments"]) >= MAX_EXPERIMENTS:
                raise ValueError("experiment store is full")
            exp_id = experiment_id.strip() or self._new_experiment_id()
            if not EXPERIMENT_ID_RE.fullmatch(exp_id):
                raise ValueError("experiment_id must be 1-48 letters/numbers/._-")
            if exp_id in self.state["experiments"]:
                raise ValueError(f"experiment already exists: {exp_id}")
            clean_params = validate_experiment_parameters(kind, parameters)
            experiment = {
                "id": exp_id,
                "kind": kind,
                "label": EXPERIMENT_TYPES[kind]["label"],
                "title": (title or EXPERIMENT_TYPES[kind]["label"]).strip()[:100],
                "hypothesis": (hypothesis or "").strip()[:1000],
                "parameters": clean_params,
                "created_by": agent_id,
                "created_at": now_ms(),
                "status": "DRAFT",
                "run_count": 0,
                "runs": [],
                "last_result": None,
            }
            self.state["experiments"][exp_id] = experiment
            self.state["experiment_order"].append(exp_id)
            event = self._event("experiment_create", {
                "agent_id": agent_id,
                "experiment_id": exp_id,
                "kind": kind,
            })
            experiment["created_seq"] = event["seq"]
            self._save()
            return experiment

    def _run_lattice_pulse(self, parameters: dict) -> dict:
        values = {cell_id: 0.0 for cell_id in self.cells}
        center = self.manifest["baseline_zero"]
        values[center] = parameters["amplitude"]
        center_trace = [round(values[center], 8)]
        active_trace = [1 if values[center] else 0]
        for _ in range(parameters["steps"]):
            next_values = {}
            for cell_id, cell in self.cells.items():
                neighbors = list(cell["neighbors"].values())
                neighbor_mean = (
                    sum(values[n] for n in neighbors) / len(neighbors)
                    if neighbors else values[cell_id]
                )
                mixed = values[cell_id] + parameters["coupling"] * (neighbor_mean - values[cell_id])
                next_values[cell_id] = parameters["retention"] * mixed
            values = next_values
            center_trace.append(round(values[center], 8))
            active_trace.append(sum(1 for value in values.values() if abs(value) >= 0.01))
        abs_values = {cell_id: abs(value) for cell_id, value in values.items()}
        return {
            "model": "abstract_graph_signal_spread",
            "measurements": {
                "final_peak_abs": round(max(abs_values.values()), 8),
                "final_total_abs": round(sum(abs_values.values()), 8),
                "final_active_cells": float(sum(1 for value in abs_values.values() if value >= 0.01)),
                "center_final": round(values[center], 8),
            },
            "series": {
                "center_trace": center_trace,
                "active_cells_trace": active_trace,
            },
            "claim_boundary": "Software graph experiment; not a physical One-Wave validation.",
        }

    def _run_reference_recovery(self, parameters: dict) -> dict:
        value = parameters["perturbation"]
        trace = [round(value, 10)]
        settling_step = None
        for step in range(1, parameters["steps"] + 1):
            value *= parameters["retention"]
            trace.append(round(value, 10))
            if settling_step is None and abs(value) <= parameters["tolerance"]:
                settling_step = step
        return {
            "model": "scalar_reference_recovery",
            "measurements": {
                "final_error_abs": round(abs(value), 10),
                "settled": settling_step is not None,
                "settling_step": float(settling_step) if settling_step is not None else None,
            },
            "series": {"error_trace": trace},
            "claim_boundary": "Software control/reference experiment; not a physical validation.",
        }

    def run_experiment(self, agent_id: str, experiment_id: str) -> dict:
        with self.lock:
            self._require_agent(agent_id)
            try:
                experiment = self.state["experiments"][experiment_id]
            except KeyError as exc:
                raise ValueError(f"unknown experiment: {experiment_id}") from exc
            if experiment["kind"] == "lattice_pulse":
                result = self._run_lattice_pulse(experiment["parameters"])
            elif experiment["kind"] == "reference_recovery":
                result = self._run_reference_recovery(experiment["parameters"])
            else:
                raise ValueError(f"no built-in runner for {experiment['kind']}")
            run = {
                "run": experiment["run_count"] + 1,
                "ts": now_ms(),
                "agent_id": agent_id,
                "source": "miniverse_builtin",
                "status": "COMPLETE",
                **result,
            }
            experiment["run_count"] += 1
            experiment["status"] = "COMPLETE"
            experiment["last_result"] = run
            experiment["runs"].append(run)
            experiment["runs"] = experiment["runs"][-MAX_EXPERIMENT_RUNS:]
            self._event("experiment_run", {
                "agent_id": agent_id,
                "experiment_id": experiment_id,
                "run": run["run"],
                "source": run["source"],
            })
            self._save()
            return run

    def attach_experiment_result(
        self,
        agent_id: str,
        experiment_id: str,
        source: str,
        summary: str,
        measurements: object = None,
    ) -> dict:
        with self.lock:
            self._require_agent(agent_id)
            try:
                experiment = self.state["experiments"][experiment_id]
            except KeyError as exc:
                raise ValueError(f"unknown experiment: {experiment_id}") from exc
            source = (source or "external").strip()[:64]
            summary = (summary or "").strip()[:1000]
            if not summary:
                raise ValueError("experiment result summary cannot be empty")
            run = {
                "run": experiment["run_count"] + 1,
                "ts": now_ms(),
                "agent_id": agent_id,
                "source": source,
                "status": "COMPLETE",
                "summary": summary,
                "measurements": validate_measurements(measurements),
                "claim_boundary": "External receipt; source evidence must be checked separately.",
            }
            experiment["run_count"] += 1
            experiment["status"] = "COMPLETE"
            experiment["last_result"] = run
            experiment["runs"].append(run)
            experiment["runs"] = experiment["runs"][-MAX_EXPERIMENT_RUNS:]
            self._event("experiment_result", {
                "agent_id": agent_id,
                "experiment_id": experiment_id,
                "run": run["run"],
                "source": source,
            })
            self._save()
            return run

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
    server_version = "MiniverseRoom/0.3"

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
            self._json(200, {"ok": True, "service": "miniverse-room", "version": "0.3"})
            return
        if path == "/api/state":
            self._json(200, self.world.snapshot())
            return
        if path == "/api/experiments/catalog":
            self._json(200, {"ok": True, "catalog": self.world.experiment_catalog()})
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
            elif path == "/api/experiment/create":
                result = self.world.create_experiment(
                    body.get("agent_id", ""),
                    body.get("kind", ""),
                    body.get("title", ""),
                    body.get("hypothesis", ""),
                    body.get("parameters"),
                    body.get("experiment_id", ""),
                )
            elif path == "/api/experiment/run":
                result = self.world.run_experiment(
                    body.get("agent_id", ""),
                    body.get("experiment_id", ""),
                )
            elif path == "/api/experiment/result":
                result = self.world.attach_experiment_result(
                    body.get("agent_id", ""),
                    body.get("experiment_id", ""),
                    body.get("source", "external"),
                    body.get("summary", ""),
                    body.get("measurements"),
                )
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
