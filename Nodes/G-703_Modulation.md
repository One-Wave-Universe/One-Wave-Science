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
Upstream: G-702 Evaluation, B-207 Threshold State, B-216 Threshold Mathematics, B-206b Four Views, B-206c Four Actions
Downstream: G-705 Correction, B-210 Return, B-209 Break Condition, G-708 Persistence B, G-710 Grow The Fuck Up Gate, G-713 Modulation Mathematics

## Definition

Modulation converts an evaluation signal into a bounded change of activation, polarity, integrity support, or access state.

Root Rule: Field Modulates.

```text
M_n = M(E_n, Theta_n, Theta*_n, available_control_operators)
```

where

```text
Theta_n = (q_n,a_n,p_n).
```

## Naming Correction

The following are **modulation control operators**, not the canonical Four Actions:

- Hold: no commanded change.
- Increase: raise activation.
- Decrease: lower activation.
- Redirect: change polarity without requiring an activation increase.
- Stabilize: move the state toward a selected reference.
- Reject: close or reduce an access gate.
- Admit: open or increase an access gate.

The canonical Four Actions are defined in `B-206c` as:

```text
Inward / Outward / Across / Over
```

The canonical Four Views are defined in `B-206b` as:

```text
Direction / Phase / Strength / Reference
```

Do not merge these layers.

## Five-State Relationship

Coarse modulation strength may be represented by the five neutral bands from `B-225`:

```text
-2 -1 0 +1 +2
```

Fine thresholding may use a separate calibrated envelope. Domain labels and numerical boundaries remain wrappers/implementation choices.

## Mathematical Boundary

Modulation does not decide whether the relationship is valuable or whether a person should obey another person. It selects a bounded state change inside the control space defined by B-216. Independent participants retain self-control under G-720.

## Yellow Audit

- Modulation's role and controlled variables are explicit.
- The control-operator list is kept distinct from the invariant Four Actions.
- Scale-specific actuation limits require calibration.
- Whether multiple control operators can be applied concurrently remains an implementation choice.
