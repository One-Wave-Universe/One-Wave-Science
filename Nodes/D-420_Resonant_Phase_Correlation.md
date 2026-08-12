---
node_id: "D-420"
canonical_name: "Resonant Phase Correlation"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Geometry, Resonance, and Simulation"
claim_gate_detail: "GREEN (definition, consistent with standard resonance theory) / not yet simulated against a specific orbital case"
metadata_standard: "I-06"
---

# Node D-420: Resonant Phase Correlation

**Dependencies**
Upstream: D-402 Resonant Mode, F-604 Resonance
Downstream: D-421 Coherent Differential Accumulation, D-422 Incoherent Differential Cancellation; also the Wake Phase Encounter and Resonance Detector backlog items (RELATIONAL_MECHANICS_NODE_BACKLOG.md)

## Definition

Resonance between a perturbed body and a repeating perturber (e.g. a
body and Jupiter under repeated conjunctions) is defined as **recurring
correlated phase**, not necessarily identical impulses:

```text
resonant  <=> encounter phase phi_n at successive close approaches n
              stays approximately constant (or advances by a fixed,
              small increment) across many encounters
non-resonant <=> phi_n drifts, becoming effectively uniformly
              distributed over successive encounters
```

`phi_n` here is C-331's encounter geometry (approach direction,
timing relative to the perturber's own cycle) at the n-th close
approach, not the size of the individual kick.

## Relation to Existing Nodes

F-604 already defines resonance as "aligned-choice reinforcement" —
"when two states choose the same phase, their combination exceeds
either alone." D-420 is the orbital-mechanics specialization of that
same statement: the "choice" being aligned is the encounter phase
`phi_n` across repeated passes, and D-402's Resonant Mode ("a
persistent mode whose recursive update returns to itself after k
steps") is the geometric condition (commensurate periods) that makes
`phi_n` recur in the first place rather than drift.

## Why Phase, Not Impulse Size

A perturber's individual encounter can be weak while still driving
significant long-term change, provided its direction correlates across
many encounters (D-421). Conversely, a perturber's individual encounter
can be strong while driving negligible long-term change, if its
direction is effectively random from one encounter to the next (D-422).
D-420 exists to separate these two cases at the source: it is the
recurrence of `phi_n`, not the magnitude of any single `Delta v`, that
determines whether repeated encounters accumulate or cancel.

## Required Next Work

- A concrete numerical measure of "approximately constant phase" (a
  tolerance band on `phi_n` drift per encounter) rather than a
  qualitative description.
- The backlog's Resonance Detector item: an operational test that
  flags D-420 without presupposing which commensurability is being
  looked for.

## Failure / Revision Conditions

This node fails if "resonance" is asserted from a single encounter, or
if a case with drifting `phi_n` is described as resonant because the
individual encounters happen to be strong.
