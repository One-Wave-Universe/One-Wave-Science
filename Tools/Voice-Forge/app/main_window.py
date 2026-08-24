"""One-Wave Voice Forge main window.

A render-and-preview workflow (not real-time): sliders edit an in-memory
Recipe, "Preview" renders it to a temp WAV and plays it back, "Render"
writes the Animator handoff bundle (dialogue.wav + dialogue.recipe.json
+ optional stems/) to a chosen folder.
"""
from __future__ import annotations

import os
import random
import tempfile

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from engine import pipeline
from engine.recipe import Recipe, SourceEntry

from .controller import RecipeController
from .controls import BoolControl, TraitSlider
from .player import Previewer

SOURCE_IDS = ["A", "B", "C", "D"]

TRAIT_SPECS = [
    ("pitch_semitones", "Pitch shift (semitones)", -12.0, 12.0, 2),
    ("formant_ratio", "Formant shift (vocal tract size)", 0.7, 1.5, 3),
    ("body_db", "Body / chest resonance (dB)", -12.0, 12.0, 2),
    ("brightness_db", "Brightness / presence (dB)", -12.0, 12.0, 2),
    ("breathiness", "Breathiness", 0.0, 1.0, 2),
    ("rasp", "Rasp / grit", 0.0, 1.0, 2),
    ("nasality_db", "Nasality (dB)", -12.0, 12.0, 2),
    ("articulation", "Articulation", 0.0, 1.0, 2),
    ("time_stretch_ratio", "Timing stretch (no pitch change)", 0.5, 2.0, 2),
    ("micro_pitch_instability", "Micro-pitch instability / vibrato", 0.0, 1.0, 2),
    ("layer_doubler_amount", "Layer / doubler amount", 0.0, 1.0, 2),
    ("stereo_width", "Stereo width", 0.0, 2.0, 2),
    ("dry_wet", "Dry / Wet", 0.0, 1.0, 2),
    ("output_gain_db", "Output gain (dB)", -24.0, 12.0, 2),
]

# Randomize picks within a musically "safe" sub-range, not the full slider span.
SAFE_RANGES = {
    "pitch_semitones": (-5.0, 5.0),
    "formant_ratio": (0.9, 1.1),
    "body_db": (-6.0, 6.0),
    "brightness_db": (-6.0, 6.0),
    "breathiness": (0.0, 0.4),
    "rasp": (0.0, 0.4),
    "nasality_db": (-4.0, 4.0),
    "articulation": (0.0, 0.5),
    "time_stretch_ratio": (0.9, 1.1),
    "micro_pitch_instability": (0.0, 0.3),
    "layer_doubler_amount": (0.0, 0.4),
    "stereo_width": (0.8, 1.3),
    "dry_wet": (0.6, 1.0),
    "output_gain_db": (-3.0, 3.0),
}

FINISHING_SIMPLE_SPECS = [
    ("high_cut_hz", "High cut (Hz)", 2000.0, 20000.0, 0),
    ("low_cut_hz", "Low cut (Hz)", 20.0, 500.0, 0),
    ("presence_db", "Presence (dB)", -12.0, 12.0, 2),
    ("deesser_amount", "De-esser amount", 0.0, 1.0, 2),
    ("saturation_drive", "Saturation / drive", 0.0, 1.0, 2),
]

COMPRESSOR_SPECS = [
    ("threshold_db", "Threshold (dB)", -40.0, 0.0, 1),
    ("ratio", "Ratio", 1.0, 10.0, 2),
    ("attack_ms", "Attack (ms)", 0.5, 50.0, 2),
    ("release_ms", "Release (ms)", 10.0, 500.0, 1),
    ("makeup_db", "Makeup gain (dB)", 0.0, 12.0, 2),
]

DELAY_SPECS = [
    ("time_ms", "Delay time (ms)", 20.0, 600.0, 0),
    ("feedback", "Feedback", 0.0, 0.9, 2),
    ("mix", "Delay mix", 0.0, 1.0, 2),
]

REVERB_SPECS = [
    ("size", "Reverb size", 0.0, 1.0, 2),
    ("mix", "Reverb mix", 0.0, 1.0, 2),
]

AUDIO_FILE_FILTER = "Audio files (*.wav *.flac *.aiff *.aif *.ogg);;All files (*)"


class SourceRow(QWidget):
    """One reference-voice slot: load button, amount slider, solo/mute."""

    def __init__(self, main_window, source_id, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.source_id = source_id
        controller = main_window.controller

        layout = QHBoxLayout(self)
        layout.setContentsMargins(2, 0, 2, 0)

        layout.addWidget(QLabel(f"Ref {source_id}"))

        self.path_label = QLabel("(not loaded)")
        self.path_label.setMinimumWidth(220)
        layout.addWidget(self.path_label, stretch=1)

        load_btn = QPushButton("Load...")
        load_btn.clicked.connect(self._on_load)
        layout.addWidget(load_btn)

        self.amount_slider = TraitSlider(
            controller,
            "Amount",
            getter=self._get_amount,
            setter=self._set_amount,
            minv=0.0,
            maxv=1.0,
            decimals=2,
        )
        layout.addWidget(self.amount_slider, stretch=2)

        self.solo_box = QCheckBox("Solo")
        self.solo_box.toggled.connect(self._on_solo)
        layout.addWidget(self.solo_box)

        self.mute_box = QCheckBox("Mute")
        self.mute_box.toggled.connect(self._on_mute)
        layout.addWidget(self.mute_box)

        controller.changed.connect(self.refresh)
        self.refresh()

    def _entry(self) -> SourceEntry | None:
        return next((s for s in self.main_window.controller.recipe.sources if s.id == self.source_id), None)

    def _get_amount(self, recipe):
        entry = self._entry()
        return entry.amount if entry else 0.0

    def _set_amount(self, recipe, value):
        entry = self._entry()
        if entry is not None:
            entry.amount = value

    def _on_load(self):
        path, _ = QFileDialog.getOpenFileName(self, f"Load reference {self.source_id}", "", AUDIO_FILE_FILTER)
        if not path:
            return
        self.main_window.load_source(self.source_id, path)

    def _on_solo(self, checked):
        entry = self._entry()
        if entry is None:
            return
        self.main_window.controller.snapshot()
        entry.solo = checked
        self.main_window.controller.commit()

    def _on_mute(self, checked):
        entry = self._entry()
        if entry is None:
            return
        self.main_window.controller.snapshot()
        entry.mute = checked
        self.main_window.controller.commit()

    def refresh(self):
        entry = self._entry()
        loaded = entry is not None
        if loaded:
            self.path_label.setText(os.path.basename(entry.path))
        else:
            self.path_label.setText("(not loaded)")
        self.setEnabled(True)
        self.amount_slider.setEnabled(loaded)
        self.solo_box.setEnabled(loaded)
        self.mute_box.setEnabled(loaded)
        if loaded:
            self.solo_box.blockSignals(True)
            self.solo_box.setChecked(entry.solo)
            self.solo_box.blockSignals(False)
            self.mute_box.blockSignals(True)
            self.mute_box.setChecked(entry.mute)
            self.mute_box.blockSignals(False)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("One-Wave Voice Forge")
        self.resize(900, 800)

        self.controller = RecipeController(Recipe())
        self.previewer = Previewer()
        self._compare_snapshots = {"A": None, "B": None}
        self._temp_dir = tempfile.mkdtemp(prefix="voiceforge_")

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)

        root.addWidget(self._build_sources_group())

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.addWidget(self._build_traits_group())
        scroll_layout.addWidget(self._build_finishing_group())
        scroll_layout.addStretch(1)
        scroll.setWidget(scroll_content)
        root.addWidget(scroll, stretch=1)

        root.addWidget(self._build_transport_bar())

        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Load two or more reference voices to begin.")

    # -- building blocks ---------------------------------------------------

    def _build_sources_group(self) -> QGroupBox:
        group = QGroupBox("References")
        layout = QVBoxLayout(group)
        self.source_rows = {}
        for sid in SOURCE_IDS:
            row = SourceRow(self, sid)
            self.source_rows[sid] = row
            layout.addWidget(row)

        timing_row = QHBoxLayout()
        timing_row.addWidget(QLabel("Timing source (sets duration/pauses):"))
        self.timing_combo = QComboBox()
        self.timing_combo.currentTextChanged.connect(self._on_timing_changed)
        timing_row.addWidget(self.timing_combo)
        timing_row.addStretch(1)
        layout.addLayout(timing_row)

        self.controller.changed.connect(self._refresh_timing_combo)
        self._refresh_timing_combo()
        return group

    def _build_traits_group(self) -> QGroupBox:
        group = QGroupBox("Voice Combiner Traits")
        layout = QVBoxLayout(group)
        for field, label, minv, maxv, decimals in TRAIT_SPECS:
            slider = TraitSlider(
                self.controller,
                label,
                getter=lambda r, f=field: getattr(r.traits, f),
                setter=lambda r, v, f=field: setattr(r.traits, f, v),
                minv=minv,
                maxv=maxv,
                decimals=decimals,
                lock_key=field,
            )
            layout.addWidget(slider)
        return group

    def _build_finishing_group(self) -> QGroupBox:
        group = QGroupBox("Character Finishing")
        layout = QVBoxLayout(group)

        for field, label, minv, maxv, decimals in FINISHING_SIMPLE_SPECS:
            layout.addWidget(TraitSlider(
                self.controller, label,
                getter=lambda r, f=field: getattr(r.finishing, f),
                setter=lambda r, v, f=field: setattr(r.finishing, f, v),
                minv=minv, maxv=maxv, decimals=decimals,
            ))

        layout.addWidget(QLabel("Compressor"))
        for field, label, minv, maxv, decimals in COMPRESSOR_SPECS:
            layout.addWidget(TraitSlider(
                self.controller, "  " + label,
                getter=lambda r, f=field: getattr(r.finishing.compressor, f),
                setter=lambda r, v, f=field: setattr(r.finishing.compressor, f, v),
                minv=minv, maxv=maxv, decimals=decimals,
            ))

        layout.addWidget(BoolControl(
            self.controller, "Delay enabled",
            getter=lambda r: r.finishing.delay.enabled,
            setter=lambda r, v: setattr(r.finishing.delay, "enabled", v),
        ))
        for field, label, minv, maxv, decimals in DELAY_SPECS:
            layout.addWidget(TraitSlider(
                self.controller, "  " + label,
                getter=lambda r, f=field: getattr(r.finishing.delay, f),
                setter=lambda r, v, f=field: setattr(r.finishing.delay, f, v),
                minv=minv, maxv=maxv, decimals=decimals,
            ))

        layout.addWidget(BoolControl(
            self.controller, "Reverb enabled",
            getter=lambda r: r.finishing.reverb.enabled,
            setter=lambda r, v: setattr(r.finishing.reverb, "enabled", v),
        ))
        for field, label, minv, maxv, decimals in REVERB_SPECS:
            layout.addWidget(TraitSlider(
                self.controller, "  " + label,
                getter=lambda r, f=field: getattr(r.finishing.reverb, f),
                setter=lambda r, v, f=field: setattr(r.finishing.reverb, f, v),
                minv=minv, maxv=maxv, decimals=decimals,
            ))

        return group

    def _build_transport_bar(self) -> QWidget:
        bar = QWidget()
        layout = QHBoxLayout(bar)

        undo_btn = QPushButton("Undo")
        undo_btn.clicked.connect(self._on_undo)
        layout.addWidget(undo_btn)

        redo_btn = QPushButton("Redo")
        redo_btn.clicked.connect(self._on_redo)
        layout.addWidget(redo_btn)

        randomize_btn = QPushButton("Randomize")
        randomize_btn.clicked.connect(self._on_randomize)
        layout.addWidget(randomize_btn)

        layout.addSpacing(16)

        for slot in ("A", "B"):
            set_btn = QPushButton(f"Snapshot {slot}")
            set_btn.clicked.connect(lambda _=False, s=slot: self._on_set_snapshot(s))
            layout.addWidget(set_btn)
            play_btn = QPushButton(f"Play {slot}")
            play_btn.clicked.connect(lambda _=False, s=slot: self._on_play_snapshot(s))
            layout.addWidget(play_btn)

        preview_btn = QPushButton("Preview current")
        preview_btn.clicked.connect(self._on_preview_current)
        layout.addWidget(preview_btn)

        layout.addSpacing(16)

        load_preset_btn = QPushButton("Load Preset...")
        load_preset_btn.clicked.connect(self._on_load_preset)
        layout.addWidget(load_preset_btn)

        save_preset_btn = QPushButton("Save Preset...")
        save_preset_btn.clicked.connect(self._on_save_preset)
        layout.addWidget(save_preset_btn)

        layout.addSpacing(16)

        self.stems_checkbox = QCheckBox("Render stem layers")
        layout.addWidget(self.stems_checkbox)

        render_btn = QPushButton("Render...")
        render_btn.clicked.connect(self._on_render)
        layout.addWidget(render_btn)

        return bar

    # -- actions -------------------------------------------------------

    def load_source(self, source_id: str, path: str) -> None:
        self.controller.snapshot()
        recipe = self.controller.recipe
        entry = next((s for s in recipe.sources if s.id == source_id), None)
        if entry is None:
            recipe.sources.append(SourceEntry(id=source_id, path=path, amount=1.0))
            # A newly added slot rebalances everyone to an even blend; amounts
            # the user already tuned are only touched by this first-load case.
            n = len(recipe.sources)
            for s in recipe.sources:
                s.amount = 1.0 / n
        else:
            entry.path = path
        if recipe.timing_source_id is None:
            recipe.timing_source_id = source_id
        self.controller.commit()
        self.statusBar().showMessage(f"Loaded reference {source_id}: {os.path.basename(path)}")

    def _refresh_timing_combo(self):
        ids = [s.id for s in self.controller.recipe.sources]
        current = self.controller.recipe.timing_source_id
        self.timing_combo.blockSignals(True)
        self.timing_combo.clear()
        self.timing_combo.addItems(ids)
        if current in ids:
            self.timing_combo.setCurrentText(current)
        self.timing_combo.blockSignals(False)

    def _on_timing_changed(self, text):
        if not text:
            return
        self.controller.snapshot()
        self.controller.recipe.timing_source_id = text
        self.controller.commit()

    def _on_undo(self):
        if not self.controller.undo():
            self.statusBar().showMessage("Nothing to undo.")

    def _on_redo(self):
        if not self.controller.redo():
            self.statusBar().showMessage("Nothing to redo.")

    def _on_randomize(self):
        self.controller.snapshot()
        traits = self.controller.recipe.traits
        locked = set(self.controller.recipe.locked_traits)
        for field, lo, hi in ((f, *SAFE_RANGES[f]) for f in SAFE_RANGES):
            if field in locked:
                continue
            setattr(traits, field, random.uniform(lo, hi))
        self.controller.commit()

    def _on_set_snapshot(self, slot):
        self._compare_snapshots[slot] = self.controller.recipe.clone()
        self.statusBar().showMessage(f"Snapshot {slot} captured from current settings.")

    def _on_play_snapshot(self, slot):
        recipe = self._compare_snapshots.get(slot)
        if recipe is None:
            self.statusBar().showMessage(f"No snapshot in slot {slot} yet -- click Snapshot {slot} first.")
            return
        self._render_and_play(recipe, f"compare_{slot}")

    def _on_preview_current(self):
        self._render_and_play(self.controller.recipe, "preview")

    def _render_and_play(self, recipe, label):
        try:
            result = pipeline.render_recipe(recipe, base_dir=self.controller.base_dir, render_stems=False)
        except Exception as exc:  # noqa: BLE001 - surface any DSP error to the user
            QMessageBox.warning(self, "Preview failed", str(exc))
            return
        from engine import io_utils

        path = os.path.join(self._temp_dir, f"{label}.wav")
        io_utils.save_wav(path, result.audio, result.sr)
        if self.previewer.play_file(path):
            self.statusBar().showMessage(f"Playing {label} ({path}).")
        else:
            self.statusBar().showMessage(f"Rendered {label} to {path} (audio playback unavailable on this machine).")

    def _on_load_preset(self):
        path, _ = QFileDialog.getOpenFileName(self, "Load recipe", "", "Voice Forge recipe (*.json);;All files (*)")
        if not path:
            return
        try:
            recipe = Recipe.load(path)
        except Exception as exc:  # noqa: BLE001
            QMessageBox.warning(self, "Load failed", str(exc))
            return
        self.controller.replace(recipe, base_dir=os.path.dirname(path))
        self.statusBar().showMessage(f"Loaded preset: {path}")

    def _on_save_preset(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save recipe", "voice.recipe.json", "Voice Forge recipe (*.json)")
        if not path:
            return
        self.controller.recipe.save(path)
        self.statusBar().showMessage(f"Saved preset: {path}")

    def _on_render(self):
        if not self.controller.recipe.sources:
            QMessageBox.information(self, "Nothing to render", "Load at least one reference voice first.")
            return
        out_dir = QFileDialog.getExistingDirectory(self, "Choose output folder")
        if not out_dir:
            return
        try:
            result = pipeline.render_recipe(
                self.controller.recipe,
                base_dir=self.controller.base_dir,
                render_stems=self.stems_checkbox.isChecked(),
            )
            written = pipeline.export(result, out_dir, self.controller.recipe, base_name="dialogue")
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self, "Render failed", str(exc))
            return
        self.statusBar().showMessage(f"Rendered: {written['wav']}")
        QMessageBox.information(self, "Render complete", f"Wrote:\n{written['wav']}\n{written['recipe']}")
