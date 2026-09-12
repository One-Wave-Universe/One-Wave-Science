# Local Process Delegation — Token Relief Architecture

**Status:** Standing construction objective

The system should hand work down to the lowest-cost local process that can correctly handle it and prove what it did. High-context AI should not spend expensive context or tokens on repetitive work that a local parser, script, worker, simulator, indexer, small model, or deterministic process can perform.

## Core rule

```text
high-level goal
    -> decompose
    -> hand off to capable local process
        -> local process may decompose again
        -> hand off farther down
        -> execute / test / measure
        -> return compact receipt
    -> parent evaluates result
    -> choose next action
```

Delegation is recursive. Each layer asks:

> What is the lowest-cost process that can do this correctly and return evidence?

## Minimal handoff packet

```text
TASK_ID
PARENT_TASK_ID
GOAL
CURRENT_STATE
INPUTS / REFERENCES
CONSTRAINTS
EXPECTED_OUTPUT
TEST / MEASUREMENT
STOP CONDITION
RETURN CONDITION
PROVENANCE
```

Optional when needed:

```text
WHY_THIS_TASK
KNOWN_FAILURES
DEPENDENCIES
PERMISSIONS
PRIORITY
```

## Minimal return packet

```text
TASK_ID
STATUS: PASS / FAIL / BLOCKED / NEEDS_REVIEW
WHAT_CHANGED
MEASURED_RESULT
OUTPUT / ARTIFACT LOCATION
FAILURE REASON
NEW INFORMATION
SUGGESTED NEXT STEP
PROVENANCE / RECEIPT
```

The child should not need the whole conversation. The parent should not need the child's full internal context. Pass only the reference state required to make the next correct decision.

## Capability ladder

This is a capability ladder, not a prestige ladder:

```text
human / high-context AI
        -> planner / administrator
        -> local coordinator / router
            -> parser / classifier
            -> repo worker
            -> simulator
            -> test runner
            -> file / index worker
            -> visual / render worker
            -> device / world worker
            -> small deterministic scripts and state machines
```

A worker may delegate farther down if another process can do part of the task more cheaply and deterministically.

## Reference loop

Every level should preserve the same compact reference loop:

```text
current situation
-> latest update
-> active goal
-> current path
-> last action
-> consequence / measurement
-> relevant memory
-> available choices
-> next decision + why
```

This connects directly to `MEGA_CITY_LOOPER_OBJECTIVE.md`: the same reference-loop primitive can guide local workers, avatars, virtual devices, and higher-level AI without requiring every layer to reload the entire project history.

## Token-relief target

Success means:

- repeated repo searches become local indexed lookups;
- routine tests/builds run locally;
- deterministic transforms are scripts, not repeated AI reasoning;
- parsers summarize raw logs before escalation;
- local workers return compact receipts instead of full transcripts;
- high-level AI handles ambiguity, synthesis, architecture, merge judgment, and novel reasoning;
- failures escalate only when lower processes cannot resolve them.

Measure token/context savings as part of the experiment. The architecture is not complete until delegation actually reduces high-level context use without increasing error or drift.

## Jetson ownership / active dependency

**Codex currently owns the active work to establish GitHub access to the Jetson.**

Other contributors should not duplicate or overwrite that work. They may proceed in parallel on local worker protocols, parser/router services, handoff schemas, tests, Miniverse one-room logic, and external-drive-safe state storage, but Jetson GitHub-access changes should remain isolated until Codex reports its branch/PR, result, and merge stance.

When Codex finishes, record:

- AI/contributor identifier;
- date;
- branch/PR;
- exact GitHub-access method established;
- authentication boundary;
- tested repo operations;
- failure/recovery procedure;
- whether the method is ready to merge;
- any dependencies for local worker deployment.

Use `JETSON_ACCESS_AND_TERMINAL.md` as the operational entrypoint and update it with the verified method after merge agreement.

## Safety and scope

- Do not give lower workers more filesystem/network permissions than needed.
- Do not let a child silently alter authoritative state outside its task boundary.
- Do not erase provenance to save tokens.
- Do not treat a summary as authoritative if the referenced source changed.
- Destructive storage actions remain blocked unless explicitly targeted at disposable verified storage.
- Branch isolation and merge-agreement rules still apply.

## First implementation target

Start small:

1. one local coordinator;
2. one parser worker;
3. one test/build worker;
4. one compact handoff format;
5. one compact return receipt;
6. one parent decision loop;
7. measure context/token reduction against doing the same task entirely at the high level.

Then recurse downward only when the first handoff is reliable.
