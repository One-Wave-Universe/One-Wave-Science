---
node_id: "B-226"
canonical_name: "Research Discovery and Invention Loop"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Cycle and Relationship Structure"
claim_gate_detail: "GREEN (defined operational method; not yet independently validated across research domains)"
metadata_standard: "I-06"
---

# Node B-226: Research Discovery and Invention Loop

## Purpose
Provide a reusable six-step research method that separates teaching/using known primitives from genuine discovery and invention.

This node does not replace B-221 Six Recursive Steps. B-221 is the repository's abstract master cycle. B-226 is a research/problem-solving instantiation used to move from inherited knowledge toward new knowledge without forcing the learner or researcher to rediscover established primitives unnecessarily.

## Six Steps

1. **PRIMITIVE** — State the smallest reusable rule, object, operation, or known fact needed for the problem.
2. **RELATION** — Identify how the primitive connects to the other relevant primitives, observations, or constraints.
3. **OPERATION** — State the allowed transformation or action clearly enough that it can be repeated rather than guessed.
4. **COMPOSITION** — Combine primitives and operations into a candidate structure, explanation, model, or procedure.
5. **TEST** — Compare the candidate against calculation, simulation, experiment, observation, or a falsifiable consistency check.
6. **DISCOVERY** — Record what the test revealed that was not already contained in the starting primitive set. A stable discovery may become a new primitive for the next pass.

Canonical recurrence:

`Primitive -> Relation -> Operation -> Composition -> Test -> Discovery -> next Primitive`

## Generational-Learning Rule
Established primitives should be taught explicitly and inherited where they are already known. Do not require a learner to independently rediscover a basic operation before allowing them to use it.

Discovery exercises may be useful after the primitive is clear, but successful guessing is not evidence that the primitive was learned.

## Research Rule
When a problem remains unresolved, do not automatically add abstraction or complexity. First identify which of the six steps is unresolved.

Examples:
- unclear primitive -> define or measure the primitive;
- unclear relation -> determine what is actually coupled;
- unclear operation -> derive the transformation rule;
- composition failure -> inspect how valid parts were combined;
- test failure -> preserve the failed result and revise the smallest unsupported assumption;
- discovery -> compress the supported result into the next cycle's starting knowledge.

## Complexity-Bottleneck Rule
Repeated patches at higher levels are evidence to inspect lower-level assumptions, not proof that the higher-level structure is wrong.

For example, if a scientific model repeatedly requires additional dimensions, parameters, correction terms, or exceptions, the research loop should ask whether an unresolved primitive, relation, operation, or scale transition is generating that complexity before treating another layer as fundamental.

This is a diagnostic rule, not a prohibition on higher-dimensional mathematics or legitimate additional structure.

## Evidence Discipline
Every pass should record:
- starting primitive set;
- relation being tested;
- operation used;
- candidate composition;
- exact test/evidence;
- result;
- failure or discovery;
- what becomes the next primitive, if anything.

## Dependencies
Upstream: B-221 Six Recursive Steps, A-111 Recursion, B-220 Scale Layer.
Downstream: research workflows, educational tools, model debugging, scientific bottleneck analysis, invention workflows, AI reasoning orchestration.

## Open Questions
- Formal mapping between B-226's six positions and each B-221 position remains to be derived rather than assumed.
- Criteria for promoting a Discovery into a stable Primitive require domain-specific evidence standards.
- Cross-domain validation is still required before claiming the loop is universally optimal.
