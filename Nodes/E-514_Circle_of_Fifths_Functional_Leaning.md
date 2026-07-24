---
node_id: "E-514"
canonical_name: "Circle of Fifths Clock and Functional Leaning"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Resolution / Formalization Node"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node E-514: Circle of Fifths Clock and Functional Leaning

Reason:
A complete, internally coherent system, distinct from E-510's clock.
Genuinely new content, well-organized, but entirely unvalidated against
anything upstream — this is music theory convention formalized into
this repo's vocabulary, not derived from the field equations the way
A-105/A-109 were checked against Book 1's claims.

CRITICAL DISAMBIGUATION (read first — this is a real, active naming
collision, resolved by keeping both, not merging):

"Clock" — E-510 is a CHROMATIC clock (12 semitones: A,A#,B,C...),
used PER-CHORD (rotates one chord's root to zero, reads where that
chord's other notes land). This node's clock is a FIFTHS clock (12
positions ordered by perfect fifths: C,G,D,A,E...), used PER-KEY
(tracks how far a whole progression wanders from a tonic across a
song). Different ordering, different scope. Not the same clock
wearing two names — genuinely two different tools.

"Leaning" — E-513 uses "leaning" for a single chord's internal
compression/expression asymmetry. This node uses "leaning" for a
chord's FUNCTIONAL ROLE within a key (Tonic/Subdominant/Dominant).
Different concept, same word. Do not merge.

Real correspondence (checked, not just shared vocabulary): E-510's
"6 o'clock = mirror/inversion point" and this node's "6 o'clock =
tritone = maximum instability" occupy the SAME structural role
(maximum distance from root) on two DIFFERENT underlying clocks. This
is a genuine structural parallel, not a coincidence of both using
"6 o'clock" — worth noting, not worth merging the clocks over.

Dependencies:
Upstream: none (independent music-theory formalization, not derived from field equations)
Downstream: none yet (proposed)

Definition:

PART 1 — The Fifths Clock:
12 positions ordered by ascending perfect fifths, not chromatic
semitones: C(12)-G(1)-D(2)-A(3)-E(4)-B(5)-F#/Gb(6)-Db(7)-Ab(8)-Eb(9)-Bb(10)-F(11)-back to C(12).
Clockwise (+1 per step) = add a sharp, move up a fifth: brighter,
forward momentum.
Counter-clockwise (-1 per step) = add a flat, move down a fifth (up a
fourth): heavier, grounding pull.
6 o'clock = the tritone position, maximum distance from home, maximum
instability — the point furthest from any tonic before the system
must fall back.

PART 2 — Functional Leaning (within a key, distinct from E-513):
Tonic (I) — the ground state, 12 o'clock, zero stored tension.
Subdominant (IV) — outward lean, one step counter-clockwise (11
o'clock), departs from home without urgency.
Dominant (V) — inward gravitational pull, one step clockwise (1
o'clock), maximum functional tension wanting to collapse back to I.

PART 3 — The Recursive Songwriting Pipeline:
Stability (hit I) => Triadic Modulation (move to IV) => Peak Stored
Tension (hit V, or pivot through vi) => Recursive Reset (turnaround
chord sharing overtones with both peak and ground) => back to Stability.

This is explicitly framed (correctly, and worth keeping) as a
practical bridge from the abstract recursive-cycle math (B-221's six
steps) into actual songwriting: tension and release as the audible
form of build-and-break.

Mathematics:
No independent field-equation mathematics. This is music theory
(functional harmony, circle of fifths) restated in this repo's
vocabulary (tension, ground state, recursive reset). It is NOT derived
from A-105/A-109/etc. the way E-510 at least attempts to connect to
A-111's harmonic mapping. This is a real difference in grounding level,
not a criticism of the content's internal coherence — it's genuinely
well-organized, just not connected upstream to anything yet.

Candidate structural parallel to B-221 (reframed — "may instantiate,"
not "equals" or "is caused by"; this replaces an earlier, tighter
mapping that overstated the connection):

Songwriting may instantiate the same recursive structure B-221
describes, not be evidence that one causes the other. A more general,
defensible mapping than the earlier I-IV-V-turnaround-specific version:

BEGIN — establish tonal center
MOVE — introduce contrast
HOLD — maintain motif
BUILD — increase harmonic complexity
BREAK — maximum tension
LOOP — resolve or modulate into the next cycle

This is looser than the original Tonic/Subdominant/Dominant-specific
mapping (Stability~BEGIN, Triadic Modulation~MOVE, etc.) and
deliberately so — it describes a structural correspondence without
claiming the six-step math derives songwriting practice, or that
following I-IV-V is the only way to instantiate the pattern. Still
unverified term-by-term, same as before; the claim itself is just
stated more carefully now.

Operational Chain:
Tonic (I) => Subdominant (IV) => Dominant (V) => Recursive Reset => Tonic (next cycle)

Yellow Audit:
- Entirely disconnected from the field-equation layer (A-series,
  B-221 update rule) — this is formalized music theory, not derived
  physics-analog math, and should not be cited as if it were
- The candidate B-221 correspondence (Stability~BEGIN etc.) is
  unverified — real work needed before treating it as confirmed
- No connection yet to E-510/E-511/E-512/E-513's chromatic, per-chord
  system despite both existing in the same appendix — by design, per
  the disambiguation above, but worth flagging that a reader could
  still expect them to connect and currently won't find that link

Future Work:
Check the candidate B-221 correspondence term-by-term, the same rigor
used for B-207.
Determine whether any real connection between the fifths-clock system
and the chromatic per-chord system (E-510-513) exists, or whether they
should remain fully independent by design.

---
