---
node_id: "E-512"
canonical_name: "Chord Coordinate Set"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Applied Dynamics and Stability"
claim_gate_detail: "GRAY coordinate set / YELLOW shape interpretation"
metadata_standard: "I-06"
---

# Node E-512: Chord Coordinate Set

Former canonical name: Oscillation Window

Class: RESULT / DATA TYPE

Dependencies:
Upstream: E-511 Chord Rotation
Downstream: E-513 Musical Boundary Hypothesis Register

Definition:
A Chord Coordinate Set is the complete root-relative signed coordinate set produced by E-511.

Examples:
- Major: `{0,+4,-5}`
- Minor: `{0,+3,-5}`
- Power: `{0,-5}`
- Augmented: `{0,+4,-4}`
- Diminished: `{0,+3,±6}`

Canonical correction:
The former definition of Oscillation Window as a compression-side / expression-side pair is retired.

Reasons:
- sign does not equal compression or expression
- `±6` is shared between mirrored routes
- dyads do not require one tone on each side
- seventh and extended chords lose information when reduced to two extrema

The phrase “oscillation window” may still be used later for a measured time-dependent window, but it is not the canonical name for a static chord coordinate pair.

Operational Chain:
Chord Rotation => Complete Coordinate Set => Candidate Structural Questions

Yellow Audit:
- Coordinates are exact under the selected tuning and root.
- Labels such as symmetric Field, boundary dyad, or Mirror shape are interpretive and require tests.

Future Work:
Add measured phase, amplitude, duration, and transition data to determine whether genuine oscillation windows exist.

---
