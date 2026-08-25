"""Measured classification of candidate center geometries."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class CenterGeometryReceipt:
    point_residence_fraction: float
    band_residence_fraction: float
    crossing_times: tuple[float, ...]
    crossing_directions: tuple[int, ...]
    crossing_speeds: tuple[float, ...]
    recurrent_direction: int
    return_time_cv: float
    crossing_speed_cv: float
    slow_speed_ratio: float
    has_point_residence: bool
    has_finite_band: bool
    has_crossing_section: bool
    has_limit_cycle_section: bool
    has_slow_manifold_candidate: bool


def _cv(values: np.ndarray) -> float:
    if values.size < 2:
        return float("inf")
    mean = float(np.mean(np.abs(values)))
    return float(np.std(values) / mean) if mean > 0.0 else float("inf")


def classify_center_geometry(
    time: np.ndarray,
    x: np.ndarray,
    v: np.ndarray,
    *,
    point_x_tol: float,
    point_v_tol: float,
    band_half_width: float,
    recurrence_cv_tol: float = 0.05,
    speed_cv_tol: float = 0.05,
    slow_ratio_min: float = 3.0,
) -> CenterGeometryReceipt:
    time = np.asarray(time, dtype=float)
    x = np.asarray(x, dtype=float)
    v = np.asarray(v, dtype=float)
    if time.ndim != 1 or x.shape != time.shape or v.shape != time.shape:
        raise ValueError("time, x, and v must be equal-length one-dimensional arrays")
    if time.size < 3 or not np.isfinite(time).all() or not np.isfinite(x).all() or not np.isfinite(v).all():
        raise ValueError("trajectory must contain at least three finite samples")
    if not np.all(np.diff(time) > 0.0):
        raise ValueError("time must be strictly increasing")
    if not (0.0 <= point_x_tol < band_half_width and point_v_tol >= 0.0):
        raise ValueError("require 0 <= point_x_tol < band_half_width and point_v_tol >= 0")
    if recurrence_cv_tol < 0.0 or speed_cv_tol < 0.0 or slow_ratio_min <= 1.0:
        raise ValueError("dispersion tolerances must be nonnegative and slow_ratio_min > 1")

    point = (np.abs(x) <= point_x_tol) & (np.abs(v) <= point_v_tol)
    band = np.abs(x) <= band_half_width

    crossing_times, directions, speeds = [], [], []
    for i in np.flatnonzero(x[:-1] * x[1:] < 0.0):
        fraction = -x[i] / (x[i + 1] - x[i])
        tc = time[i] + fraction * (time[i + 1] - time[i])
        vc = v[i] + fraction * (v[i + 1] - v[i])
        crossing_times.append(float(tc))
        directions.append(1 if vc > 0.0 else -1 if vc < 0.0 else 0)
        speeds.append(float(abs(vc)))

    best_direction, best_return_cv, best_speed_cv = 0, float("inf"), float("inf")
    for direction in (-1, 1):
        ids = [i for i, d in enumerate(directions) if d == direction]
        if len(ids) < 3:
            continue
        ts = np.asarray([crossing_times[i] for i in ids])
        ss = np.asarray([speeds[i] for i in ids])
        return_cv, speed_cv = _cv(np.diff(ts)), _cv(ss)
        if (return_cv, speed_cv) < (best_return_cv, best_speed_cv):
            best_direction, best_return_cv, best_speed_cv = direction, return_cv, speed_cv

    inside_speed = np.abs(v[band])
    outside_speed = np.abs(v[~band])
    positive_inside = inside_speed[inside_speed > point_v_tol]
    if positive_inside.size and outside_speed.size:
        slow_ratio = float(np.median(outside_speed) / np.median(positive_inside))
    else:
        slow_ratio = 0.0

    return CenterGeometryReceipt(
        point_residence_fraction=float(np.mean(point)),
        band_residence_fraction=float(np.mean(band)),
        crossing_times=tuple(crossing_times),
        crossing_directions=tuple(directions),
        crossing_speeds=tuple(speeds),
        recurrent_direction=best_direction,
        return_time_cv=best_return_cv,
        crossing_speed_cv=best_speed_cv,
        slow_speed_ratio=slow_ratio,
        has_point_residence=bool(np.any(point)),
        has_finite_band=bool(np.any(band & ~point)),
        has_crossing_section=bool(crossing_times),
        has_limit_cycle_section=(
            best_direction != 0
            and best_return_cv <= recurrence_cv_tol
            and best_speed_cv <= speed_cv_tol
        ),
        has_slow_manifold_candidate=slow_ratio >= slow_ratio_min,
    )
