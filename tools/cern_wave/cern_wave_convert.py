#!/usr/bin/env python3
"""Convert HEP four-vectors into traceable standard wave-equivalent quantities.

This tool preserves source columns and distinguishes STANDARD_DERIVED values from
SCALED_ANALOG values. It does not claim that the conversion proves One-Wave.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import math
import pathlib
import sys
import urllib.request
from dataclasses import dataclass, asdict
from typing import Dict, Iterable, Iterator, List, Optional, TextIO, Tuple

H_GEV_S = 4.135667696e-24
HBAR_GEV_S = 6.582119569e-25
HC_GEV_M = 1.239841984e-15
HBAR_C_GEV_M = 1.973269804e-16
C_M_S = 299_792_458.0
TRANSFORM_VERSION = "cern-fourvector-wave-v1"


@dataclass
class WaveView:
    p_GeV: float
    pt_GeV: float
    mass_from_fourvector_GeV: float
    mass2_raw_GeV2: float
    frequency_Hz: float
    angular_frequency_rad_s: float
    de_broglie_wavelength_m: Optional[float]
    wave_number_rad_m: Optional[float]
    transverse_wavelength_m: Optional[float]
    compton_wavelength_m: Optional[float]
    reduced_compton_wavelength_m: Optional[float]
    beta: Optional[float]
    gamma: Optional[float]
    group_velocity_m_s: Optional[float]
    phase_velocity_m_s: Optional[float]
    dir_x: Optional[float]
    dir_y: Optional[float]
    dir_z: Optional[float]
    rapidity: Optional[float]
    mass2_negative_warning: bool
    beta_gt_one_warning: bool


def _finite_float(value: str, name: str) -> float:
    try:
        x = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} is not numeric: {value!r}") from exc
    if not math.isfinite(x):
        raise ValueError(f"{name} is not finite: {value!r}")
    return x


def derive_wave_view(E: float, px: float, py: float, pz: float, beta_tolerance: float = 5e-4) -> WaveView:
    p2 = px * px + py * py + pz * pz
    p = math.sqrt(max(p2, 0.0))
    pt = math.hypot(px, py)
    mass2_raw = E * E - p2
    # Rounded educational CSVs can make a physically small positive m^2 slightly negative.
    # Keep the raw value and warning visible; never hide it.
    mass = math.sqrt(max(mass2_raw, 0.0))

    frequency = E / H_GEV_S
    omega = E / HBAR_GEV_S
    wavelength = HC_GEV_M / p if p > 0.0 else None
    k = p / HBAR_C_GEV_M if p > 0.0 else None
    transverse_wavelength = HC_GEV_M / pt if pt > 0.0 else None
    compton = HC_GEV_M / mass if mass > 0.0 else None
    reduced_compton = HBAR_C_GEV_M / mass if mass > 0.0 else None

    beta = p / E if E > 0.0 else None
    gamma = E / mass if mass > 0.0 else None
    group_velocity = beta * C_M_S if beta is not None else None
    phase_velocity = (E / p) * C_M_S if p > 0.0 else None

    if p > 0.0:
        direction = (px / p, py / p, pz / p)
    else:
        direction = (None, None, None)

    rapidity = None
    if E > abs(pz) and E - pz > 0.0 and E + pz > 0.0:
        rapidity = 0.5 * math.log((E + pz) / (E - pz))

    return WaveView(
        p_GeV=p,
        pt_GeV=pt,
        mass_from_fourvector_GeV=mass,
        mass2_raw_GeV2=mass2_raw,
        frequency_Hz=frequency,
        angular_frequency_rad_s=omega,
        de_broglie_wavelength_m=wavelength,
        wave_number_rad_m=k,
        transverse_wavelength_m=transverse_wavelength,
        compton_wavelength_m=compton,
        reduced_compton_wavelength_m=reduced_compton,
        beta=beta,
        gamma=gamma,
        group_velocity_m_s=group_velocity,
        phase_velocity_m_s=phase_velocity,
        dir_x=direction[0],
        dir_y=direction[1],
        dir_z=direction[2],
        rapidity=rapidity,
        mass2_negative_warning=mass2_raw < -1e-6,
        beta_gt_one_warning=bool(beta is not None and beta > 1.0 + beta_tolerance),
    )


def pair_mass(v1: Tuple[float, float, float, float], v2: Tuple[float, float, float, float]) -> float:
    E = v1[0] + v2[0]
    px = v1[1] + v2[1]
    py = v1[2] + v2[2]
    pz = v1[3] + v2[3]
    m2 = E * E - px * px - py * py - pz * pz
    return math.sqrt(max(m2, 0.0))


def _open_text(source: str) -> TextIO:
    if source.startswith("http://") or source.startswith("https://"):
        req = urllib.request.Request(source, headers={"User-Agent": "One-Wave-CERN-wave-transform/1.0"})
        response = urllib.request.urlopen(req, timeout=60)
        return io.TextIOWrapper(response, encoding="utf-8-sig", newline="")
    return open(source, "r", encoding="utf-8-sig", newline="")


def _jsonable(x):
    if isinstance(x, float) and not math.isfinite(x):
        return None
    return x


def _row_mode(fieldnames: List[str]) -> str:
    fields = set(fieldnames)
    if {"E1", "px1", "py1", "pz1", "E2", "px2", "py2", "pz2"}.issubset(fields):
        return "paired"
    if {"E", "px", "py", "pz"}.issubset(fields):
        return "single"
    raise ValueError(
        "unrecognized four-vector schema; expected E/px/py/pz or paired E1..pz1 + E2..pz2"
    )


def iter_converted(
    reader: csv.DictReader,
    source_record: str,
    source_url: str,
    reference_energy_GeV: Optional[float],
    bench_frequency_Hz: Optional[float],
    max_events: Optional[int],
) -> Iterator[Dict[str, object]]:
    mode = _row_mode(reader.fieldnames or [])
    for event_index, row in enumerate(reader):
        if max_events is not None and event_index >= max_events:
            break

        vectors: List[Tuple[int, float, float, float, float]] = []
        if mode == "paired":
            for idx in (1, 2):
                E = _finite_float(row[f"E{idx}"], f"E{idx}")
                px = _finite_float(row[f"px{idx}"], f"px{idx}")
                py = _finite_float(row[f"py{idx}"], f"py{idx}")
                pz = _finite_float(row[f"pz{idx}"], f"pz{idx}")
                vectors.append((idx, E, px, py, pz))
        else:
            vectors.append(
                (
                    1,
                    _finite_float(row["E"], "E"),
                    _finite_float(row["px"], "px"),
                    _finite_float(row["py"], "py"),
                    _finite_float(row["pz"], "pz"),
                )
            )

        reconstructed_pair_mass = None
        source_pair_mass = None
        pair_mass_delta = None
        if mode == "paired":
            v1 = vectors[0][1:]
            v2 = vectors[1][1:]
            reconstructed_pair_mass = pair_mass(v1, v2)
            if row.get("M") not in (None, ""):
                source_pair_mass = _finite_float(row["M"], "M")
                pair_mass_delta = reconstructed_pair_mass - source_pair_mass

        for idx, E, px, py, pz in vectors:
            wave = derive_wave_view(E, px, py, pz)
            out: Dict[str, object] = {
                "transform_version": TRANSFORM_VERSION,
                "derivation_class": "STANDARD_DERIVED",
                "source_record": source_record,
                "source_url": source_url,
                "event_index": event_index,
                "Run": row.get("Run", ""),
                "Event": row.get("Event", ""),
                "object_index": idx,
                "source_E_GeV": E,
                "source_px_GeV": px,
                "source_py_GeV": py,
                "source_pz_GeV": pz,
                "source_pt_GeV": row.get(f"pt{idx}", row.get("pt", "")),
                "source_eta": row.get(f"eta{idx}", row.get("eta", "")),
                "source_phi": row.get(f"phi{idx}", row.get("phi", "")),
                "source_charge": row.get(f"Q{idx}", row.get("Q", row.get("charge", ""))),
                "source_pair_mass_GeV": source_pair_mass,
                "reconstructed_pair_mass_GeV": reconstructed_pair_mass,
                "pair_mass_delta_GeV": pair_mass_delta,
            }
            for key, value in asdict(wave).items():
                out["std_wave_" + key] = _jsonable(value)

            if reference_energy_GeV is not None and bench_frequency_Hz is not None:
                out["analog_derivation_class"] = "SCALED_ANALOG"
                out["analog_reference_energy_GeV"] = reference_energy_GeV
                out["analog_reference_frequency_Hz"] = bench_frequency_Hz
                out["analog_energy_ratio"] = E / reference_energy_GeV
                out["analog_frequency_Hz"] = (E / reference_energy_GeV) * bench_frequency_Hz
            yield out


def write_jsonl(rows: Iterable[Dict[str, object]], fp: TextIO) -> Dict[str, float]:
    count = 0
    warning_mass2 = 0
    warning_beta = 0
    max_pair_delta = 0.0
    min_frequency = math.inf
    max_frequency = 0.0
    min_wavelength = math.inf
    max_wavelength = 0.0
    for row in rows:
        fp.write(json.dumps(row, sort_keys=True, allow_nan=False) + "\n")
        count += 1
        warning_mass2 += int(bool(row.get("std_wave_mass2_negative_warning")))
        warning_beta += int(bool(row.get("std_wave_beta_gt_one_warning")))
        delta = row.get("pair_mass_delta_GeV")
        if isinstance(delta, (int, float)):
            max_pair_delta = max(max_pair_delta, abs(float(delta)))
        f = row.get("std_wave_frequency_Hz")
        if isinstance(f, (int, float)):
            min_frequency = min(min_frequency, float(f))
            max_frequency = max(max_frequency, float(f))
        wl = row.get("std_wave_de_broglie_wavelength_m")
        if isinstance(wl, (int, float)):
            min_wavelength = min(min_wavelength, float(wl))
            max_wavelength = max(max_wavelength, float(wl))
    return {
        "objects": count,
        "mass2_negative_warnings": warning_mass2,
        "beta_gt_one_warnings": warning_beta,
        "max_abs_pair_mass_delta_GeV": max_pair_delta,
        "min_frequency_Hz": None if min_frequency is math.inf else min_frequency,
        "max_frequency_Hz": max_frequency,
        "min_de_broglie_wavelength_m": None if min_wavelength is math.inf else min_wavelength,
        "max_de_broglie_wavelength_m": max_wavelength,
    }


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, help="CSV path or http(s) URL")
    p.add_argument("--output", required=True, help="JSONL output path")
    p.add_argument("--summary", help="optional JSON summary path")
    p.add_argument("--source-record", default="")
    p.add_argument("--source-url", default="")
    p.add_argument("--reference-energy-gev", type=float)
    p.add_argument("--bench-frequency-hz", type=float)
    p.add_argument("--max-events", type=int)
    args = p.parse_args(argv)
    if (args.reference_energy_gev is None) != (args.bench_frequency_hz is None):
        p.error("--reference-energy-gev and --bench-frequency-hz must be supplied together")
    if args.reference_energy_gev is not None and args.reference_energy_gev <= 0:
        p.error("--reference-energy-gev must be > 0")
    if args.bench_frequency_hz is not None and args.bench_frequency_hz <= 0:
        p.error("--bench-frequency-hz must be > 0")
    return args


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    source_url = args.source_url or (args.input if args.input.startswith(("http://", "https://")) else "")
    out_path = pathlib.Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with _open_text(args.input) as source_fp:
        reader = csv.DictReader(source_fp)
        converted = iter_converted(
            reader,
            source_record=args.source_record,
            source_url=source_url,
            reference_energy_GeV=args.reference_energy_gev,
            bench_frequency_Hz=args.bench_frequency_hz,
            max_events=args.max_events,
        )
        with out_path.open("w", encoding="utf-8") as out_fp:
            summary = write_jsonl(converted, out_fp)

    summary.update(
        {
            "transform_version": TRANSFORM_VERSION,
            "source_record": args.source_record,
            "source_url": source_url,
            "input": args.input,
            "output": str(out_path),
            "derivation_classes": ["STANDARD_DERIVED"]
            + (["SCALED_ANALOG"] if args.reference_energy_gev is not None else []),
        }
    )
    text = json.dumps(summary, indent=2, sort_keys=True, allow_nan=False)
    print(text)
    if args.summary:
        summary_path = pathlib.Path(args.summary)
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(text + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
