---
node_id: "G-736"
canonical_name: "No Hidden Controller Rule"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Evaluation, Control, and Route Grammar / Simulation Governance"
claim_gate_detail: "YELLOW (procedural requirement, no physics claim of its own)"
metadata_standard: "I-06"
---

# Node G-736: No Hidden Controller Rule

**Dependencies**
Upstream: G-706 Validation, D-412 Lattice Simulation and State-Driven Visualization Standard
Downstream: G-737 No Victory Without Observable Match; also the Emergent-Orbit Test and Three-Body Silver-Bullet Benchmark backlog items (RELATIONAL_MECHANICS_NODE_BACKLOG.md)

## Rule

No relational-mechanics simulation may contain code that:

```text
- nudges a body back toward a "correct" orbit,
- damps or resets a resonance toward a target width,
- imposes a stability condition as a constraint rather than letting
  instability be a possible outcome, or
- otherwise steers the outcome toward the behavior the simulation is
  meant to be testing for.
```

Any orbit, resonance gap, libration, or clearing behavior a simulation
reports must arise solely from the declared update rule (A-118's
relational differencing, applied per C-327 and downstream) acting on
the declared initial state — the same requirement D-412 already places
on lattice simulations generally, applied here specifically to hidden
correction terms.

## Why This Is Separate From D-412

D-412 requires that "a valid One-Wave simulation must evolve declared
state variables under a reproducible update law" and exposes failure
conditions. G-736 names the specific, easy-to-miss violation this
backlog is most at risk of: a controller that makes an orbit look
stable or a resonance look correctly locked without the underlying
relational primitive actually producing that behavior. This failure
mode is easy to introduce unintentionally (e.g. a numerical damping
term added "for stability" that also happens to suppress the very
divergence a test was supposed to detect).

## Required Check

Every simulation submission must include a code-level audit statement
listing every term in the update step and confirming none of them is a
target-seeking or stability-imposing term outside the declared
relational primitive.

## Failure / Revision Conditions

This node fails if any simulation supporting one of the backlog's
emergent-orbit, emergent-gravity-assist, emergent-resonance-gap, or
emergent-libration test claims contains an undeclared
correction, damping, or steering term, or if such a term exists but is
not disclosed in the audit statement.
