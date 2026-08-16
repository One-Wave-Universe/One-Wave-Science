---
node_id: "G-724"
canonical_name: "M4 Heterogeneous Runtime and Dual Six-Gate Controller"
namespace: "NODE"
gate: "GREEN"
lifecycle: "PROPOSED_BUILD"
classification: "Heterogeneous Compute / Brainstem Control / Associative and Generative Memory"
claim_gate_detail: "YELLOW (state architecture) / GREEN (device allocation)"
metadata_standard: "I-06"
---

# Node G-724: M4 Heterogeneous Runtime and Dual Six-Gate Controller

## Dependencies

Upstream: A-101, A-110, A-111, B-203, B-204, B-206, B-208, B-221,
B-222, B-223, B-224, C-312, D-411, G-711, G-718, G-719, G-720, G-722.

Authority and full engineering contract:
`UPDATED_42_CENTER_ORIGIN_M4_HETEROGENEOUS_RUNTIME.md`.

## Definition

G-724 places the corrected center-origin control architecture on heterogeneous
hardware while preserving G-722's role separation.

- CPU: authoritative state, safety, scheduling, database, receipts, Gate-7 commit.
- GPU: Field/lattice/tensor computation, visualization, and batched Boltzmann exploration.
- NPU: M4 fast loop, dual six-gate inference, Hopfield attractor recall, coherence scoring.

The NPU is a bounded inference device, not the authoritative database and not a
verified seat of consciousness.

## Center-origin invariant

`BEGIN = current shared reference region`.

The six stability gates are observations around a bidirectional oscillation,
not a one-way lifecycle. Mirror is phase rotation and never a Field/Void label swap.

## Dual six-gate and Gate-7 rule

Let `S in [0,1]^6` be Field-stability scores and `E in [0,1]^6` be
Presence-to-Emergence scores. Let `L_phi` be phase/coherence lock and `P` be
CPU-approved permission.

A provisional, testable coupling score is

`C7 = min(min(S), min(E), L_phi) * P`.

Hysteretic commit:

- open when `C7 >= T_open` for `N_open` accepted ticks;
- remain open while `C7 > T_close`;
- close when `C7 <= T_close` for `N_close` accepted ticks;
- require `T_open > T_close`.

This is an engineering candidate, not derived physical law.

## Runtime boundary

The NPU returns scores and proposals. The CPU validates event identity,
thresholds, units, permissions, model version, and safety before committing.
The GPU consumes only committed state. Every output carries device provenance.

## Build order

1. CPU reference implementation.
2. GPU parity implementation.
3. Hopfield partial-cue benchmark.
4. Boltzmann bounded-exploration benchmark.
5. NPU model export and parity benchmark.
6. Closed-loop Gate-7 integration.
7. Device and memory-layer ablations.

## Advancement requirement

Remain GREEN until an executable implementation, schemas, and deterministic
CPU tests exist. Advance the build claim to YELLOW only when CPU/GPU/NPU
semantics and failure conditions are constrained and testable. Hardware results
require receipts before BRONZE.

