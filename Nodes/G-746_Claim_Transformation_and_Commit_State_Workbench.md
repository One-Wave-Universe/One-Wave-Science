---
node_id: "G-746"
canonical_name: "Claim Transformation and Commit-State Workbench"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Database Builder / Claim Normalization / State Commit"
claim_gate_detail: "Workflow architecture defined; automatic transformation and commit authorization remain implementation questions."
metadata_standard: "I-06"
---

# Node G-746: Claim Transformation and Commit-State Workbench

## Reconciliation Note (read before the architecture below)

1. **G-704 Kabeuchi is the closest existing precedent for this node's
   commit cycle** (`Receive: Delta_n = R_n - I_n -> Evaluate: E_n =
   E(Delta_n) -> Modulate: M_n = M(E_n) -> Apply: I_{n+1} = I_n +
   alpha*M_n`) and has been added as upstream — this node's five-stage
   pipeline (Source -> Normalize -> Apply Lens -> Cross-reference ->
   Commit State) is a database-construction generalization of that
   same receive/evaluate/apply shape, not an unrelated new cycle.
2. **This is the one of the three companion nodes (G-744, G-745,
   G-746) found to be genuinely least redundant against existing
   content.** No normalization/change-ledger, commit-versioning, or
   claim-forking mechanism was found anywhere else in the repository,
   including in the existing `Nexus_Integration/Truth_Computer/`
   implementation — that code classifies and traces records but does
   not normalize incoming claims, maintain a change ledger, or version
   commits. This node's Stage 2 (Normalize) through Stage 5 (Commit
   State) describe real, unbuilt territory.
3. **This node consumes G-744's ternary states and G-745's trace
   directly** (Stage 5 commit uses G-744's `{-1,0,+1}`; the required
   audit trail matches G-745's provenance-chain requirement) and should
   not be built or read independently of them.

**Dependencies**
Upstream: A-101 Ground / Zero, A-103 Differential, G-701 Evaluation Differential, G-702 Evaluation, G-703 Modulation, G-704 Kabeuchi (structural precedent for the commit cycle — see Reconciliation Note 1), G-705 Correction, G-706 Validation, G-744 Field / Mirror / Void Ternary Claim Evaluation, G-745 Provenance Lens Trace and Evidence Inspector
Lateral: I-03 Cross-Platform Packet Intake, I-05 Active Hypothesis vs. Quarantine, I-06 Canonical Node Metadata
Downstream: One-Wave database builder, human/AI collaborative entry system, automated chapter/node intake

## Purpose

This node defines how an incoming statement becomes a structured,
auditable database claim without silently changing its meaning.

The workbench separates five operations:

\[
\boxed{
\text{Source}
\rightarrow
\text{Normalize}
\rightarrow
\text{Apply Lens}
\rightarrow
\text{Cross-reference}
\rightarrow
\text{Commit State}
}
\]

These are different operations and must remain separately inspectable.

## Stage 1 — Source

Capture the original statement exactly enough to preserve provenance.

Required fields:

```text
original claim:
source type:
author:
capture date:
language:
source identifier:
```

The original statement is immutable historical input. Later
normalization does not overwrite it.

## Stage 2 — Normalize

Normalization converts free-form language into a structured
proposition. Allowed operations include: identifying entities; adding
explicit temporal anchors already implied by the source; resolving
grammar; standardizing units; separating compound claims; identifying
modality; declaring scope.

Normalization may not silently strengthen the claim. For every
transformation, record:

```text
field changed:
before:
after:
reason:
```

### Change Ledger

The workbench maintains a change ledger. Useful categories include:
Structure; Quantification; Scope; Modality; Terminology; Temporal
anchor; Other. Each category records the number and nature of
modifications. This creates a differential between original and
transformed claim:

\[
\Delta C=C_{\text{structured}}-C_{\text{source}}.
\]

The purpose is not mathematical subtraction of prose. It is an audit
record of semantic displacement.

## Stage 3 — Apply Lens

The structured claim is evaluated through a declared lens (G-745).
Example:

```text
Lens: Causal Analysis
Transform Mode: Interpretive -> Analytical
Claim Type: Causal
Entities: declared explicitly
Confidence Requirement: High
```

The lens must specify what evidence would count for and against the
claim. A lens cannot be selected solely because it is likely to
produce the desired result.

## Stage 4 — Cross-reference

The transformed claim is compared against the database. The system
searches for: supporting nodes; contradictory nodes; duplicates;
aliases; unresolved dependencies; obsolete claims; cross-domain
numeral collisions; missing evidence; active tests.

Cross-reference is not a vote. One strong contradiction may matter
more than numerous loosely related supporting records.

## Stage 5 — Commit State

After cross-reference, the claim receives a ternary evaluation (G-744):

```text
FIELD       +1
MIRROR/HOLD  0
VOID        -1
```

**FIELD (+1):** sufficient coherent evidence supports the transformed
claim within declared scope.

**MIRROR / HOLD (0):** evidence is incomplete, mixed, conditional,
dependent, or not yet discriminating.

**VOID (-1):** sufficient coherent evidence refutes the transformed
claim or demonstrates failure of a required condition.

The committed state must include the reasoning trace (G-745).

## Commit Does Not Mean Permanent

A committed state is versioned. New evidence may produce `+1 -> 0`, `0
-> +1`, `0 -> -1`, or `+1 -> -1`. Revision is not database failure.
Untraceable revision is failure.

## Human and AI Roles

The architecture permits human and AI participation, but neither
receives authority merely by being the source. The system evaluates:

\[
\boxed{\text{claim content + evidence + provenance}}
\]

rather than:

\[
\boxed{\text{speaker status}}
\]

Human operators may override workflow actions where repository
governance permits, but the override itself must be recorded.

## Database-Building Primitive

The workbench turns Truth Computer evaluation into a database
construction mechanism. Each committed record becomes one of:
supported current claim; unresolved active claim; contradicted /
superseded claim; candidate requiring test; duplicate / alias;
historical source. This prevents unresolved material from being forced
into either canon or deletion — the same discipline I-05 already
requires for physics hypotheses, applied here to individual claims.

## Required Audit Trail

Every committed record must preserve:

```text
original source
normalized proposition
change ledger
lens
canonical references consulted
contradictions found
unresolved dependencies
selected ternary state
confidence if used
next test
commit timestamp
version
operator / agent
```

## No Hidden Rewrite Rule

If normalization changes what would make the claim true or false, it
is no longer mere normalization. It is a new claim. The system must
fork it:

\[
\boxed{
\text{semantic change}
\Rightarrow
\text{new proposition}
}
\]

not silent replacement.

## Failure / Revision Conditions

Revise this node if:

1. original wording is destroyed during normalization;
2. semantic changes are mislabeled as formatting;
3. cross-reference occurs only after a state has already been chosen;
4. unresolved dependencies are ignored during commit;
5. a commit cannot be traced to its evidence;
6. AI-generated confidence is mistaken for empirical support;
7. contradicted records are deleted instead of retained as provenance;
8. the database forces every claim into permanent true/false status;
9. this node is built or evaluated independently of G-744's ternary states or G-745's trace requirement (see Reconciliation Note 3).

## Canonical Guardrail

\[
\boxed{
\text{Source}\neq\text{Normalized Claim}\neq\text{Evaluation}\neq\text{Committed State}
}
\]

The four must remain distinguishable even when they appear in one
interface.
