"""End-to-end render: load references -> blend by trait -> pitch/formant ->
character coloring -> finishing chain -> stereo output.

This is the only module that knows the full signal flow; the GUI and any
CLI/batch caller just build a Recipe and call render_recipe().
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from . import blend as blend_mod
from . import dsp
from . import io_utils
from .recipe import Recipe, resolve_source_path

N_FFT = 1024
HOP = 256


@dataclass
class RenderResult:
    audio: np.ndarray  # stereo, shape (n, 2)
    sr: int
    stems: dict = field(default_factory=dict)  # name -> mono/stereo array
    weights: dict = field(default_factory=dict)  # source id -> normalized blend weight


def _enabled_amounts(recipe: Recipe) -> dict:
    any_solo = any(s.solo for s in recipe.sources)
    amounts = {}
    for s in recipe.sources:
        if any_solo:
            amounts[s.id] = s.amount if s.solo else 0.0
        else:
            amounts[s.id] = 0.0 if s.mute else s.amount
    return amounts


def render_recipe(recipe: Recipe, base_dir: str | None = None, render_stems: bool = False) -> RenderResult:
    if not recipe.sources:
        raise ValueError("recipe has no sources to render")

    sr = recipe.sample_rate
    amounts = _enabled_amounts(recipe)

    blend_inputs = []
    for s in recipe.sources:
        path = resolve_source_path(s, base_dir)
        y, _sr = io_utils.load_audio(path, target_sr=sr)
        blend_inputs.append(blend_mod.BlendInput(id=s.id, y=y, amount=amounts.get(s.id, 0.0)))

    result = blend_mod.blend_sources(
        blend_inputs, sr, timing_id=recipe.timing_source_id, n_fft=N_FFT, hop=HOP
    )

    t = recipe.traits

    residual = dsp.pitch_shift(result.residual, sr, t.pitch_semitones)
    residual = dsp.micro_pitch_jitter(residual, sr, t.micro_pitch_instability)

    env_final = dsp.warp_envelope_freq(result.env_mag, result.freqs, t.formant_ratio)

    y_blend = dsp.resynthesize(residual, env_final, sr, n_fft=N_FFT, hop=HOP, length=len(residual))
    y_blend = dsp.time_stretch_to_ratio(y_blend, t.time_stretch_ratio)

    timing_entry = next((s for s in blend_inputs if s.id == recipe.timing_source_id), blend_inputs[0])
    dry_reference = dsp.match_length(timing_entry.y, len(y_blend))
    y_mixed = t.dry_wet * y_blend + (1.0 - t.dry_wet) * dry_reference
    y_mixed = y_mixed.astype(np.float32)

    y_char = dsp.low_shelf(y_mixed, sr, freq=220.0, gain_db=t.body_db)
    y_char = dsp.high_shelf(y_char, sr, freq=7000.0, gain_db=t.brightness_db)
    y_char = dsp.nasality(y_char, sr, t.nasality_db)
    y_char = dsp.add_breath(y_char, sr, t.breathiness)
    y_char = dsp.add_rasp(y_char, t.rasp)
    y_char = dsp.articulate(y_char, sr, t.articulation)

    fin = recipe.finishing
    y_fin = dsp.high_low_cut(y_char, sr, low_hz=fin.low_cut_hz, high_hz=fin.high_cut_hz)
    y_fin = dsp.peaking_eq(y_fin, sr, freq=4000.0, gain_db=fin.presence_db, q=0.9)
    y_fin = dsp.deesser(y_fin, sr, fin.deesser_amount)
    y_fin = dsp.compressor(
        y_fin,
        sr,
        threshold_db=fin.compressor.threshold_db,
        ratio=fin.compressor.ratio,
        attack_ms=fin.compressor.attack_ms,
        release_ms=fin.compressor.release_ms,
        makeup_db=fin.compressor.makeup_db,
    )
    y_fin = dsp.saturate(y_fin, fin.saturation_drive)
    if fin.delay.enabled:
        y_fin = dsp.delay_fx(y_fin, sr, fin.delay.time_ms, fin.delay.feedback, fin.delay.mix)
    if fin.reverb.enabled:
        y_fin = dsp.reverb_fx(y_fin, sr, fin.reverb.size, fin.reverb.mix)

    stereo = dsp.doubler(y_fin, sr, t.layer_doubler_amount)
    stereo = dsp.stereo_width(stereo, t.stereo_width)
    stereo = stereo * (10 ** (t.output_gain_db / 20.0))
    stereo = np.clip(stereo, -1.0, 1.0).astype(np.float32)

    stems = {}
    if render_stems:
        stems["01_blend"] = y_mixed
        stems["02_character"] = y_char
        stems["03_final"] = stereo

    return RenderResult(audio=stereo, sr=sr, stems=stems, weights=result.weights)


def export(result: RenderResult, out_dir: str, recipe: Recipe, base_name: str = "dialogue") -> dict:
    """Write the Animator-handoff bundle: <base>.wav, <base>.recipe.json,
    and (if stems were rendered) a stems/ directory."""
    import os

    os.makedirs(out_dir, exist_ok=True)
    wav_path = os.path.join(out_dir, f"{base_name}.wav")
    recipe_path = os.path.join(out_dir, f"{base_name}.recipe.json")

    io_utils.save_wav(wav_path, result.audio, result.sr)
    recipe.save(recipe_path)

    written = {"wav": wav_path, "recipe": recipe_path}
    if result.stems:
        stems_dir = os.path.join(out_dir, "stems")
        os.makedirs(stems_dir, exist_ok=True)
        stem_paths = {}
        for name, audio in result.stems.items():
            path = os.path.join(stems_dir, f"{name}.wav")
            io_utils.save_wav(path, audio, result.sr)
            stem_paths[name] = path
        written["stems"] = stem_paths
    return written
