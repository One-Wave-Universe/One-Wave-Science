---
node_id: "G-703"
canonical_name: "Modulation"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Evaluation, Control, and Route Grammar"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node G-703: Modulation

Dependencies:
Upstream: G-702 Evaluation, B-207 Threshold State, B-216 Threshold Mathematics
Downstream: G-705 Correction, B-210 Return, B-209 Break Condition,
G-708 Persistence B, G-710 Grow The Fuck Up Gate, G-711 Gate 7,
G-713 Modulation Mathematics

## Definition

Modulation converts an evaluation signal into a bounded change of activation,
polarity, integrity support, or access state.

Root Rule: Field Modulates.

```text
M_n = M(E_n, Theta_n, Theta*_n, available_actions)
```

where

```text
Theta_n = (q_n,a_n,p_n).
```

## Action Set

- Hold: no commanded change.
- Increase: raise activation.
- Decrease: lower activation.
- Redirect: change polarity without requiring an activation increase.
- Stabilize: move the state toward a selected reference.
- Reject: close or reduce an access gate.
- Admit: open or increase an access gate.

Decrease is a normal healthy action. It includes cooling, rest, de-escalation,
resource conservation, and recovery.

## Mathematical Boundary

Modulation does not decide whether the relationship is valuable or whether a
person should obey another person. It selects a state change inside the control
space defined by B-216. Independent participants retain self-control under
G-720.

## Yellow Result

The role and controlled variables are explicit. The exact action-selection rule
is formalized in G-713.

## Yellow Audit

- Scale-specific actuation limits require calibration.
- Whether multiple actions can be applied concurrently is handled as a control
  vector in G-713 but remains an implementation choice.
- Bronze requires a reproducible simulation.
