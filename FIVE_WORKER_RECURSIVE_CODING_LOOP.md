# Five-Worker Recursive Coding Loop

Status: control-law lock for the coding/app/program engine.

Purpose: make five workers of increasing scope operate as one recursive system rather than five unrelated agents.

## 1. Scale law

The five workers increase in scope:

1. **Parser** — smallest local unit; resolves syntax, references, exact local meaning, malformed input, and bounded evidence.
2. **Builder** — constructs or changes one bounded implementation unit from parsed material.
3. **Connector** — integrates units across files, modules, interfaces, state flow, and dependencies.
4. **Explorer** — searches broader alternatives, reconstructs failed paths, compares architectures, and handles cross-subsystem problems.
5. **Administrator** — holds the main goal/reference, compares whole-program outcomes, protects known-good state, resolves competing directions, and commits or rejects the result.

The worker names may later be refined, but the **increasing-scope law is locked**:

`local token/statement -> component -> subsystem -> whole-program alternatives -> project-level resolution`

No higher worker may silently perform a lower worker's job without recording the descent in scale.

## 2. Same loop at every scale

Every worker uses the same six-gate recursive process:

`Begin -> Build -> Hold -> Build -> Break -> Loop`

These are process gates, not lifecycle states.

### Gate 1 — BEGIN

Establish the current reference before movement.

Required state:
- main goal
- local goal
- current worker scale
- source/reference
- known-good state
- allowed scope
- success condition

If reference is missing or inconsistent: HOLD.

### Gate 2 — BUILD

Expand one candidate move from the reference.

At each worker scale this means:
- Parser: one interpretation/parse
- Builder: one bounded implementation
- Connector: one integration route
- Explorer: one broader solution path
- Administrator: one candidate whole-system resolution

No commitment occurs here.

### Gate 3 — HOLD

Stop movement long enough to compare candidate against reference.

Check:
- contradiction
- drift
- protected behavior
- missing evidence
- scope leak
- stale state
- whether escalation in scale is actually required

HOLD is an active comparison state, not inactivity.

### Gate 4 — BUILD

Perform the authorized movement and gather consequence.

This is the execution/build/test side of the loop.

The output must include:
- actual change/result
- actual evidence
- differential from expected
- current known-good state

### Gate 5 — BREAK

Resolve the differential.

BREAK means break the current assumption/path when evidence requires it.

Outcomes:
- accept local result
- correct and retry
- descend to a lower worker for a local repair
- ascend to a higher worker for wider context
- reject the approach
- hard-stop/escalate

BREAK does not mean destroy working code. It means break the current path/assumption when the evidence says it is wrong.

### Gate 6 — LOOP

Compress the resolved result into the next reference and re-enter.

A successful lower-scale result becomes input/reference for the next scale.

A higher-scale correction descends as a bounded reference/action for the lower scale.

The loop is therefore bidirectional:

`Parser -> Builder -> Connector -> Explorer -> Administrator`

and

`Administrator -> Explorer -> Connector -> Builder -> Parser`

The next pass always begins at BEGIN with a new explicit reference.

## 3. Field / Void relation

The five workers are **not** replacements for Field and Void.

Field and Void operate across every worker scale:

- **Field** expands/proposes/moves.
- **Void** references/checks/compresses/overrides.
- **M4/OpenClaw** routes scale, timing, task state, tests, receipts, and worker handoff.

Minimum inner cycle:

`Reference -> Field proposal -> Void check -> movement -> consequence -> Void resolution -> new reference`

The six gates are the process envelope around this reciprocal pair.

## 4. Escalation law

A worker may only move upward when its current scale cannot resolve the problem with bounded evidence.

Examples:
- Parser cannot resolve conflicting symbols/references -> Builder or Connector.
- Builder discovers interface conflict -> Connector.
- Connector finds architecture-wide tradeoff -> Explorer.
- Explorer finds competing whole-program routes requiring project authority -> Administrator.

A worker should move downward when the problem becomes local again.

Higher scope is not automatically better. Use the smallest worker that can solve the problem.

## 5. Reconstruction law

Workers do not carry the entire expanded project state forever.

At re-entry:
1. recover the current reference;
2. recover the minimal route/history needed;
3. reconstruct the local working state;
4. verify it against source/provenance;
5. continue only after the reference matches.

Generated reconstruction is never allowed to silently replace exact source state.

## 6. Three-strike law inside the recursive loop

Each materially identical approach gets at most three evidence-bearing passes.

After three failures:
- BREAK the approach;
- record what each attempt proved;
- change angle materially;
- re-enter at the smallest scale that can test the new angle.

Do not call a fourth repeat a new loop.

## 7. Handoff packet

Every worker handoff must preserve:

- main goal
- current local goal
- from-worker
- to-worker
- current reference
- exact evidence
- differential/problem
- protected working state
- attempted path(s)
- allowed next action
- success test
- provenance/receipt

If this packet is incomplete, the receiver enters HOLD rather than guessing.

## 8. Relation to lifecycle states

The five lifecycle states remain separate:

`Idle -> Primed -> Executing -> Vectoring -> Resolving`

Lifecycle states describe the overall behavioral phase.

The six gates describe the recursive process.

The five workers describe scope/complexity.

Field/Void describe opposed processing roles.

M4/OpenClaw describes routing/orchestration.

Do not collapse these layers into one numbering system.

## 9. Canonical operating law

`GOAL`
-> `BEGIN(reference)`
-> `BUILD(candidate)`
-> `HOLD(compare)`
-> `BUILD(execute/test)`
-> `BREAK(resolve/correct/escalate)`
-> `LOOP(compress into next reference)`
-> re-enter at the appropriate worker scale.

Short form:

**same recursive law, five increasing scales, two opposed state machines, one routed loop.**
