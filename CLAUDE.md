# Claude Start Here

This repository already contains architecture, runtime rules, tests, and project history. Do not replace them with a narrower local interpretation.

## Read first

Before editing code:

1. Read `AGENTS.md`.
2. Read the active GitHub issue/task completely.
3. Read `AI_CANONICAL_START_HERE.md` when the task touches One-Wave architecture, state machines, lattice, Miniverse/Dreamworld, physics, memory/recall, or other canonical system concepts.
4. Read the exact files and tests related to the assigned task before proposing changes.
5. Use `BRANCH_STEP_PROJECT_TEMPLATE.md` for substantial coding work.

## Working rules

- Inspect before editing.
- Work on a branch and open a PR for code changes; do not silently rewrite `main`.
- Keep each task bounded to the active issue.
- Change one targeted thing at a time when debugging or repairing behavior.
- Run the exact relevant test immediately after a change.
- Do not weaken, delete, or rewrite tests merely to make broken code pass.
- Preserve already verified working behavior unless the task explicitly requires changing it.
- Prefer deterministic code and tests before adding LLM behavior.
- Keep code straightforward enough to inspect line by line.
- Do not invent a second implementation of architecture that already exists in the repo.
- Separate established fact, derived result, simulation result, bench result, proposal, and speculation.
- Stop at the task's hard stop. Do not expand into the next worker/project without an explicit task.

## Learner App authority boundary

The learner architecture has a strict separation of jobs.

### Router owns

- which rules are sent to a worker
- target rules
- allowed supporting rules
- forbidden/not-yet-learned rules
- prerequisites
- sequencing
- difficulty
- review/repetition scheduling
- learner state
- progression
- domain/adapter selection

### Parser / Problem Builder owns

- receiving a router-supplied rule packet
- generating a candidate problem/artifact that obeys that packet
- reparsing the generated external form into structure
- independently verifying requested rules are present
- verifying forbidden rules are absent
- rejecting contradictory/impossible packets
- returning structural metadata

The parser/problem-builder must NOT choose curriculum rules, inspect learner readiness, reorder the curriculum, or expose the final answer.

## Reusable parser rule

Do not hard-code the learner parser core to algebra.

Use a reusable core plus thin domain adapters:

```text
ROUTER
  -> rule packet + domain
  -> reusable parser/problem-builder core
  -> domain adapter
  -> generated problem + structural verification
```

The core should understand generic concepts such as rule IDs, allowed/forbidden rules, constraints, difficulty budget, seeded variation, artifact text, structural representation, validation, and adapter dispatch.

Domain-specific syntax and semantics belong in adapters. `math/basic_equations` is only the first adapter. Future adapters must be possible without replacing the core.

Generation must not verify itself by trusting its internal construction object. The generated external representation must be parsed again and checked independently before it is returned.

No public result, normal log, example, serialization, or API object may expose the learner's solved answer unless a later explicitly authorized component owns answer checking.

## Evidence before completion

Before claiming a coding task is complete:

- inspect the actual diff
- run the relevant tests
- report failures instead of hiding them
- record unsupported cases or remaining limitations
- verify the change did not cross the task boundary

The default construction loop is the one defined in `AGENTS.md`:

`goal -> reference -> inspect -> propose -> edit -> diff -> test -> learn/retry -> review-ready result`
