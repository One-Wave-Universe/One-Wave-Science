---
node_id: "B-220"
canonical_name: "Scale Layer (Micro/Small/Medium/Large/Macro)"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Resolution / Formalization Node"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node B-220: Scale Layer (Micro/Small/Medium/Large/Macro)

Reason:
Definition complete (the five-scale requirement already exists repo-wide).
No mathematics exists yet connecting one scale to the next — this node
formalizes the requirement into a primitive, it does not yet solve it.

Dependencies:
Upstream: A-101 Ground / Zero (§8 Recursive Scaling — the original source of this requirement)
Bidirectional: E-507 Scale-Invariant Loop — NOT a one-way upstream/downstream
relationship. Both nodes converge on the same unresolved problem (deriving
γ(s) and β(s)) from different entry points; neither resolves first and
feeds the other. Solving γ(s)/β(s) resolves both nodes' open questions
at once. Drawing this as strictly one-directional (as an earlier version
of this file did) overstated the dependency.
Downstream: B-221 Six Recursive Steps (nested-recursion claim), all nodes whose own §8 Recursive Scaling section currently repeats this requirement without a shared primitive to point to

Definition:
Every A-series node (A-101 through A-113) independently states the same
requirement in its own §8 Recursive Scaling section: "Preserve [node]
meaning across Micro, Small, Medium, Large, Macro." This requirement has
been restated at least a dozen times across the repo and never given its
own primitive. B-220 is that primitive.

This node does NOT define Compression/Expression (B-203/B-204), does not
define the six-step cycle (B-221), does not define the Oscillation
Center (B-222), and does NOT define the Field Cycle (B-225) — the size
hierarchy (this node) and the phase cycle (B-225) are orthogonal axes,
explicitly not merged. A system state is (scale, phase), not one
five-way position shared between two different meanings of "five."
It defines only the scale dimension itself: what a scale
is, how scales relate to each other, and what "preserved across scales"
actually requires mathematically — none of which any existing node states.

Scale ordering (containment, not magnitude):
Micro ⊂ Small ⊂ Medium ⊂ Large ⊂ Macro
Each scale is assumed to be nested inside the next. This is stated
repo-wide by implication (B-221's "nested scale map" diagram shows this
same containment) but never formally defined as a relation.

Mathematics (candidate, largely undone — this is the honest state):
No scale-transition function exists anywhere in the repo in fully
derived form. But a real, more precise reframing exists via E-507
Scale-Invariant Loop (checked directly, not assumed): E-507 establishes
that the SAME update rule governs every scale —
ψᵢⁿ⁺¹ = ψᵢⁿ + (1-γ)(ψᵢⁿ-ψᵢⁿ⁻¹) + βᵢ(⟨ψⱼⁿ⟩-ψᵢⁿ) — with scale-dependent
γ(s) and β(s). This REFRAMES the transition question: it is not
"transform the state S from one scale to the next," it is "how do
γ and β themselves scale with s." E-507's own Yellow Audit already
flags this as unresolved ("whether gamma and beta scale in a
predictable way across scales") — the same open problem as B-220's
transition function, discovered independently, not yet connected
until now.

Corrected candidate form (replaces the earlier vaguer S_(n+1)=T(...)):
Scale ordering: S = {Micro, Small, Medium, Large, Macro}, by containment.
For scale index s, the transition question reduces to finding γ(s) and
β(s), NOT a separate function T acting on state directly. If γ(s) and
β(s) are known, the update rule itself (already real, from A-109/A-111)
handles the rest — no new transformation function needs to be invented.

Earlier candidate (kept for record, now understood as less precise):
S_(n+1) = T(S_n, C_n, R_n) — this was a reasonable guess at the shape
of an answer, but E-507 shows the real shape is narrower: solve for
γ(s), β(s) specifically, not a generic T.

WITHDRAWN CANDIDATE (added last turn, retracted this turn — flagged
as a mistake, not softened): a previous version of this section cited
Book 1 Ch15's electroweak/Planck lattice-step ratio (~10^17) as a
"candidate direction" for gamma(s)/beta(s). That was wrong to include,
not just under-confirmed. The ratio is anchored to Standard Model
particle-mass hierarchy (Higgs/W/Z boson masses) — a narrow slice of
subatomic energy scales with no actual bearing on the Micro/Small/
Medium/Large/Macro range this node needs, which spans cell-to-planet-
to-galaxy, not electroweak-to-Planck. The only thing the two share is
being called "a scale" in the loosest sense. Citing it dressed up an
irrelevant borrowed number as progress. Retracted rather than left
hedged, since hedging it would still leave it sitting here looking
like a lead worth following.

Relationship to B-221's nested-recursion claim:
B-221 claims each scale contains a COMPLETE six-step cycle, not just
the same label reused. If true, B-220's containment relation
(Micro ⊂ Small ⊂ ... ⊂ Macro) would need to hold not just for static
properties but for entire running cycles — a stronger and unverified
requirement. B-221 already flagged this as untested; B-220 is the
node responsible for actually defining the containment relation that
claim depends on, and does not yet do so.

Operational Chain:
A-101 §8 requirement (repeated repo-wide) => B-220 Scale Layer (this node, formalizes the requirement) => B-221 (uses it for nested-recursion claim)

Yellow Audit:
- No scale-transition function exists in fully derived form; but the
  question is now sharper (γ(s)/β(s) scaling, per E-507) than the
  earlier vague "find T" framing — real progress, not yet a solution
- WITHDRAWN this turn: an electroweak/Planck lattice-ratio candidate
  from Ch15 was cited here briefly and retracted — it's anchored to
  Standard Model particle-mass hierarchy, unrelated to the actual
  Micro-to-Macro range this node needs. Noted so the same borrowed
  number doesn't get re-added later without this context.
- Whether containment (Micro ⊂ Small ⊂ ...) is the right relation, versus
  some other relation (ratio, resolution, sampling rate), is not derived
- B-221's stronger nested-cycle claim depends on this node resolving the
  containment relation first — currently unresolved, so B-221's claim
  remains unverified pending this node
- Whether every A-series node's §8 section should be rewritten to cite
  this node instead of independently restating "Micro, Small, Medium,
  Large, Macro" each time is a real cleanup question, not yet decided —
  rewriting a dozen A-series nodes is a bigger change than this node
  alone should authorize

Future Work:
Derive γ(s) and β(s) scaling laws — this is the actual target now,
replacing the vaguer "define T" framing. E-507 already calls for
exactly this (its own Future Work lists deriving scaling laws for
gamma(s) and beta(s)) — this is one shared problem, not two.
Decide whether to retrofit A-101 through A-113's §8 sections to cite this
node rather than each independently restating the same five scale names.
Resolve the B-221 dependency once γ(s)/β(s) exist.

---
