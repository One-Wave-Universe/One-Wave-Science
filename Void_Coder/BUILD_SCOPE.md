# Void Coder — Locked Build Scope

## MAIN GOAL — CARRIES INTO EVERY VOID STEP

Build the mirrored Void-side half of the same reliable coding engine defined by the Field network.

The shared project objective is to carry one narrow software task through:

`goal -> reference -> inspect -> propose -> edit -> diff -> test -> learn/retry -> review-ready result`

without wandering into unrelated work or losing project state.

Every Void branch must reread and restate this MAIN GOAL before beginning its local step. No local optimization, checker feature, memory feature, or branch-specific task may replace or outrank the MAIN GOAL.

## Project identity

This project builds the **Void-side coding/evaluation engine**.

It is the opposite/complementary half of the Field coding engine. Field expresses a candidate change; Void preserves reference, measures the difference between intended and actual state, challenges unsupported movement, detects regression, compresses evidence into a decision state, and determines whether the candidate is ready to return to the shared loop.

Void does not become the Field worker and does not silently rewrite Field work as its primary behavior.

## Void role

Void reconstructs the known-good reference state, receives the same current goal and bounded task, checks Field's proposed movement against repository evidence and architecture, verifies actual diffs and tests, records disagreement/failure evidence, protects previously verified behavior, and returns a bounded evaluation state such as PASS / RETRY / REPLAN / BLOCKED.

## Mirror objective

Produce a reliable Void coding/evaluation engine that can take the Field-side result through:

`goal -> reference -> compare -> challenge -> verify -> measure difference -> preserve/reject -> learn -> decision -> handoff`

while remaining anchored to the same MAIN GOAL and current project state.

## Scope lock

This MAIN GOAL and scope carry forward to every `void-coder/*` branch and every Void step.

A step may extend implementation only inside this scope. Any proposed scope change must be recorded as a blocked architecture decision rather than silently implemented.
