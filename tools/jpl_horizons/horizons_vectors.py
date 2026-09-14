#!/usr/bin/env python3
"""Fetch NASA/JPL Horizons state vectors as a fixed orbital comparison target.

The tool preserves API query/version information, parses Cartesian state vectors,
and derives only transparent relative geometry. It does not implement or fit a
One-Wave gravity model.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import itertools
import json
import math
import pathlib
import urllib.parse
import urllib.request
from typing import Dict, List, Optional, Sequence

API_URL = "https://ssd.jpl.nasa.gov/api/horizons.api"
USER_AGENT = "One-Wave-JPL-Horizons-source-first/1.0"
TRANSFORM_VERSION = "jpl-horizons-vectors-v1"
BODY_NAMES = {
    "10": "Sun",
    "399": "Earth",
    "301": "Moon",
}


def request_json(url: str, timeout: int = 90) -> Dict[str, object]:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        raw = response.read()
    data = json.loads(raw.decode("utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Horizons API returned non-object JSON")
    return data


def quoted(value: str) -> str:
    return f"'{value}'"


def build_vectors_url(
    body_id: str,
    center: str,
    start: str,
    stop: str,
    step: str,
) -> str:
    params = {
        "format": "json",
        "COMMAND": quoted(body_id),
        "OBJ_DATA": "NO",
        "MAKE_EPHEM": "YES",
        "EPHEM_TYPE": "VECTORS",
        "CENTER": quoted(center),
        "START_TIME": quoted(start),
        "STOP_TIME": quoted(stop),
        "STEP_SIZE": quoted(step),
        "TIME_TYPE": "TDB",
        "TIME_DIGITS": "SECONDS",
        "REF_SYSTEM": "ICRF",
        "REF_PLANE": "FRAME",
        "OUT_UNITS": "KM-S",
        "VEC_TABLE": "2",
        "VEC_CORR": "NONE",
        "CSV_FORMAT": "YES",
        "VEC_LABELS": "YES",
    }
    return API_URL + "?" + urllib.parse.urlencode(params)


def _float(token: str) -> float:
    value = float(token.strip())
    if not math.isfinite(value):
        raise ValueError(f"non-finite Horizons numeric token: {token!r}")
    return value


def parse_vector_result(result_text: str) -> List[Dict[str, object]]:
    if "$$SOE" not in result_text or "$$EOE" not in result_text:
        tail = result_text[-1000:]
        raise ValueError(f"Horizons result missing $$SOE/$$EOE markers; tail={tail!r}")
    table = result_text.split("$$SOE", 1)[1].split("$$EOE", 1)[0]
    rows: List[Dict[str, object]] = []
    reader = csv.reader(io.StringIO(table))
    for raw in reader:
        tokens = [x.strip() for x in raw if x.strip()]
        if not tokens:
            continue
        # VEC_TABLE=2 + CSV_FORMAT=YES gives JD, calendar date, x,y,z,vx,vy,vz.
        # Keep parsing strict so format drift fails visibly.
        if len(tokens) < 8:
            raise ValueError(f"unexpected Horizons vector row: {raw!r}")
        try:
            jd = _float(tokens[0])
            x, y, z, vx, vy, vz = map(_float, tokens[2:8])
        except ValueError as exc:
            raise ValueError(f"failed to parse Horizons vector row: {raw!r}") from exc
        rows.append(
            {
                "jd_tdb": jd,
                "calendar_tdb": tokens[1],
                "x_km": x,
                "y_km": y,
                "z_km": z,
                "vx_km_s": vx,
                "vy_km_s": vy,
                "vz_km_s": vz,
            }
        )
    if not rows:
        raise ValueError("Horizons vector result contained no data rows")
    return rows


def fetch_body_vectors(
    body_id: str,
    center: str,
    start: str,
    stop: str,
    step: str,
) -> Dict[str, object]:
    url = build_vectors_url(body_id, center, start, stop, step)
    response = request_json(url)
    signature = response.get("signature")
    if not isinstance(signature, dict):
        raise ValueError("Horizons response missing signature/version")
    result = response.get("result")
    if not isinstance(result, str):
        raise ValueError("Horizons response missing text result")
    rows = parse_vector_result(result)
    return {
        "body_id": body_id,
        "body_name": BODY_NAMES.get(body_id, body_id),
        "source_api_url": url,
        "api_signature": signature,
        "raw_result_sha256": hashlib.sha256(result.encode("utf-8")).hexdigest(),
        "center": center,
        "reference_system": "ICRF",
        "reference_plane": "FRAME",
        "time_type": "TDB",
        "units": {"position": "km", "velocity": "km/s"},
        "rows": rows,
    }


def relative_geometry(a: Dict[str, object], b: Dict[str, object]) -> Dict[str, float]:
    dx = float(b["x_km"]) - float(a["x_km"])
    dy = float(b["y_km"]) - float(a["y_km"])
    dz = float(b["z_km"]) - float(a["z_km"])
    dvx = float(b["vx_km_s"]) - float(a["vx_km_s"])
    dvy = float(b["vy_km_s"]) - float(a["vy_km_s"])
    dvz = float(b["vz_km_s"]) - float(a["vz_km_s"])
    distance = math.sqrt(dx * dx + dy * dy + dz * dz)
    speed = math.sqrt(dvx * dvx + dvy * dvy + dvz * dvz)
    radial = (dx * dvx + dy * dvy + dz * dvz) / distance if distance else 0.0
    transverse = math.sqrt(max(speed * speed - radial * radial, 0.0))
    return {
        "dx_km": dx,
        "dy_km": dy,
        "dz_km": dz,
        "dvx_km_s": dvx,
        "dvy_km_s": dvy,
        "dvz_km_s": dvz,
        "distance_km": distance,
        "relative_speed_km_s": speed,
        "radial_speed_km_s": radial,
        "transverse_speed_km_s": transverse,
    }


def build_pair_series(bodies: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    output: List[Dict[str, object]] = []
    for left, right in itertools.combinations(bodies, 2):
        left_rows = {round(float(r["jd_tdb"]), 9): r for r in left["rows"]}  # type: ignore[index]
        right_rows = {round(float(r["jd_tdb"]), 9): r for r in right["rows"]}  # type: ignore[index]
        common = sorted(set(left_rows) & set(right_rows))
        series = []
        for jd in common:
            geom = relative_geometry(left_rows[jd], right_rows[jd])
            series.append({"jd_tdb": jd, **geom})
        output.append(
            {
                "body_a_id": left["body_id"],
                "body_a_name": left["body_name"],
                "body_b_id": right["body_id"],
                "body_b_name": right["body_name"],
                "rows": series,
            }
        )
    return output


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--bodies", default="10,399,301", help="comma-separated Horizons body IDs")
    p.add_argument("--center", default="500@0", help="Horizons vector center")
    p.add_argument("--start", default="2026-09-01")
    p.add_argument("--stop", default="2026-09-05")
    p.add_argument("--step", default="1 d")
    p.add_argument("--output", required=True)
    return p.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    body_ids = [x.strip() for x in args.bodies.split(",") if x.strip()]
    if len(body_ids) < 2:
        raise SystemExit("supply at least two body IDs")

    # JPL asks API users to submit one request at a time; keep this loop sequential.
    bodies = [
        fetch_body_vectors(body_id, args.center, args.start, args.stop, args.step)
        for body_id in body_ids
    ]
    pairs = build_pair_series(bodies)

    result = {
        "transform_version": TRANSFORM_VERSION,
        "derivation_class": "SOURCE_EPHEMERIS_PLUS_STANDARD_GEOMETRY_DERIVED",
        "source_project": "NASA/JPL Horizons",
        "source_api_documentation": "https://ssd-api.jpl.nasa.gov/doc/horizons.html",
        "query": {
            "bodies": body_ids,
            "center": args.center,
            "start": args.start,
            "stop": args.stop,
            "step": args.step,
            "reference_system": "ICRF",
            "reference_plane": "FRAME",
            "time_type": "TDB",
            "out_units": "KM-S",
            "vec_table": 2,
            "vec_corr": "NONE",
        },
        "bodies": bodies,
        "pairs": pairs,
        "one_wave_status": "YELLOW_OPEN_NO_GRAVITY_EQUATION_APPLIED",
        "interpretation_warning": (
            "These vectors are a target for One-Wave orbital/gravity predictions, not proof of a proposed mechanism."
        ),
    }

    path = pathlib.Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(result, indent=2, sort_keys=True, allow_nan=False)
    path.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
