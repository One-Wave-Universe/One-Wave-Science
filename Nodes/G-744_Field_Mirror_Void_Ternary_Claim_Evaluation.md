---
node_id: "G-744"
canonical_name: "Field / Mirror / Void Ternary Claim Evaluation"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Evaluation Architecture / Truth Computer / Ternary Decision"
claim_gate_detail: "Architecture defined; scoring and calibration not yet empirically validated."
metadata_standard: "I-06"
---

# Node G-744: Field / Mirror / Void Ternary Claim Evaluation

## Reconciliation Note (read before the architecture below)

This node arrived as a fully-drafted proposal alongside G-745 and
G-746, with an explicit instruction not to trust its dependency
citations without checking them against the existing G-series
evaluation chain and an existing, already-built Truth Computer
implementation. That check changed this node's dependency structure
and added the boundaries below; the core architecture is otherwise
preserved as drafted.

1. **G-702 Evaluation already asks the question this node answers, and
   is the correct primary upstream, not a peer citation.** G-702's own
   Yellow Audit states: "Whether Evaluation is binary (act/don't act)
   or graded unresolved." This node's ternary `{-1, 0, +1}` is a
   defensible candidate answer to that specific open question — for
   claim evaluation specifically, not for G-702's general
   differential-significance evaluation. G-702 has been moved to
   primary upstream accordingly.
2. **This node does not resolve G-712 Evaluation Mathematics' open
   significance-threshold and signal-classification questions.** G-712
   asks a related but distinct question (is a differential significant
   enough to act on at all, e.g. its candidate
   `E_pattern/E_noise > 1` form) that belongs to the general
   field-update evaluation cycle. This node's ternary state answers "is
   this specific claim, given this specific evidence, supported,
   refuted, or unresolved" — a claim-evaluation question, not a
   signal-detection question. The two must not be treated as the same
   problem restated; G-712 stays open on its own terms.
3. **G-711 Gate 7's "Root Split: Void -> Evaluate, Field -> Modulate"
   uses "Field" and "Void" for a different referent than this node
   does.** G-711's Field/Void names which *function* (evaluate vs.
   modulate) a repository-review step performs. This node's Field/Void
   name the *outcome* of a per-claim ternary evaluation (+1/-1), with
   Mirror as the third, hold state. Same words, different roles — not
   merged, and any future reader must not assume G-711's split
   determines this node's states.
4. **G-718 Connection Gates, cited in the original draft, has been
   dropped from this node's dependencies.** G-718 is a seven-gate
   framework for two independent systems connecting relationally
   (Invitation, Truth, Recognition, Synchronization, Choice, Respect,
   Connection) — a genuinely different domain from claim/evidence
   evaluation, and no operational overlap was found on inspection. If
   a real connection exists it has not yet been shown; re-add only
   with an explicit mapping, not by proximity of subject matter.
5. **An existing, already-built "Truth Computer" implementation exists
   in this repository** at `Nexus_Integration/Truth_Computer/`
   (`og-system.json`, `truth-computer-core.js`,
   `truth-computer-panel.js`, version "Updated 41," predating this
   node). It classifies source records into a **five-way** status
   (`canonical`, `observed`, `one-wave`, `candidate`, `unknown`) and
   walks a **fixed** 22-stage `OG-00` through `OG-21` topic-explanation
   spine — a different axis (source status, not claim truth-value) and
   a different structure (one fixed spine, not a ternary per-claim
   evaluator) from what this node defines. **This is prior art in the
   same "Truth Computer" project, not a duplicate of this node's
   mechanism, and it has never itself been reconciled against the
   canonical A-G node system** (its OG-00 through OG-12 stages overlap
   substantially with the A-series foundation chain, and its OG-13
   through OG-18 six-stage active-gate sequence overlaps with B-221 Six
   Recursive Steps and, at OG-16 specifically, with the canonical C-301
   Mirror Gate). That reconciliation is a separate, larger task, out of
   scope here, and is flagged rather than attempted in this pass.

**Dependencies**
Upstream: G-702 Evaluation (this node's ternary answers G-702's own flagged "binary or graded" question, for claims specifically), A-101 Ground / Zero, A-103 Differential, B-205 Mirror, B-222 Oscillation Center, B-223 Three Moves, G-701 Evaluation Differential, G-706 Validation, G-743 Claim/Metaphor/Test Separation
Lateral: G-711 Gate 7 (shares Field/Void vocabulary for a different referent — see Reconciliation Note 3, not merged), G-712 Evaluation Mathematics (adjacent open question, not resolved by this node — see Reconciliation Note 2)
Downstream: G-745 Provenance Lens Trace and Evidence Inspector, G-746 Claim Transformation and Commit-State Workbench, claim workbench, database-building interface, automated contradiction review

## Purpose

This node defines the One-Wave Truth Computer's claim-level evaluation
primitive.

The underlying substrate is treated as a two-state opposition:

\[
\boxed{\text{Field}\leftrightarrow\text{Void}}
\]

but evaluation is not binary.

Every claim resolves provisionally into one of three states:

\[
\boxed{-1,\;0,\;+1}
\]

with:

- `+1 = FIELD`
- `0 = MIRROR / HOLD`
- `-1 = VOID`

The zero state is not indecision noise and is not discarded. It is an
active outcome used when the available evidence does not justify
either acceptance or rejection.

## Core Evaluation Rule

For claim `C` and evidence set `E`,

\[
T(C,E)\in\{-1,0,+1\}.
\]

Interpretation:

\[
T=+1
\]

when the cited evidence is sufficiently coherent with the transformed
claim.

\[
T=-1
\]

when the cited evidence supplies a sufficient contradiction or
counterexample.

\[
T=0
\]

when evidence is incomplete, mixed, internally balanced, dependent on
an unresolved definition, or blocked by an untested condition.

The system therefore distinguishes:

\[
\boxed{\text{not supported}\neq\text{refuted}}
\]

and

\[
\boxed{\text{unresolved}\neq\text{false}}.
\]

## Two-State Substrate / Three-State Evaluation

The ternary result does not introduce a third underlying substrate.

Field and Void remain the opposed substrate states.

Mirror / Hold is the comparison boundary between them.

Thus:

```text
substrate:
Field <-> Void

evaluation:
-1   0   +1
Void Mirror Field
```

The zero state is relational. It exists because a comparison can fail
to justify displacement toward either opposed side.

## Claim Evaluation Sequence

A claim should not jump directly from input to truth value. Minimum
sequence:

```text
claim
-> normalize
-> select lens
-> retrieve evidence
-> compare
-> inspect contradiction
-> identify unresolved dependency
-> assign provisional state
-> record provenance
```

Each transition must remain inspectable.

## Field Result (+1)

A Field result means: "Under the declared lens, definitions, evidence
set, and current repository state, the claim is sufficiently
supported."

It does not mean: universal truth; permanent truth; proof outside the
declared scope; immunity from future contradiction.

## Void Result (-1)

A Void result means: "Under the declared lens and evidence, a
contradiction or failed condition is sufficient to reject the
evaluated form of the claim."

The system must state which proposition failed. A Void result cannot
be assigned merely because evidence is absent.

## Mirror / Hold Result (0)

Mirror / Hold is required when:

1. supporting and contradictory evidence coexist;
2. a definition changes the result;
3. an unresolved dependency remains;
4. a required test has not been run;
5. evidence applies only under restricted conditions;
6. the claim is too broad for the evidence;
7. competing transformations remain viable.

Mirror / Hold should produce a next unresolved test whenever possible:

\[
\boxed{0\rightarrow\text{next discriminating question}}
\]

rather than:

\[
0\rightarrow\text{dead end}.
\]

## Gate Aggregation

Multiple lens gates (G-745) may independently return:

\[
g_i\in\{-1,0,+1\}.
\]

The final state must not be generated by naive majority vote unless a
separate node explicitly defines that aggregation rule. A single
decisive contradiction may outweigh several weak supporting gates.
Likewise, several unresolved gates may prevent a Field result even
when no explicit contradiction exists. The aggregation rule must
therefore preserve: evidence strength; dependency structure;
contradiction severity; lens relevance; unresolved conditions.

## Confidence

A confidence value may accompany the ternary state:

\[
0\leq q\leq1
\]

but confidence and truth state are distinct. For example, `0` at
confidence `0.80` means strong confidence that the issue remains
unresolved. It does not mean "80% true."

## Required Record

Every evaluated claim must preserve:

```text
claim:
normalized claim:
lens:
evidence consulted:
supporting records:
contradictions:
unresolved dependencies:
gate results:
final ternary state:
confidence, if used:
next test:
timestamp/version:
```

## Failure / Revision Conditions

Revise this node if:

1. "0" becomes a disguised low-confidence "+1" or "-1";
2. lack of evidence is treated as refutation;
3. majority voting silently replaces evidence-weighted evaluation;
4. source provenance is not recoverable;
5. a claim changes wording during evaluation without being recorded;
6. confidence is presented as probability of absolute truth;
7. Field/Void substrate and ternary evaluation are conflated into the same thing;
8. this node's Field/Void is conflated with G-711's Field/Void function split (see Reconciliation Note 3);
9. this node is cited as having resolved G-702's or G-712's own open questions (see Reconciliation Note 2).

## Canonical Guardrail

\[
\boxed{\text{Truth Computer output is a recorded evaluation state, not an oracle declaration.}}
\]
