---
node_id: "B-226"
canonical_name: "Differential Triad Computing Primitive"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Computing Primitive / Differential Hardware"
claim_gate_detail: "Working VTC physical interpretation from Updated 33; hardware minimum remains experimental"
metadata_standard: "I-06"
---

# Node B-226: Differential Triad Computing Primitive

## Dependencies

Upstream: B-206 Paired Exchange / Paired Loop, B-221a Six-Step Oscillator Program, B-223 Three Moves, B-224 Two Choices, C-301 Mirror Gate

Downstream: balanced-ternary arithmetic test structures, recursive differential interfaces, processing-is-memory clusters, connected cube modules

## Core

The current VTC computing primitive is a differential triad, not a conventional one-way logic gate.

## Definition

One triad consists of:

```text
two physically linked/opposed mirror elements
+ one differential evaluator
= one differential triad
```

The opposed elements should switch as one complementary physical relation where practical, rather than a processor detecting one side and issuing a second command to imitate the mirror.

The evaluator resolves the relation between the two sides.

## Signed Differential Output

The local AC/differential result is:

```text
LEFT / STAY / RIGHT
 -1      0      +1
```

`0` is the balanced directional result. It is not a third actively driven DC command.

The separate DC participation choice is:

```text
EVERYTHING / NOTHING
engage       do not engage
```

DC participation and AC ternary direction are different layers.

## Cell / Cluster Counting

The current mapping is:

```text
1 triad = 2 opposed mirror elements + 1 differential evaluator
3 triads = 9 active elements = 3 physical Mirror Gates
3 physical Mirror Gates x 2 orientations/phases = 6 logical pair positions
```

Therefore:

```text
6 logical pair positions != 6 independent physical gates
```

and the repository should not define the computing cell merely as "six gates."

Two mirrored cells can each accept an input relation and express a differential output. Their shared differential is itself a new relation and can feed the next identical interface.

## Recursive Interface

```text
OUTPUT relation of level n
==
INPUT relation expected by level n+1
```

A higher cluster should therefore be externally substitutable for a lower relational node without exposing its internal implementation.

## Processing Is Memory Target

The intended primitive co-locates:

```text
state + memory + transition / logic
```

A cell holds physical state, receives a differential, evaluates or changes that state, leaves the new state locally available, and allows a neighboring differential to use it.

Persistent magnetic or other physical state is not assumed proven. Retention requires measurement of write, retain, read, rewrite, and propagation behavior.

## First Compute Test

The first arithmetic target is a complete balanced-ternary one-trit adder covering all nine input combinations of two trits in `-1/0/+1`, including carry where required.

Examples:

```text
+1 + (-1) -> 0
+1 + +1 = +2 = (+1 x 3) + (-1 x 1)
-1 + -1 = -2 = (-1 x 3) + (+1 x 1)
```

Two triads are a minimum candidate for time-shared arithmetic. Three triads provide a clearer dedicated experimental cluster. The physical minimum is not yet established.

## Yellow Audit

- Demonstrate opposed linked switching physically.
- Demonstrate stable `-1/0/+1` differential regions.
- Demonstrate that a resolved differential can condition the next identical stage.
- Demonstrate physical state retention before calling the primitive compute-in-memory hardware.
- Determine whether two or three triads are required for a practical complete one-trit adder.
- Measure power, delay, drift, common-mode rejection, and rewrite endurance for the chosen physical implementation.
