#!/usr/bin/env python3
"""Y5-style NODE->LINKAGE sandbox over the four registered casings.

Reads REGISTRY.json + LINKAGE.json + cells/*/STATE.json.
Writes only cells/*/STATE.json.

A-111 neighbor-average coupling is represented as linkage pressure:
    pressure_i = beta * (<q_j> - q_i)

This module does NOT silently change q. q remains the hysteresis memory path
advanced by hysteresis.py / wave_app.py.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
CELLS = ROOT / "cells"
REGISTRY = ROOT / "REGISTRY.json"
LINKAGE = ROOT / "LINKAGE.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(cell_id: str, state: dict[str, Any]) -> None:
    path = CELLS / cell_id / "STATE.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def registered_ids() -> set[str]:
    reg = load_json(REGISTRY)
    return {str(c["id"]) for c in reg["cells"]}


def adjacency() -> dict[str, list[tuple[str, float, str]]]:
    ids = registered_ids()
    doc = load_json(LINKAGE)
    graph = {cell_id: [] for cell_id in ids}
    for edge in doc.get("links", []):
        a, b = str(edge["a"]), str(edge["b"])
        if a not in ids or b not in ids:
            raise RuntimeError(f"link references unregistered cell: {a}<->{b}")
        w = float(edge.get("weight", 1.0))
        t = str(edge.get("type", "LINK"))
        graph[a].append((b, w, t))
        graph[b].append((a, w, t))
    return graph


def read_states() -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for cell_id in registered_ids():
        path = CELLS / cell_id / "STATE.json"
        out[cell_id] = load_json(path) if path.is_file() else {"id": cell_id, "q": 0.0, "choice": 0}
    return out


def compute() -> dict[str, Any]:
    states = read_states()
    graph = adjacency()
    beta = float(load_json(LINKAGE).get("coupling", {}).get("beta", 0.2))
    result: dict[str, Any] = {}

    for cell_id, neighbors in graph.items():
        q_i = float(states[cell_id].get("q", 0.0))
        weighted = []
        total_w = 0.0
        for neighbor_id, weight, edge_type in neighbors:
            q_j = float(states[neighbor_id].get("q", 0.0))
            weighted.append({
                "id": neighbor_id,
                "q": q_j,
                "weight": weight,
                "type": edge_type,
            })
            total_w += weight
        neighbor_q = (
            sum(item["q"] * item["weight"] for item in weighted) / total_w
            if total_w else q_i
        )
        pressure = beta * (neighbor_q - q_i)
        result[cell_id] = {
            "q": q_i,
            "neighbor_q": neighbor_q,
            "link_pressure": pressure,
            "neighbors": weighted,
        }
    return {
        "job": "Y5_node_to_linkage_sandbox",
        "brick": "YELLOW",
        "beta": beta,
        "cells": result,
        "honest": "A linked four-cell graph. Not yet a flower/domain-wall network.",
        "canonical_refs": [
            "Nodes/G-719_Neural_System_Functional_Analogy_Map.md",
            "Nodes/A-111_Recursion.md",
            "Nodes/G-722_Android_Subconscious_Motor_Memory_Architecture.md",
        ],
    }


def apply_to_state() -> dict[str, Any]:
    report = compute()
    for cell_id, link in report["cells"].items():
        state = read_states()[cell_id]
        state["linkage"] = {
            "neighbor_q": round(float(link["neighbor_q"]), 6),
            "pressure": round(float(link["link_pressure"]), 6),
            "neighbors": [
                {"id": n["id"], "weight": n["weight"], "type": n["type"]}
                for n in link["neighbors"]
            ],
        }
        save_state(cell_id, state)
    return report


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write linkage readout into cells/*/STATE.json only")
    args = ap.parse_args()
    report = apply_to_state() if args.apply else compute()
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
