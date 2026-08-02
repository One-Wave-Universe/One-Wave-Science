---
node_id: "B-209"
canonical_name: "Break Condition"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Cycle and Relationship Structure"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node B-209: Break Condition

Dependencies:
Upstream: B-207 Threshold State, B-208 Threshold Windows,
B-216 Threshold Mathematics, G-703 Modulation, G-714 Decision Mathematics
Downstream: B-210 Return, B-211 Loop Break, B-213 Access Line,
G-719 Neural System Functional Analogy Map

## Definition

A Break Condition is the state in which reliable restoration of the Paired Loop
or internal access relation is no longer available under the current control
range.

Break is determined by integrity `q`, not by activation `a`.

```text
q_n <= q_break  => Break Condition candidate
```

Low activation with high integrity may represent sleep, standby, rest, or
conservation and is not a break.

## Hysteresis

Use two boundaries:

```text
q_break < q_return.
```

The loop enters Break Condition at `q_break` but must recover above `q_return`
before Return is accepted. This prevents repeated one-step toggling.

## Possible Outcomes

1. Separation
2. Recursive collapse
3. Access Line preservation or formation
4. Reset
5. Dormant but recoverable state

Outcome selection remains downstream in G-714.

## Yellow Result

The break criterion is now mathematically disambiguated from energy level and
contains an explicit hysteresis requirement.

## Yellow Audit

- `q_break` and `q_return` require scale-specific calibration.
- Outcome-selection mathematics remains incomplete.
- The time allowed below `q_break` before irreversible separation is unresolved.
