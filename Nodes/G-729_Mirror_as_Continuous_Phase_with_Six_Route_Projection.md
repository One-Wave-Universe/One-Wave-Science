---
node_id: "G-729"
canonical_name: "Mirror Operator for the Three Mirror Gates"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Legacy G-Series / Canonicalized Node"
claim_gate_detail: "Mathematical mirror operator used by the three canonical Mirror-gate positions; physical carrier remains unresolved"
metadata_standard: "I-06"
---

# G-729 — Mirror Operator for the Three Mirror Gates

**Status:** YELLOW mathematical operator / physical carrier unresolved  
**Dependencies:** B-205, B-208, B-221a, B-222, C-301, G-727, G-728

## Canonical role

There are exactly three primitive Mirror-gate positions in the six-gate cycle:

```text
M1 -> A1 -> M2 -> A2 -> M3 -> A3 -> M1 ...
```

This node supplies a candidate mathematical **Mirror operation** for `M1`, `M2`, and `M3`. It does not create six Mirror gates and it does not insert an additional Mirror crossover between every pair of steps.

Mirror is not a YES/NO swap and does not exchange Field and Void identities.

## Continuous reference operator

The current mathematical reference is a continuous phase rotation in normalized local oscillator coordinates,

```text
z = (x, v/omega)
z' = R(delta_phi) z
```

For the undamped reference oscillator, `R` preserves

```text
x^2 + (v/omega)^2
```

A full `2*pi` cycle returns to the same reference state; a half-cycle maps `(x,v/omega)` to `(-x,-v/omega)`.

How much phase change belongs to each of the three physical Mirror gates remains a scale/implementation question unless separately derived.

## Relationship to six-route projection

A separate finite route projection may still retain binary choice and reverse ternary movement:

```text
M(choice, move) = (choice, -move)
```

That six-route address space is a routing/readout representation. It is **not** the six-gate architecture. Matching the number six does not create more gates.

## Mirror versus Action

The primitive role distinction is:

```text
Mirror gate: read / compare / reflect through shared reference
Action gate: change / carry the resolved relation forward
```

The consequence of each Action gate becomes part of what the next Mirror gate reads.

Mapped onto the six process steps:

```text
BEGIN = M1
BUILD = A1
HOLD  = M2
BUILD = A2
BREAK = M3
LOOP  = A3
```

## Center is not automatically Hold

Position relative to the shared center and movement must still be measured separately. A center crossing can have `x=0` and nonzero velocity, while a turning point can have `v=0` far from center.

Therefore the `HOLD = M2` position must demonstrate the declared retained/coherent relation; zero speed by itself does not prove Hold.

## What remains open

Drive, damping, asymmetry, nonlinear potential, thresholds, residence bands, phase slip, and scale-specific physical realization remain experimental. Those dynamics determine whether the continuous Mirror operator remains useful outside the ideal reference oscillator.

## Anti-drift rule

Do not infer:

```text
3 Mirror gates x 2 orientations = 6 primitive gates
```

The six primitive gates are already fixed as:

```text
3 Mirror + 3 Action = 6
```

Orientation or phase is state carried through a gate, not another gate count.

## Executable authority

- `One_Wave_Bench/logic_core/mirror_operator.py`
- `One_Wave_Bench/logic_core/test_mirror_operator.py`

Existing tests validate the reference operator only; they must not be cited as proof of the physical carrier.
