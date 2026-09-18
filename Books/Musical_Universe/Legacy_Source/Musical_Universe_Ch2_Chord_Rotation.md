Musical Universe, Chapter 2: Chord Rotation and Oscillation Windows

Version: 1.0
Date: July 19, 2026
Class: E-Series Application
Status: YELLOW

Dependencies: E-510 Music Clock, E-511 Chord Rotation, E-512 Oscillation Window

---

## Gray — Standard Music Theory Reference

A chord is a set of notes considered together — a major triad, for
example, is built from a root, a major third, and a perfect fifth
above it. Real music theory analyzes chords relative to their root,
regardless of what key they're in — this is standard, established
practice (Roman numeral analysis, chord quality classification).

---

## Chord Rotation

E-511's real definition: Chord Rotation re-centers any chord onto its
own local instance of the Music Clock (Ch1/E-510), converting a fixed
set of pitches into a signed-position relationship around the chosen
root. Any chord becomes its own local coordinate system — the same
clock, re-zeroed to whichever note is the root.

## Oscillation Window

E-512's real definition: once Chord Rotation re-centers a chord, the
result is a signed pair of positions — (Compression-side position,
Expression-side position) — a per-chord result, not a coordinate
system itself.

Real, checked values (verified against corrected data in E-513):
A Major: (P_compress=-5, P_expr=+4)
A Minor: (P_compress=-5, P_expr=+3)

## Mathematics

Chord Rotation Rule: for a chord with root R and other tones T_i,
compute each tone's signed position relative to R on the Music Clock.
Oscillation Window: the resulting pair (P_compress, P_expr) — the
most negative (Compression-side) and most positive (Expression-side)
signed positions in the rotated chord.

## Predictions

Different chord qualities (major, minor, diminished) should produce
genuinely different Oscillation Windows, not just different labels —
tested directly against real values in Chapter 3.

## Yellow Audit

- The rule for selecting WHICH tones in a chord define the
  Compression-side vs. Expression-side position (as opposed to just
  using the two extremes of the whole chord) has not been fully
  specified for chords with more than three tones (sevenths, extended
  chords) — flagged as untested territory
- Whether the SAME chord in a different octave or inversion produces
  the identical Oscillation Window has not been checked

## Future Work

Extend Chord Rotation to seventh chords and extended harmony, checking
whether the Oscillation Window rule still produces a well-defined
pair, or needs a generalized form for chords with more than three tones.

---

END OF MUSICAL UNIVERSE, CHAPTER 2
One wave. Mirror builds.
