---
node_id: "E-511"
canonical_name: "Chord Rotation"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Applied Dynamics and Stability"
claim_gate_detail: "YELLOW (proposed — new node, split out from E-510)"
metadata_standard: "I-06"
---

# Node E-511: Chord Rotation

Class: FUNCTION

Not a book chapter. Not a book node.
This is a reusable function node within Appendix E. It is the operator
that acts on the E-510 Music Clock reference frame — the same relationship
as A-102 Displacement acting on A-101 Ground/Zero, or B-205 Mirror acting
at C-301 Mirror Gate.

Dependencies:
Upstream: E-510 Music Clock Harmonic Oscillation
Downstream: E-512 Oscillation Window

Definition:
Chord Rotation is the function that re-centers any chord onto its own
local instance of the E-510 clock, converting a fixed set of pitches into
a signed-position relationship around a chosen root.

Any chord can become its own local coordinate system.

Mathematics:
Chord Rotation Rule:
1. Select chord.
2. Move root to (0).
3. Rotate the clock so root = 0.
4. Measure harmonic distances of remaining chord tones as signed positions.
5. Identify the oscillation window (compression pull vs expression pull).

Output of this function is an Oscillation Window: a signed pair
(compression-side position, expression-side position) describing where
the chord's other tones fall relative to its root. The Oscillation
Window is now its own node — see E-512 — since it is consumed
independently of this function.

Worked examples (full values and analysis now live in E-512):
CORRECTION (this turn — the values below were wrong in the original
build, checked against E-510's own real clock and fixed):
A Major -> Window: Compression side (fifth, E) = -5, Expression side (third, C#) = +4
A Minor -> Window: Compression side (fifth, E) = -5, Expression side (third, C) = +3
Previously stated as (-4,+5) and (-3,+5) — both the sign and the
compression/expression assignment were backwards. E-510's clock places
E at -5 (counter-clockwise/Compression) and C#/C at +4/+3
(clockwise/Expression), not the reverse.

Operational Chain:
E-510 Music Clock => Chord Rotation => E-512 Oscillation Window

Yellow Audit:
- Only tested informally on A Major / A Minor; not yet checked against other roots or chord qualities (diminished, augmented, seventh chords, etc.)
- Whether this rule generalizes is now tracked in E-512, since that's where the pattern claim actually lives

Future Work:
Test the chord rotation rule against a full set of chord qualities, not just Major/Minor on one root.

---
