---
node_id: "B-208"
canonical_name: "Threshold Windows"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Cycle and Relationship Structure"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node B-208: Threshold Windows

Dependencies:
Upstream: B-207 Threshold State
Downstream: B-209 Break Condition, B-210 Return, B-216 Threshold Mathematics,
G-703 Modulation, G-714 Decision Mathematics

## Definition

Threshold Windows are operating regions in the state

```text
Theta = (q, a, p)
```

They are not a single ladder from "perfect" to "broken." Activation, polarity,
and integrity must be read separately.

## 1. Activation Windows

Let `A = 100 a` be normalized activation in percent-like units.
The following values are current design scaffolds, not universal constants.

| Activation A | Provisional interpretation |
|---|---|
| 90-100 | overload / danger / reset candidate |
| 75-85 | strong active engagement candidate |
| 60-70 | upper modulation pivot; controlled upshift or sustained activity |
| about 50 | reference operating center |
| 30-40 | lower modulation pivot; controlled downshift, cooling, rest, or conservation |
| 0-10 | very low activation; may be rest, sleep, standby, or collapse depending on q |

The gap regions are deliberately not assigned rigid meanings. They are transition
space to be calibrated rather than filled with invented precision.

### Critical correction

```text
Low activation does not imply break.
High activation does not imply connection.
```

A sleeping system may have low `a` and high `q`. An overloaded conflict may have
high `a` and falling `q`.

## 2. Polarity Windows

Polarity is independent of activation:

```text
p < 0  compressive / restraining / containing lean
p = 0  no directional lean
p > 0  expressive / releasing / propagating lean
```

The magnitude `|p|` measures directional commitment. The sign does not determine
whether activation is high or low.

## 3. Integrity Windows

Let `Q = 100 q`.

The old 100-to-0 threshold map is retained only for integrity:

| Integrity Q | Interpretation |
|---|---|
| near 100 | strongly synchronized or internally coherent |
| intermediate | connected but correction is required |
| near q_break | restoration is uncertain |
| below q_break | Break Condition candidate |
| near 0 | loop/access relationship no longer functions |

Exact integrity boundaries remain parameters. They must not be copied from the
activation bands merely because both are normalized to 0-100.

## 4. Balanced Share Illustration

If a shared active budget is provisionally capped at `A_shared = 85`, an equal
allocation is

```text
85 / 2 = 42.5
```

This is an allocation illustration, not a universal constant and not a claim
that a person is "42.5 percent of a self." A healthy pair also requires retained
agency, acceptable asymmetry, and sufficient integrity `q`.

## 5. Reset Rule

A reset must depend on state and duration, not activation alone. A candidate
trigger is

```text
A >= A_danger for N_danger consecutive steps
AND q is falling or below q_safe.
```

This allows brief high-energy activity without declaring every peak a failure.

## Yellow Result

The window map is now internally consistent with the two-axis correction:
activation can rise or fall intentionally, polarity remains independent, and
break is determined by integrity rather than by low energy alone.

## Yellow Audit

- `A_danger`, `q_break`, `q_safe`, and `N_danger` are parameters awaiting
  calibration.
- The exact widths of the pivot zones remain provisional.
- Whether the same normalized bands recur across scales is an I-04 test, not an
  assumption.
- Simulation of the update law is required for Bronze.
