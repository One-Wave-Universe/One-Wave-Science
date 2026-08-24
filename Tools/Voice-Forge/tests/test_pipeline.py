import os

import numpy as np

from engine import io_utils, pipeline
from engine.recipe import Recipe
from tools.make_sample_voices import synth_voice

SR = 16000


def _write_two_voices(tmp_path):
    voice_a = synth_voice(SR, duration=0.9, f0=110.0, formants=[(650, 12, 3.5), (1100, 10, 4.0)], breath=0.02, seed=20)
    voice_b = synth_voice(SR, duration=0.8, f0=200.0, formants=[(900, 12, 3.5), (2200, 10, 4.0)], breath=0.03, seed=21)
    path_a = str(tmp_path / "voice_a.wav")
    path_b = str(tmp_path / "voice_b.wav")
    io_utils.save_wav(path_a, voice_a, SR)
    io_utils.save_wav(path_b, voice_b, SR)
    return path_a, path_b


def test_render_recipe_produces_valid_stereo_audio(tmp_path):
    path_a, path_b = _write_two_voices(tmp_path)
    recipe = Recipe.default_two_source(path_a, path_b, name="Phase 1 Demo")
    recipe.sample_rate = SR
    recipe.traits.pitch_semitones = -1.0
    recipe.traits.formant_ratio = 1.05
    recipe.traits.body_db = 2.0
    recipe.finishing.reverb.enabled = True
    recipe.finishing.reverb.mix = 0.1

    result = pipeline.render_recipe(recipe, base_dir=None, render_stems=True)

    assert result.audio.ndim == 2 and result.audio.shape[1] == 2
    assert result.sr == SR
    assert np.max(np.abs(result.audio)) <= 1.0 + 1e-6
    assert np.max(np.abs(result.audio)) > 1e-3
    assert set(result.stems.keys()) == {"01_blend", "02_character", "03_final"}


def test_render_respects_mute_and_solo(tmp_path):
    path_a, path_b = _write_two_voices(tmp_path)
    recipe = Recipe.default_two_source(path_a, path_b)
    recipe.sample_rate = SR
    recipe.sources[1].mute = True

    result = pipeline.render_recipe(recipe, render_stems=False)
    assert result.weights["B"] == 0.0
    assert result.weights["A"] == 1.0


def test_solo_overrides_other_sources(tmp_path):
    path_a, path_b = _write_two_voices(tmp_path)
    recipe = Recipe.default_two_source(path_a, path_b)
    recipe.sample_rate = SR
    recipe.sources[0].solo = True

    result = pipeline.render_recipe(recipe, render_stems=False)
    assert result.weights["A"] == 1.0
    assert result.weights["B"] == 0.0


def test_export_writes_animator_handoff_bundle(tmp_path):
    path_a, path_b = _write_two_voices(tmp_path)
    recipe = Recipe.default_two_source(path_a, path_b, name="Export Test")
    recipe.sample_rate = SR

    result = pipeline.render_recipe(recipe, render_stems=True)
    out_dir = str(tmp_path / "out")
    written = pipeline.export(result, out_dir, recipe, base_name="dialogue")

    assert os.path.isfile(written["wav"])
    assert os.path.isfile(written["recipe"])
    assert os.path.isdir(os.path.join(out_dir, "stems"))
    for stem_path in written["stems"].values():
        assert os.path.isfile(stem_path)

    reloaded_audio, sr = io_utils.load_audio(written["wav"])
    assert sr == SR
    assert len(reloaded_audio) > 0


def test_render_is_reproducible_from_recipe(tmp_path):
    """Non-destructive guarantee: re-rendering the saved recipe from the
    same originals reproduces the same audio."""
    path_a, path_b = _write_two_voices(tmp_path)
    recipe = Recipe.default_two_source(path_a, path_b)
    recipe.sample_rate = SR
    recipe.traits.pitch_semitones = 2.0

    result1 = pipeline.render_recipe(recipe, render_stems=False)

    saved_path = str(tmp_path / "voice.recipe.json")
    recipe.save(saved_path)
    reloaded = Recipe.load(saved_path)
    result2 = pipeline.render_recipe(reloaded, render_stems=False)

    assert result1.audio.shape == result2.audio.shape
    assert np.allclose(result1.audio, result2.audio, atol=1e-5)
