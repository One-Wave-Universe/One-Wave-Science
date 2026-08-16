"""One integrated evolution ledger for Gray, relativity, and One Wave channels."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import numpy as np

from solar_system_control import MASSES, acceleration_receipt, step


class OneWaveLaw(Protocol):
    def __call__(self, r: np.ndarray, v: np.ndarray, time: float) -> np.ndarray: ...


@dataclass(frozen=True)
class HybridReceipt:
    time: float
    newtonian_norm: float
    relativity_norm: float
    one_wave_raw_norm: float
    one_wave_closed_norm: float
    one_wave_net_force: tuple[float, float, float]
    one_wave_net_torque: tuple[float, float, float]
    total_norm: float


def close_internal_channel(r: np.ndarray, raw: np.ndarray) -> np.ndarray:
    """Remove translation and rigid-rotation modes from an internal candidate.

    An internal One Wave exchange may redistribute acceleration, but it cannot
    create system momentum or angular momentum from nowhere. External forcing
    must be declared as a separate boundary channel rather than hidden here.
    """
    total_mass = float(MASSES.sum())
    closed = raw - np.sum(MASSES[:, None] * raw, axis=0) / total_mass
    center = np.sum(MASSES[:, None] * r, axis=0) / total_mass
    rel = r - center
    torque = np.sum(np.cross(rel, MASSES[:, None] * closed), axis=0)
    inertia = np.zeros((3, 3))
    for mass, vector in zip(MASSES, rel):
        inertia += mass * ((vector @ vector) * np.eye(3) - np.outer(vector, vector))
    omega_accel = np.linalg.pinv(inertia, rcond=1e-14) @ torque
    closed -= np.cross(omega_accel, rel)
    # Floating-point cleanup of the translation mode after torque projection.
    closed -= np.sum(MASSES[:, None] * closed, axis=0) / total_mass
    return closed


def hybrid_channels(r: np.ndarray, v: np.ndarray, time: float,
                    one_wave_law: OneWaveLaw | None = None) -> dict[str, np.ndarray]:
    gray = acceleration_receipt(r, v, time, candidate_law=None, relativity=True)
    raw = np.zeros_like(r) if one_wave_law is None else one_wave_law(r, v, time)
    if raw.shape != r.shape or not np.isfinite(raw).all():
        raise ValueError("One Wave law must return a finite acceleration for every body")
    return {
        "newtonian": gray["newtonian"],
        "relativity_1pn": gray["relativity_1pn"],
        "one_wave_raw": raw,
        "one_wave_closed": close_internal_channel(r, raw),
    }


def make_receipt(r: np.ndarray, v: np.ndarray, time: float,
                 one_wave_law: OneWaveLaw | None = None) -> HybridReceipt:
    channels = hybrid_channels(r, v, time, one_wave_law)
    closed = channels["one_wave_closed"]
    center = np.sum(MASSES[:, None] * r, axis=0) / MASSES.sum()
    net_force = np.sum(MASSES[:, None] * closed, axis=0)
    net_torque = np.sum(np.cross(r - center, MASSES[:, None] * closed), axis=0)
    total = channels["newtonian"] + channels["relativity_1pn"] + closed
    return HybridReceipt(
        time=time,
        newtonian_norm=float(np.linalg.norm(channels["newtonian"])),
        relativity_norm=float(np.linalg.norm(channels["relativity_1pn"])),
        one_wave_raw_norm=float(np.linalg.norm(channels["one_wave_raw"])),
        one_wave_closed_norm=float(np.linalg.norm(closed)),
        one_wave_net_force=tuple(float(x) for x in net_force),
        one_wave_net_torque=tuple(float(x) for x in net_torque),
        total_norm=float(np.linalg.norm(total)),
    )


def hybrid_step(r: np.ndarray, v: np.ndarray, dt: float, time: float,
                one_wave_law: OneWaveLaw | None = None) -> tuple[np.ndarray, np.ndarray, HybridReceipt]:
    """Advance one state with the closed One Wave channel and return its receipt."""
    def closed_law(x: np.ndarray, u: np.ndarray, t: float) -> np.ndarray:
        raw = np.zeros_like(x) if one_wave_law is None else one_wave_law(x, u, t)
        return close_internal_channel(x, raw)

    receipt = make_receipt(r, v, time, one_wave_law)
    r1, v1 = step(r, v, dt, time, candidate_law=closed_law, relativity=True)
    return r1, v1, receipt
