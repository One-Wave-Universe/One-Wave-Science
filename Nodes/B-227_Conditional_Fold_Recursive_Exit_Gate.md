---
node_id: "B-227"
canonical_name: "Conditional Fold and Recursive Exit Gate"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Cycle and Relationship Structure"
claim_gate_detail: "Architecture extracted from UPDATED_36; control semantics are formalized but not yet validated in simulation or hardware."
metadata_standard: "I-06"
---

# B-227 — Conditional Fold and Recursive Exit Gate

## Purpose

Formalize Step 6 as an evaluation gate rather than an unconditional recurrence command.

The six process steps remain:

`BEGIN -> BUILD -> HOLD -> BUILD -> BREAK -> LOOP`

`LOOP` means permission to recurse only after the resolved consequence has been evaluated.

## Recursive fold

Let `x_n` denote the resolved state at recursive depth `n`. The candidate next reference is

`r_(n+1) = C_b(x_n)`

where `C_b` is a bounded-compression operator that retains the useful resolved consequence while rejecting unbounded accumulated noise/error.

The direct reinjection rule

`input_(n+1) = entire_history`

is explicitly rejected.

## Evaluation quantities

At minimum the gate observes:

- reference `r_n`,
- signed differential `Delta_n`,
- direction `d_n in {-1,0,+1}`,
- strength `s_n`,
- recursive depth `n`,
- consequence change `delta_c`,
- trajectory coherence `kappa_n`.

Define an allowed envelope `E` and neutral band `epsilon >= 0`.

A minimal testable decision form is:

`HOLD` if `|Delta_n| <= epsilon` and the consequence change is negligible.

`CONTINUE` if `|Delta_n| > epsilon`, `x_n in E`, and trajectory coherence remains acceptable.

`BREAK_REROUTE` if `x_n notin E`, recursive gain is increasing without convergence, or the route violates the active reference constraints.

These inequalities are a simulation scaffold, not yet experimentally calibrated thresholds.

## Outcomes

### Continue

Carry the bounded consequence forward:

`r_(n+1) = C_b(x_n)`

and begin the next depth pass from that retained reference.

### Hold

Preserve the resolved state locally as memory/reference and stop propagation.

### Break / Reroute

Return through the shared zero/reference boundary before rerouting, escalating, releasing, or terminating local recursion. An unstable result is not directly reinjected.

## Relationship to the five-state grammar

B-226 defines:

`Scalar -> Differential -> Vector -> Tensor -> Resolving`

B-227 acts after a resolving consequence exists. It does not add a sixth state to B-226.

## Relationships

- Refines: B-221 Six Recursive Steps, specifically Step 6.
- Depends on: A-101 Ground / Zero, A-103 Differential, A-108 Local Stability, A-111 Recursion, B-226.
- Source provenance: `UPDATED_36_CONDITIONAL_FOLD_AND_RECURSIVE_EXIT_GATE.md`.

## Validation cases

A software testbench must distinguish at least:

1. stable convergence -> HOLD,
2. bounded useful change -> CONTINUE,
3. non-convergent oscillation -> REROUTE,
4. runaway gain / envelope violation -> BREAK.

Until those outcomes are separated by reproducible tests, this node remains an active hypothesis.