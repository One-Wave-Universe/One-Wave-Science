#!/usr/bin/env python3
"""Non-executing 24→1 manifest and local-reference validator (not a science test)."""
from __future__ import annotations

import argparse
from collections import Counter
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
REPOSITORY_ROOT = ROOT.parent.parent
SCHEMA = "one-wave-sandbox-module/v1"


def load_manifests(root=ROOT):
    manifests = []
    for path in sorted((root / "modules").glob("*/manifest.json")):
        try:
            manifest = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(manifest, dict):
                raise ValueError("manifest:must-be-object")
            manifest.pop("_error", None)
        except (OSError, ValueError) as error:
            manifest = {"_error": str(error)}
        # Never trust diagnostic metadata supplied by the input JSON.
        manifest["_path"] = str(path)
        manifests.append(manifest)
    return manifests


def validate(manifest):
    """Validate structure only; referenced paths are checked by registry_report."""
    if not isinstance(manifest, dict):
        return ["manifest:must-be-object"]
    errors = []

    def string(value, key):
        if not isinstance(value, str) or not value.strip():
            errors.append(key + ":must-be-nonempty-string")

    def strings(value, key, nonempty=False):
        if not isinstance(value, list) or (nonempty and not value) or any(
            not isinstance(item, str) or not item.strip() for item in value
        ):
            errors.append(key + ":must-be-string-list")

    def obj(value, key):
        if not isinstance(value, dict):
            errors.append(key + ":must-be-object")
            return {}
        return value

    if manifest.get("schema") != SCHEMA:
        errors.append("schema")
    for key in ("id", "name", "version", "claim_gate", "state_schema"):
        string(manifest.get(key), key)
    slot = manifest.get("slot")
    if type(slot) is not int or not 1 <= slot <= 24:
        errors.append("slot:must-be-1..24")
    strings(manifest.get("dimensions"), "dimensions", nonempty=True)
    strings(manifest.get("controls"), "controls")
    if "data_sources" in manifest:
        strings(manifest["data_sources"], "data_sources")
    solver = obj(manifest.get("solver"), "solver")
    string(solver.get("kind"), "solver.kind")
    strings(solver.get("equations"), "solver.equations")
    units = obj(solver.get("units"), "solver.units")
    for key, value in units.items():
        string(key, "solver.units.key")
        string(value, "solver.units." + str(key))
    render = obj(manifest.get("render"), "render")
    strings(render.get("views"), "render.views", nonempty=True)
    if render.get("solver_independent") is not True:
        errors.append("render:must-be-solver-independent")
    for key, fields in (("fixtures", ("positive", "negative", "nulls")),
                        ("validation", ("convergence", "invariants", "falsification"))):
        value = obj(manifest.get(key), key)
        for field in fields:
            strings(value.get(field), key + "." + field)
    if "adapter" in manifest:
        adapter = obj(manifest["adapter"], "adapter")
        string(adapter.get("existing"), "adapter.existing")
        if "entry_point" in adapter:
            string(adapter["entry_point"], "adapter.entry_point")
        if "node_bindings" in adapter:
            strings(adapter["node_bindings"], "adapter.node_bindings")
    return errors


def check_paths(manifest, repository_root):
    """Check existence/type without importing, reading, or executing targets."""
    errors = []
    present = False
    base = pathlib.Path(manifest["_path"]).parent
    adapter = manifest.get("adapter", {})
    references = [("state_schema", manifest["state_schema"], "file")]
    if adapter:
        references.append(("adapter.existing", adapter["existing"], "directory"))
        if "entry_point" in adapter:
            references.append(("adapter.entry_point", adapter["entry_point"], "file"))
    for label, value, kind in references:
        try:
            relative = pathlib.Path(value)
            target = (base / relative).resolve()
            if relative.is_absolute() or not target.is_relative_to(repository_root.resolve()):
                errors.append(label + ":must-stay-inside-repository")
                continue
            exists = target.is_file() if kind == "file" else target.is_dir()
            if not exists:
                errors.append(label + ":missing-or-not-" + kind)
            if label == "adapter.entry_point":
                present = exists
        except (OSError, ValueError, RuntimeError):
            errors.append(label + ":unreadable-path")
    return errors, present


def registry_report(root=ROOT, repository_root=REPOSITORY_ROOT):
    try:
        manifests = load_manifests(root)
    except OSError as error:
        return {"schema": SCHEMA, "validation_scope": "manifest-and-paths-only",
                "module_execution": "not-run", "modules": [], "occupied_slots": [],
                "errors": ["registry:unreadable:" + str(error)], "ok": False}
    ids = Counter(m.get("id") for m in manifests if isinstance(m.get("id"), str))
    slots = Counter(m.get("slot") for m in manifests if type(m.get("slot")) is int)
    reports = []
    occupied = set()
    for manifest in manifests:
        errors = [manifest["_error"]] if "_error" in manifest else validate(manifest)
        present = None
        if not errors:
            path_errors, present = check_paths(manifest, repository_root)
            errors.extend(path_errors)
        identity, slot = manifest.get("id"), manifest.get("slot")
        if isinstance(identity, str) and ids[identity] > 1:
            errors.append("duplicate-id")
        if type(slot) is int and slots[slot] > 1:
            errors.append("duplicate-slot")
        if not errors:
            occupied.add(slot)
        reports.append({"id": identity, "slot": slot, "path": manifest["_path"],
                        "errors": errors, "entry_point_present": present,
                        "module_execution": "not-run"})
    errors = [] if manifests else ["registry:no-manifests"]
    return {"schema": SCHEMA, "validation_scope": "manifest-and-paths-only",
            "module_execution": "not-run", "modules": reports,
            "occupied_slots": sorted(occupied), "errors": errors,
            "ok": not errors and all(not item["errors"] for item in reports)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = registry_report()
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("Manifest/path checks only; module execution: not-run")
        for item in report["modules"]:
            status = "MANIFEST/PATH PASS" if not item["errors"] else "FAIL " + ",".join(item["errors"])
            print(f'{item["slot"]}: {item["id"]} {status}')
        for error in report["errors"]:
            print("FAIL " + error)
    raise SystemExit(0 if report["ok"] else 2)


if __name__ == "__main__":
    main()
