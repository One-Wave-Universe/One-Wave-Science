"""Gray-Brick solar-system control for One Wave displacement experiments.

This module is the anti-drift control, not a claim that the One Wave candidate
law has been derived.  Planet states begin from JPL's published approximate
Keplerian elements and advance through barycentric Newtonian N-body dynamics.
Candidate displacement acceleration is an explicit optional input and defaults
to exactly zero.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, pi, sin, sqrt
from typing import Callable

import numpy as np

# Units: AU, day, solar mass. Gaussian gravitational constant squared.
G_AU3_SOLAR_MASS_DAY2 = 0.0002959122082855911
C_AU_PER_DAY = 173.144632674240
J2000 = 2451545.0


@dataclass(frozen=True)
class Elements:
    a: tuple[float, float]
    e: tuple[float, float]
    inc: tuple[float, float]
    mean_longitude: tuple[float, float]
    long_perihelion: tuple[float, float]
    long_node: tuple[float, float]


# JPL SSD Table 1, valid 1800-2050. Value, rate per Julian century.
ELEMENTS = {
    "Mercury": Elements((.38709927, .00000037), (.20563593, .00001906), (7.00497902, -.00594749), (252.25032350, 149472.67411175), (77.45779628, .16047689), (48.33076593, -.12534081)),
    "Venus": Elements((.72333566, .00000390), (.00677672, -.00004107), (3.39467605, -.00078890), (181.97909950, 58517.81538729), (131.60246718, .00268329), (76.67984255, -.27769418)),
    "Earth": Elements((1.00000261, .00000562), (.01671123, -.00004392), (-.00001531, -.01294668), (100.46457166, 35999.37244981), (102.93768193, .32327364), (0., 0.)),
    "Mars": Elements((1.52371034, .00001847), (.09339410, .00007882), (1.84969142, -.00813131), (-4.55343205, 19140.30268499), (-23.94362959, .44441088), (49.55953891, -.29257343)),
    "Jupiter": Elements((5.20288700, -.00011607), (.04838624, -.00013253), (1.30439695, -.00183714), (34.39644051, 3034.74612775), (14.72847983, .21252668), (100.47390909, .20469106)),
    "Saturn": Elements((9.53667594, -.00125060), (.05386179, -.00050991), (2.48599187, .00193609), (49.95424423, 1222.49362201), (92.59887831, -.41897216), (113.66242448, -.28867794)),
    "Uranus": Elements((19.18916464, -.00196176), (.04725744, -.00004397), (.77263783, -.00242939), (313.23810451, 428.48202785), (170.95427630, .40805281), (74.01692503, .04240589)),
    "Neptune": Elements((30.06992276, .00026291), (.00859048, .00005105), (1.77004347, .00035372), (-55.12002969, 218.45945325), (44.96476227, -.32241464), (131.78422574, -.00508664)),
}

# JPL physical-parameter masses converted from 10^24 kg to solar masses.
SOLAR_MASS_KG = 1.98847e30
MASS_KG = {
    "Sun": SOLAR_MASS_KG,
    "Mercury": .330103e24, "Venus": 4.86731e24, "Earth": 5.97217e24,
    "Mars": .641691e24, "Jupiter": 1898.125e24, "Saturn": 568.317e24,
    "Uranus": 86.8099e24, "Neptune": 102.4092e24, "Moon": 7.342e22,
}
NAMES = ("Sun", "Mercury", "Venus", "Earth", "Moon", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune")
MASSES = np.array([MASS_KG[n] / SOLAR_MASS_KG for n in NAMES])


def _value(pair: tuple[float, float], centuries: float) -> float:
    return pair[0] + pair[1] * centuries


def kepler_position(name: str, jd: float) -> np.ndarray:
    """J2000 ecliptic heliocentric position using JPL's approximation."""
    el = ELEMENTS[name]
    t = (jd - J2000) / 36525.0
    a, e = _value(el.a, t), _value(el.e, t)
    inc = np.deg2rad(_value(el.inc, t))
    long_peri = np.deg2rad(_value(el.long_perihelion, t))
    node = np.deg2rad(_value(el.long_node, t))
    mean_anomaly = np.deg2rad((_value(el.mean_longitude, t) - np.rad2deg(long_peri)) % 360.0)
    eccentric = mean_anomaly
    for _ in range(12):
        eccentric -= (eccentric - e * sin(eccentric) - mean_anomaly) / (1.0 - e * cos(eccentric))
    xp = a * (cos(eccentric) - e)
    yp = a * sqrt(1.0 - e * e) * sin(eccentric)
    arg_peri = long_peri - node
    cw, sw, co, so, ci, si = cos(arg_peri), sin(arg_peri), cos(node), sin(node), cos(inc), sin(inc)
    return np.array([
        (cw * co - sw * so * ci) * xp + (-sw * co - cw * so * ci) * yp,
        (cw * so + sw * co * ci) * xp + (-sw * so + cw * co * ci) * yp,
        sw * si * xp + cw * si * yp,
    ])


def kepler_state(name: str, jd: float) -> tuple[np.ndarray, np.ndarray]:
    """Position and central-difference velocity from the same JPL formula."""
    dt = 1e-3
    p = kepler_position(name, jd)
    v = (kepler_position(name, jd + dt) - kepler_position(name, jd - dt)) / (2 * dt)
    return p, v


def initial_state(jd: float = J2000) -> tuple[np.ndarray, np.ndarray]:
    """Barycentric Sun/planets plus Moon attached to Earth's current state."""
    positions = [np.zeros(3)]
    velocities = [np.zeros(3)]
    planet_states = {name: kepler_state(name, jd) for name in ELEMENTS}
    # A simple epoch-relative lunar state. It is always added to Earth, never
    # advanced as an independent screen-space orb.
    moon_a = 384400.0 / 149597870.7
    moon_period = 27.321661
    phase = 2 * pi * (jd - J2000) / moon_period
    moon_rel = np.array([moon_a * cos(phase), moon_a * sin(phase), 0.0])
    moon_vel_rel = np.array([-moon_a * sin(phase), moon_a * cos(phase), 0.0]) * (2 * pi / moon_period)
    for name in NAMES[1:]:
        if name == "Moon":
            earth_p, earth_v = planet_states["Earth"]
            positions.append(earth_p + moon_rel)
            velocities.append(earth_v + moon_vel_rel)
        else:
            p, v = planet_states[name]
            positions.append(p)
            velocities.append(v)
    r, v = np.array(positions), np.array(velocities)
    r -= np.sum(MASSES[:, None] * r, axis=0) / MASSES.sum()
    v -= np.sum(MASSES[:, None] * v, axis=0) / MASSES.sum()
    return r, v


def gravity_acceleration(r: np.ndarray) -> np.ndarray:
    a = np.zeros_like(r)
    for i in range(len(r)):
        delta = r - r[i]
        dist2 = np.sum(delta * delta, axis=1)
        mask = np.arange(len(r)) != i
        a[i] = G_AU3_SOLAR_MASS_DAY2 * np.sum(
            MASSES[mask, None] * delta[mask] / dist2[mask, None] ** 1.5, axis=0
        )
    return a


def relativistic_acceleration(r: np.ndarray, v: np.ndarray) -> np.ndarray:
    """Leading Schwarzschild 1PN correction relative to the Sun.

    This captures the dominant solar relativistic perihelion correction. It is
    not a full Einstein-Infeld-Hoffmann solar-system integrator.
    """
    result = np.zeros_like(r)
    sun = NAMES.index("Sun")
    mu = G_AU3_SOLAR_MASS_DAY2 * MASSES[sun]
    for i in range(1, len(r)):
        rel_r = r[i] - r[sun]
        rel_v = v[i] - v[sun]
        radius = np.linalg.norm(rel_r)
        speed2 = float(rel_v @ rel_v)
        radial_speed = float(rel_r @ rel_v)
        correction = mu / (C_AU_PER_DAY**2 * radius**3) * (
            (4.0 * mu / radius - speed2) * rel_r + 4.0 * radial_speed * rel_v
        )
        result[i] += correction
        result[sun] -= MASSES[i] / MASSES[sun] * correction
    return result


CandidateLaw = Callable[[np.ndarray, np.ndarray, float], np.ndarray]


def acceleration_receipt(r: np.ndarray, v: np.ndarray, time: float = 0.0,
                         candidate_law: CandidateLaw | None = None,
                         relativity: bool = True) -> dict[str, np.ndarray]:
    """Return named acceleration channels so no mechanism is hidden."""
    return {
        "newtonian": gravity_acceleration(r),
        "relativity_1pn": relativistic_acceleration(r, v) if relativity else np.zeros_like(r),
        "one_wave_candidate": np.zeros_like(r) if candidate_law is None else candidate_law(r, v, time),
    }


def step(r: np.ndarray, v: np.ndarray, dt: float, time: float = 0.0,
         candidate_law: CandidateLaw | None = None,
         relativity: bool = True) -> tuple[np.ndarray, np.ndarray]:
    """Velocity-Verlet step; optional candidate law is separately auditable."""
    channels0 = acceleration_receipt(r, v, time, candidate_law, relativity)
    a0 = sum(channels0.values())
    r1 = r + v * dt + 0.5 * a0 * dt * dt
    predicted_v = v + a0 * dt
    channels1 = acceleration_receipt(r1, predicted_v, time + dt, candidate_law, relativity)
    a1 = sum(channels1.values())
    return r1, v + 0.5 * (a0 + a1) * dt


def energy(r: np.ndarray, v: np.ndarray) -> float:
    kinetic = .5 * np.sum(MASSES[:, None] * v * v)
    potential = 0.0
    for i in range(len(r)):
        for j in range(i + 1, len(r)):
            potential -= G_AU3_SOLAR_MASS_DAY2 * MASSES[i] * MASSES[j] / np.linalg.norm(r[j] - r[i])
    return float(kinetic + potential)


def attached_marker(body_position: np.ndarray, body_velocity: np.ndarray,
                    local_offset: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """A field/shell marker inherits its body state; it cannot outpace it."""
    return body_position + local_offset, body_velocity.copy()
