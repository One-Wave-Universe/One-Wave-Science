---
node_id: "G-728"
canonical_name: "Gate 5-to-6 Oversight, Override, and Speech Commit Boundary"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "PROPOSED_BUILD"
classification: "Commit Control / Loop Break / Think-Before-Speech"
claim_gate_detail: "Control rule locked; timing ratios and thresholds remain to be calibrated"
metadata_standard: "I-06"
---

# Node G-728: Gate 5-to-6 Oversight, Override, and Speech Commit Boundary

## 1. Purpose
Prevent thought, imagination, habit, or candidate speech from becoming outward action merely because it was generated.

## 2. Canonical Role
Gate 5 is the evaluation pivot. Gate 6 is the commitment lock.
```text
thought ≠ speech
candidate State ≠ committed State
```

## 3. Dependencies
Upstream: OG-17, OG-18, B-209, B-211, G-727.
Lateral: G-729 virtual switches.
Downstream: speech, motor, file-write, and external-communication commits.

## 4. Inputs
Candidate State, factual support, uncertainty, expected audience effect, safety conflicts, Reference Ground, current Field, and override signals.

## 5. State Representation
```text
review_complete, evidence_status, uncertainty,
risk, purpose, inverse_available, override_pending,
speech_permission, commit_permission
```

## 6. Forward Operation
```text
candidate thought → internal question → revision → Mirror return → State review → Commit → speech/action
```

## 7. Reverse and Loop-Break Operation
From Gate 5 the system may:
```text
5→6 Commit
5→5 Hold
5→4 Correct through Mirror
5→3 reverse/change Move
5→2 reopen Choice
5→1 rebuild Field
5↛6 break current loop without committing
```

## 8. Oversight and Override
Oversight observes, compares, and flags. Override interrupts the active route and prevents Gate 6. The provisional 6:1 relation remains a coordination hypothesis, not a mandatory wait during immediate danger.

## 9. Algorithms and Weights
Exact permission rules and hard safety constraints outrank confidence weights. Learned confidence may request review; it may not open an external Commit switch by itself.

## 10. Safety and Permission
Default external permission is Hold. Dream mode blocks outward Commit. Serious conflict forces Inhibit or reverse. Every Commit stores the prior state and reason.

## 11. Outputs
Approved speech/action, silence/hold, revised candidate, loop break, rollback, or escalation.

## 12. Tests and Falsifiers
Inject unsupported claims, contradictory instructions, misleading recalls, and urgent hazards. Fail if candidate speech leaks before Commit, if override cannot stop output, or if the system cannot state uncertainty when support is incomplete.

## 13. Status and Open Questions
The think-before-speak boundary is locked. Review cadence, 6:1 implementation, confidence calibration, and emergency override timing require experiment.
