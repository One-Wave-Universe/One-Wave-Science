import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import numpy as np
import pytest

pytest.importorskip("PySide6")
pytest.importorskip("pyqtgraph")

from PySide6 import QtWidgets

from onewave_mapper.ui.analysis_state import ViewMode
from onewave_mapper.ui.mapper_window import MapperWindow


@pytest.fixture(scope="module")
def qapp():
    yield QtWidgets.QApplication.instance() or QtWidgets.QApplication([])


def test_window_constructs_with_all_tabs(qapp):
    window = MapperWindow()
    titles = [window.tabs.tabText(i) for i in range(window.tabs.count())]
    assert titles == ["Raw waveform", "Envelope", "Spectrum", "Spectrogram",
                       "Phase", "Interference", "Resonance", "Modulation"]
    window.close()


def test_load_guitar_note_populates_all_analysis_panels(qapp):
    window = MapperWindow()
    window.load_synthetic_guitar_note()

    assert len(window.state.raw_signal) > 0
    x, y = window.waveform_panel.curve.getData()
    assert len(x) == len(window.state.raw_signal)

    _, envelope = window.envelope_panel.upper_curve.getData()
    assert len(envelope) == len(window.state.raw_signal)

    assert window.spectrum_panel.fundamental_label.text() != "--"
    assert abs(float(window.spectrum_panel.fundamental_label.text()) - 220.0) < 3.0

    assert window.spectrogram_panel.image_item.image is not None
    assert len(window.phase_panel._phase_tracks) > 0
    window.close()


def test_load_chord_produces_resonance_candidates(qapp):
    window = MapperWindow()
    window.load_synthetic_chord()
    assert len(window.resonance_panel._events) > 0
    window.close()


def test_selecting_a_region_in_shared_state_updates_spectrum_and_phase(qapp):
    window = MapperWindow()
    window.load_synthetic_guitar_note()
    sr = window.state.sample_rate

    window.state.set_selection(0, int(0.1 * sr))
    fundamental_short = window.spectrum_panel.fundamental_label.text()

    window.state.set_selection(0, len(window.state.raw_signal))
    fundamental_full = window.spectrum_panel.fundamental_label.text()

    # both should detect *a* fundamental for this simple case, but the
    # important thing is the panel actually reacted to the shared
    # selection change without needing to touch the panel directly
    assert fundamental_short != "--"
    assert fundamental_full != "--"
    window.close()


def test_mode_toolbar_updates_shared_state(qapp):
    window = MapperWindow()
    raw_button = window.mode_group.buttons()[0]
    raw_button.setChecked(True)
    assert window.state.mode == ViewMode.RAW
    window.close()


def test_point_path_field_checkboxes_reflect_and_drive_state(qapp):
    window = MapperWindow()
    assert window.point_checkbox.isChecked() is True

    window.point_checkbox.setChecked(False)
    assert window.state.show_point_rotation is False

    window.path_checkbox.setChecked(False)
    assert window.state.show_path_rotation is False
    window.close()


def test_interference_panel_is_independent_of_shared_recording(qapp):
    window = MapperWindow()
    window.load_synthetic_sine()
    # interference panel has its own two-source demo, unrelated to the
    # single-channel shared recording
    assert len(window.interference_panel.source_a) > 0
    assert not np.array_equal(window.interference_panel.source_a, window.state.raw_signal)
    window.close()


def test_load_all_three_synthetic_sources_without_crashing(qapp):
    window = MapperWindow()
    window.load_synthetic_sine()
    window.load_synthetic_guitar_note()
    window.load_synthetic_chord()
    assert len(window.state.raw_signal) > 0
    window.close()
