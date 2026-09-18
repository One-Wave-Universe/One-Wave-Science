Musical Universe, Chapter 3: Leaning Direction

Version: 1.0

Wiki Page (with embedded chart): Wiki_Pages/Musical_Universe_Ch3_Wiki_Page.html
Date: July 19, 2026
Class: E-Series Application
Status: YELLOW

Dependencies: E-512 Oscillation Window, E-513 Chord Leaning Direction

---

## Gray — Standard Music Theory Reference

Major and minor chords are often described, informally, as having
different "character" — major commonly described as brighter, minor
as darker or more melancholic. This is a real, widely-shared musical
intuition, though not itself a rigorous physical claim in standard
theory — it's a perceptual/cultural description, not a formula.

---

## Chord Leaning Direction

E-513's real definition: a chord's Oscillation Window (P_compress,
P_expr) has a directional lean when |P_compress| != |P_expr| — one
side pulls harder than the other.

Real, checked values:
A Major: (P_compress=-5, P_expr=+4). |-5| > |4|. Compression dominates,
  by a gap of 1.
A Minor: (P_compress=-5, P_expr=+3). |-5| > |3|. Compression dominates,
  by a gap of 2 — MORE strongly than Major, not less.

This is a real, checkable, somewhat counter-intuitive finding: both
Major and Minor lean toward Compression in this system, not opposite
directions — Minor leans harder, not oppositely. This does NOT match
a naive "major=Expression/bright, minor=Compression/dark" binary that
might be assumed from the informal "bright vs. dark" description above
— the real computed values show both leaning the same direction, with
Minor's lean simply stronger.

Power chords (root + fifth only, no third): explicitly UNDEFINED under
this formula — with no third, there is no asymmetry to measure, and
the leaning-direction concept doesn't apply.

## Expansion: Diminished and Augmented (computed this session)

Using the same formula, extended to two more real chord types:

Diminished (root, minor third +3, diminished fifth +6): positions
(3, 6) — BOTH POSITIVE. Neither tone falls on the Compression side at
all under this convention. This means the "Compression-side/
Expression-side" labeling genuinely breaks down for this chord — the
arithmetic still works, but calling either position "the compression
side" would be misleading. Flagged honestly rather than forced to fit.

Augmented (root, major third +4, augmented fifth +8, converts to
clock position -4): positions (-4, 4) — perfectly symmetric, L=0.
This has a real, independent correlate worth noting: augmented triads
are well-known in standard music theory for their ambiguous, centerless
quality, built from two stacked major thirds dividing the octave
symmetrically. The computed L=0 and this real, independent musical
property point the same direction — a genuine, if modest, piece of
supporting evidence that this measure tracks something real, not
just an artifact of the formula.

Full table:
Major:      (-5, +4), L=1
Minor:      (-5, +3), L=2
Diminished: (+3, +6), L=3 (labels break down — both positive)
Augmented:  (-4, +4), L=0 (perfectly symmetric)

## Mathematics

Leaning magnitude: L = | |P_compress| - |P_expr| |
A Major: L = |5-4| = 1
A Minor: L = |5-3| = 2

## Predictions

If this framework's leaning measure tracks anything real about
perceived musical character, chords with larger L (like minor, L=2)
should be independently describable as having a more pronounced
directional quality than chords with smaller L (like major, L=1) —
a real, testable claim against listener perception studies, not yet
tested here.

## Yellow Audit

- This node's own real finding directly contradicts a naive "major
  leans one way, minor leans the other" assumption — flagged
  explicitly rather than smoothed over, since it's a genuine surprise
  worth keeping visible
- No listener-perception data has been checked against these L values
  — the mathematical result is real; whether it corresponds to
  anything perceptually meaningful is untested
- Power chords are explicitly outside this formula's domain, not a
  silent gap

## Future Work

Test whether L (leaning magnitude) correlates with any independent,
real measure of perceived chord brightness/darkness — this would be a
genuine, falsifiable prediction if pursued.
Determine whether diminished and augmented chords (not yet computed)
show even larger or smaller L values than major/minor.

---

END OF MUSICAL UNIVERSE, CHAPTER 3
One wave. Mirror builds.
