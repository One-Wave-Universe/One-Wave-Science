---
node_id: "G-729"
canonical_name: "M4 Virtual Switch Bank"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "PROPOSED_BUILD"
classification: "Subconscious Permission / Attention / Interrupt Registry"
claim_gate_detail: "Initial registry locked with reserved expansion space; hardware mapping remains open"
metadata_standard: "I-06"
---

# Node G-729: M4 Virtual Switch Bank

## 1. Purpose
Provide compact subconscious control points for attention, habit, dream, speech, learning, external communication, motor output, and commitment.

## 2. Canonical Role
Every switch uses a signed state:
```text
-1 inhibit/reverse
 0 hold/closed pending review
+1 permit/forward
```

## 3. Dependencies
Upstream: G-726, G-728, B-224.
Downstream: sensor routing, speech, motor control, coding cells, Nexus communication.

## 4. Inputs
Instinct, habit, Administrator permission, danger interrupt, attention request, timeout, current Field, and expected-return status.

## 5. State Representation
Each switch stores:
```text
switch_id, signed_state, source, reason, priority,
timestamp, expiration, inverse_route, override_authority
```

## 6. Forward Operation
Open or close a gate crossing, route attention, permit a practiced routine, or hold an external action while review continues.

## 7. Reverse Operation
Every switch change retains its prior state and inverse transition. Expired or contradicted permissions return to Hold rather than remaining silently open.

## 8. Initial Registry
```text
VS-000 Master Hold
VS-001 Speech Permission
VS-002 Audio Attention
VS-003 Visual Attention
VS-004 Internal Dialogue
VS-005 Imagination
VS-006 Dream Mode
VS-007 Memory Recall
VS-008 Habit Execution
VS-009 Danger Interrupt
VS-010 Oversight Escalation
VS-011 Override
VS-012 External Communication
VS-013 Motor Output
VS-014 Learning Permission
VS-015 Commit Permission
VS-016..VS-063 Reserved
```

## 9. Algorithms and Weights
Switch transition logic is exact. Learned weights may influence a request to change a switch, but only authorized exact rules can change protected switch classes.

## 10. Safety and Permission
Master Hold, Danger Interrupt, Override, and Commit Permission are protected instinct switches. Habits cannot rewrite them. Normal operation is hidden; research mode exposes complete switch logs.

## 11. Outputs
A compact switch mask, transition journal, interrupt event, or permission denial.

## 12. Tests and Falsifiers
Test stale permission expiry, simultaneous conflicts, priority inversion, emergency interruption, and audit replay. Fail if a switch lacks provenance, inverse route, or expiration behavior.

## 13. Status and Open Questions
The initial 64-slot address space is a build choice, not a universal constant. Reserved slots must remain unassigned until a named function and authority rule exist.
