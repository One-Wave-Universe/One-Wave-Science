---
node_id: "B-210"
canonical_name: "Return"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Cycle and Relationship Structure"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node B-210: Return

Dependencies:
Upstream: B-207 Threshold State, B-208 Threshold Windows,
B-216 Threshold Mathematics, G-702 Evaluation, G-703 Modulation,
G-714 Decision Mathematics
Downstream: B-206 Paired Loop, B-212 Loop Counter

## Definition

Return is successful restoration of loop integrity after evaluation and
modulation. Return does not require returning to the previous activation or
polarity. It requires restored access and a stable direction of change.

## Mathematics

With `q_return > q_break`, accept Return when

```text
q_(n+1) >= q_return
AND q_(n+1) >= q_n
AND danger exposure is not increasing.
```

A practical danger condition is

```text
[a_(n+1)-a_danger]_+ <= [a_n-a_danger]_+.
```

This allows Return through intentional down-modulation.

## Partial and Full Return

```text
Partial Return: q increases but remains below q_return.
Full Return:    q reaches or exceeds q_return.
```

The previous claim `T_(n+1) >= T_n => Return` was too weak because any tiny
increase could be called restoration. The hysteresis boundary supplies the
missing acceptance condition.

## Yellow Audit

- Energy/time cost of Return requires a scale-specific model.
- The seven-return Hyperloop claim remains separate and unvalidated.
- Bronze requires simulation of noisy trajectories and delayed feedback.
