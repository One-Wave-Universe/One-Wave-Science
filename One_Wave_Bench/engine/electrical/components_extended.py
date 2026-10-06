"""Extended electrical components for P0 ternary circuit simulation.

Adds to the basic DC batch:
- NMOS and PMOS MOSFETs with on/off resistance modeling
- Capacitors with energy storage state
- Inductors with current state
- OpAmpBuffer (idealized op-amp unity buffer for virtual ground)

Each component is self-contained: it knows only its own pins, parameters,
and state. No component knows about any circuit, build, or project.

See BREADBOARD_CANONICAL_ARCHITECTURE.md layer definitions for how these
are tested and used.
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class NMOS:
    """N-channel MOSFET: conducts drain-to-source when Vgs >= Vth.

    Simplified model:
    - Vth: gate-source threshold voltage (typically 1.0-2.0V)
    - Rds_on: on-state drain-source resistance when fully on (Vgs >> Vth)
    - off_leakage_nA: leakage current (drain to source) when off, in nanoamps

    No body diode modeled in P0. Back-conduction must use two MOSFETs
    back-to-back if bidirectional is required.
    """
    id: str
    gate: str
    drain: str
    source: str
    Vth: float = 1.0
    Rds_on: float = 0.5
    off_leakage_nA: float = 100.0

    def __post_init__(self):
        if self.Vth <= 0:
            raise ValueError(f"NMOS {self.id!r} Vth must be > 0, got {self.Vth}")
        if self.Rds_on <= 0:
            raise ValueError(f"NMOS {self.id!r} Rds_on must be > 0, got {self.Rds_on}")
        if self.off_leakage_nA < 0:
            raise ValueError(f"NMOS {self.id!r} off_leakage_nA must be >= 0, got {self.off_leakage_nA}")


@dataclass(frozen=True)
class PMOS:
    """P-channel MOSFET: conducts drain-to-source when Vgs <= -Vth.

    Simplified model (same as NMOS but gate voltage is relative to source,
    which is typically at +V):
    - Vth: gate-source threshold magnitude (typically 0.7-1.5V, sign ignored here)
    - Rds_on: on-state drain-source resistance when fully on
    - off_leakage_nA: leakage current when off, in nanoamps
    """
    id: str
    gate: str
    drain: str
    source: str
    Vth: float = 1.0
    Rds_on: float = 0.5
    off_leakage_nA: float = 100.0

    def __post_init__(self):
        if self.Vth <= 0:
            raise ValueError(f"PMOS {self.id!r} Vth must be > 0, got {self.Vth}")
        if self.Rds_on <= 0:
            raise ValueError(f"PMOS {self.id!r} Rds_on must be > 0, got {self.Rds_on}")
        if self.off_leakage_nA < 0:
            raise ValueError(f"PMOS {self.id!r} off_leakage_nA must be >= 0, got {self.off_leakage_nA}")


@dataclass(frozen=True)
class Capacitor:
    """Linear capacitor: I = C * dV/dt, energy = 0.5 * C * V^2.

    State is stored externally (in a transient solver's state vector).
    The voltage across the capacitor is V(a) - V(b).
    """
    id: str
    a: str
    b: str
    farads: float

    def __post_init__(self):
        if self.farads <= 0:
            raise ValueError(f"Capacitor {self.id!r} must have farads > 0, got {self.farads}")


@dataclass(frozen=True)
class Inductor:
    """Linear inductor: V = L * dI/dt, energy = 0.5 * L * I^2.

    State is stored externally (in a transient solver's state vector).
    Current flows from a to b.
    """
    id: str
    a: str
    b: str
    henries: float

    def __post_init__(self):
        if self.henries <= 0:
            raise ValueError(f"Inductor {self.id!r} must have henries > 0, got {self.henries}")


@dataclass(frozen=True)
class OpAmpBuffer:
    """Idealized unity-gain op-amp buffer (buffer, follower, virtual ground).

    Models a high-impedance input, low-impedance output, infinite gain,
    and frequency response (modeled as pole at cutoff_hz).

    V_out = V_in (ideal), but with output driving capability limited by
    max_sourcing_mA and output impedance Rout.

    For P0 virtual ground: TLE2426 or similar rail splitter can be
    approximated as a 1x buffer with Rout ~ 1 ohm and max current ~ 100mA.
    """
    id: str
    v_in: str
    v_out: str
    gnd: str  # reference (ground) node
    gain: float = 1.0
    Rout: float = 1.0  # output impedance, ohms
    max_sourcing_mA: float = 100.0
    max_sinking_mA: float = 100.0
    cutoff_hz: float = 1e6  # pole frequency for transient response

    def __post_init__(self):
        if self.Rout < 0:
            raise ValueError(f"OpAmpBuffer {self.id!r} Rout must be >= 0, got {self.Rout}")
        if self.max_sourcing_mA < 0:
            raise ValueError(f"OpAmpBuffer {self.id!r} max_sourcing_mA must be >= 0, got {self.max_sourcing_mA}")
