"""Reproducible D-415 parameter, ablation, and refinement audit."""

from __future__ import annotations

import csv
import json
import tempfile
from dataclasses import replace
from pathlib import Path

from nonlocal_field_bench import Config, run


def execute(label: str, factor: str, value: float, cfg: Config) -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="d415_") as directory:
        summary = run(cfg, Path(directory))
    initial = summary["initial"]
    final = summary["final"]
    initial_weight = sum(initial[f"weight{k}"] for k in (1, 2, 3))
    final_weight = sum(final[f"weight{k}"] for k in (1, 2, 3))
    return {
        "label": label,
        "factor": factor,
        "value": value,
        "hyperradius_ratio": final["hyperradius"] / initial["hyperradius"],
        "weight_retention": final_weight / initial_weight,
        "coherence_change": final["phase_coherence"] - initial["phase_coherence"],
        "vorticity_retention": final["field_vorticity_rms"]
        / initial["field_vorticity_rms"],
        "lock_returns": sum(summary["lock_returns"]),
        "lock_breaks": sum(summary["lock_breaks"]),
        "classification": summary["classification"],
    }


def audit(output: Path) -> list[dict[str, object]]:
    output.mkdir(parents=True, exist_ok=True)
    base = Config(n=32, steps=120)
    rows: list[dict[str, object]] = []
    sweeps = {
        "nonlocal_response": (0.0, 0.06, 0.12, 0.24),
        "nonlinear_response": (0.0, 0.01, 0.02, 0.05),
        "kernel_length": (4.0, 10.0, 20.0),
        "damping": (0.0, 0.02, 0.08),
    }
    for factor, values in sweeps.items():
        for value in values:
            rows.append(execute("factor_sweep", factor, value, replace(base, **{factor: value})))

    physical_time = base.steps * base.dt
    for dt in (0.02, 0.04, 0.08):
        cfg = replace(base, dt=dt, steps=round(physical_time / dt))
        rows.append(execute("time_refinement", "dt", dt, cfg))

    for size in (24, 32, 48):
        rows.append(execute("raw_lattice_size", "n", float(size), replace(base, n=size)))

    csv_path = output / "sweep_results.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    factor_rows = [row for row in rows if row["label"] == "factor_sweep"]
    dt_rows = [row for row in rows if row["label"] == "time_refinement"]
    baseline = next(
        row
        for row in factor_rows
        if row["factor"] == "nonlocal_response" and row["value"] == 0.12
    )
    dt_spread = max(row["hyperradius_ratio"] for row in dt_rows) - min(
        row["hyperradius_ratio"] for row in dt_rows
    )
    kernel_rows = [row for row in rows if row["factor"] == "kernel_length"]
    kernel_spread = max(row["hyperradius_ratio"] for row in kernel_rows) - min(
        row["hyperradius_ratio"] for row in kernel_rows
    )
    findings = {
        "baseline": baseline,
        "dt_hyperradius_spread": dt_spread,
        "kernel_hyperradius_spread": kernel_spread,
        "all_classifications": sorted({str(row["classification"]) for row in rows}),
        "math_gaps": [
            "Persistent-mode potential: measured excitation weight is not retained.",
            "Rotational source/transfer: vorticity is not reliably retained.",
            "Harmonic feedback: locking is measured but does not yet act on Field evolution.",
            "Global kernel derivation: outcomes change with the candidate kernel scale.",
            "Moving-wake transport: no material/advection term carries deformation with a structure.",
            "Conserved transfer ledger: Point, Path, Field, and nonlocal energy exchange are not closed.",
            "Dimensionless scaling: lattice-size runs change physical extent and cannot yet be compared.",
            "Measurement identity: moving windows require merge/split and identity-continuity rules.",
        ],
    }
    (output / "findings.json").write_text(json.dumps(findings, indent=2), encoding="utf-8")
    return rows


if __name__ == "__main__":
    audit(Path("math_gap_audit"))
    print("math_gap_audit/sweep_results.csv")
    print("math_gap_audit/findings.json")
