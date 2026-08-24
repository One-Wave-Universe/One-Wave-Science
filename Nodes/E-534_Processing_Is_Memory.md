---
node_id: "E-534"
canonical_name: "Processing Is Memory"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Field Mechanics, Cognition and Applied Extensions"
claim_gate_detail: "Architecture formalized from UPDATED_33/34; physical retention/read/rewrite/propagation remains to be demonstrated."
metadata_standard: "I-06"
---

# E-534 — Processing Is Memory

## Purpose

Define the VTC compute-in-memory target in which persistent local physical state is simultaneously the stored state, the operand acted on, and the result presented to the next differential stage.

## Core Rule

The target is not:

`CPU -> RAM -> CPU -> RAM`

The target is:

`local state -> differential input -> local transition -> retained local state -> next differential`

For cell state `x_i[n]`, differential input `d_i[n]`, and local transition operator `U_i`, write

`x_i[n+1] = U_i(x_i[n], d_i[n])`.

The key memory condition is that after the driving transient is removed,

`Retain(x_i[n+1], tau_hold) = true`

for a declared hold interval `tau_hold`, and the retained state remains readable with bounded disturbance.

## Required Physical Proof

A claimed physical implementation must demonstrate all of the following:

1. **Write:** distinguishable states can be intentionally set.
2. **Retain:** the state persists after immediate drive is removed.
3. **Read:** the retained state can be measured with bounded disturbance.
4. **Compute:** a new differential can act on the retained state.
5. **Rewrite:** the state can be changed intentionally.
6. **Propagate:** the resulting retained relation can condition another stage using the same interface.

A device that only produces ternary output while relying on separate external storage does not satisfy this node.

## Local State Contract

Local relational state may expose:

`R_i = (Direction_i, Phase_i, Strength_i, Reference_i)`.

The richer local decision channel is ternary:

`d_i ∈ {-1, 0, +1}`.

A sparse supervisory signal may remain binary:

`o_i ∈ {0,1}`

where `0` means allow local resolution and `1` means intervene/reroute/reset. Binary oversight does not replace the local ternary state.

## Energy / Disturbance Accounting

For a physical memory mechanism, characterize at minimum:

- write energy `E_write`,
- read disturbance `delta_read`,
- retention time `tau_hold`,
- rewrite energy `E_rewrite`,
- propagation latency `tau_prop`,
- state error probability `p_err` over the declared operating window.

No claim of compute-in-memory advantage is complete without comparing these costs against a conventional architecture on the same task.

## Relationships

- Depends on: A-109 Inertial Memory; B-206 Paired Loop; B-223 Three Moves; B-224 Two Choices; B-228 Mirrored Three-Gate Grammar.
- Feeds: E-535 Field/Void Processor Split; E-536 Recursive Cube Relational Interface.
- Provenance: UPDATED_33_INVARIANT_ENGINE_VTC_BUILD_AND_VIEW_ACTION_CORRECTION.md and the UPDATED_34 processing-is-memory handoffs.

## Status

The architecture is defined. Magnetic remanence, magnetoresistive retention, or any other proposed physical memory mechanism remains an experimental implementation choice until the six proof conditions above are measured.