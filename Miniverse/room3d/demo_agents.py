#!/usr/bin/env python3
"""Populate visible bridge-ready bodies; no model inference occurs here."""
from pathlib import Path
import json
from client import request, DEFAULT_URL

ROOT = Path(__file__).resolve().parent
AGENTS = [
    ("field", "FIELD", "AI PORT / BUILDER", "#6df6ff", "field-builder.json"),
    ("void", "VOID", "AI PORT / CHECKER", "#ff7edb", "void-checker.json"),
    ("m4", "M4", "AI PORT / ROUTER", "#98ffb4", "m4-router.json"),
]

for agent_id, name, role, color, body_file in AGENTS:
    request(DEFAULT_URL, "/api/join", {
        "agent_id": agent_id, "name": name, "role": role, "color": color
    })
    spec = json.loads((ROOT / "bodies" / body_file).read_text(encoding="utf-8"))
    request(DEFAULT_URL, "/api/body", {"agent_id": agent_id, "body": spec})
    request(DEFAULT_URL, "/api/say", {
        "agent_id": agent_id,
        "text": "Bridge-ready body online; external AI client may take this identity."
    })

print("populated 3 bridge-ready custom bodies")
