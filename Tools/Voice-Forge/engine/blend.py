"""Blend two or more reference voices by trait, not by raw waveform mix.

Each reference is decomposed into an excitation ("residual") and an LPC
spectral envelope (engine.dsp.whiten). The envelopes are combined with a
weighted log-magnitude average (the standard way to interpolate spectral
envelopes) and the excitations are combined with a plain weighted sum
once all references share the same timing. This keeps formant character
and excitation ("buzz"/breathiness) blending independent of each other,
matching the "blend by trait" requirement instead of a literal audio
crossfade.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from . import dsp

EPS = 1e-8


@dataclass
class BlendInput:
    id: str
    y: np.ndarray
    amount: float


@dataclass
class BlendResult:
    residual: np.ndarray
    env_mag: np.ndarray
    freqs: np.ndarray
    sr: int
    n_fft: int
    hop: int
    timing_len: int
    weights: dict


def blend_sources(
    sources: list[BlendInput],
    sr: int,
    timing_id: str | None = None,
    n_fft: int = 1024,
    hop: int = 256,
    order: int | None = None,
) -> BlendResult:
    if not sources:
        raise ValueError("blend_sources requires at least one source")

    timing_source = None
    if timing_id is not None:
        timing_source = next((s for s in sources if s.id == timing_id), None)
    if timing_source is None:
        timing_source = max(sources, key=lambda s: s.amount)
    timing_len = len(timing_source.y)

    amounts = np.array([max(0.0, s.amount) for s in sources], dtype=np.float64)
    if amounts.sum() <= EPS:
        amounts = np.ones_like(amounts)
    weights = amounts / amounts.sum()

    residuals = []
    envs = []
    freqs = None
    for s in sources:
        y_aligned = dsp.time_stretch_to_length(s.y, timing_len)
        residual, env_mag, freqs = dsp.whiten(y_aligned, sr, n_fft=n_fft, hop=hop, order=order)
        residuals.append(residual)
        envs.append(env_mag)

    n_frames_min = min(e.shape[1] for e in envs)
    envs = [dsp.resize_env_time(e, n_frames_min) for e in envs]
    len_min = min(len(r) for r in residuals)
    residuals = [r[:len_min] for r in residuals]

    log_env_blend = np.zeros_like(envs[0])
    for w, e in zip(weights, envs):
        log_env_blend += w * np.log(e + EPS)
    env_blend = np.exp(log_env_blend)

    residual_blend = np.zeros(len_min, dtype=np.float64)
    for w, r in zip(weights, residuals):
        residual_blend += w * r
    residual_blend = residual_blend.astype(np.float32)

    weight_map = {s.id: float(w) for s, w in zip(sources, weights)}
    return BlendResult(
        residual=residual_blend,
        env_mag=env_blend,
        freqs=freqs,
        sr=sr,
        n_fft=n_fft,
        hop=hop,
        timing_len=len_min,
        weights=weight_map,
    )
