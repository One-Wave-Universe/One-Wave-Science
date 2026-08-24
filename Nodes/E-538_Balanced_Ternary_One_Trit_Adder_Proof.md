---
node_id: "E-538"
canonical_name: "Balanced-Ternary One-Trit Adder Proof"
namespace: "NODE"
gate: "GREEN"
lifecycle: "PROPOSED_BUILD"
classification: "Field Mechanics, Cognition and Applied Extensions"
claim_gate_detail: "Arithmetic truth table is exact; implementation in the VTC primitive remains to be demonstrated."
metadata_standard: "I-06"
---

# E-538 — Balanced-Ternary One-Trit Adder Proof

## Purpose

Define the first computation that must be demonstrated using the same physical mirrored-differential primitive that holds and propagates state.

## Trit Domain

Each operand is one balanced ternary trit:

`A,B ∈ {-1,0,+1}`.

For arithmetic sum

`q = A + B`,

represent the result as

`q = 3C + S`

with carry `C ∈ {-1,0,+1}` and sum trit `S ∈ {-1,0,+1}`.

## Complete Truth Table

| A | B | q | Carry C | Sum S |
|---:|---:|---:|---:|---:|
| -1 | -1 | -2 | -1 | +1 |
| -1 | 0 | -1 | 0 | -1 |
| -1 | +1 | 0 | 0 | 0 |
| 0 | -1 | -1 | 0 | -1 |
| 0 | 0 | 0 | 0 | 0 |
| 0 | +1 | +1 | 0 | +1 |
| +1 | -1 | 0 | 0 | 0 |
| +1 | 0 | +1 | 0 | +1 |
| +1 | +1 | +2 | +1 | -1 |

The overflow identities are therefore:

`+2 = 3(+1) + (-1)`

`-2 = 3(-1) + (+1)`.

## Physical Proof Requirement

A valid VTC demonstration must do more than compute the truth table in software. It must show that the same primitive family can:

1. encode the two input trits,
2. resolve the correct sum state,
3. emit the correct carry state when required,
4. retain the result locally if E-534 is claimed,
5. condition a subsequent identical stage without a new translation grammar.

## Error / Margin Measurements

For each of the nine input cases, record:

- measured input state values,
- differential margins from state thresholds,
- output sum state,
- carry state,
- settling time,
- repeatability over repeated trials,
- error rate,
- energy per operation if measurable.

## Information Capacity Clarification

One trit contains

`log2(3) ≈ 1.585 bits`

of Shannon state capacity when all three values are available. A hierarchy of `n` ternary routing decisions can address `3^n` endpoints; that addressing reach must not be confused with the information content of one trit.

## Relationships

- Depends on: E-537 Physical Triad Mirror-Gate Primitive; E-534 Processing Is Memory; B-223 Three Moves.
- Feeds: future multi-trit arithmetic and benchmark nodes.
- Provenance: UPDATED_33 and UPDATED_34 first-compute-target sections.

## Status

The arithmetic definition is exact. The VTC hardware realization is a proposed build and remains unvalidated.