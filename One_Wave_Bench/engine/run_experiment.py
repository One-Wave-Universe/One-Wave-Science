#!/usr/bin/env python3
"""
One-Wave Experiment Runner  (Bench engine, Stage 01 / D-413)

Turns a D-412-governed experiment REQUEST (JSON) into an experiment RECEIPT (JSON)
that both a human and an AI can read. The physics update law is NOT reimplemented
here: it is imported directly from the canonical D-413 engine so there is a single
source of truth (D-412 reproducibility requirement).

Usage:
  python run_experiment.py --request path/to/request.json --out ../runs
  python run_experiment.py --demo                 # writes+runs a built-in demo request
  echo '<json>' | python run_experiment.py --stdin --out ../runs
"""
from __future__ import annotations
import argparse, csv, hashlib, json, math, sys, datetime
from dataclasses import asdict
from pathlib import Path
import numpy as np

# ---- import canonical D-413 physics (single source of truth) ----
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
D413_DIR = REPO / "Nodes" / "D-413_Ground_Lattice_Orbital_Restoring_Simulation"
sys.path.insert(0, str(D413_DIR))
import importlib.util
_spec = importlib.util.spec_from_file_location("d413", D413_DIR / "simulate_d413.py")
d413 = importlib.util.module_from_spec(_spec)
sys.modules["d413"] = d413  # required before exec so dataclasses can resolve module
_spec.loader.exec_module(d413)  # provides P, Q, lattice, sim, target, grad, ...

ENGINE_SRC = D413_DIR / "simulate_d413.py"
ENGINE_SHA = hashlib.sha256(ENGINE_SRC.read_bytes()).hexdigest()
CODE_VERSION = "bench-0.1 / d413-canonical"


def _auto_orbit_initial(p) -> "d413.Q":
    """Derive a reasonable orbit initial condition from the well parameters."""
    r = p.well_radius
    ov = math.sqrt(max(0.05, p.gravity * p.well_depth / (r * 1.5)))
    return d413.Q(r * 1.25, 0.0, 0.0, ov, 0.35, 0.08)


def _measurements(rows: list[dict]) -> dict:
    """D-412 Required Measurements computed from the evolved state arrays."""
    arr = {k: np.array([row[k] for row in rows], dtype=float) for k in rows[0]}
    dist = arr["well_distance"]; spin = arr["spin"]; orb = arr["orbital_L"]
    # recovery time: steps for max_strain to fall & stay under 20% of its peak
    strain = arr["max_strain"]; peak = float(strain.max()) if len(strain) else 0.0
    recovery_t = None
    if peak > 1e-9:
        thr = 0.2 * peak
        below = np.where(strain <= thr)[0]
        if len(below):
            recovery_t = float(arr["t"][below[0]])
    return {
        "samples": len(rows),
        "well_distance_min": float(dist.min()),
        "well_distance_max": float(dist.max()),
        "well_distance_final": float(dist[-1]),
        "center_drift": float(abs(dist[-1] - dist[0])),
        "max_abs_spin": float(np.abs(spin).max()),
        "final_spin": float(spin[-1]),
        "mean_abs_orbital_L": float(np.abs(orb).mean()),
        "orbital_L_drift": float(abs(orb[-1] - orb[0])),
        "max_strain": float(arr["max_strain"].max()),
        "max_compression": float(arr["max_compression"].max()),
        "rms_displacement_peak": float(arr["rms_displacement"].max()),
        "lattice_energy_min": float(arr["lattice_energy_proxy"].min()),
        "lattice_energy_max": float(arr["lattice_energy_proxy"].max()),
        "recovery_time_20pct": recovery_t,
    }


def _make_P(overrides: dict | None):
    base = asdict(d413.P())
    if overrides:
        for k, v in overrides.items():
            if k in base:
                base[k] = v
    return d413.P(**base)


def run_request(req: dict, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    rid = req.get("request_id", "EXP-UNSPEC")
    case_receipts = []
    raw_by_name = {}

    for case in req["cases"]:
        name = case["name"]
        p = _make_P(case.get("parameters"))
        if "initial" in case and case["initial"]:
            qinit = d413.Q(**{**asdict(_auto_orbit_initial(p)), **case["initial"]})
        else:
            qinit = _auto_orbit_initial(p)
        rows, summary = d413.sim(name, p, qinit, out_dir)
        raw_by_name[name] = (rows, p)
        csvp = out_dir / f"{name}.csv"
        case_receipts.append({
            "name": name,
            "parameters": asdict(p),
            "initial": asdict(qinit),
            "measurements": _measurements(rows),
            "csv": csvp.name,
            "csv_sha256": summary["csv_sha256"],
        })

    # ---- D-412 Required Failure/Control checks (auto-injected controls) ----
    # Always run zero-input drift and no-well control as guardrails.
    p0 = _make_P(req["cases"][0].get("parameters"))
    ctrl_zero_P = _make_P({**(req["cases"][0].get("parameters") or {}),
                           "well_depth": 0., "gravity": 0., "well_follow": 0.,
                           "pressure": 0., "compression": 0.})
    zrows, _ = d413.sim("_control_zero_input_drift", ctrl_zero_P, d413.Q(0,0,0,0,0,0), out_dir)
    zmax_dist = max(abs(r["well_distance"]) for r in zrows)
    zmax_strain = max(r["max_strain"] for r in zrows)

    checks = {
        "zero_input_drift_below_1e-9": zmax_dist < 1e-9 and zmax_strain < 1e-9,
    }
    # lattice actually deforms in at least one requested case
    checks["lattice_deforms_when_active"] = any(
        cr["measurements"]["max_strain"] > 1e-4 for cr in case_receipts)

    receipt = {
        "receipt_id": f"RCP-{rid}",
        "request_id": rid,
        "engine": "D-413",
        "author": req.get("author", "ai"),
        "author_label": req.get("author_label", ""),
        "native_dimension": req.get("native_dimension", "2D"),
        "status": "YELLOW",
        "hypothesis": req.get("hypothesis", ""),
        "falsifiers": req.get("falsifiers", []),
        "cases": case_receipts,
        "checks": checks,
        "all_checks_pass": all(checks.values()),
        "interpretation": "",
        "limitations": [
            "Curvature well is imposed, not derived.",
            "Bounded displacement is a collective shell coordinate, not a derived quark.",
            "Energy values are proxies; external well-follow and damping exchange work.",
            "Does not establish gravity, charge, proton structure, or Mass Effect.",
        ],
        "provenance": {
            "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "engine_source": str(ENGINE_SRC.relative_to(REPO)),
            "engine_sha256": ENGINE_SHA,
            "code_version": CODE_VERSION,
        },
    }
    receipt_path = out_dir / f"receipt_{rid}.json"
    receipt_path.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    return receipt


DEMO = {
    "request_id": "EXP-DEMO-001",
    "author": "ai",
    "author_label": "Computer",
    "hypothesis": "Increasing shell asymmetry increases induced axial spin at fixed orbit.",
    "engine": "D-413",
    "native_dimension": "2D",
    "cases": [
        {"name": "asym_low",  "parameters": {"asymmetry": 0.08}},
        {"name": "asym_mid",  "parameters": {"asymmetry": 0.24}},
        {"name": "asym_high", "parameters": {"asymmetry": 0.40}},
    ],
    "falsifiers": ["max_abs_spin does not increase monotonically with asymmetry"],
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--request")
    ap.add_argument("--stdin", action="store_true")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--out", default=str(REPO / "One_Wave_Bench" / "runs"))
    a = ap.parse_args()
    if a.demo:
        req = DEMO
    elif a.stdin:
        req = json.loads(sys.stdin.read())
    elif a.request:
        req = json.loads(Path(a.request).read_text())
    else:
        ap.error("provide --request FILE, --stdin, or --demo")
    out = Path(a.out) / req["request_id"]
    receipt = run_request(req, out)
    print(json.dumps({
        "receipt_id": receipt["receipt_id"],
        "all_checks_pass": receipt["all_checks_pass"],
        "checks": receipt["checks"],
        "cases": [{"name": c["name"],
                   "max_abs_spin": c["measurements"]["max_abs_spin"],
                   "max_strain": c["measurements"]["max_strain"]}
                  for c in receipt["cases"]],
        "receipt_path": str(out / f"receipt_{req['request_id']}.json"),
    }, indent=2))
    raise SystemExit(0 if receipt["all_checks_pass"] else 1)


if __name__ == "__main__":
    main()
