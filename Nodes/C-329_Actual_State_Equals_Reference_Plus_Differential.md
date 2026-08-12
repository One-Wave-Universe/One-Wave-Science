---
node_id: "C-329"
canonical_name: "Actual State Equals Reference Plus Differential"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Applied Mechanics and Boundary Structure"
claim_gate_detail: "GREEN (bookkeeping identity and stated failure mode) / trivial by construction, kept as its own node because the failure mode it guards against is easy to make"
metadata_standard: "I-06"
---

# Node C-329: Actual State Equals Reference Plus Differential

**Numbering note:** originally drafted as C-325; renumbered to C-329.
See `RELATIONAL_MECHANICS_NODE_BACKLOG.md`.

**Dependencies**
Upstream: A-118 Relational Differential Primitive, C-327 Relational Acceleration Equation
Downstream: C-330 Moving Local Potential Perturbation; also the Dynamic Barycentric Reference backlog item (RELATIONAL_MECHANICS_NODE_BACKLOG.md)

## Definition

```text
ACTUAL_STATE = REFERENCE_STATE + DIFFERENTIAL_STATE
```

For any quantity decomposed by A-118 into a reference term and a
differential term (e.g. C-328's `S_i = S_common + s_i'`), the actual,
complete physical state is the **sum** of both terms, not the
differential term alone.

## Why This Node Exists

This looks trivial — it is an identity by construction — but the
specific failure it exists to name is not trivial: once a calculation
has computed a clean differential term (A-118's `CHANGE`, or C-328's
residual `s_i' - s_j'`), it is easy to treat that differential as the
*entire* physical state and silently drop the reference term, because
the differential is the quantity that was actually being solved for.
C-329 states explicitly that this is only valid when the reference
term is genuinely zero or has already been separately accounted for —
otherwise the reference field's own contribution has been erased from
the dynamics by omission, not by a physical cancellation like C-328's.

## Worked Example of the Failure Mode

Given C-328's result `d̈_ij = s_i' - s_j'`, it is correct to say the
*relative* acceleration depends only on the residuals. It is **not**
correct to then compute either body's *absolute* trajectory using only
`s_i'` — that would silently drop `S_common`, which C-328 showed
cancels from the relative motion specifically, not from either body's
actual absolute state. The absolute state of body `i` remains:

```text
S_i (actual) = S_common (reference) + s_i' (differential)
```

## Relation to A-119

This node is the general-purpose safeguard A-119 (Moving Reference
State) needs: A-119 requires the reference's own motion be tracked
rather than assumed zero; C-329 requires that, once tracked, it is
added back in wherever the actual (not merely relative) state is
needed.

## Required Next Work

- An audit pass over any future simulation built from C-327/C-328 to
  confirm absolute-state outputs (not just relative-state outputs)
  correctly re-include the reference term.

## Failure / Revision Conditions

This node fails if any downstream node reports an "actual state" that
is provably missing its reference-term contribution, or if this
identity is used to justify adding an *undeclared* reference term back
in to force agreement with a desired result.
