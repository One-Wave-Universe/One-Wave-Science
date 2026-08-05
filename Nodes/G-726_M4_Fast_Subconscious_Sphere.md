---
node_id: "G-726"
canonical_name: "M4 Fast Subconscious Sphere"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "PROPOSED_BUILD"
classification: "Fast Subconscious / Instinct / Habit / Recall Boundary"
claim_gate_detail: "Role locked; software scheduling and later reflex hardware remain proposed"
metadata_standard: "I-06"
---

# Node G-726: M4 Fast Subconscious Sphere

## 1. Purpose
Provide the hidden fast layer for instinct, habit, reflex-like routing, associative recall, timing, attention, urgency, and automatic practiced procedures.

## 2. Canonical Role
M4 is represented as a sphere because it has a center reference, continuous directional access, and no single preferred route. The geometry is a control map, not a claim about physical brain shape.

## 3. Dependencies
Upstream: G-720, G-721 through G-723, G-724.
Downstream: G-728, G-729, G-730.

## 4. Inputs
Partial cues, danger signals, timing events, active Field ID, habit triggers, virtual-switch states, and recall requests from either slow brain.

## 5. State Representation
```text
pattern_id, instinct_id, habit_id, route_id,
urgency, attention_target, expected_return,
interrupt_flag, switch_mask, cached_attractor_id
```
M4 normally carries IDs, coordinates, timing, signs, and bounded values, not paragraphs.

## 6. Forward Operation
Recognize a cue, activate an exact instinct or verified habit, route attention, issue a cached recall, and execute a compact gate path until an unexpected return requires slow-brain review.

## 7. Reverse Operation
Unexpected return weakens or freezes the active habit, opens the inverse route, and escalates the state to Gate 4/5 review. M4 must never hide a failed automatic path.

## 8. Brain Mapping
M4 does not require a separate processor for the first build. It requires a reserved low-latency execution lane on the Jetson CPU, shared memory, high-priority threads, and bounded deterministic routines. A later microcontroller may execute body safety reflexes without becoming a third brain.

## 9. Algorithms and Weights
Exact M4 memory is primarily instinct: protected automatic rules and safety routes. Adaptive M4 memory is habit strength and cached associations. Deeper Hopfield reconstruction remains available on the compressive CPU side when cached recall is incomplete.

## 10. Safety and Permission
M4 may interrupt, inhibit, hold, orient, or request review. It may not independently perform irreversible Commit, rewrite canonical records, or silently promote a habit into instinct.

## 11. Outputs
Attention shifts, recall IDs, habit routes, timing changes, virtual-switch transitions, interrupt signals, and expected-return templates.

## 12. Tests and Falsifiers
Measure latency, missed interrupts, false habit activation, recall completion, and recovery after unexpected returns. Fail if M4 becomes slower than deliberate processing, cannot be audited, or acts as an unbounded third chooser.

## 13. Status and Open Questions
The subconscious role is locked. Core allocation, hard-real-time requirements, cache size, and habit-promotion thresholds require simulation and hardware testing.
