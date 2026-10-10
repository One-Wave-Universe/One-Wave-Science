#!/usr/bin/env python3
"""12-state octave-doubling validation for Algorithm Zero/Rabbit Hop/M4.

Known-domain test only: pitch class is state, octave is scale, and physical
frequency doubles across an octave. Passing does not establish a universal
physical law.
"""
from dataclasses import dataclass

A4_HZ = 440.0

def frequency_hz(midi: int) -> float:
    return A4_HZ * (2.0 ** ((midi - 69) / 12.0))

@dataclass(frozen=True)
class StateScale:
    pitch_class: int
    octave_band: int
    midi: int

@dataclass(frozen=True)
class Receipt:
    source_midi: int
    source_pitch_class: int
    source_scale: int
    hop: int
    target_midi: int
    target_pitch_class: int
    target_scale: int

    def reverse(self) -> "Receipt":
        return Receipt(self.target_midi, self.target_pitch_class, self.target_scale,
                       -self.hop, self.source_midi, self.source_pitch_class,
                       self.source_scale)

def state_scale(midi: int) -> StateScale:
    return StateScale(midi % 12, midi // 12, midi)

def hop(midi: int, semitones: int) -> Receipt:
    a = state_scale(midi)
    b = state_scale(midi + semitones)
    return Receipt(a.midi, a.pitch_class, a.octave_band, semitones,
                   b.midi, b.pitch_class, b.octave_band)

def apply(receipt: Receipt) -> int:
    assert receipt.source_midi + receipt.hop == receipt.target_midi
    return receipt.target_midi

def m4_view_up(receipt: Receipt) -> dict:
    """M4 VIEW-UP: observe relation without collapsing state and scale."""
    return {
        "same_pitch_class": receipt.source_pitch_class == receipt.target_pitch_class,
        "scale_delta": receipt.target_scale - receipt.source_scale,
        "hop": receipt.hop,
    }

def m4_action_down(receipt: Receipt) -> Receipt:
    """M4 ACTION-DOWN: exact inverse action using the retained receipt."""
    return receipt.reverse()

def test_all_12_octave_doublings():
    # MIDI 60..71 gives one complete chromatic cycle C4..B4.
    for midi in range(60, 72):
        r = hop(midi, 12)
        view = m4_view_up(r)
        assert view["same_pitch_class"]
        assert view["scale_delta"] == 1
        f0, f1 = frequency_hz(midi), frequency_hz(r.target_midi)
        assert abs((f1 / f0) - 2.0) < 1e-12
        back = m4_action_down(r)
        assert apply(back) == midi
        assert back.target_pitch_class == r.source_pitch_class
        assert back.target_scale == r.source_scale

def test_24_is_two_12_traversals_not_24_pitch_classes():
    for midi in range(60, 72):
        r24 = hop(midi, 24)
        view = m4_view_up(r24)
        assert view["same_pitch_class"]
        assert view["scale_delta"] == 2
        assert abs((frequency_hz(r24.target_midi) / frequency_hz(midi)) - 4.0) < 1e-12
        assert apply(m4_action_down(r24)) == midi

def test_state_scale_do_not_collapse():
    r = hop(60, 12)
    assert r.source_pitch_class == r.target_pitch_class
    assert r.source_midi != r.target_midi
    assert r.source_scale != r.target_scale

def test_wrong_receipt_fails_visibly():
    r = hop(60, 12)
    bad = Receipt(r.source_midi, r.source_pitch_class, r.source_scale,
                  11, r.target_midi, r.target_pitch_class, r.target_scale)
    try:
        apply(bad)
    except AssertionError:
        return
    raise AssertionError("wrong hop receipt was silently accepted")

if __name__ == "__main__":
    tests=[
        test_all_12_octave_doublings,
        test_24_is_two_12_traversals_not_24_pitch_classes,
        test_state_scale_do_not_collapse,
        test_wrong_receipt_fails_visibly,
    ]
    for t in tests:
        t()
        print("PASS", t.__name__)
    print("PASS: 12 pitch classes retain identity across f->2f; scale changes; exact inverse receipts restore origin.")
