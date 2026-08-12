---
node_id: "G-743"
canonical_name: "Claim/Metaphor/Test Separation"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Evaluation, Control, and Route Grammar / Simulation Governance"
claim_gate_detail: "GREEN (procedural requirement, no physics claim of its own)"
metadata_standard: "I-06"
---

# Node G-743: Claim/Metaphor/Test Separation

**Dependencies**
Upstream: G-706 Validation
Lateral: I-05 Active Hypothesis vs Quarantine
Downstream: every node in `RELATIONAL_MECHANICS_NODE_BACKLOG.md`, all future node authorship generally

## Rule

Every new physical idea entered into the repository — not only in the
relational-mechanics backlog — must explicitly separate four distinct
kinds of statement rather than letting them blur together in one
paragraph:

```text
1. Mathematical definition — an operator, equation, or formal
   structure that is true by construction (e.g. A-118's
   CHANGE = LOCAL_SLOPE - REFERENCE_SLOPE).

2. Physical hypothesis — a claim about what that structure means
   in the physical world, which could be wrong (e.g. "the reference
   slope corresponds to an actual moving background field").

3. Intuitive analogy — language borrowed from an unrelated domain to
   build intuition (e.g. "wake," "assimilation," "reinjection"),
   explicitly flagged as analogy, not as evidence the borrowed
   domain's mechanics actually apply here.

4. Falsification test — a specific, checkable procedure (ideally with
   a stated observable and tolerance, per G-737) that could show the
   hypothesis wrong.
```

A node is not required to have all four filled in — many backlog
entries are (1) only, honestly marked MAPPED or DEVELOPED-without-test
— but it must never present (3) as though it were (1) or (2), and must
never present (2) as though it were already validated by (4) when no
such test has actually been run.

## Why This Is Its Own Node Rather Than Restating I-05

I-05 already distinguishes Active Hypothesis, Proposed Build, Disputed
Formulation, and Quarantined Source at the level of a whole node's
lifecycle status. G-743 operates one level down, inside a single
node's own prose: it is possible for a node with a correct I-05 status
label to still blur claim types internally (e.g. a YELLOW node whose
"Definition" section quietly slides from equation to hypothesis to
metaphor without a reader being able to tell where). G-743 is the
sentence-level discipline I-05's node-level labeling depends on to
mean what it says.

## Worked Example From This Backlog

The backlog's Finite Wake Assimilation item uses "wake" and
"assimilation" — biological/fluid-dynamics language. Under G-743, any
future full node for it must state plainly that "wake" is an
analogy for a propagating field disturbance (kind 3), give the actual
mathematical propagation rule separately (kind 1), state the physical
hypothesis of what "assimilation" means as a field-state change (kind
2), and state what a test of that assimilation claim would measure
(kind 4) — rather than letting the wake language itself carry
argumentative weight.

## Failure / Revision Conditions

This node fails if a node's prose uses an analogy-derived term (kind
3) as though it settles a physical question (kind 2), or presents an
untested hypothesis (kind 2) as validated without citing an actual
falsification test result (kind 4).
