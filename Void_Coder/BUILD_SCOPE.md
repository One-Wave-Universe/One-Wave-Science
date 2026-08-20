# Void Coder — Locked Build Scope

## MAIN GOAL — CARRIES INTO EVERY VOID STEP

Build the mirrored Void-side half of the same reliable **coding, app-building, and program-building engine** defined by the Field network.

The shared project objective is to take one bounded software-building goal and carry it through:

`goal -> reference -> inspect -> propose -> edit -> diff -> test -> learn/retry -> review-ready result`

for real code, applications, tools, services, and programs, without wandering into unrelated work or losing project state.

Every Void branch must reread and restate this MAIN GOAL before beginning its local step. No local optimization, oversight feature, memory feature, or branch-specific task may replace or outrank the MAIN GOAL.

## Project identity

This project builds the **Void-side software oversight/override engine**.

It is the opposite/complementary half of the Field coding engine. Field expresses a candidate software movement or change. Void holds the software reference, measures the difference between intended and actual program state, oversees the movement, protects verified behavior, and has authority to permit, correct, override, hold, or escalate the next move.

Void is not merely a checker and does not become the Field worker. Its defining function is **oversight with override authority for code, app, and program construction**.

## Software-building focus

All Void reasoning must stay grounded in the actual software being built. Oversight must consider, when relevant:

- source code correctness
- application architecture
- module boundaries
- interfaces and APIs
- data/state flow
- UI/application behavior
- build/install/launch behavior
- tests and runtime evidence
- regressions in verified features
- repository state and diffs
- deployment/runtime constraints
- maintainability and future integration

The engine is not a generic conversation loop. It is a **software construction system** whose state machine exists to help build working programs reliably.

## Void role — Oversight / Override

Void reconstructs the known-good software reference state, receives the same current goal and bounded task, compares Field movement against repository evidence and architecture, verifies actual diffs and tests, records disagreement/failure evidence, protects previously verified behavior, and determines the next permitted software-building state.

Void returns one of these bounded oversight states:

- `ALLOW` — evidence supports the Field movement and the software build may advance.
- `CORRECT` — the direction is valid but a bounded correction is required before advancement.
- `OVERRIDE` — the proposed movement conflicts with reference, architecture, verified behavior, or software-building goals; replace the proposed next move with the Void-directed safe next move.
- `HOLD` — insufficient or conflicting evidence; preserve current known-good program state and do not advance.
- `ESCALATE` — local resolution is unsafe or exhausted; package software evidence for the higher admin gate.

An override changes the **next permitted action/state**, not the historical evidence. Void must never erase or rewrite evidence to justify an override.

## Mirror objective

Produce a reliable Void software oversight/override engine that can take the Field-side result through:

`goal -> reference -> compare -> challenge -> verify -> measure differential -> oversee -> allow/correct/override/hold/escalate -> handoff`

while remaining anchored to the same MAIN GOAL and current program state.

The controlling relation is:

`Field software movement -> Void oversight -> differential -> permit/override -> next software state`

## Scope lock

This MAIN GOAL, the coding/app/program-building focus, the oversight/override role, and this scope carry forward to every `void-coder/*` branch and every Void step.

A step may extend implementation only inside this scope. Any proposed scope change must be recorded as a blocked architecture decision rather than silently implemented.
