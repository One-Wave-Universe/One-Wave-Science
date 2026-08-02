"""Session metadata, directory structure, and note-event export (Section 7.2/7.3, 21.3)."""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path

from onewave_mapper import __version__


@dataclass
class Session:
    session_id: str
    created_at: str
    application_version: str
    sample_rate: int
    bit_depth: str
    channel_count: int
    buffer_size: int
    instrument: str | None = None
    guitar_string: int | None = None
    fret: int | None = None
    expected_note: str | None = None
    calibration_profile: str | None = None
    annotations: str = ""

    @classmethod
    def create(cls, sample_rate: int, bit_depth: str, channel_count: int,
               buffer_size: int, **metadata) -> "Session":
        return cls(
            session_id=f"session_{uuid.uuid4().hex[:12]}",
            created_at=datetime.now(timezone.utc).isoformat(),
            application_version=__version__,
            sample_rate=sample_rate,
            bit_depth=bit_depth,
            channel_count=channel_count,
            buffer_size=buffer_size,
            **metadata,
        )

    def root_dir(self, sessions_root: str | Path) -> Path:
        return Path(sessions_root) / self.session_id

    def make_directory_structure(self, sessions_root: str | Path) -> Path:
        root = self.root_dir(sessions_root)
        for sub in ("audio", "analysis/pitch_tracks", "analysis/harmonic_tracks",
                    "analysis/envelopes", "analysis/resonance_events",
                    "analysis/interference_events", "thumbnails", "exports", "logs"):
            (root / sub).mkdir(parents=True, exist_ok=True)
        return root

    def save(self, sessions_root: str | Path) -> Path:
        root = self.make_directory_structure(sessions_root)
        path = root / "session.json"
        with open(path, "w") as f:
            json.dump(asdict(self), f, indent=2)
        return path

    @classmethod
    def load(cls, session_json_path: str | Path) -> "Session":
        with open(session_json_path) as f:
            data = json.load(f)
        return cls(**data)


@dataclass
class NoteEvent:
    event_id: str
    source_channel: int
    start_sample: int
    end_sample: int
    sample_rate: int
    expected_note: str | None = None
    measured_frequency_hz: float | None = None
    cents_offset: float | None = None
    pitch_confidence: float | None = None
    attack_time_ms: float | None = None
    decay_20db_seconds: float | None = None
    rms_dbfs: float | None = None
    peak_dbfs: float | None = None
    harmonics: list = field(default_factory=list)
    resonances: list = field(default_factory=list)
    cycles: list = field(default_factory=list)
    one_wave_tags: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    def save(self, path: str | Path) -> None:
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, path: str | Path) -> "NoteEvent":
        with open(path) as f:
            data = json.load(f)
        return cls(**data)
