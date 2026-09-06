"""C1 — recursive Point-Path-Field state schema.

X_s = {P_s, gamma_s, F_s; children X_{s-1,k}}

This is a bookkeeping object with declared units and frames.
It does not derive Point, Path, or Field rotation (C2-C4).
It does not claim a physical Field equation.

Frames:
  ground  — A-101 undisplaced reference
  local   — Point-attached orthonormal frame
  path    — parallel-transported along gamma
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Optional, Sequence, Tuple


ALLOWED_UNITS = frozenset(
    {
        "1",
        "m",
        "s",
        "rad",
        "m/s",
        "rad/s",
        "1/s",
        "N",
        "J",
        "V",
        "A",
        "T",
        "Pa",
    }
)
ALLOWED_FRAMES = frozenset({"ground", "local", "path"})
ALLOWED_SCALES = frozenset({"micro", "small", "middle", "large", "macro", "unspecified"})


def _check_unit(unit: str, label: str) -> str:
    if unit not in ALLOWED_UNITS:
        raise ValueError(f"{label} unit {unit!r} is not in ALLOWED_UNITS")
    return unit


def _check_frame(frame: str, label: str) -> str:
    if frame not in ALLOWED_FRAMES:
        raise ValueError(f"{label} frame {frame!r} is not in ALLOWED_FRAMES")
    return frame


@dataclass(frozen=True)
class Quantity:
    value: Tuple[float, ...]
    unit: str
    frame: str
    name: str = ""

    def __post_init__(self) -> None:
        _check_unit(self.unit, self.name or "quantity")
        _check_frame(self.frame, self.name or "quantity")
        if not self.value:
            raise ValueError(f"{self.name or 'quantity'} has empty value")


@dataclass(frozen=True)
class PointState:
    """Localized carrier of position and intrinsic orientation."""

    position: Quantity
    orientation: Quantity
    scale_label: str = "unspecified"

    def __post_init__(self) -> None:
        if self.scale_label not in ALLOWED_SCALES:
            raise ValueError(f"unknown scale_label {self.scale_label!r}")
        if self.position.unit != "m":
            raise ValueError("Point.position unit must be m")
        if self.orientation.unit != "rad":
            raise ValueError("Point.orientation unit must be rad")


@dataclass(frozen=True)
class PathState:
    """Finite directed connection that transports a Point frame."""

    start: Quantity
    end: Quantity
    length: Quantity
    circulation: Quantity

    def __post_init__(self) -> None:
        if self.start.unit != "m" or self.end.unit != "m":
            raise ValueError("Path endpoints must be in m")
        if self.length.unit != "m":
            raise ValueError("Path.length unit must be m")
        if self.circulation.unit != "m/s":
            raise ValueError("Path.circulation unit must be m/s (proxy until C3)")
        if self.length.value[0] < 0:
            raise ValueError("Path.length cannot be negative")


@dataclass(frozen=True)
class FieldState:
    """Enclosing carrier sampled at the Point, not a Path substitute."""

    amplitude: Quantity
    phase: Quantity

    def __post_init__(self) -> None:
        if self.phase.unit != "rad":
            raise ValueError("Field.phase unit must be rad")


@dataclass
class PPFState:
    """Recursive PPF node at one scale."""

    scale: int
    point: PointState
    path: PathState
    field: FieldState
    children: List["PPFState"] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.scale < 0:
            raise ValueError("scale must be >= 0")
        for child in self.children:
            if child.scale != self.scale - 1:
                raise ValueError(
                    f"child scale {child.scale} must be parent scale {self.scale} minus 1"
                )

    def depth(self) -> int:
        if not self.children:
            return 1
        return 1 + max(child.depth() for child in self.children)

    def leaf_count(self) -> int:
        if not self.children:
            return 1
        return sum(child.leaf_count() for child in self.children)

    def walk(self) -> Iterable["PPFState"]:
        yield self
        for child in self.children:
            yield from child.walk()


def quantity(values: Sequence[float], unit: str, frame: str, name: str = "") -> Quantity:
    return Quantity(tuple(float(v) for v in values), unit, frame, name)


def leaf_point(x: float, y: float, theta: float = 0.0, scale_label: str = "micro") -> PointState:
    return PointState(
        position=quantity((x, y, 0.0), "m", "ground", "position"),
        orientation=quantity((theta,), "rad", "local", "orientation"),
        scale_label=scale_label,
    )


def segment_path(x0: float, y0: float, x1: float, y1: float) -> PathState:
    dx = x1 - x0
    dy = y1 - y0
    length = (dx * dx + dy * dy) ** 0.5
    return PathState(
        start=quantity((x0, y0, 0.0), "m", "ground", "start"),
        end=quantity((x1, y1, 0.0), "m", "ground", "end"),
        length=quantity((length,), "m", "path", "length"),
        circulation=quantity((0.0,), "m/s", "path", "circulation"),
    )


def zero_field(amplitude_unit: str = "1") -> FieldState:
    return FieldState(
        amplitude=quantity((0.0,), amplitude_unit, "ground", "amplitude"),
        phase=quantity((0.0,), "rad", "ground", "phase"),
    )


def nest(parent_scale: int, parent_point: PointState, children: Sequence[PPFState]) -> PPFState:
    if not children:
        raise ValueError("nest requires at least one child")
    xs = [c.point.position.value[0] for c in children]
    ys = [c.point.position.value[1] for c in children]
    path = segment_path(min(xs), min(ys), max(xs), max(ys))
    return PPFState(
        scale=parent_scale,
        point=parent_point,
        path=path,
        field=zero_field(),
        children=list(children),
    )
