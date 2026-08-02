"""Synthetic test signals for validating the DSP engine (Section 24.2)."""

from __future__ import annotations

import numpy as np


def time_vector(duration_seconds: float, sample_rate: float) -> np.ndarray:
    n = int(round(duration_seconds * sample_rate))
    return np.arange(n) / sample_rate


def sine(frequency_hz: float, duration_seconds: float, sample_rate: float,
         amplitude: float = 1.0, phase_rad: float = 0.0) -> np.ndarray:
    t = time_vector(duration_seconds, sample_rate)
    return amplitude * np.sin(2 * np.pi * frequency_hz * t + phase_rad)


def square(frequency_hz: float, duration_seconds: float, sample_rate: float,
           amplitude: float = 1.0, duty: float = 0.5) -> np.ndarray:
    t = time_vector(duration_seconds, sample_rate)
    phase = np.mod(frequency_hz * t, 1.0)
    return amplitude * np.where(phase < duty, 1.0, -1.0)


def triangle(frequency_hz: float, duration_seconds: float, sample_rate: float,
             amplitude: float = 1.0) -> np.ndarray:
    t = time_vector(duration_seconds, sample_rate)
    phase = np.mod(frequency_hz * t, 1.0)
    return amplitude * (4 * np.abs(phase - 0.5) - 1.0)


def sawtooth(frequency_hz: float, duration_seconds: float, sample_rate: float,
             amplitude: float = 1.0) -> np.ndarray:
    t = time_vector(duration_seconds, sample_rate)
    phase = np.mod(frequency_hz * t, 1.0)
    return amplitude * (2 * phase - 1.0)


def white_noise(duration_seconds: float, sample_rate: float, amplitude: float = 1.0,
                 seed: int | None = None) -> np.ndarray:
    rng = np.random.default_rng(seed)
    n = int(round(duration_seconds * sample_rate))
    return amplitude * rng.uniform(-1.0, 1.0, size=n)


def pink_noise(duration_seconds: float, sample_rate: float, amplitude: float = 1.0,
               seed: int | None = None) -> np.ndarray:
    """Voss-McCartney approximation of 1/f pink noise."""
    rng = np.random.default_rng(seed)
    n = int(round(duration_seconds * sample_rate))
    n_rows = 16
    array = rng.uniform(-1, 1, size=(n_rows, n))
    weights = 1.0 / (2.0 ** np.arange(n_rows))
    for row in range(1, n_rows):
        step = 2 ** row
        array[row, ::step] = rng.uniform(-1, 1, size=array[row, ::step].shape)
        for i in range(1, step):
            if step + i <= n:
                array[row, i::step] = array[row, 0:1]
    pink = (weights[:, None] * array).sum(axis=0)
    pink /= np.max(np.abs(pink)) + 1e-12
    return amplitude * pink


def two_tone(freq1_hz: float, freq2_hz: float, duration_seconds: float, sample_rate: float,
             amplitude: float = 0.5) -> np.ndarray:
    return sine(freq1_hz, duration_seconds, sample_rate, amplitude) + \
        sine(freq2_hz, duration_seconds, sample_rate, amplitude)


def harmonic_series(fundamental_hz: float, duration_seconds: float, sample_rate: float,
                     harmonic_amplitudes: list[float] | None = None,
                     amplitude: float = 1.0) -> np.ndarray:
    if harmonic_amplitudes is None:
        harmonic_amplitudes = [1.0, 0.5, 0.33, 0.25, 0.2, 0.16, 0.14, 0.12]
    t = time_vector(duration_seconds, sample_rate)
    out = np.zeros_like(t)
    for n, a in enumerate(harmonic_amplitudes, start=1):
        out += a * np.sin(2 * np.pi * fundamental_hz * n * t)
    out *= amplitude / (np.max(np.abs(out)) + 1e-12)
    return out


def frequency_sweep(start_hz: float, end_hz: float, duration_seconds: float, sample_rate: float,
                     amplitude: float = 1.0) -> np.ndarray:
    t = time_vector(duration_seconds, sample_rate)
    k = (end_hz - start_hz) / duration_seconds
    phase = 2 * np.pi * (start_hz * t + 0.5 * k * t ** 2)
    return amplitude * np.sin(phase)


def exponential_decay(frequency_hz: float, duration_seconds: float, sample_rate: float,
                       decay_tau_seconds: float, amplitude: float = 1.0) -> np.ndarray:
    t = time_vector(duration_seconds, sample_rate)
    envelope = np.exp(-t / decay_tau_seconds)
    return amplitude * envelope * np.sin(2 * np.pi * frequency_hz * t)


def amplitude_modulated(carrier_hz: float, mod_hz: float, duration_seconds: float,
                         sample_rate: float, mod_depth: float = 0.5,
                         amplitude: float = 1.0) -> np.ndarray:
    t = time_vector(duration_seconds, sample_rate)
    carrier = np.sin(2 * np.pi * carrier_hz * t)
    envelope = 1.0 + mod_depth * np.sin(2 * np.pi * mod_hz * t)
    return amplitude * envelope * carrier


def frequency_modulated(carrier_hz: float, mod_hz: float, duration_seconds: float,
                         sample_rate: float, mod_index: float = 2.0,
                         amplitude: float = 1.0) -> np.ndarray:
    t = time_vector(duration_seconds, sample_rate)
    phase = 2 * np.pi * carrier_hz * t + mod_index * np.sin(2 * np.pi * mod_hz * t)
    return amplitude * np.sin(phase)


def guitar_note(fundamental_hz: float, duration_seconds: float, sample_rate: float,
                 decay_tau_seconds: float = 1.2, amplitude: float = 0.8,
                 vibrato_hz: float = 5.5, vibrato_depth_cents: float = 8.0,
                 n_harmonics: int = 12) -> np.ndarray:
    """A plausible synthetic guitar-note test signal: decaying harmonic series with vibrato."""
    t = time_vector(duration_seconds, sample_rate)
    vibrato_ratio = 2 ** ((vibrato_depth_cents / 100.0) * np.sin(2 * np.pi * vibrato_hz * t) / 12.0)
    inst_fundamental = fundamental_hz * vibrato_ratio
    phase = 2 * np.pi * np.cumsum(inst_fundamental) / sample_rate

    out = np.zeros_like(t)
    for n in range(1, n_harmonics + 1):
        harmonic_amp = 1.0 / n
        harmonic_decay = np.exp(-t / (decay_tau_seconds / (1.0 + 0.15 * (n - 1))))
        out += harmonic_amp * harmonic_decay * np.sin(n * phase)

    attack_samples = max(1, int(0.003 * sample_rate))
    attack_env = np.ones_like(t)
    attack_env[:attack_samples] = np.linspace(0, 1, attack_samples)
    out *= attack_env

    out *= amplitude / (np.max(np.abs(out)) + 1e-12)
    return out


def with_dc_offset(signal: np.ndarray, offset: float) -> np.ndarray:
    return signal + offset


def with_phase_offset_copy(signal: np.ndarray, frequency_hz: float, sample_rate: float,
                            phase_offset_deg: float) -> np.ndarray:
    """Reconstruct a phase-shifted copy of a pure-tone signal (for phase-difference tests)."""
    n = len(signal)
    t = np.arange(n) / sample_rate
    phase_offset_rad = np.deg2rad(phase_offset_deg)
    return np.sin(2 * np.pi * frequency_hz * t + phase_offset_rad)


def with_delay(signal: np.ndarray, delay_samples: int) -> np.ndarray:
    if delay_samples <= 0:
        return signal.copy()
    return np.concatenate([np.zeros(delay_samples), signal[:-delay_samples] if delay_samples < len(signal) else np.zeros(0)])


def clipped(signal: np.ndarray, ceiling: float = 1.0) -> np.ndarray:
    return np.clip(signal, -ceiling, ceiling)
