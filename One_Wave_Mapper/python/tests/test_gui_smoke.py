"""Smoke tests for the oscilloscope UI, run against Qt's offscreen
platform since this environment has no real display. These prove the
window constructs, actually redraws across timer ticks with a live
source running, Freeze genuinely stops updates, changing trigger
settings doesn't crash, and a grabbed screenshot is a real non-blank
image -- not that a human has looked at it on a real screen.
"""

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import time

import numpy as np
import pytest

pytest.importorskip("PySide6")
pytest.importorskip("pyqtgraph")

from PySide6 import QtWidgets

from onewave_mapper.ui.oscilloscope_window import OscilloscopeWindow


@pytest.fixture(scope="module")
def qapp():
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    yield app


def _pump(qapp, iterations: int = 20, delay_seconds: float = 0.01) -> None:
    for _ in range(iterations):
        qapp.processEvents()
        time.sleep(delay_seconds)


def test_oscilloscope_window_constructs(qapp):
    window = OscilloscopeWindow(sample_rate=48000)
    assert window.windowTitle().startswith("One-Wave Mapper")
    assert "normalized" in window.plot_widget.getAxis("left").labelText.lower() \
        or "dbfs" in window.plot_widget.getAxis("left").labelText.lower()
    window.close()


def test_start_stop_toggles_button_state(qapp):
    window = OscilloscopeWindow(sample_rate=48000)
    assert window.start_button.isEnabled()
    assert not window.stop_button.isEnabled()

    window._on_start_clicked()
    assert not window.start_button.isEnabled()
    assert window.stop_button.isEnabled()
    assert window.source is not None

    window._on_stop_clicked()
    assert window.start_button.isEnabled()
    assert not window.stop_button.isEnabled()
    assert window.source is None
    window.close()


def test_oscilloscope_updates_live_over_time(qapp):
    window = OscilloscopeWindow(sample_rate=48000, refresh_interval_ms=10)
    window.show()
    window._on_start_clicked()
    _pump(qapp, 20)

    x1, y1 = window.curve.getData()
    assert x1 is not None and len(x1) > 0
    assert window.readout_labels["Peak"].text() != "--"
    assert float(window.readout_labels["Peak"].text()) > 0
    written_after_first_pump = window.ring_buffer.total_written

    _pump(qapp, 20)
    x2, y2 = window.curve.getData()

    # the ring buffer must keep receiving new samples, and the plotted
    # frame must not be stuck on the very first render
    assert window.ring_buffer.total_written > written_after_first_pump
    assert len(y2) > 0 and not np.array_equal(y1, y2)

    window._on_stop_clicked()
    window.close()


def test_pitch_wavelength_and_note_readouts_populate_for_a_tone(qapp):
    window = OscilloscopeWindow(sample_rate=48000, refresh_interval_ms=10)
    window.source_combo.setCurrentText("Synthetic: 220 Hz sine")
    window.show()
    window._on_start_clicked()
    _pump(qapp, 40)

    assert window.readout_labels["Pitch (Hz)"].text() != "--"
    pitch_hz = float(window.readout_labels["Pitch (Hz)"].text())
    assert abs(pitch_hz - 220.0) < 5.0
    assert "A3" in window.readout_labels["Note"].text()
    assert window.readout_labels["Wavelength (m)"].text() != "--"
    wavelength_m = float(window.readout_labels["Wavelength (m)"].text())
    assert abs(wavelength_m - 343.0 / pitch_hz) < 0.01

    window._on_stop_clicked()
    window.close()


def test_life_cycle_envelope_panel_shows_growth_and_decay(qapp):
    # A single guitar note has a fast attack (growth) then a decay (die
    # off) -- looped by SyntheticSource, so within one 2-second envelope
    # window the panel should show real, non-flat variation, not just
    # whatever the oscilloscope's short trigger frame happens to catch.
    window = OscilloscopeWindow(sample_rate=48000, refresh_interval_ms=10,
                                 envelope_window_seconds=2.0, envelope_refresh_interval_ms=20)
    window.source_combo.setCurrentText("Synthetic: guitar note")
    window.show()
    window._on_start_clicked()
    _pump(qapp, 250, delay_seconds=0.01)  # let >2s of real note audio accumulate

    t, envelope = window.envelope_curve.getData()
    assert t is not None and len(envelope) > 100
    assert np.max(envelope) > 0.05  # real signal, not silence
    assert np.max(envelope) - np.min(envelope) > 0.02  # actually varies -- not a flat line

    assert window.readout_labels["Life-cycle state"].text() not in ("--", "")

    window._on_stop_clicked()
    window.close()


def test_envelope_panel_freezes_with_scope(qapp):
    window = OscilloscopeWindow(sample_rate=48000, refresh_interval_ms=10,
                                 envelope_refresh_interval_ms=20)
    window._on_start_clicked()
    _pump(qapp, 30)

    window.freeze_button.setChecked(True)
    _, env_frozen = window.envelope_curve.getData()
    _pump(qapp, 30)
    _, env_after = window.envelope_curve.getData()

    assert np.array_equal(env_frozen, env_after)
    window._on_stop_clicked()
    window.close()


def test_freeze_stops_updating(qapp):
    window = OscilloscopeWindow(sample_rate=48000, refresh_interval_ms=10)
    window._on_start_clicked()
    _pump(qapp, 15)

    window.freeze_button.setChecked(True)
    _, y_frozen = window.curve.getData()

    _pump(qapp, 15)
    _, y_after = window.curve.getData()

    assert np.array_equal(y_frozen, y_after)
    window._on_stop_clicked()
    window.close()


def test_trigger_edge_and_threshold_changes_do_not_crash(qapp):
    window = OscilloscopeWindow(sample_rate=48000, refresh_interval_ms=10)
    window._on_start_clicked()

    window.edge_combo.setCurrentText("Falling")
    window.threshold_spin.setValue(0.1)
    _pump(qapp, 10)
    window.edge_combo.setCurrentText("Either")
    window.threshold_spin.setValue(-0.1)
    _pump(qapp, 10)

    assert window.trigger_engine.config.threshold == pytest.approx(-0.1)

    window._on_stop_clicked()
    window.close()


def test_screenshot_renders_nonblank_image(qapp, tmp_path):
    window = OscilloscopeWindow(sample_rate=48000, refresh_interval_ms=10)
    window.resize(900, 600)
    window.show()
    window._on_start_clicked()
    _pump(qapp, 30)

    pixmap = window.grab()
    path = tmp_path / "oscilloscope.png"
    pixmap.save(str(path))

    assert path.exists()
    assert path.stat().st_size > 2000  # not a degenerate/blank image
    assert pixmap.width() > 0 and pixmap.height() > 0

    window._on_stop_clicked()
    window.close()


def test_guitar_note_source_loops_without_crashing(qapp):
    window = OscilloscopeWindow(sample_rate=48000, refresh_interval_ms=10)
    window.source_combo.setCurrentText("Synthetic: guitar note")
    window._on_start_clicked()
    _pump(qapp, 30)
    assert window.ring_buffer.total_written > 0
    window._on_stop_clicked()
    window.close()
