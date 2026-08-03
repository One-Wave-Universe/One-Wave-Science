"""Predict how N already-recorded isolated notes will interact, without
needing a real combined recording.

This is the forward-looking counterpart to
interference.compare_isolated_vs_combined_n, which judges a *real*
combined recording against a prediction. Everything here -- beat
frequency, shared harmonic collisions, roughness, interference scores --
is derived purely from linear superposition of the isolated signals, so
it's exactly as accurate as that assumption: it will not predict
amplifier/pickup nonlinearity, string coupling, or room effects, which is
precisely the gap compare_isolated_vs_combined_n's residual is for
measuring once a real recording exists (Section 14.4).
"""

from __future__ import annotations

from dataclasses import dataclass, asdict

import numpy as np

from onewave_mapper import pitch as pitch_module, metering, chord as chord_module
from onewave_mapper import interference as interference_module


@dataclass
class PairwisePrediction:
    indices: list
    fundamental_i_hz: float | None
    fundamental_j_hz: float | None
    beat_frequency_hz: float | None
    cents_interval: float | None
    shared_harmonics: list
    roughness: float | None
    interference_scores: dict

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class PredictedInteraction:
    n_sources: int
    fundamentals_hz: list
    predicted_peak_dbfs: float
    predicted_rms_dbfs: float
    predicted_clipping_count: int
    pairwise: list

    def to_dict(self) -> dict:
        return asdict(self)


def predict_interaction(signals: list[np.ndarray], sample_rate: float, fmin: float = 60.0,
                         fmax: float = 1500.0) -> tuple[PredictedInteraction, np.ndarray]:
    """Predict the linear-sum combination of N isolated signals and forecast
    every pairwise interaction among them. Returns (result, predicted_sum)."""
    if len(signals) < 1:
        raise ValueError("predict_interaction requires at least one signal")

    length = min(len(s) for s in signals)
    trimmed = [s[:length] for s in signals]
    predicted_sum = np.sum(trimmed, axis=0)

    fundamentals: list[float | None] = []
    for s in trimmed:
        pitch_result = pitch_module.detect_pitch(s, sample_rate, fmin=fmin, fmax=fmax)
        fundamentals.append(pitch_result.frequency_hz)

    pairwise = []
    for i in range(len(trimmed)):
        for j in range(i + 1, len(trimmed)):
            f_i, f_j = fundamentals[i], fundamentals[j]
            scores = interference_module.interference_scores(trimmed[i], trimmed[j], sample_rate)

            beat_frequency_hz = chord_module.beat_frequency(f_i, f_j) if f_i and f_j else None
            cents_interval = chord_module.cents_interval(f_i, f_j) if f_i and f_j else None
            shared = chord_module.shared_harmonics(f_i, f_j) if f_i and f_j else []
            roughness = chord_module.harmonic_series_roughness(f_i, f_j) if f_i and f_j else None

            pairwise.append(PairwisePrediction(
                indices=[i, j],
                fundamental_i_hz=f_i,
                fundamental_j_hz=f_j,
                beat_frequency_hz=beat_frequency_hz,
                cents_interval=cents_interval,
                shared_harmonics=shared,
                roughness=roughness,
                interference_scores=scores.to_dict(),
            ).to_dict())

    m = metering.measure(predicted_sum, sample_rate)
    result = PredictedInteraction(
        n_sources=len(signals),
        fundamentals_hz=fundamentals,
        predicted_peak_dbfs=float(20 * np.log10(max(m.peak, 1e-12))),
        predicted_rms_dbfs=float(20 * np.log10(max(m.rms, 1e-12))),
        predicted_clipping_count=m.clipping_count,
        pairwise=pairwise,
    )
    return result, predicted_sum
