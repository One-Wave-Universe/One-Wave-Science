---
node_id: "E-510"
canonical_name: "Music Clock Harmonic Oscillation"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Applied Dynamics and Stability"
claim_gate_detail: "YELLOW (proposed — new node, elaborates existing A-111 content)"
metadata_standard: "I-06"
---

# Node E-510: Music Clock Harmonic Oscillation

Class: FUNCTION

Not a book chapter. Not a book node.
This is a reusable function node within Appendix E, in the same class as
other Appendix E functions (E-501 through E-509).

Term disambiguation:
"Chord" in this node refers exclusively to a musical chord (e.g., A Major).
It is unrelated to "Operational Chain" (the standard per-node dependency
field used throughout the repo) and unrelated to "Chapter" (a Book
document-structure unit). No cross-meaning is intended anywhere in this node.

Dependencies:
Upstream: A-111 Recursion (Harmonic Mapping / Four Harmonic Behavior Axes sections)
Lateral: G-721 Mirrored Alphabet Rabbit-Hop Coordinate Algorithm (separate symbolic coordinate system)
Downstream: E-511 Chord Rotation

Separation rule:
The Music Clock and G-721 must not be collapsed. The Music Clock supplies a 12-position harmonic/movement relation. G-721 supplies A-to-Z symbolic identity and mirrored recursive coordinates. A later compiler may connect them, but neither one is the other.

Definition:
The Music Clock is a rotational coordinate system for harmonic relationships,
built on the 12-tone equal-temperament relation already stated in A-111:

f_n = f_0(2^(n/12))

A-111 established root distance, octave position, interval ratio, and
oscillation width as the quantities to track, and named the Major/Minor,
Forward/Backward axes. This node formalizes those into a signed 12-position
clock centered on a chosen root.

CLOCK REFERENCE:
Root position (12 o'clock) = (0), the harmonic zero reference —
this is a root-relative instance of the same Ground/Zero pattern used
throughout the repo (Δψ = ψ − ψ₀, from A-101), applied to pitch instead
of field displacement.

Clockwise rotation = positive displacement (Expression direction, per B-203/B-204 convention)
Counter-clockwise rotation = negative displacement (Compression direction)

SIGNED POSITIONS (example, root = A):
Clockwise:  A(0) -> A#(+1) -> B(+2) -> C(+3) -> C#(+4) -> D(+5)
Counter-clockwise: A(0) -> G#(-1) -> G(-2) -> F#(-3) -> F(-4) -> E(-5)
Opposite pole (6 o'clock) = (-0-), the mirror/inversion reference —
this is the same Mirror operation as B-205, applied to the harmonic clock.

VERTICAL DIAGRAM CONVENTION (added, consistent with the confirmed
values above — this is a display convention, not a new claim):
For a given chord, its Expression-side tone (positive position) is
drawn on top, its root at center, and its Compression-side tone
(negative position) on the bottom:

        C# (+4)
          |
        A  (0)
          |
        E  (-5)

Positive/Expression = up. Root = center. Negative/Compression = down.
This matches the earlier cross-style diagrams used for the worked
Major/Minor examples, now stated as an explicit convention rather than
left implicit in each individual diagram.

OCTAVE BOUNDARY / WRAPAROUND (added — closes a real gap: this clock
was previously only defined for positions 0 through ±5, meeting at
the shared 6 o'clock mirror point, with no stated behavior beyond that
boundary):

Octave transition:
f(n+1) = 2 * f(n)

When clock position would extend past +5 or -5 (i.e., past the G#/A
boundary in either direction), the position wraps: the coordinate
repeats (A is A again), but the scale has changed by one octave
(frequency doubled or halved). This is the same "same recursive
structure, different scale" principle already established for A-111/
E-507 — applied here specifically to the clock's own boundary rather
than left unstated.

Consequence: the Music Clock is not a single fixed 12-position ring.
It is one ring repeated at every octave, with position 0 (root)
recurring at every doubling of frequency. A chord tone that would
"fall off" the ±5 boundary does not leave the system — it re-enters
at the corresponding position one octave up or down.

Mathematics:
No independent mathematics beyond the clock positions above. The operation
that uses this coordinate system — re-centering an arbitrary chord onto it —
is defined separately in E-511 Chord Rotation, since a reference system and
the function that operates on it are distinct (same split as A-101 Ground/Zero
vs A-102 Displacement, or C-301 Mirror Gate vs B-205 Mirror).

Operational Chain:
A-111 Harmonic Mapping => Music Clock (reference frame) => E-511 Chord Rotation (function)

Yellow Audit:
- Relationship between clock position and actual perceived consonance/dissonance not derived, only positional
- Connection to the guitar-signal physical validation goal (waveform/frequency measurement) not yet built — this node is currently music-theory-level, not signal-level
- Relationship to B-206b's Four Views (Inward/Outward/Across/Over) not yet mapped, despite conceptual similarity to Compression/Expression framing

Future Work:
Connect clock positions to actual measured guitar frequencies (bridge to the Wave Reader hardware work).
Determine whether this node should formally cite B-203 Expression / B-204 Compression as upstream, given the shared directional convention.

---
