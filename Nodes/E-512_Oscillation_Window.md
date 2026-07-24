---
node_id: "E-512"
canonical_name: "Oscillation Window"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Applied Dynamics and Stability"
claim_gate_detail: "YELLOW (proposed — new node, split out from E-511)"
metadata_standard: "I-06"
---

# Node E-512: Oscillation Window

Class: FUNCTION (output/result type — not an operator itself)

Not a book chapter. Not a book node.
This is the result state produced by E-511 Chord Rotation, given its own
node because it is consumed downstream independently of the function that
produces it — the same relationship as A-104 Gradient's output feeding
A-105 Restoring Response as a distinct stage, rather than staying folded
inside Gradient itself.

Dependencies:
Upstream: E-511 Chord Rotation
Downstream: E-513 Chord Leaning Direction

Definition:
An Oscillation Window is the signed pair of positions that a chord
produces once Chord Rotation (E-511) has re-centered it on the Music
Clock (E-510):

Oscillation Window = (Compression-side position, Expression-side position)

It is a per-chord result, not a coordinate system and not a function. It
is what a chord looks like after being run through Chord Rotation, held
as its own value so it can be compared across chords, tracked over time,
or fed into whatever consumes it next — none of which is yet defined.

Mathematics:
For a given chord with root at (0):

Window = (P_compress, P_expr)

where P_compress and P_expr are signed clock positions from E-510,
produced by E-511's rotation procedure.

Worked values, corrected this turn (checked against E-510's real clock;
the original build had both the sign and the compression/expression
assignment backwards):
A Major: Window = (P_compress=-5, P_expr=+4)
A Minor: Window = (P_compress=-5, P_expr=+3)

Observed pattern (corrected — the fixed and shifting sides are swapped
from the original claim, still unconfirmed beyond two data points):
Compression-side position (the fifth, E) appears to stay fixed at -5
across Major/Minor. Expression-side position (the third) shifts: C#
at +4 for Major, C at +3 for Minor. The underlying discovery is the
same as before — one side holds, the other moves by one semitone
between Major and Minor — but which side is fixed and which shifts
was previously reported backwards. Whether this holds as a general
rule or is specific to this one root and these two chord qualities is
still not known — see Yellow Audit.

Operational Chain:
E-511 Chord Rotation => Oscillation Window (per chord) => [not yet defined downstream use]

Yellow Audit:
- Only two data points exist (A Major, A Minor on root A) — nowhere near enough to call the "expression side fixed at +5" pattern a rule
- No downstream consumer defined yet — this node currently terminates the chain
- Whether Oscillation Window should be tracked over time (e.g., across a chord progression) or only evaluated per-chord in isolation is unresolved
- No connection yet to B-208 Threshold Windows despite the shared "Window" terminology — these are NOT the same concept and should not be assumed related without checking; flagging explicitly to avoid a repeat of the earlier Mirror/Mirror Gate and Balance/Balance naming confusion

Future Work:
Gather more chord-quality data points (diminished, augmented, seventh chords, other roots) before treating the +5/-4/-3 pattern as anything more than a two-point observation.
Define what, if anything, consumes an Oscillation Window downstream.
Explicitly confirm or rule out any relationship to B-208 Threshold Windows given the name overlap.

---
