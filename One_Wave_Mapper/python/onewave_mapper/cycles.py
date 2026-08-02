"""Cycle objects, Point/Path/Field tagging, and modulation detection
(Section 16).

Point/Path/Field is assigned here by simple, inspectable rules (fast
carrier-rate oscillation vs. a whole attack-decay process vs. a multi-
source organization) -- Section 16.3 is explicit that these labels "must
initially be user-editable tags rather than unquestionable automatic
truths," so every Cycle carries the measurements that produced its label
and callers are expected to be able to override it.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field, asdict
from enum import Enum

import numpy as np
from scipy.signal import hilbert, detrend

from onewave_mapper.envelope import hilbert_envelope


class CycleLevel(Enum):
    POINT = "point_rotation"
    PATH = "path_rotation"
    FIELD = "field_rotation"


def new_cycle_id() -> str:
    return f"cycle_{uuid.uuid4().hex[:12]}"


@dataclass
class Cycle:
    cycle_id: str
    parent_cycle_id: str | None
    child_cycle_ids: list
    source_channel: int
    start_sample: int
    end_sample: int
    period_samples: float | None
    frequency_hz: float | None
    amplitude: float | None
    phase: float | None
    confidence: float
    detection_method: str
    cycle_level: str
    one_wave_tags: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def modulation_spectrum(signal: np.ndarray, sample_rate: float,
                         feature: str = "envelope") -> dict:
    """Spectrum of a slow-varying feature, kept separate from the audio-rate
    carrier spectrum (Section 16.1). feature: "envelope", "instantaneous_frequency",
    or "instantaneous_phase"."""
    if feature == "envelope":
        track = hilbert_envelope(signal)
    elif feature in ("instantaneous_frequency", "instantaneous_phase"):
        analytic = hilbert(signal)
        phase = np.unwrap(np.angle(analytic))
        if feature == "instantaneous_phase":
            track = phase
        else:
            track = np.concatenate([[0.0], np.diff(phase) / (2 * np.pi) * sample_rate])
    else:
        raise ValueError(f"unknown modulation feature: {feature}")

    if feature == "instantaneous_phase":
        # a linear trend here is the carrier frequency itself, not a
        # macro-scale artifact -- only remove the mean, not the slope.
        track = track - np.mean(track)
    else:
        # detrend (not just de-mean) so a decaying/rising note envelope's
        # own macro-scale slope doesn't masquerade as a very-low-frequency
        # modulation component when hunting for vibrato/tremolo/beating.
        track = detrend(track, type="linear")

    n = len(track)
    spectrum = np.abs(np.fft.rfft(track * np.hanning(n)))
    freqs = np.fft.rfftfreq(n, d=1.0 / sample_rate)
    return {"freqs_hz": freqs, "magnitude": spectrum, "feature": feature}


def detect_point_cycles(signal: np.ndarray, sample_rate: float, source_channel: int = 1,
                         max_cycles: int | None = None) -> list[Cycle]:
    """One Cycle per waveform period, from consecutive rising zero crossings
    (Section 16.3 Point Rotation: "individual waveform cycle")."""
    centered = signal - np.mean(signal)
    signs = np.signbit(centered)
    rising = np.where((~signs[1:]) & signs[:-1])[0] + 1
    # linear-interpolated sub-sample crossing position, consistent with trigger.py
    crossings = []
    for i in rising:
        prev, curr = centered[i - 1], centered[i]
        frac = -prev / (curr - prev) if curr != prev else 0.0
        crossings.append(i - 1 + frac)

    cycles = []
    pairs = list(zip(crossings[:-1], crossings[1:]))
    if max_cycles is not None:
        pairs = pairs[:max_cycles]

    for start, end in pairs:
        period_samples = end - start
        if period_samples <= 0:
            continue
        start_i, end_i = int(round(start)), int(round(end))
        segment = centered[start_i:max(end_i, start_i + 1)]
        amplitude = float(np.max(np.abs(segment))) if segment.size else 0.0

        cycles.append(Cycle(
            cycle_id=new_cycle_id(),
            parent_cycle_id=None,
            child_cycle_ids=[],
            source_channel=source_channel,
            start_sample=start_i,
            end_sample=end_i,
            period_samples=float(period_samples),
            frequency_hz=float(sample_rate / period_samples),
            amplitude=amplitude,
            phase=0.0,
            confidence=1.0,
            detection_method="zero_crossing_period",
            cycle_level=CycleLevel.POINT.value,
        ))

    return cycles


def detect_modulation_cycle(signal: np.ndarray, sample_rate: float, source_channel: int = 1,
                             min_mod_hz: float = 0.5, max_mod_hz: float = 20.0,
                             min_confidence: float = 0.05) -> Cycle | None:
    """A single slower repeating cycle in the envelope -- vibrato, tremolo,
    or beating (Section 16.3 Path Rotation: "beat envelope developing
    through time")."""
    if len(signal) < 8:
        return None

    result = modulation_spectrum(signal, sample_rate, feature="envelope")
    freqs, magnitude = result["freqs_hz"], result["magnitude"]
    mask = (freqs >= min_mod_hz) & (freqs <= max_mod_hz)
    if not np.any(mask):
        return None

    masked_magnitude = magnitude[mask]
    masked_freqs = freqs[mask]
    peak_index = int(np.argmax(masked_magnitude))
    mod_freq = float(masked_freqs[peak_index])

    total_energy = float(np.sum(masked_magnitude))
    confidence = float(masked_magnitude[peak_index] / total_energy) if total_energy > 1e-12 else 0.0
    if confidence < min_confidence:
        return None

    envelope = hilbert_envelope(signal)
    amplitude = float(np.std(envelope))

    return Cycle(
        cycle_id=new_cycle_id(),
        parent_cycle_id=None,
        child_cycle_ids=[],
        source_channel=source_channel,
        start_sample=0,
        end_sample=len(signal),
        period_samples=float(sample_rate / mod_freq) if mod_freq > 0 else None,
        frequency_hz=mod_freq,
        amplitude=amplitude,
        phase=None,
        confidence=confidence,
        detection_method="envelope_modulation_spectrum_peak",
        cycle_level=CycleLevel.PATH.value,
    )


def build_note_cycle_tree(signal: np.ndarray, sample_rate: float, source_channel: int = 1,
                           max_point_cycles: int = 32, min_mod_hz: float = 0.5,
                           max_mod_hz: float = 20.0) -> dict:
    """A whole note as a Path-level Cycle (Section 16.3: "attack into sustain
    and decay"), with the first max_point_cycles waveform periods and any
    detected modulation as children."""
    path_cycle = Cycle(
        cycle_id=new_cycle_id(),
        parent_cycle_id=None,
        child_cycle_ids=[],
        source_channel=source_channel,
        start_sample=0,
        end_sample=len(signal),
        period_samples=None,
        frequency_hz=None,
        amplitude=float(np.max(np.abs(signal))) if len(signal) else 0.0,
        phase=None,
        confidence=1.0,
        detection_method="attack_sustain_decay_span",
        cycle_level=CycleLevel.PATH.value,
    )

    point_cycles = detect_point_cycles(signal, sample_rate, source_channel, max_cycles=max_point_cycles)
    for c in point_cycles:
        c.parent_cycle_id = path_cycle.cycle_id
    path_cycle.child_cycle_ids.extend(c.cycle_id for c in point_cycles)

    modulation_cycle = detect_modulation_cycle(signal, sample_rate, source_channel,
                                                min_mod_hz, max_mod_hz)
    if modulation_cycle is not None:
        modulation_cycle.parent_cycle_id = path_cycle.cycle_id
        path_cycle.child_cycle_ids.append(modulation_cycle.cycle_id)

    return {"path_cycle": path_cycle, "point_cycles": point_cycles, "modulation_cycle": modulation_cycle}


def build_field_cycle(child_cycles: list[Cycle], source_channel: int = 1,
                       detection_method: str = "multi_source_grouping") -> Cycle:
    """A containing organization made of multiple cycles (Section 16.3 Field
    Rotation), e.g. grouping several notes' Path cycles into one chord field."""
    if not child_cycles:
        raise ValueError("build_field_cycle requires at least one child cycle")

    field_cycle = Cycle(
        cycle_id=new_cycle_id(),
        parent_cycle_id=None,
        child_cycle_ids=[c.cycle_id for c in child_cycles],
        source_channel=source_channel,
        start_sample=min(c.start_sample for c in child_cycles),
        end_sample=max(c.end_sample for c in child_cycles),
        period_samples=None,
        frequency_hz=None,
        amplitude=float(np.mean([c.amplitude for c in child_cycles if c.amplitude is not None]))
        if any(c.amplitude is not None for c in child_cycles) else None,
        phase=None,
        confidence=float(np.mean([c.confidence for c in child_cycles])),
        detection_method=detection_method,
        cycle_level=CycleLevel.FIELD.value,
    )
    for c in child_cycles:
        c.parent_cycle_id = field_cycle.cycle_id
    return field_cycle
