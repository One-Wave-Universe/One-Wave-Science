"""GUI smoke test: load two reference voices, tweak controls, undo/redo,
save/load a preset, and render -- exercised headlessly via the 'offscreen'
Qt platform plugin, same pattern as the Animator's GUI smoke test."""
import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

PySide6 = pytest.importorskip("PySide6")

from PySide6.QtWidgets import QApplication  # noqa: E402

from app.main_window import MainWindow  # noqa: E402
from engine import io_utils  # noqa: E402
from engine.recipe import Recipe  # noqa: E402
from tools.make_sample_voices import synth_voice  # noqa: E402

SR = 16000


@pytest.fixture(scope="module")
def app():
    return QApplication.instance() or QApplication(sys.argv)


@pytest.fixture()
def two_voices(tmp_path):
    voice_a = synth_voice(SR, duration=0.7, f0=115.0, formants=[(650, 12, 3.5), (1100, 10, 4.0)], breath=0.02, seed=30)
    voice_b = synth_voice(SR, duration=0.6, f0=195.0, formants=[(900, 12, 3.5), (2200, 10, 4.0)], breath=0.03, seed=31)
    path_a = str(tmp_path / "voice_a.wav")
    path_b = str(tmp_path / "voice_b.wav")
    io_utils.save_wav(path_a, voice_a, SR)
    io_utils.save_wav(path_b, voice_b, SR)
    return path_a, path_b


def test_load_blend_and_render(app, tmp_path, two_voices):
    path_a, path_b = two_voices
    window = MainWindow()

    window.load_source("A", path_a)
    window.load_source("B", path_b)

    assert len(window.controller.recipe.sources) == 2
    assert window.controller.recipe.sources[0].amount == pytest.approx(0.5)
    assert window.controller.recipe.sources[1].amount == pytest.approx(0.5)
    assert window.controller.recipe.timing_source_id == "A"

    # Row widgets reflect the loaded state.
    assert window.source_rows["A"].path_label.text() == os.path.basename(path_a)
    assert window.source_rows["A"].amount_slider.isEnabled()

    # Move the pitch slider: this should be undoable.
    pitch_slider = next(w for w in window.findChildren(object) if getattr(w, "lock_key", None) == "pitch_semitones")
    pitch_slider.spin.setValue(4.0)
    assert window.controller.recipe.traits.pitch_semitones == pytest.approx(4.0)

    assert window.controller.undo() is True
    assert window.controller.recipe.traits.pitch_semitones == pytest.approx(0.0)
    assert window.controller.redo() is True
    assert window.controller.recipe.traits.pitch_semitones == pytest.approx(4.0)

    # Lock a trait, randomize, and confirm it was left untouched.
    pitch_slider.lock_box.setChecked(True)
    window._on_randomize()
    assert window.controller.recipe.traits.pitch_semitones == pytest.approx(4.0)
    assert "pitch_semitones" in window.controller.recipe.locked_traits

    # Save/load a preset roundtrips through the controller.
    preset_path = str(tmp_path / "voice.recipe.json")
    window.controller.recipe.save(preset_path)
    reloaded = Recipe.load(preset_path)
    window.controller.replace(reloaded, base_dir=None)
    assert window.controller.recipe.traits.pitch_semitones == pytest.approx(4.0)

    # Solo A: pipeline should drop B's contribution entirely.
    window.source_rows["A"].solo_box.setChecked(True)
    from engine import pipeline

    result = pipeline.render_recipe(window.controller.recipe, render_stems=True)
    assert result.weights["A"] == 1.0
    assert result.weights["B"] == 0.0
    assert result.audio.shape[1] == 2

    written = pipeline.export(result, str(tmp_path / "out"), window.controller.recipe)
    assert os.path.isfile(written["wav"])
    assert os.path.isfile(written["recipe"])
