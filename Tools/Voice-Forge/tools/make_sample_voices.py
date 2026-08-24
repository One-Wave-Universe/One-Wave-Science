"""Synthesizes two original, non-human demo reference voices so Voice
Forge can be exercised without needing real recordings. These are plain
additive-synthesis "characters" (different pitch, formants, breathiness)
built for this project -- exactly the "original generated base voices"
case the README allows as a Voice Forge input.

Re-run with: python tools/make_sample_voices.py
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from engine import dsp, io_utils  # noqa: E402

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "sample")


def synth_voice(sr, duration, f0, formants, breath=0.03, n_syllables=4, seed=0):
    rng = np.random.default_rng(seed)
    n = int(sr * duration)
    t = np.arange(n) / sr

    env = np.zeros(n)
    for i in range(n_syllables):
        center = (i + 0.5) / n_syllables * duration
        width = duration / n_syllables * 0.35
        env += np.exp(-0.5 * ((t - center) / width) ** 2)
    env = np.clip(env / env.max(), 0.0, 1.0)

    f0_t = f0 * (1.0 + 0.015 * np.sin(2 * np.pi * 3.2 * t))
    phase = 2 * np.pi * np.cumsum(f0_t) / sr

    n_harm = min(40, int(sr / 2 / f0))
    exc = np.zeros(n)
    for k in range(1, n_harm + 1):
        exc += (1.0 / k) * np.sin(k * phase)
    exc = exc / (np.max(np.abs(exc)) + 1e-9)

    y = exc * env
    for freq, gain_db, q in formants:
        y = dsp.peaking_eq(y, sr, freq=freq, gain_db=gain_db, q=q)

    y = y + breath * rng.standard_normal(n) * env
    y = y / (np.max(np.abs(y)) + 1e-9) * 0.9
    return y.astype(np.float32)


def main():
    sr = 22050
    os.makedirs(OUT_DIR, exist_ok=True)

    voice_a = synth_voice(
        sr, duration=1.8, f0=105.0,
        formants=[(650, 14, 3.5), (1100, 12, 4.0), (2600, 8, 3.0)],
        breath=0.02, seed=1,
    )
    voice_b = synth_voice(
        sr, duration=1.6, f0=190.0,
        formants=[(850, 14, 3.5), (1700, 12, 4.0), (3100, 8, 3.0)],
        breath=0.035, seed=2,
    )

    path_a = os.path.join(OUT_DIR, "sample_voice_a.wav")
    path_b = os.path.join(OUT_DIR, "sample_voice_b.wav")
    io_utils.save_wav(path_a, voice_a, sr)
    io_utils.save_wav(path_b, voice_b, sr)
    print(f"Wrote sample reference voices to {os.path.abspath(OUT_DIR)}")


if __name__ == "__main__":
    main()
