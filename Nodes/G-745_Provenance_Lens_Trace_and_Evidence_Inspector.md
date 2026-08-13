---
node_id: "G-745"
canonical_name: "Provenance Lens Trace and Evidence Inspector"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Provenance / Reasoning Trace / Evidence Inspection"
claim_gate_detail: "Trace architecture defined; automated source-ranking and lens-selection rules remain open."
metadata_standard: "I-06"
---

# Node G-745: Provenance Lens Trace and Evidence Inspector

## Reconciliation Note (read before the architecture below)

1. **G-704 Kabeuchi is this node's closest existing structural
   precedent and has been added as upstream.** G-704 already defines a
   single-lens constructive review cycle, `Delta_n -> E(Delta_n) ->
   M(E(Delta_n))` — receive, evaluate, modulate. This node generalizes
   that single cycle into a *chain* of multiple declared lenses
   (`C ->L1-> g1 ->L2-> g2 -> ... ->Ln-> gn`), each an independent
   evaluation rather than one modulated response. The generalization
   is the new content here; the single-step form is not.
2. **An existing, already-built, narrower version of a "lens trace"
   exists in this repository** at
   `Nexus_Integration/Truth_Computer/truth-computer-core.js`
   (function `buildTrace`, predating this node). It walks one **fixed**
   sequence — the 22-stage `OG-00` through `OG-21` spine defined in
   `og-system.json` — applying the same fixed stage-questions and
   keyword-based evidence search to every topic. That is materially
   different from this node's architecture, which requires each lens
   to be *declared* per claim (recurrence, identity preservation,
   causality, symmetry, dimensional consistency, conservation,
   provenance, contradiction, scope — an open, extensible list, not one
   fixed 22-step spine). **If this node's architecture is ever
   implemented in code, it must be reconciled against the existing
   `truth-computer-core.js` first** — either as a generalization that
   replaces the fixed-spine approach, or as a second, explicitly
   distinct trace mode — rather than building a second, silently
   competing implementation. Not resolved here; flagged for whoever
   implements this node next.
3. **G-744's ternary states (`g_k \in \{-1,0,+1\}`) are used here
   unmodified** — this node does not redefine them, only chains them
   per lens.

**Dependencies**
Upstream: G-701 Evaluation Differential, G-702 Evaluation, G-704 Kabeuchi (structural precedent for the single-lens cycle this node chains — see Reconciliation Note 1), G-706 Validation, G-743 Claim/Metaphor/Test Separation, G-744 Field / Mirror / Void Ternary Claim Evaluation
Lateral: I-02 Node Proof / Trust Lifecycle, I-03 Cross-Platform Packet Intake, I-06 canonical metadata standard
Downstream: Truth Computer interface, audit trails, reference tracing, AI database construction

## Purpose

This node defines the inspectable reasoning trace between a claim and
its final ternary evaluation.

The Truth Computer must not produce only an answer. It must preserve
the path by which the answer was reached.

\[
\boxed{\text{claim}\rightarrow\text{trace}\rightarrow\text{evidence}\rightarrow\text{state}}
\]

Each step in that trace is independently inspectable.

## Lens

A lens is a declared transformation or evaluation rule applied to a
claim. Examples include: recurrence; identity preservation; causality;
symmetry; dimensional consistency; conservation; provenance;
contradiction; scope.

A lens does not create evidence. It determines which relationship in
the evidence is being tested. Formally:

\[
L_k(C,E)\rightarrow g_k
\]

where `C` = claim, `E` = evidence set, `L_k` = declared lens, `g_k \in
\{-1,0,+1\}` (G-744's states).

## Reasoning Trace

A claim may pass through a sequence of lens gates:

\[
C\xrightarrow{L_1}g_1
\xrightarrow{L_2}g_2
\xrightarrow{L_3}g_3
\dots
\xrightarrow{L_n}g_n.
\]

The system must retain the entire sequence. A later gate must not
erase an earlier contradiction. Likewise, an earlier Field result
cannot force later gates to agree.

## Evidence Inspector

Selecting any gate must expose at minimum four evidence classes.

**1. Stored Definition** — the exact definition or rule controlling the
lens. Answers: "What does this term mean in the current canonical
database?"

**2. Supporting Record** — evidence or derivation that satisfies the
lens condition. Answers: "What currently supports this
interpretation?"

**3. Contradiction** — a counterexample, incompatible record, failed
condition, or conflicting derivation. Answers: "What could make the
claim fail?"

**4. Unresolved Question** — a missing derivation, dependency,
measurement, boundary condition, or discriminating test. Answers:
"What still prevents closure?"

These classes must remain separate. A contradiction cannot be
relabeled as an unresolved question merely to protect a preferred
claim.

## Gate Result

Each lens gate produces:

```text
+1 FIELD    condition satisfied
 0 MIRROR / HOLD   condition unresolved, conditional, or mixed
-1 VOID     condition contradicted or failed
```

A gate result must cite the record that produced it.

## Provenance Chain

Every trace must preserve a path back to canonical source material.
Example structure:

```text
database
-> lens library
-> lens family
-> gate sequence
-> selected gate
-> canonical source record
```

The exact repository implementation may differ, but the chain must be
reversible. From the displayed result, a reviewer must be able to
recover the source. From the source, a reviewer must be able to
determine why it entered the trace.

## Evidence Identity

Synthetic example IDs used in interface mockups are not automatically
canonical records. Before ingestion, every source ID must resolve to
an actual repository object, external citation, experimental receipt,
or explicitly marked hypothetical example. Therefore:

\[
\boxed{\text{displayed source label}\neq\text{canonical evidence until resolved}}
\]

This prevents a polished UI from manufacturing evidentiary authority.

## Trace Independence

The trace should expose disagreement between gates. For example:

```text
Gate 1 +1
Gate 2 +1
Gate 3  0
Gate 4 -1
Gate 5 +1
```

is more informative than collapsing the sequence immediately to one
score. The structure of disagreement may reveal the actual research
problem.

## Next-Test Generation

When a gate returns `0`, the Evidence Inspector should attempt to
identify a discriminating test. A good next test should be capable of
changing the state. Formally, if current evidence gives `g_k = 0`,
seek test `X` such that `X \Rightarrow g_k \in \{-1,+1\}` under
declared success/failure criteria. Tests that cannot change the
classification are not discriminating tests.

## Reversibility Requirement

Every transformation must be recorded sufficiently to reconstruct:
original claim, normalized claim, lens applied, rule applied, source
record, resulting gate state. No invisible semantic rewrite is
allowed.

## Failure / Revision Conditions

Revise this node if:

1. a gate cannot identify its source;
2. interface-only example records are treated as canonical evidence;
3. contradictions disappear from later views;
4. lens definitions change without versioning;
5. an AI-generated summary replaces the underlying source;
6. the trace cannot be reconstructed in reverse;
7. unresolved questions are silently converted into support;
8. this node's implementation duplicates or silently competes with the existing `truth-computer-core.js` fixed-spine trace rather than reconciling with it (see Reconciliation Note 2).

## Canonical Guardrail

\[
\boxed{\text{No result without a recoverable path back to evidence.}}
\]
