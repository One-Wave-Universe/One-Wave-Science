"""Audio-first, provider-neutral film-reel timeline for Goblin Raccoon Studio.

This module intentionally does *not* animate a character container and does not
invent procedural movement.  A shot is an old-school strip of film:

1. audio establishes the shot duration;
2. time is divided into frame slots;
3. drawings are exposed on explicit slots;
4. each exposure owns a ground-contact position in the background world;
5. perspective scale is derived from that ground point;
6. human UI and AI agents edit the same JSON-shaped project data.

Artwork is referenced, never redesigned here.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Iterable, Mapping, Sequence


DEFAULT_FPS = 24


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


@dataclass(frozen=True)
class PerspectiveGrid:
    """Editor calibration for one background plate.

    Coordinates are normalized to the background: 0.0..1.0.  ``horizon_scale``
    is the actor size at/above the horizon and ``front_scale`` is the actor size
    at the bottom edge of the scene.  The grid is calibration metadata only; it
    is never a render layer.
    """

    horizon_y: float = 0.38
    vanishing_x: float = 0.50
    horizon_scale: float = 0.22
    front_scale: float = 1.00

    def scale_at(self, ground_y: float) -> float:
        y = _clamp(float(ground_y), 0.0, 1.0)
        horizon = _clamp(float(self.horizon_y), 0.0, 0.99)
        if y <= horizon:
            return float(self.horizon_scale)
        u = _clamp((y - horizon) / max(1e-9, 1.0 - horizon), 0.0, 1.0)
        # Smoothstep prevents visible scale kinks when an actor crosses bands.
        eased = u * u * (3.0 - 2.0 * u)
        return float(self.horizon_scale) + (
            float(self.front_scale) - float(self.horizon_scale)
        ) * eased


@dataclass(frozen=True)
class AudioTrack:
    kind: str
    path: str
    duration_ms: int
    gain: float = 0.90
    start_ms: int = 0

    @property
    def end_ms(self) -> int:
        return max(0, int(self.start_ms)) + max(0, int(self.duration_ms))


@dataclass(frozen=True)
class Exposure:
    """One drawing exposed across one or more film frames."""

    asset_id: str
    start_frame: int
    hold_frames: int = 1
    x: float = 0.50
    ground_y: float = 0.82
    rotation_deg: float = 0.0
    layer: int = 0

    @property
    def end_frame(self) -> int:
        return self.start_frame + max(1, self.hold_frames)


@dataclass(frozen=True)
class ResolvedFrame:
    frame: int
    time_ms: float
    asset_id: str | None
    x: float | None
    ground_y: float | None
    scale: float | None
    rotation_deg: float | None
    layer: int | None


@dataclass
class FilmProject:
    fps: int = DEFAULT_FPS
    background: str | None = None
    background_width: int = 1280
    background_height: int = 720
    grid: PerspectiveGrid = field(default_factory=PerspectiveGrid)
    audio: list[AudioTrack] = field(default_factory=list)
    exposures: list[Exposure] = field(default_factory=list)
    fallback_duration_ms: int = 6000

    @property
    def duration_ms(self) -> int:
        """Audio owns duration when audio exists; otherwise use fallback."""
        if self.audio:
            return max(1, max(track.end_ms for track in self.audio))
        return max(1, int(self.fallback_duration_ms))

    @property
    def frame_count(self) -> int:
        fps = max(1, int(self.fps))
        # Ceiling without importing math keeps the time/frame relation explicit.
        return max(1, (self.duration_ms * fps + 999) // 1000)

    def sorted_exposures(self) -> list[Exposure]:
        return sorted(self.exposures, key=lambda item: (item.start_frame, item.layer))

    def resolve_frame(self, frame: int) -> ResolvedFrame:
        """Resolve a complete actor placement for one film slot.

        If no exposure covers the slot, ``asset_id`` is None.  There is no
        hidden tween, interpolation, or procedural movement.
        """
        frame = int(_clamp(int(frame), 0, self.frame_count - 1))
        active = [
            item
            for item in self.sorted_exposures()
            if item.start_frame <= frame < item.end_frame
        ]
        if not active:
            return ResolvedFrame(
                frame=frame,
                time_ms=frame * 1000.0 / max(1, self.fps),
                asset_id=None,
                x=None,
                ground_y=None,
                scale=None,
                rotation_deg=None,
                layer=None,
            )
        chosen = active[-1]
        return ResolvedFrame(
            frame=frame,
            time_ms=frame * 1000.0 / max(1, self.fps),
            asset_id=chosen.asset_id,
            x=chosen.x,
            ground_y=chosen.ground_y,
            scale=self.grid.scale_at(chosen.ground_y),
            rotation_deg=chosen.rotation_deg,
            layer=chosen.layer,
        )

    def resolve_all(self) -> list[ResolvedFrame]:
        return [self.resolve_frame(frame) for frame in range(self.frame_count)]

    def lay_sequence(
        self,
        asset_ids: Sequence[str],
        *,
        start_ms: int,
        end_ms: int,
        x: float = 0.50,
        ground_y: float = 0.82,
        layer: int = 0,
    ) -> list[Exposure]:
        """Distribute drawings in order across a requested section of film.

        The operation is deterministic, making it suitable for either a human
        button or an AI tool call.  Every drawing gets at least one film frame.
        """
        ids = [str(asset_id) for asset_id in asset_ids if str(asset_id)]
        if not ids:
            return []
        fps = max(1, int(self.fps))
        start = max(0, round(int(start_ms) * fps / 1000))
        end = min(self.frame_count, round(int(end_ms) * fps / 1000))
        if end <= start:
            end = min(self.frame_count, start + 1)
        available = max(1, end - start)
        if len(ids) > available:
            # Multiple source drawings cannot occupy distinct time slots when
            # there are fewer slots than drawings. Keep earliest drawings and
            # make the loss explicit by returning only what could be placed.
            ids = ids[:available]
        placed: list[Exposure] = []
        count = len(ids)
        for index, asset_id in enumerate(ids):
            frame = start + (available * index) // count
            next_frame = start + (available * (index + 1)) // count
            exposure = Exposure(
                asset_id=asset_id,
                start_frame=frame,
                hold_frames=max(1, next_frame - frame),
                x=float(x),
                ground_y=float(ground_y),
                layer=int(layer),
            )
            self.exposures.append(exposure)
            placed.append(exposure)
        return placed

    def to_dict(self) -> dict[str, Any]:
        return {
            "format": "goblin-film-reel-v1",
            "fps": self.fps,
            "duration_ms": self.duration_ms,
            "background": {
                "path": self.background,
                "width": self.background_width,
                "height": self.background_height,
            },
            "grid": asdict(self.grid),
            "audio": [asdict(track) for track in self.audio],
            "exposures": [asdict(item) for item in self.sorted_exposures()],
        }


def project_from_dict(data: Mapping[str, Any]) -> FilmProject:
    background = data.get("background") or {}
    grid = PerspectiveGrid(**dict(data.get("grid") or {}))
    audio = [AudioTrack(**dict(item)) for item in data.get("audio", [])]
    exposures = [Exposure(**dict(item)) for item in data.get("exposures", [])]
    return FilmProject(
        fps=max(1, int(data.get("fps", DEFAULT_FPS))),
        background=background.get("path"),
        background_width=max(1, int(background.get("width", 1280))),
        background_height=max(1, int(background.get("height", 720))),
        grid=grid,
        audio=audio,
        exposures=exposures,
        fallback_duration_ms=max(1, int(data.get("duration_ms", 6000))),
    )


def make_project_spec(project: FilmProject) -> dict[str, Any]:
    """Stable provider-neutral boundary for humans, ChatGPT, Claude, etc."""
    return project.to_dict()


def lay_art_sequence(
    project: FilmProject,
    asset_ids: Iterable[str],
    start_ms: int,
    end_ms: int,
    **placement: Any,
) -> list[Exposure]:
    """Agent-facing convenience call; equivalent to the human sequence button."""
    return project.lay_sequence(
        list(asset_ids), start_ms=start_ms, end_ms=end_ms, **placement
    )
