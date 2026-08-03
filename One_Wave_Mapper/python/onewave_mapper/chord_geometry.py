"""Chord coordinate geometry, following this repo's own canonical nodes
(Nodes/Appendix_E/E-510, E-511, E-512).

Two distinct outputs are kept deliberately separate, per this repo's own
canonical correction (Musical_Universe_Ch2_Chord_Rotation.md / E-512):

1. The chord's complete literal coordinate set (chord_coordinates) --
   never collapsed, always the primary representation.
2. An optional two-value "envelope boundary" descriptor
   (envelope_boundary) -- this was the *retired* "Oscillation Window"
   representation (E-512, formerly a compression-side/expression-side
   pair), retired because sign doesn't mean compression/expression, +/-6
   is shared between mirrored routes, dyads don't require a second side,
   and extended chords lose information when reduced to two extrema.
   It is kept here ONLY as an explicit derived overlay describing the
   coordinate set's outer boundary -- never as a replacement for the
   literal per-tone coordinates. Callers must display both, not just this.

Named geometries are checked for an *exact* match against measured
boundaries, not assumed -- e.g. the canonical Major triad rooted at its
bass note is {0,+4,-5} (boundary -5/+4), not any of the four named shapes
below. This is intentional: root selection and voicing change the
boundary, so a name only applies when the measured shape actually
produces it, per Section 18's "do not reduce the analysis to standard
labels only" and this repo's own "measure what the chords actually do."
"""

from __future__ import annotations

from dataclasses import dataclass, asdict

import numpy as np


def semitone_distance(fundamental_hz: float, root_hz: float) -> int:
    """k = (T - R) mod 12, nearest-semitone rounding (E-511 step 3)."""
    semitones = 12 * np.log2(fundamental_hz / root_hz)
    return int(round(semitones)) % 12


def mirrored_coordinate(k: int):
    """E-510 signed coordinate rule. Returns an int for interior/boundary
    positions ("0"/"+-1".."+-5"), or the string "±6" for the shared Mirror
    position (k == 6)."""
    k = k % 12
    if k == 6:
        return "±6"
    if 0 <= k <= 5:
        return k
    return k - 12  # 7..11 -> -5..-1


@dataclass
class ChordCoordinateSet:
    root_hz: float
    tone_frequencies_hz: list
    coordinates: list  # one per tone, int or "±6", in tone order

    def to_dict(self) -> dict:
        return asdict(self)


def chord_coordinates(tone_frequencies_hz: list[float], root_hz: float | None = None) -> ChordCoordinateSet:
    """E-511 Chord Rotation: the complete root-relative signed coordinate
    set. root_hz defaults to the lowest tone (the common bass-root case);
    pass it explicitly for an ambiguous or inverted chord (E-511's Yellow
    Audit: "Root selection must be explicit for ambiguous chords")."""
    if not tone_frequencies_hz:
        raise ValueError("chord_coordinates requires at least one tone")
    root_hz = root_hz if root_hz is not None else min(tone_frequencies_hz)
    coordinates = [mirrored_coordinate(semitone_distance(f, root_hz)) for f in tone_frequencies_hz]
    return ChordCoordinateSet(root_hz=root_hz, tone_frequencies_hz=list(tone_frequencies_hz), coordinates=coordinates)


# Named derived envelope-boundary geometries a measured coordinate set may
# be checked against. See module docstring for why this is a secondary,
# explicitly-labeled overlay and not the primary representation.
NAMED_ENVELOPE_GEOMETRIES = {
    "triad": (-3, 5),
    "augmented_balance": (-4, 4),
    "wider_augmented": (-5, 5),
    "augmented_third": (-3, 3),
}


@dataclass
class EnvelopeBoundary:
    low: int
    high: int
    matched_geometry: str | None
    is_retired_representation: bool = True
    notes: str = (
        "Derived envelope-boundary overlay only -- the retired two-value "
        "Oscillation Window form (E-512). Does not replace the literal "
        "per-tone coordinate set."
    )

    def to_dict(self) -> dict:
        return asdict(self)


def envelope_boundary(coordinate_set: ChordCoordinateSet) -> EnvelopeBoundary:
    """The coordinate set's outer boundary (min, max) of its numeric
    coordinates, matched against NAMED_ENVELOPE_GEOMETRIES when it lines
    up exactly. A shared-Mirror "±6" tone is excluded from the min/max,
    since it belongs to both mirrored routes at once, not one extremum."""
    numeric = [c for c in coordinate_set.coordinates if isinstance(c, int)]
    if not numeric:
        return EnvelopeBoundary(low=0, high=0, matched_geometry=None)

    low, high = min(numeric), max(numeric)
    matched = next((name for name, bounds in NAMED_ENVELOPE_GEOMETRIES.items()
                     if bounds == (low, high)), None)
    return EnvelopeBoundary(low=low, high=high, matched_geometry=matched)
