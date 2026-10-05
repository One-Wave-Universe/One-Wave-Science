#!/usr/bin/env python3
"""Static G-767 diagnostic adapter; no time evolution or physical inference."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import platform
import subprocess
import types

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
ID = "spectral-lattice-phase"
VERSION = "spectral-adapter/v1"
SCHEMA = "one-wave-spectral-run/v1"
NODE = "Nodes/G-767_Measured_Spectrum_Lattice_Phase_Map.md"
ENGINE_PATH = "sims/06-spectral-lattice-phase/spectral_lattice_phase.py"
SOURCES = (NODE, ENGINE_PATH,
           "sims/24-1-sandbox/modules/06-spectral-lattice-phase/adapter.py",
           "sims/24-1-sandbox/modules/06-spectral-lattice-phase/manifest.json",
           "sims/00-state-container/state-schema.json")
MAX_RECORDS = 10000
MAX_TRIALS = 10000
MAX_SAMPLE_TRIALS = 250000
LIMITATIONS = [
    "Exploratory static log-scale/circular-coherence diagnostic, not a physical solver or FFT.",
    "The log-uniform null does not match observed smooth density, acceptance or background.",
    "The empirical upper-tail p is diagnostic only; it cannot establish a lattice or significance under required controls.",
    "Uncertainty and width are retained as metadata; uncertainty propagation and width/Q analysis are not implemented.",
    "Reference policy, source description and common units are caller declarations, not independently verified.",
    "Held-out tests, matched-density/acceptance nulls and selection/resolution sweeps remain unverified.",
    "Geometry is a nonspatial coordinate plot; no spatial fields, time, sample rate or physical frequency are inferred.",
    "Browser visual review and GOLD compliance are unverified.",
    "Hashes identify source files; engine source is compiled from captured bytes. Host interpreter and arbitrary in-process monkeypatches are not attested.",
]


def _json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


def _hash(value):
    return hashlib.sha256(value).hexdigest()


def manifest():
    return json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))


def references():
    m = manifest()
    if not isinstance(m, dict) or not isinstance(m.get("adapter"), dict):
        raise ValueError("Manifest and adapter must be objects")
    a = m["adapter"]
    if m.get("id") != ID or m.get("claim_gate") != "YELLOW" or a.get("node_bindings") != ["G-767"]:
        raise ValueError("Manifest identity/gate/binding mismatch")
    for path in (m.get("state_schema"), a.get("existing"), a.get("entry_point")):
        if not isinstance(path, str) or not path.strip():
            raise ValueError("Manifest reference must be a nonempty path string")
        if not (HERE / path).exists():
            raise ValueError("Missing module reference: " + path)
    node = (ROOT / NODE).read_text(encoding="utf-8")
    if 'node_id: "G-767"' not in node or 'gate: "YELLOW"' not in node:
        raise ValueError("Canonical node identity/gate changed; re-reference before using adapter")
    return {path: _hash((ROOT / path).read_bytes()) for path in SOURCES}


_IMPORT_ERROR = None
try:
    _CAPTURED_BYTES = {path: (ROOT / path).read_bytes() for path in SOURCES}
    _IMPORT_HASHES = {path: _hash(data) for path, data in _CAPTURED_BYTES.items()}
    ENGINE = types.ModuleType("g767_captured_engine")
    exec(compile(_CAPTURED_BYTES[ENGINE_PATH], str(ROOT / ENGINE_PATH), "exec"), ENGINE.__dict__)
except (OSError, ValueError, SyntaxError) as error:
    _IMPORT_ERROR = error


def _sources():
    if _IMPORT_ERROR is not None:
        raise ValueError("Adapter source loading failed: " + str(_IMPORT_ERROR))
    current = references()
    if current != _IMPORT_HASHES:
        raise ValueError("Source changed since import; restart and re-reference")
    return current


def _keys(value, allowed, required, name):
    if not isinstance(value, dict):
        raise ValueError(name + " must be an object")
    if set(value) - set(allowed) or set(required) - set(value):
        raise ValueError(name + " has unknown or missing fields")


def _finite(value, name, positive=False, nonnegative=False):
    try:
        valid = type(value) in (int, float) and math.isfinite(value)
    except OverflowError:
        valid = False
    if not valid or (positive and value <= 0) or (nonnegative and value < 0):
        raise ValueError(name + " must be finite" + (" and positive" if positive else ""))
    return value


def _text(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(name + " must be a nonempty string")


def _configuration(config):
    required = ("records", "x0", "scale_unit", "reference_unit", "reference_policy", "source")
    _keys(config, (*required, "trials", "seed"), required, "configuration")
    result = copy.deepcopy(config)
    result.setdefault("trials", 1000)
    result.setdefault("seed", 767)
    _finite(result["x0"], "x0", positive=True)
    for name in ("scale_unit", "reference_unit"):
        _text(result[name], name)
    if result["scale_unit"] != result["reference_unit"]:
        raise ValueError("scale and reference units must match; no implicit conversion")
    if result["reference_policy"] not in ("predeclared", "training-frozen"):
        raise ValueError("reference_policy must declare predeclared or training-frozen x0")
    _keys(result["source"], ("kind", "description"), ("kind", "description"), "source")
    if result["source"]["kind"] not in ("synthetic", "caller-provided"):
        raise ValueError("source.kind must be synthetic or caller-provided")
    _text(result["source"]["description"], "source.description")
    records = result["records"]
    if not isinstance(records, list) or not 3 <= len(records) <= MAX_RECORDS:
        raise ValueError("records must contain 3..10000 positive-scale measurements")
    for record in records:
        _keys(record, ("scale", "width", "uncertainty", "label", "unit"), ("scale",), "record")
        x = _finite(record["scale"], "scale", positive=True)
        for name in ("width", "uncertainty"):
            if record.get(name) is not None:
                _finite(record[name], name, nonnegative=True)
        if "label" in record and not isinstance(record["label"], str):
            raise ValueError("label must be a metadata string")
        if "unit" in record and record["unit"] != result["scale_unit"]:
            raise ValueError("record unit must match declared scale unit")
        # Preserve the existing engine's arithmetic, refusing unrepresentable domains.
        try:
            ratio = x / result["x0"]
            reconstructed = 2 ** math.log2(x)
        except (OverflowError, ValueError, ZeroDivisionError):
            raise ValueError("scale/reference outside representable engine domain") from None
        if not math.isfinite(ratio) or ratio <= 0 or not math.isfinite(reconstructed) or reconstructed <= 0:
            raise ValueError("scale/reference outside representable engine domain")
    trials, seed = result["trials"], result["seed"]
    if type(trials) is not int or not 1 <= trials <= MAX_TRIALS:
        raise ValueError("trials must be an integer in 1..10000")
    if len(records) * trials > MAX_SAMPLE_TRIALS:
        raise ValueError("sample-trial budget exceeds 250000")
    if type(seed) is not int or not 0 <= seed <= 2**32 - 1:
        raise ValueError("seed must be an integer in 0..2^32-1")
    _json(result)
    return result


def _default():
    return {"records": [{"scale": 2**n} for n in range(5)], "x0": 1,
            "scale_unit": "dimensionless", "reference_unit": "dimensionless",
            "reference_policy": "predeclared", "trials": 1000, "seed": 767,
            "source": {"kind": "synthetic", "description": "exact-octave positive fixture; not measured data"}}


def _analysis(config):
    xs = [(record["scale"], record.get("width")) for record in config["records"]]
    phase = ENGINE.phases(xs, config["x0"])
    real, mean, p = ENGINE.null_test(xs, config["x0"], config["trials"], config["seed"])
    coordinate = [math.log2(x / config["x0"]) for x, _ in xs]
    output = {"log2_ratio": coordinate, "octave": [math.floor(u) for u in coordinate],
              "phase": phase, "coherence": real, "null_mean_coherence": mean,
              "empirical_upper_tail_p": p}
    _json(output)
    return output


def initialize(config=None):
    _sources()
    return {"configuration": _configuration(_default() if config is None else config), "analysis": None}


def _state(state):
    _sources()
    _keys(state, ("configuration", "analysis"), ("configuration", "analysis"), "state")
    config = _configuration(state["configuration"])
    analysis = state["analysis"]
    if analysis is not None and _json(analysis) != _json(_analysis(config)):
        raise ValueError("Analysis does not reproduce the declared input and seed")
    return {"configuration": config, "analysis": copy.deepcopy(analysis)}


def step(state, dt=None, inputs=None):
    """One bounded static analysis, not an integration timestep."""
    checked = _state(state)
    if dt is not None or inputs is not None:
        raise ValueError("Static transform has no dt or dynamic inputs")
    if checked["analysis"] is not None:
        raise ValueError("Static analysis already completed; initialize a new configuration")
    checked["analysis"] = _analysis(checked["configuration"])
    return checked


def measure(state):
    checked = _state(state)
    analysis = checked["analysis"]
    return {"count": len(checked["configuration"]["records"]),
            **{key: analysis[key] if analysis else None for key in
               ("coherence", "null_mean_coherence", "empirical_upper_tail_p")}}


def geometry(state):
    checked = _state(state)
    a = checked["analysis"]
    if a is None:
        raise ValueError("Analyze the static state before requesting geometry")
    records = checked["configuration"]["records"]
    return {"dimension": "2D nonspatial coordinate plots", "solver_independent": True,
            "axes": {"scatter": ["log2(scale/x0) [dimensionless]", "scale phase [cycles, dimensionless]"],
                     "circle": ["cos(2*pi*phase) [dimensionless]", "sin(2*pi*phase) [dimensionless]"]},
            "points": [{"id": i, "scale": record["scale"], "scale_unit": checked["configuration"]["scale_unit"],
                        "scatter": [a["log2_ratio"][i], a["phase"][i]],
                        "unit_circle": [math.cos(2 * math.pi * a["phase"][i]), math.sin(2 * math.pi * a["phase"][i])]}
                       for i, record in enumerate(records)],
            "physical_spatial_geometry": False}


def _provenance(config):
    return {"source": NODE, "version": VERSION, "source_sha256": _sources(),
            "normalized_input_sha256": _hash(_json(config).encode("utf-8")),
            "input_identity": "canonical JSON of declared configuration; not an external raw-file checksum",
            "source_declaration": copy.deepcopy(config["source"]), "source_declaration_verified": False,
            "python_version": platform.python_version(), "seed": config["seed"]}


def serialize(state):
    checked = _state(state)
    values = measure(checked)
    return {"id": ID, "state": checked,
            "measurements": [{"name": name, "value": value, "unit": "count" if name == "count" else "dimensionless"}
                             for name, value in values.items()],
            "provenance": _provenance(checked["configuration"])}


def restore(snapshot):
    _keys(snapshot, ("id", "state", "measurements", "provenance"),
          ("id", "state", "measurements", "provenance"), "snapshot")
    if snapshot["id"] != ID:
        raise ValueError("Unsupported snapshot identity")
    checked = _state(snapshot["state"])
    if _json(snapshot) != _json(serialize(checked)):
        raise ValueError("Snapshot measurements/provenance do not match current sources and deterministic replay")
    return checked


def controls():
    return {"implemented": ["exact-octave positive", "quarter-phase resultant cancellation",
                            "direct-engine equivalence", "seeded log-uniform null", "metadata-only labels"],
            "null_method": "independent matched-range log-uniform draws; not a permutation test",
            "unverified": ["smooth-density null", "detector acceptance/background", "uncertainty propagation",
                           "held-out validation", "selection/resolution sweeps"]}


def run(config=None):
    initial = initialize(config)
    final = step(initial)
    commit = None
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, stderr=subprocess.DEVNULL, text=True).strip()
    except (OSError, subprocess.SubprocessError):
        pass
    return {"schema": SCHEMA, "module": ID, "status": "completed", "claim_gate": manifest()["claim_gate"],
            "scientific_status": "exploratory-only", "physical_validation": "unverified",
            "node_bindings": [{"node_id": "G-767", "source": NODE, "scope": "static scale-phase diagnostic only"}],
            "configuration": copy.deepcopy(final["configuration"]), "initial": serialize(initial), "final": serialize(final),
            "measurements": measure(final), "geometry": geometry(final), "controls": controls(),
            "null_model": {"method": "matched-range log-uniform independent draws",
                           "tail": "greater-than-or-equal", "p_formula": "(1 + count(null_coherence >= observed))/(trials + 1)",
                           "rng": "Python random.Random(seed)", "inference": "diagnostic-only"},
            "execution": {"kind": "one static analysis", "physical_time": None, "sample_rate": None,
                          "frequency": None, "commit": commit, "commit_is_context_only": True},
            "limitations": list(LIMITATIONS)}


def validate(receipt):
    """Replay proof only, never scientific or hypothesis validation."""
    if not isinstance(receipt, dict) or receipt.get("schema") != SCHEMA:
        raise ValueError("Unsupported receipt")
    expected = run(receipt.get("configuration"))
    # HEAD is context, not source identity. Everything else must replay exactly.
    candidate = copy.deepcopy(receipt)
    if isinstance(candidate.get("execution"), dict):
        candidate["execution"]["commit"] = expected["execution"]["commit"]
    if _json(candidate) != _json(expected):
        raise ValueError("Receipt does not reproduce current sources and declared input")
    return {"ok": True, "scope": "deterministic-software-replay-only", "physical_validation": "unverified"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("request", nargs="?", help="JSON configuration; default is explicitly synthetic")
    args = parser.parse_args()
    try:
        config = json.loads(Path(args.request).read_text(encoding="utf-8")) if args.request else None
        if args.request and not isinstance(config, dict):
            raise ValueError("Request must be a JSON configuration object")
        receipt = run(config)
        print(json.dumps(receipt, indent=2, allow_nan=False))
    except (OSError, ValueError, TypeError, OverflowError) as error:
        print(json.dumps({"schema": SCHEMA, "status": "invalid", "error": {"name": type(error).__name__, "message": str(error)}}))
        raise SystemExit(2)


if __name__ == "__main__":
    main()
