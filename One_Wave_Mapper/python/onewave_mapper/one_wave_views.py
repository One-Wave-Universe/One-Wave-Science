"""One-Wave interpretive views: Inward, Outward, Across, Over (Section 17).

These are experimental, configurable classifications layered on top of
objective measurement, never a substitute for it (Section 2.3) -- every
OneWaveTag below carries the measurements that produced it, in the same
shape as the spec's own worked example:

    Tag: Over
    Reason:
    - 5.8 Hz repeating modulation
    - confidence 0.91
    - detected in fundamental amplitude envelope
    - active from sample 144000 to 288000

The default rule set implements one concrete, testable indicator per view
(Section 17.1-17.4 list several each) rather than every listed indicator;
callers can add, remove, or replace rules via the `rules` parameter,
matching Section 17's "configurable rule sets" requirement.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Callable

import numpy as np

from onewave_mapper.envelope import hilbert_envelope
from onewave_mapper import cycles as cycles_module


@dataclass
class OneWaveTag:
    tag: str  # "Inward" | "Outward" | "Across" | "Over"
    reasons: list
    confidence: float
    start_sample: int
    end_sample: int
    evidence: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)

    def __str__(self) -> str:
        lines = [f"Tag: {self.tag}", "Reason:"]
        lines.extend(f"- {r}" for r in self.reasons)
        return "\n".join(lines)


OneWaveRule = Callable[[np.ndarray, float, int, int], "OneWaveTag | None"]


def _envelope_db_slope(signal: np.ndarray, sample_rate: float) -> float | None:
    envelope = hilbert_envelope(signal)
    envelope_db = 20 * np.log10(np.maximum(envelope, 1e-12))
    if len(envelope_db) < 4:
        return None
    t = np.arange(len(envelope_db)) / sample_rate
    slope, _ = np.polyfit(t, envelope_db, 1)
    return float(slope)


def inward_rule(signal: np.ndarray, sample_rate: float, start_sample: int, end_sample: int,
                 threshold_db_per_second: float = 6.0) -> OneWaveTag | None:
    """Falling envelope / decay (Section 17.1)."""
    slope = _envelope_db_slope(signal, sample_rate)
    if slope is None or slope > -threshold_db_per_second:
        return None
    return OneWaveTag(
        tag="Inward",
        reasons=[
            f"envelope falling at {slope:.2f} dB/s",
            f"active from sample {start_sample} to {end_sample}",
        ],
        confidence=float(np.clip(-slope / (threshold_db_per_second * 4), 0.0, 1.0)),
        start_sample=start_sample,
        end_sample=end_sample,
        evidence={"envelope_slope_db_per_second": slope, "indicator": "falling_envelope"},
    )


def outward_rule(signal: np.ndarray, sample_rate: float, start_sample: int, end_sample: int,
                  threshold_db_per_second: float = 6.0) -> OneWaveTag | None:
    """Rising envelope / attack / energy emission (Section 17.2)."""
    slope = _envelope_db_slope(signal, sample_rate)
    if slope is None or slope < threshold_db_per_second:
        return None
    return OneWaveTag(
        tag="Outward",
        reasons=[
            f"envelope rising at {slope:.2f} dB/s",
            f"active from sample {start_sample} to {end_sample}",
        ],
        confidence=float(np.clip(slope / (threshold_db_per_second * 4), 0.0, 1.0)),
        start_sample=start_sample,
        end_sample=end_sample,
        evidence={"envelope_slope_db_per_second": slope, "indicator": "rising_envelope"},
    )


def across_rule(signal: np.ndarray, sample_rate: float, start_sample: int, end_sample: int,
                 min_crossings: int = 1) -> OneWaveTag | None:
    """Zero crossing / transient crossing (Section 17.3)."""
    centered = signal - np.mean(signal)
    signs = np.signbit(centered)
    crossings = np.where(np.diff(signs))[0]
    if len(crossings) < min_crossings:
        return None
    representative = crossings[: min(5, len(crossings))] + start_sample
    return OneWaveTag(
        tag="Across",
        reasons=[
            f"{len(crossings)} zero crossing(s) detected",
            f"first crossings at samples {list(map(int, representative))}",
            f"active from sample {start_sample} to {end_sample}",
        ],
        confidence=float(np.clip(len(crossings) / 10.0, 0.0, 1.0)),
        start_sample=start_sample,
        end_sample=end_sample,
        evidence={"zero_crossing_count": int(len(crossings)),
                  "zero_crossing_samples": [int(c) for c in representative]},
    )


def over_rule(signal: np.ndarray, sample_rate: float, start_sample: int, end_sample: int,
              min_mod_hz: float = 0.5, max_mod_hz: float = 20.0,
              min_confidence: float = 0.22) -> OneWaveTag | None:
    """Recurrence / repeating modulation structure (Section 17.4)."""
    modulation_cycle = cycles_module.detect_modulation_cycle(
        signal, sample_rate, min_mod_hz=min_mod_hz, max_mod_hz=max_mod_hz,
        min_confidence=min_confidence,
    )
    if modulation_cycle is None:
        return None
    return OneWaveTag(
        tag="Over",
        reasons=[
            f"{modulation_cycle.frequency_hz:.1f} Hz repeating modulation",
            f"confidence {modulation_cycle.confidence:.2f}",
            "detected in fundamental amplitude envelope",
            f"active from sample {start_sample} to {end_sample}",
        ],
        confidence=modulation_cycle.confidence,
        start_sample=start_sample,
        end_sample=end_sample,
        evidence={"modulation_frequency_hz": modulation_cycle.frequency_hz,
                  "cycle_id": modulation_cycle.cycle_id},
    )


DEFAULT_RULES: list[OneWaveRule] = [inward_rule, outward_rule, across_rule, over_rule]


def classify_window(signal: np.ndarray, sample_rate: float, start_sample: int = 0,
                     end_sample: int | None = None, rules: list[OneWaveRule] | None = None) -> list[OneWaveTag]:
    """Apply each rule to signal[start_sample:end_sample] and collect the
    tags that fire. Views are not mutually exclusive -- e.g. a decaying
    note can be both Inward (falling envelope) and Over (vibrato) at once."""
    end_sample = end_sample if end_sample is not None else len(signal)
    segment = signal[start_sample:end_sample]
    rules = rules if rules is not None else DEFAULT_RULES

    tags = []
    for rule in rules:
        tag = rule(segment, sample_rate, start_sample, end_sample)
        if tag is not None:
            tags.append(tag)
    return tags
