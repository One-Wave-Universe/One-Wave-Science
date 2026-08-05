---
node_id: "E-511"
canonical_name: "Chord Rotation"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Applied Dynamics and Stability"
claim_gate_detail: "GRAY root-relative coordinate operation / YELLOW One-Wave use"
metadata_standard: "I-06"
---

# Node E-511: Chord Rotation

Class: FUNCTION

Dependencies:
Upstream: E-510 Mirrored Music Clock
Downstream: E-512 Chord Coordinate Set

Definition:
Chord Rotation re-centers a chord on a selected root and assigns every chord tone an E-510 mirrored coordinate.

Procedure:
1. Select root `R`.
2. Set `R = 0`.
3. For every tone `T`, calculate `k = (T-R) mod 12`.
4. Convert `k` to `0..+5`, `-5..-1`, or shared `±6`.
5. Preserve every tone coordinate.
6. Preserve voicing, inversion, octave, amplitude, phase, and timing separately when available.

Canonical correction:
The output is a complete coordinate set, not automatically a compression-side / expression-side pair. Sign is route direction, not operation.

Examples:
- Major triad: `{0,+4,-5}`
- Minor triad: `{0,+3,-5}`
- Power chord: `{0,-5}`
- Augmented triad: `{0,+4,-4}`
- Diminished triad: `{0,+3,±6}`

Operational Chain:
E-510 Reference Frame => Re-center Root => Assign All Tone Coordinates => E-512 Coordinate Set

Yellow Audit:
- Root selection must be explicit for ambiguous chords.
- Pitch-class coordinates do not capture voicing or acoustic phase.
- Coordinate patterns alone do not establish force, direction, or stability.

Future Work:
Add progression traces and measured signal data without collapsing them into pitch-class position alone.

---
