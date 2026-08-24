import numpy as np

from tests.helpers import spectral_centroid
from engine import blend, dsp
from tools.make_sample_voices import synth_voice

SR = 16000


def _voices():
    voice_a = synth_voice(SR, duration=0.8, f0=110.0, formants=[(650, 12, 3.5), (1100, 10, 4.0)], breath=0.0, seed=10)
    voice_b = synth_voice(SR, duration=0.7, f0=210.0, formants=[(900, 12, 3.5), (2200, 10, 4.0)], breath=0.0, seed=11)
    return voice_a, voice_b


def test_blend_weights_normalize():
    voice_a, voice_b = _voices()
    inputs = [blend.BlendInput("A", voice_a, 3.0), blend.BlendInput("B", voice_b, 1.0)]
    result = blend.blend_sources(inputs, SR, timing_id="A")
    assert abs(result.weights["A"] - 0.75) < 1e-6
    assert abs(result.weights["B"] - 0.25) < 1e-6


def test_blend_full_weight_matches_single_source_timbre():
    voice_a, voice_b = _voices()
    inputs = [blend.BlendInput("A", voice_a, 1.0), blend.BlendInput("B", voice_b, 0.0)]
    result = blend.blend_sources(inputs, SR, timing_id="A")
    y_out = dsp.resynthesize(result.residual, result.env_mag, SR, length=len(result.residual))

    centroid_out = spectral_centroid(y_out, SR)
    centroid_a = spectral_centroid(voice_a, SR)
    centroid_b = spectral_centroid(voice_b, SR)

    assert abs(centroid_out - centroid_a) < abs(centroid_out - centroid_b)


def test_blend_midpoint_is_between_sources_spectrally():
    voice_a, voice_b = _voices()
    inputs = [blend.BlendInput("A", voice_a, 0.5), blend.BlendInput("B", voice_b, 0.5)]
    result = blend.blend_sources(inputs, SR, timing_id="A")
    y_mid = dsp.resynthesize(result.residual, result.env_mag, SR, length=len(result.residual))

    centroid_mid = spectral_centroid(y_mid, SR)
    centroid_a = spectral_centroid(voice_a, SR)
    centroid_b = spectral_centroid(voice_b, SR)

    lo, hi = sorted([centroid_a, centroid_b])
    assert lo - 200 <= centroid_mid <= hi + 200


def test_blend_aligns_to_timing_source_length():
    voice_a, voice_b = _voices()
    inputs = [blend.BlendInput("A", voice_a, 0.5), blend.BlendInput("B", voice_b, 0.5)]
    result = blend.blend_sources(inputs, SR, timing_id="A")
    assert abs(len(result.residual) - len(voice_a)) <= 512
