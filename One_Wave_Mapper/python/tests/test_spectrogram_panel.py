import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest

pytest.importorskip("PySide6")
pytest.importorskip("pyqtgraph")

from PySide6 import QtWidgets

from onewave_mapper import signal_generator
from onewave_mapper.ui.analysis_state import AnalysisState
from onewave_mapper.ui.panels.spectrogram_panel import SpectrogramPanel


@pytest.fixture(scope="module")
def qapp():
    yield QtWidgets.QApplication.instance() or QtWidgets.QApplication([])


def test_spectrogram_image_populates_for_a_note(qapp):
    sr = 48000
    state = AnalysisState(sample_rate=sr)
    state.set_recording(signal_generator.guitar_note(220.0, 1.0, sr))
    panel = SpectrogramPanel(state, fft_size=2048, hop_size=256)

    image = panel.image_item.image
    assert image is not None
    assert image.shape[0] > 0 and image.shape[1] > 0


def test_spectrogram_redraws_on_view_range_change(qapp):
    sr = 48000
    state = AnalysisState(sample_rate=sr)
    state.set_recording(signal_generator.guitar_note(220.0, 2.0, sr))
    panel = SpectrogramPanel(state, fft_size=2048, hop_size=256)
    first_shape = panel.image_item.image.shape

    state.set_view_range(0, 24000)
    second_shape = panel.image_item.image.shape
    assert second_shape != first_shape or second_shape[0] < first_shape[0]


def test_short_signal_clears_image_without_crashing(qapp):
    sr = 48000
    state = AnalysisState(sample_rate=sr)
    state.set_recording(signal_generator.sine(440, 0.01, sr))  # shorter than fft_size
    panel = SpectrogramPanel(state, fft_size=2048, hop_size=256)
    assert panel.image_item.image is None or panel.image_item.image.size == 0


def test_empty_recording_does_not_crash(qapp):
    state = AnalysisState(sample_rate=48000)
    panel = SpectrogramPanel(state)
    assert panel.image_item.image is None or panel.image_item.image.size == 0


def test_image_rect_time_axis_matches_view_start(qapp):
    sr = 48000
    state = AnalysisState(sample_rate=sr)
    state.set_recording(signal_generator.guitar_note(220.0, 2.0, sr))
    panel = SpectrogramPanel(state, fft_size=2048, hop_size=256)
    state.set_view_range(48000, 96000)  # second half

    rect = panel.image_item.boundingRect()
    x_in_item_coords = 0  # image item's own local coordinate, transform holds the offset
    transform = panel.image_item.transform()
    mapped_x = transform.map(x_in_item_coords, 0)[0]
    assert mapped_x == pytest.approx(1.0, abs=0.05)  # 48000 samples / 48000 Hz = 1.0s
