---
node_id: "E-513"
canonical_name: "Chord Leaning Direction"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Resolution / Formalization Node"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node E-513: Chord Leaning Direction

Reason:
New claim, checked against real corrected E-512 values, partially
confirmed. The mechanism for the power-chord "flip" is stated but not
fully derived — flagged honestly below.

Term disambiguation (read first): "Leaning" here means the directional
asymmetry of a single chord's Oscillation Window (E-512) — whether its
compression side or expression side dominates. This is UNRELATED to a
separate "leaning" concept describing chord function within a key
(Tonic/Subdominant/Dominant roles) — see E-514 Circle of Fifths, which
uses "leaning" for that different, key-level concept. Do not merge
these two uses of the word.

Dependencies:
Upstream: E-512 Oscillation Window
Downstream: none yet (proposed)

Definition:
A chord's Oscillation Window (P_compress, P_expr) has a directional
lean when |P_compress| != |P_expr| — one side pulls harder than the
other.

Checked against corrected real values:
A Major: (P_compress=-5, P_expr=+4). |−5| > |4|. Compression dominates.
A Minor: (P_compress=-5, P_expr=+3). |−5| > |3|. Compression dominates,
  more strongly than Major (gap of 2 instead of 1).

Both tested chords lean backward (toward compression) — this matches
the claim that standard triads have "natural movement built in" toward
resolution/compression. Confirmed for these two data points, not yet
tested beyond them.

Power chord claim (stated, NOT fully derived — this is the honest gap):
A power chord (root + fifth, no third) is proposed to become
forward-leaning (toward expression) when the sign convention is
flipped. The mechanism for WHY removing the third and flipping the
convention produces this is not mathematically derived here — it is
asserted based on the absence of the third's compression pull, not
shown to necessarily follow from E-510/E-511's actual math. Flagged
as the primary open item.

Mathematics:
Generalized lean formula (replaces the earlier two-point-only version,
verified against both real data points — extends beyond triads without
needing a new rule per chord type):

L = Σ|negative positions| - Σ|positive positions|

L > 0: backward lean (compression dominates)
L < 0: forward lean (expression dominates)
L = 0: balanced, no lean

A Major: L = |-5| - |4| = 1 (mild backward lean) [verified]
A Minor: L = |-5| - |3| = 2 (stronger backward lean) [verified]

This sums ALL negative and ALL positive chord-tone positions, not just
a single compression/expression pair — so it generalizes cleanly to
seventh chords, extended chords, or anything with more than one tone
on each side, without inventing a special case per chord type.

Power chord applicability (reframed — this is a real Yellow-node gap,
not a failure to derive):
Current applicability:
  Triads: Verified (2 data points, A Major/A Minor)
  Power chords (root + fifth, no third): UNDEFINED, not undetermined.
    Reason: the Oscillation Window / lean formula requires at least
    one tone on each side of the root to produce a meaningful sum.
    A power chord has only one non-root tone (the fifth), so there is
    nothing to sum against. This is a genuine scope boundary of the
    current definition, not a problem to force an answer to.

Operational Chain:
E-512 Oscillation Window => E-513 Chord Leaning Direction (this node) => [songwriting application, not yet built]

Yellow Audit:
- Only 2 data points (A Major, A Minor) — same limitation E-512 already
  flagged, inherited here
- Power chords are UNDEFINED under the current lean formula (not a
  failed derivation) — a genuine scope boundary, since the formula
  needs at least one tone per side to produce a sum. The original
  "flip -/+ for forward-leaning power chord" claim is not evaluable
  as stated until power chords get their own applicable definition
- Whether minor chords always lean more backward than major (L=2 vs
  L=1 in this one data point) is a real, testable, currently
  unconfirmed pattern

Future Work:
Define what an Oscillation Window means for a chord with no third
(power chords, and by extension any two-note structure) before the
power-chord claim can be tested at all.
Test the L formula against more chord qualities and roots.
Check whether minor-leans-more-backward-than-major holds generally.

---
