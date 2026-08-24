"""Character voice recipe: the reusable, non-destructive description of a
blended voice. A recipe never stores rendered audio -- only trait weights,
processing settings, and references to the original source files -- so a
render can always be repeated (or re-tuned) from the originals.
"""
from __future__ import annotations

import copy
import dataclasses
import datetime
import json
import os
from dataclasses import dataclass, field

ENGINE_VERSION = "1.0"


@dataclass
class SourceEntry:
    id: str
    path: str
    amount: float = 1.0
    mute: bool = False
    solo: bool = False


@dataclass
class Traits:
    pitch_semitones: float = 0.0
    formant_ratio: float = 1.0
    body_db: float = 0.0
    brightness_db: float = 0.0
    breathiness: float = 0.0
    rasp: float = 0.0
    nasality_db: float = 0.0
    articulation: float = 0.0
    time_stretch_ratio: float = 1.0
    micro_pitch_instability: float = 0.0
    layer_doubler_amount: float = 0.0
    stereo_width: float = 1.0
    dry_wet: float = 1.0
    output_gain_db: float = 0.0


@dataclass
class CompressorSettings:
    threshold_db: float = -18.0
    ratio: float = 3.0
    attack_ms: float = 5.0
    release_ms: float = 80.0
    makeup_db: float = 0.0


@dataclass
class DelaySettings:
    enabled: bool = False
    time_ms: float = 220.0
    feedback: float = 0.3
    mix: float = 0.0


@dataclass
class ReverbSettings:
    enabled: bool = False
    kind: str = "plate"
    size: float = 0.5
    mix: float = 0.0


@dataclass
class Finishing:
    high_cut_hz: float = 16000.0
    low_cut_hz: float = 60.0
    presence_db: float = 0.0
    deesser_amount: float = 0.0
    saturation_drive: float = 0.0
    compressor: CompressorSettings = field(default_factory=CompressorSettings)
    delay: DelaySettings = field(default_factory=DelaySettings)
    reverb: ReverbSettings = field(default_factory=ReverbSettings)


@dataclass
class Recipe:
    name: str = "Untitled Voice"
    sample_rate: int = 44100
    sources: list = field(default_factory=list)  # list[SourceEntry]
    timing_source_id: str | None = None
    traits: Traits = field(default_factory=Traits)
    finishing: Finishing = field(default_factory=Finishing)
    locked_traits: list = field(default_factory=list)
    created: str = field(default_factory=lambda: datetime.datetime.utcnow().isoformat() + "Z")
    engine_version: str = ENGINE_VERSION

    def clone(self) -> "Recipe":
        return copy.deepcopy(self)

    def to_dict(self) -> dict:
        d = dataclasses.asdict(self)
        return d

    @classmethod
    def from_dict(cls, d: dict) -> "Recipe":
        d = copy.deepcopy(d)
        sources = [SourceEntry(**s) for s in d.get("sources", [])]
        traits = Traits(**d.get("traits", {}))
        fin = d.get("finishing", {})
        compressor = CompressorSettings(**fin.get("compressor", {}))
        delay = DelaySettings(**fin.get("delay", {}))
        reverb = ReverbSettings(**fin.get("reverb", {}))
        finishing = Finishing(
            high_cut_hz=fin.get("high_cut_hz", 16000.0),
            low_cut_hz=fin.get("low_cut_hz", 60.0),
            presence_db=fin.get("presence_db", 0.0),
            deesser_amount=fin.get("deesser_amount", 0.0),
            saturation_drive=fin.get("saturation_drive", 0.0),
            compressor=compressor,
            delay=delay,
            reverb=reverb,
        )
        return cls(
            name=d.get("name", "Untitled Voice"),
            sample_rate=d.get("sample_rate", 44100),
            sources=sources,
            timing_source_id=d.get("timing_source_id"),
            traits=traits,
            finishing=finishing,
            locked_traits=d.get("locked_traits", []),
            created=d.get("created", ""),
            engine_version=d.get("engine_version", ENGINE_VERSION),
        )

    def save(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, path: str) -> "Recipe":
        with open(path, "r", encoding="utf-8") as f:
            return cls.from_dict(json.load(f))

    @classmethod
    def default_two_source(cls, path_a: str, path_b: str, name: str = "Untitled Voice") -> "Recipe":
        return cls(
            name=name,
            sources=[
                SourceEntry(id="A", path=path_a, amount=0.5),
                SourceEntry(id="B", path=path_b, amount=0.5),
            ],
            timing_source_id="A",
        )


def resolve_source_path(entry: SourceEntry, base_dir: str | None) -> str:
    if os.path.isabs(entry.path) or base_dir is None:
        return entry.path
    return os.path.normpath(os.path.join(base_dir, entry.path))
