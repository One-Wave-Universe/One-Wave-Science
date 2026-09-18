## Node I-02: Node Proof & Trust Lifecycle

Status: GREEN (by this node's own definition — see Special Rules below for why this is its honest ceiling)

Classification: Special Rules Node

Verification note (added before adopting this node): "Brown" was
checked against real prior usage rather than accepted on assertion.
Confirmed present in three separate Book 1 chapters (Ch2, Ch4, Ch11),
always meaning "below Green, not yet operationally defined" — this
node is the first place that formally defines what was previously
scattered, informal usage. Real precedent, not an invented term.

Relationship to I-01: I-01 catalogs audit/construction discipline
rules (don't invent primitives, verify citations, etc.). This node
formalizes a different thing — the stage lifecycle itself. Kept
separate rather than merged, same principle applied to every other
node pairing tonight (E-510 vs E-513, B-220 vs B-225, etc.).

Relationship to the previously-confirmed Gate Ladder (from A-101/
A+101's own §12 sections: GREEN=Defined, YELLOW=Constrained/Testable,
BRONZE=Validated, SILVER=Integrated, GOLD=Confirmed): this node
extends that confirmed ladder rather than contradicting it. Brown adds
a rung below Green; the Yellow/Bronze/Silver/Gold advancement
conditions given below are consistent with, and sharpen, the
definitions already confirmed elsewhere in the repo. I-01's Rule 2
should defer to this node's fuller formalization going forward rather
than restate the simpler version.

---

Purpose:
Every node and book chapter must carry a single, unambiguous claim
about how proven it is, separate from what kind of work has been done
on it. This node defines that claim formally — the stage a node/
chapter occupies, the order stages must be passed through, and the
one conditional transform (Gray to Red) that ties the lifecycle to
actual experimental confrontation with the Standard Model rather than
internal math alone.

Definition:
Let a node or book chapter be an object x. Define the stage function

sigma(x) in S

where S is the ordered set of proof stages:

S = {Brown, Green, Yellow, Bronze, Silver, Gold}

with strict order:

Brown < Green < Yellow < Bronze < Silver < Gold

For book chapters specifically, Green is replaced by a parallel state
Gray, occupying the same position:

Brown < Gray < Yellow < Bronze < Silver < Gold (chapters only)

Gray is not a synonym for Green. Green certifies the underlying math
has room to grow and is ready for work. Gray certifies a
documentation discipline: that the chapter has stated its
relationship to the Standard Model without omission.

Mathematics:

Gray comparison, three-valued, over chapter x and Standard Model
reference point r:

C(x,r) in {DirectEquivalent, PartialEquivalent, NoEquivalent}

C must be stated for every chapter; never left undefined.

E(x,r) = the experimental result confronting the Standard Model at
comparison point r. E is undefined until an experiment is actually
run — E is not a function of math alone.

The Red transform:

sigma(x) -> Red  iff  sigma(x) = Gray  AND  E(x,r) is defined  AND
E(x,r) forces the negation of the Standard Model at r

Red is only reachable from Gray, and only when a real, defined
experimental result forces that negation. No other stage transforms
into Red. Yellow's internal consistency, however clean, does not
satisfy this — Yellow has no defined E term.

NoEquivalent branch, explicit choice not terminal state:

C(x,r) = NoEquivalent implies x in {Brown, Grow(x)}

where Grow(x) means building x out into something not derived from or
mapped onto the Standard Model at all. NoEquivalent has no forced
outcome.

Advancement conditions:

Brown -> Green/Gray  iff  x has a template slot and an ID
Green -> Yellow  iff  math for x is built and internally tested
Gray -> Yellow  iff  C(x,r) is stated for every r, without omission
Yellow -> Bronze  iff  simulation run AND metadata attached AND first successful validation
Bronze -> Silver  iff  validated in a second, independent application
Silver -> Gold  iff  extraordinary, extensive validation across applications
Gray -> Red -> Gold  iff  as defined above

Operational Chain:
Brown (slot exists, undefined) => Green/Gray (defined) => Yellow (tested) => Bronze (validated once) => Silver (validated twice) => Gold (extraordinarily validated)
Parallel branch: Gray => Red (only if a real experiment forces SM negation) => Gold

Interpretation:
The lifecycle has exactly one place where the model touches reality
rather than its own internal consistency: Gray to Red. Every other
transition can in principle be satisfied by work done entirely inside
the framework. Red cannot — it requires E(x,r) to be defined, which
requires an experiment to have actually been run. This is deliberate:
a node is never permitted to assert "the Standard Model fails here"
from math alone, no matter how elegant the derivation. Red is a
record of an outcome, not a claim of victory.

Dependencies:
Upstream: None. This is a governance node, not a physical claim — it
does not derive from psi, the lattice, or the update rule.
Downstream: Every node's Status field and local Special Rules section
across A through G. Every book chapter's Gray comparison section. Any
future audit tooling reading or assigning sigma(x).

Assumptions (stated explicitly, not hidden):
1. Every node/chapter can be assigned exactly one sigma(x) at a time —
   stages do not overlap. A future composite object (built from
   sub-nodes at different stages) may need to challenge this.
2. E(x,r), when defined, is a genuine outside result — not derived
   from or fitted to One-Wave itself.
3. The comparison point r is specific enough that C(x,r) and E(x,r)
   are both well-defined, not vague resemblance claims.

Candidate Experiment (a real, runnable check on this node's own logic):
1. Enumerate every book chapter currently carrying a Gray tag.
2. For each, check whether E(x,r) is defined for any r.
3. Confirm sigma(x)=Red has not been assigned to any chapter where
   step 2 returns undefined for all r.
4. Flag any chapter marked Red without a defined E(x,r) as a template
   violation, not a valid stage.
Not yet run — this is the procedure, not the result.

Yellow Audit:
- Whether Gray-turns-Red extends to nodes as well as chapters is not
  resolved here — carried forward, not assumed
- The Candidate Experiment above has not actually been run against
  the real repo yet — every currently-Gray Book 1 chapter should be
  checked against it before trusting that no template violation exists

Special Rules (local to this node):
- This node's own sigma cannot reach Yellow/Bronze/Silver/Gold the way
  a physics node does, because it makes no falsifiable claim about
  psi. Its ceiling is Green by design, not an unmet test — a boundary
  exception, not an open failure.
- The Red transform applies to OTHER nodes/chapters; it does not apply
  reflexively to this node, since this node has no Standard Model
  comparison point r of its own.

Final Lock:
Locked at Green: structurally complete, internally consistent,
terminology stable, ready for use as the standard other nodes and
chapters are checked against. Not Gold — a rules node doesn't undergo
the same experimental confrontation a physics node does. Green is the
honest ceiling for this node's own claim about itself.

---

Addendum: Chapter Section-Label Collision, Resolved

A proposal was made to restructure each Book chapter's INTERNAL
sections using color names — Gray (Standard reference), Blue (2D),
Green (3D), Yellow (Predictions), Bronze (Engineering implications),
Silver (Experimental tests), Gold (Validated results only).

This directly collides with this node's own vocabulary: Green,
Yellow, Bronze, Silver, and Gold are already defined here as
WHOLE-NODE/CHAPTER PROOF STAGES (sigma(x)), not per-section labels
within a single chapter. Using the same five words for two different
jobs — one chapter's internal structure, and every object's overall
trust level — would make every future reference to "this chapter's
Bronze section" versus "this chapter's Bronze stage" ambiguous.

RESOLUTION: rejected. The existing chapter spine (Gray / 2D / 3D /
Mathematics / Predictions / Yellow Audit / Future Work / Closing
Thoughts) — already in use across all 17 real Book 1 chapters —
remains the only per-chapter section template. It does not use Bronze,
Silver, or Gold as section names, and "Yellow Audit" is a section
title, not a claim that the chapter's overall stage is Yellow. No
chapter section should be renamed to match this node's stage
vocabulary. The two systems (chapter structure, proof stage) stay
visually and terminologically distinct on purpose.

---
