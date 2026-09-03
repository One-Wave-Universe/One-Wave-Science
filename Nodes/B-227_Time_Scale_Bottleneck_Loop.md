---
node_id: "B-227"
canonical_name: "Time-Scale Bottleneck Loop"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Cycle and Relationship Structure"
claim_gate_detail: "GREEN (defined diagnostic method; not yet independently validated across domains)"
metadata_standard: "I-06"
---

# Node B-227: Time-Scale Bottleneck Loop

## Purpose
Locate where a repeating problem, habit, workflow, research program, or system is getting stuck by checking the same system at six nested time scales.

This node is a diagnostic scale loop. It does not replace B-220 Scale Layer, B-221 Six Recursive Steps, or B-226 Research Discovery and Invention Loop.

## Six Time Scales

1. **SECOND** — immediate action, hesitation, trigger, signal, wrong move, or local transition.
2. **MINUTE** — short sequence, repeated retry, local routine, or failure to terminate a small task.
3. **HOUR** — session structure, task switching, fatigue, environment, sequencing, or repeated local drift.
4. **DAY** — completion pattern, routine, scheduling, repeated avoidance, or daily handoff failure.
5. **WEEK** — recurring bottleneck, missing skill, resource problem, repeated dependency, or bad process.
6. **MONTH** — strategy, architecture, long-cycle assumption, goal selection, or structural pattern that keeps reproducing the lower-level failure.

Canonical diagnostic order:

`Second -> Minute -> Hour -> Day -> Week -> Month`

The loop may also be traversed downward when a higher-scale problem is detected:

`Month -> Week -> Day -> Hour -> Minute -> Second`

## Core Rule
At every scale ask:

**Where is progress getting stuck, repeated, delayed, or recreated?**

Do not assume the visible failure occurs at the scale where its cause lives.

## Time-Scale Mismatch Rule
If a task occupies a much larger time loop than the task itself should require, inspect the smaller loop underneath it.

Example: if a seconds-to-minutes task expands into hours or an entire day, first inspect its Second and Minute loops for repeated starts, missing completion conditions, distraction, uncertainty, or failure to hand off to the next state.

The larger loop is evidence of a mismatch; it does not by itself identify the cause.

## Recurring-Bottleneck Rule
If the same failure appears repeatedly across several scales, promote it from a local incident to a structural bottleneck candidate.

The system should record:
- where the failure first appears;
- which larger scales reproduce it;
- whether the same primitive, relation, operation, dependency, or completion condition is involved;
- what intervention was attempted;
- whether the intervention changed the next larger scale.

## Coupling to B-226
When B-227 locates the likely scale of a bottleneck, run B-226 at that scale:

`Locate scale -> Primitive -> Relation -> Operation -> Composition -> Test -> Discovery -> recheck scales`

A correction is not considered complete merely because the immediate symptom disappears. Recheck the next larger time scale to determine whether the pattern stopped reproducing itself.

## Habits and Behavior
For behavior analysis, the time loop can distinguish an immediate action from the larger pattern maintaining it. A second-level behavior may be preserved by a minute routine, hourly environment, daily schedule, weekly repetition, or monthly strategy.

This node describes diagnostic structure only; it does not authorize harmful punishment or unsafe interventions.

## Scientific Research
The same method may be used to inspect research bottlenecks by interpreting the six positions as nested observation/iteration horizons rather than literal wall-clock requirements when appropriate.

Repeated accumulation of complexity at a larger research scale should trigger inspection of lower-level assumptions and transitions. Additional dimensions, parameters, exceptions, or abstractions are not automatically errors; they become bottleneck signals when they repeatedly compensate for the same unresolved lower-level issue.

## Dependencies
Upstream: B-220 Scale Layer, B-221 Six Recursive Steps, B-226 Research Discovery and Invention Loop, A-111 Recursion.
Downstream: habit analysis, workflow diagnosis, research-program analysis, AI orchestration, debugging, learning systems, project review.

## Open Questions
- Domain-specific thresholds for declaring a time-scale mismatch remain to be defined.
- Literal time scales may need translation for very fast physical systems or very slow scientific programs while preserving the six-level nesting relation.
- Cross-domain testing is required before claiming the scale ladder is universally optimal.
