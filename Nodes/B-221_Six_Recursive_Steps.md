---
node_id: "B-221"
canonical_name: "Six Recursive Steps (Master Cycle)"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Cycle and Relationship Structure"
claim_gate_detail: "YELLOW (proposed — new node, not yet cross-validated against instantiations)"
metadata_standard: "I-06"
---

# Node B-221: Six Recursive Steps (Master Cycle)

Dependencies:
Upstream: A+101 One Field Ground, A-101 Ground / Zero, A-105 Restoring Response (HOLD), A-108 Local Stability (HOLD's resolution back to BEGIN specifically), A-110 Oscillation (BREAK's crossing condition), A-111 Recursion (LOOP's candidate 1 for G — additive, unreconciled with candidate 2), C-301 Mirror Gate (LOOP's candidate 2 for G — rotational, unconfirmed, see LOOP section), D-402 Resonant Mode (BUILD's resolved Pattern term), B-220 Scale Layer (nested-recursion claim depends on B-220's containment relation), B-223 Three Moves (Loop-step composition), B-224 Two Choices (Loop-step decision)
Downstream: B-207 Threshold, B-206b Four Views (observation layer, additive cross-reference), B-203 Expression / B-204 Compression (Loop-step choice), B-222 Oscillation Center, G-719 Neural System Functional Analogy Map (partial-match comparison), all recursive operational chains repo-wide

Definition:
The Six Recursive Steps are the abstract six-stage cycle that every recursive
operational chain in the repository is expected to instantiate in some form.

Begin -> Move -> Hold -> Build -> Break -> Loop

This node does not replace any existing operational chain. It names the
pattern those chains already follow, so instantiations can be checked
against a single reference rather than each other.

STEPS (with candidate mathematical forms — all unverified except where a
form already exists in a real upstream node; see notes per step):

1. BEGIN — reference established. (Matches A-101 Ground / Zero role.)
   Form (real, inherited from A-101): ψ₀ = reference state

2. MOVE — difference introduced. (Matches A-102 Displacement / A-103 Differential role.)
   Form (real, inherited from A-101/A-102): Δψ = ψ − ψ₀

3. HOLD — response stabilizes. (Matches A-105 Restoring Response role.)
   Form (real, inherited from A-105):
   R_OW = -A(∇ψ), linear case: R_OW = -α∇ψ
   This is A-105's actual restoring-response math: HOLD is the step
   where the field's opposing response to gradient imbalance is
   active. "Stabilizes" specifically means the restoring force R_OW
   pushes back against ∇ψ — not merely that a value is held constant.

   IMPORTANT PRECISION (checked directly against real files): A-105's
   own equilibrium condition (∇ψ=0) means the field is UNIFORM — flat
   at any value, not necessarily matching BEGIN's specific reference
   ψ₀. HOLD does NOT by itself resolve back to BEGIN. The node that
   makes that connection real is A-108 Local Stability, whose entire
   stated purpose is "establishes whether a displaced state returns
   toward the Ground/Zero reference" specifically, not just toward any
   equilibrium. A-108 was already in the repo and already does this
   job — it had just never been cited from B-221's HOLD step before.
   Corrected form: HOLD (A-105) + A-108's condition together resolve
   toward BEGIN specifically. HOLD alone does not.

   Structural consequence: if HOLD's resolution point really is BEGIN
   (via A-108), the six steps are not a one-way line — they're an
   oscillation that returns to its own starting reference each cycle.
   This is consistent with, and may be the same phenomenon as, B-222's
   Oscillation Center and B-207's Threshold system. Not yet formally
   unified — flagged as a real structural candidate, not asserted.

4. BUILD — structure forms. (Matches D-402 Resonant Mode role — corrected
   from an earlier citation of A-107/A-108, which fit less well on
   inspection; see Mathematics below for the resolution.)
   Form (candidate, genuinely new — no existing node states this):
   Structure = Pattern + Persistence + Feedback
   This mixes three categories that should be cited, not owned by this
   node. Candidate citations, NOT all confirmed:
     Pattern — RESOLVED in favor of D-series, specifically D-402
       Resonant Mode (checked directly, not guessed): D-402's real
       definition is a mode that "returns to itself after k steps"
       (ψ_{n+k} = ψ_n) — a literal repeating, organized form. That's
       what "Pattern" means in this equation. The competing candidate,
       A-107/A-108, does NOT fit as well on inspection: A-107 is about
       confinement/boundedness, and A-108 is about returning-to-ground
       stability — already cited elsewhere in this node for HOLD's
       resolution back to BEGIN, a different job than "what pattern
       emerges." D-402 is the correct citation.
     Persistence — A-109 Inertial Memory. This one is solid.
     Feedback — A-105 Restoring Response / A-106 Pressure Response.
       NOT C-series — C-301 through C-308 are motion/momentum/spin
       mechanics (Mirror Gate, Momentum, Kinetic Energy, Torque, Spin-
       half), unrelated to feedback/response. A "C-layer response
       regulation" citation would be wrong; checked directly against
       the real C-series files and confirmed no match.
       UPGRADED: this citation now has real math to point to, not just
       a name — HOLD (step 3 above) was just upgraded to carry A-105's
       actual R_OW = -A(∇ψ). Feedback and Persistence are now BOTH solid
       (real math, real citation); only Pattern remains an unresolved fork.
   This is not derived from anything upstream as a SUM — no equation
   states how Pattern + Persistence + Feedback combine into Structure.
   But two of the three terms (Persistence, Feedback) now point to real
   confirmed single citation. Flagged fully in Yellow Audit below.

5. BREAK — transformation occurs. (Matches A-110 Oscillation / threshold-break behavior.)
   Form (real, inherited from A-110 — upgraded from the bare arrow
   "Old state -> altered state"):
   Memory contribution: Mᵢ = (1-γ)Δψᵢⁿ
   Crossing condition: |Mᵢ| < Rᵢ → return without overshoot (no break)
                        |Mᵢ| > Rᵢ → boundary crossing occurs (BREAK fires)
   This is A-110's actual operational rule: BREAK is not an arbitrary
   change, it's the specific case where accumulated memory contribution
   Mᵢ exceeds the restoring threshold Rᵢ. Below threshold, the step
   would just be HOLD returning to equilibrium; BREAK is specifically
   what happens when HOLD's restoring capacity is exceeded.
   Real dependency chain, not stated before: BREAK's condition depends
   directly on comparing against Rᵢ, which A-110 itself flags as
   undefined ("Restoring threshold Rᵢ requires derivation" — A-110's own
   Yellow Audit). So BREAK is now real math, but it inherits A-110's own
   open problem (Rᵢ undefined) rather than solving it.

   BRIDGE TO B-208 (built this turn — closes a real gap, not new bands):
   A-110's crossing condition and B-208's real threshold bands are two
   pieces of the same mechanism that had never been connected. Ownership
   stays clean: A-110 defines the crossing EVENT, B-208 defines the
   threshold LANDSCAPE, this node (B-221) defines BREAK's recursive
   role connecting them. Using B-208's REAL bands (100-90 through
   10-0, NOT the external five-band scheme, which was checked and
   discarded — see this node's earlier Yellow Audit entry on 42.5):
   - Approaching B-208's 45-30 "Break Risk / Decision Point" band =
     |Mᵢ| approaching Rᵢ (not yet crossed, evaluate)
   - Entering B-208's 30-15 "Break Condition" band = |Mᵢ| > Rᵢ
     confirmed (BREAK executes, transformation required)

   OPEN QUESTION (candidate, not derived): does the threshold band only
   answer "should transition happen," or does it also determine "how
   should transition happen" — i.e., does band position modify the
   transformation itself, not just gate it? Candidate form:
   New State = B(previous state, threshold position, crossing magnitude)
   where crossing magnitude = |Mᵢ| - Rᵢ. This B() function is entirely
   undefined — a candidate shape, not a solution. Flagged, not solved.

6. LOOP — cycle continues. (Matches A-111 Recursion role.)
   CORRECTION: an earlier version of this section called this step
   "RESOLVED." That was premature and is walked back here. There are
   now TWO candidates for G, and they are structurally different kinds
   of operations — they cannot both be "the answer" without more work:

   Candidate 1 — A-111's update rule (additive):
   ψᵢⁿ⁺¹ = ψᵢⁿ + (1-γ)(ψᵢⁿ-ψᵢⁿ⁻¹) + βᵢ(⟨ψⱼⁿ⟩-ψᵢⁿ)
   G(ψ_prev, M, C) = ψ_prev + M + C — plain addition, where
   M = (1-γ)(ψᵢⁿ-ψᵢⁿ⁻¹) (A-109's term) and
   C = βᵢ(⟨ψⱼⁿ⟩-ψᵢⁿ) (neighbor-coupling term).

   Candidate 2 — C-301's Mirror operator (rotational, not additive):
   M(ψ_C, ψ_E) → (ψ_E, -ψ_C), with M²=-I, M⁴=I (4π closure, same math
   as C-308 Spin-half). If G contains or equals this operator, LOOP
   does NOT return to BEGIN after one cycle — exact closure would
   require four cycles: ψ₀(n+4) = ψ₀(n), not ψ₀(n+1) = ψ₀(n).

   These are not reconciled. Addition and rotation are different kinds
   of operations; G cannot simply be both. Open question, explicitly
   not resolved: is G (a) the C-301 Mirror operator directly, (b) a
   composition containing Mirror alongside A-111's terms — candidate
   form G = Integration(Mirror, Memory, Coherence) — or (c) A-111's
   additive rule alone, independent of Mirror entirely? Only option
   (a) gives the clean four-cycle closure result. Until the operator's
   identity is established, C-301's closure period cannot be imported
   into LOOP, and A-111's additive form cannot be called the final
   answer either. Status: two candidates, not one resolution.

   TYPE-SIGNATURE FINDING (real progress, sharpens but does not close
   the fork — checked directly): A-111's update rule takes a single
   scalar ψᵢⁿ per site as input. C-301's Mirror takes a PAIR (ψ_C, ψ_E)
   as input. These are different types of objects — a scalar cannot be
   plugged directly into M(ψ_C, ψ_E) without first being split into
   two components. This means option (a), "G IS the Mirror operator
   directly," cannot be literally true unless ψ is shown to carry an
   implicit two-component structure everywhere, not just at boundaries
   where B-205/C-301 explicitly apply. Whether ψ has this implicit
   structure universally is itself unresolved — B-203/B-204
   (Expression/Compression) suggest every oscillating quantity might
   decompose this way, but this has never been stated as a general
   property of ψ, only demonstrated at specific boundaries. This makes
   option (b) — Mirror as a COMPONENT inside a larger G, not G itself —
   the more type-consistent candidate of the two, though still
   unconfirmed.

Per-Step Status Summary (CORRECTED — the first version of this summary
used GREEN/YELLOW in the colloquial traffic-light sense, which inverts
the repo's real GATE definition: GREEN=Defined is the LOWEST rung,
YELLOW=Constrained/Testable is a step ABOVE it, confirmed from A-101/
A+101's own §12 sections. Nothing here has reached BRONZE=Validated —
no empirical testing has occurred on any of these six steps. So all
six are properly YELLOW, not five-GREEN-one-YELLOW):
YELLOW, single confirmed candidate (constrained, testable, one answer):
  BEGIN, MOVE, HOLD, BUILD, BREAK
YELLOW, open fork (constrained, testable, but multiple competing
  candidates not yet decided between):
  LOOP — A-111 additive vs. C-301 rotational
The real distinction is single-candidate vs. open-fork, not a maturity
gap. Landing at YELLOW with a real testable fork is not behind the
other five steps — it's the same rung, describing a genuinely harder
question.

Mathematics:
STATUS UPDATE (final honest count as of this turn): four of six steps
(BEGIN, MOVE, HOLD, BREAK) carry real, fully resolved math with no open
operator-identity question. BUILD now has all three terms resolved to
real cited nodes (Pattern -> D-402, Persistence -> A-109, Feedback ->
A-105/A-106) — only the SUM itself (how three real terms combine into
one Structure equation) is undefined, a smaller and more specific gap
than the earlier unresolved citation. LOOP has two competing,
unreconciled candidates for its operator G (A-111 additive vs. C-301
rotational). Six steps, six honest states: five resolved or narrowly
scoped, one (LOOP) with a real fork still open.

Known Instantiation — B-207's Operational Chain:
Paired Loop => Four Views => Threshold => Evaluation (G-702) => Modulation (G-703) => Return or Break

This is the clearest existing six-stage match in the repo, but the
step-for-step correspondence to Begin/Move/Hold/Build/Break/Loop has not
been formally verified term-by-term. Treat as a strong candidate
instantiation, not a confirmed one.

Known Instantiation — A-101 through A-113 chain:
The thirteen-node A-series chain (A-101 through A-113) does not divide
evenly into six steps. Any mapping from the 13-node chain onto this
6-step cycle is provisional and requires grouping multiple A-nodes per
step (as sketched above), not a 1:1 correspondence.

Operational Chain:
One Field (A+101) => Ground (A-101) => [Six Recursive Steps] => Recursion (A-111) => Persistent Mode (A-112)

Yellow Audit:
- Step-for-step correspondence to B-207's chain not formally verified
- Grouping of the 13 A-series nodes into 6 steps is provisional, not confirmed
- Whether this cycle is meant to be scale-invariant (same 6 steps at every
  Micro/Small/Medium/Large/Macro level) is asserted by analogy to
  B-206b's scale-invariance claim, not independently derived here
- Relationship to B-220 Scale Layer is now formalized: B-220 defines the
  scale dimension (containment relation between Micro/Small/Medium/Large/
  Macro), this node defines the cycle dimension. B-220 flags that the
  nested-recursion claim above depends on its own unresolved
  scale-transition function — so this node's nested-recursion claim
  remains unverified pending B-220, not independently confirmed
- NEW: whether the "six steps" are better modeled as an oscillation
  returning to BEGIN (via A-108's resolution of HOLD) rather than a
  one-way line is a real structural question raised this session,
  not yet formally unified with B-222 Oscillation Center or B-207
  Threshold, both of which describe similar return-to-center behavior
- BUILD's Pattern term is now RESOLVED (D-402 Resonant Mode, checked
  directly — see STEPS/Mathematics above), Persistence is solid
  (A-109), and Feedback is solid (A-105/A-106). All three of BUILD's
  terms are now cited to real, checked nodes — only the SUM itself
  (how Pattern + Persistence + Feedback combine into Structure) remains
  undefined, which is a different and smaller gap than the earlier
  three-way ambiguity.
- LOOP is NOT resolved (correcting an earlier overclaim in this same
  file): A-111's additive rule gives one candidate for G, but C-301's
  Mirror operator gives a structurally different candidate (rotation,
  not addition), with a real consequence if it applies — 4-cycle
  closure (ψ₀(n+4)=ψ₀(n)) rather than 1-cycle return to BEGIN. Which
  candidate is correct, or whether G is a composition of both, is
  open. Do not cite this section as settled; cite it as "real progress,
  two candidates, operator identity unresolved."

SHARPER NESTED-RECURSION CLAIM (new, more specific than the scale-invariance
line above — needs its own verification, not assumed true by inheriting it):
Each of the five scales is claimed to contain its own COMPLETE six-step
cycle, not just the same six labels applied loosely at different sizes.
A micro-scale event would contain a full Begin-Move-Hold-Build-Break-Loop
cycle nested inside one step of a macro-scale cycle. This is a stronger,
more specific, and more testable claim than plain scale-invariance — it
predicts actual nested cycle structure, not just repeated terminology.
Not yet checked against any real instantiation in the repo.

FOUR VIEWS CROSS-REFERENCE:
B-206b's Four Views (Inward/Outward/Across/Over) are proposed as the
observation layer for any instance of this six-step cycle — i.e., a
given Begin-Move-Hold-Build-Break-Loop cycle can be examined from all
four views. This is additive to B-206b, not a redefinition of it.

CHOICE MECHANISM AT LOOP (sharpens Step 6):
The LOOP step's choice between Compression and Expression is now framed
as a full traversal through a center, not a bare binary pick:
Compression path: Expression -> Center -> Compression
Expression path: Compression -> Center -> Expression
Whether "Center" here is B-201 Equilibrium Balance (the scalar equilibrium measure)
or a distinct dynamic-state concept that merely shares the word "Balance"
is now tracked as its own node — see B-222 Oscillation Center — rather
than left as an unresolved question inside this one.

Future Work:
Establish G's operator identity: is it A-111's additive rule, C-301's
Mirror rotation, a composition of both, or something independent of
both? Only once this is answered can LOOP's closure behavior (1-cycle
vs. 4-cycle) be stated as more than a conditional candidate.
Formally verify the B-207 correspondence term-by-term.
Determine whether the 13-node A-series chain should be explicitly
regrouped into six labeled phases, or whether this node should stay a
higher-level abstraction layered on top without renaming any A-series node.
Test the nested-recursion claim against at least one real instantiation
before treating it as more than a proposal. First named candidate:
apply the complete Begin -> Move -> Hold -> Build -> Break -> Loop cycle
to one real group or company decision process. Identify the local
boundary, state variables, inputs, modulation actions, break condition,
loop closure, and the macro-scale step containing the local cycle. Track
this under I-04 as a Scale-Specific Instance with secondary status
Unproven Delta until the mapping is completed.
Resolve the Balance/Balance naming question before citing B-201 as the
"Center" in the choice mechanism above.

---
