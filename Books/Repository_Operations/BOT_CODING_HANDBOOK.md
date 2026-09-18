# Kitty Hawk Bot Coding Handbook

## Purpose

This book is the shared coding reference for the Field/Void software-building engine. It exists so a bot that is unsure, stuck, replacing another bot, or entering an unfamiliar repository can look up a disciplined next move instead of guessing.

The engine's job is to build, modify, debug, test, and improve real code, applications, and programs while preserving known-good behavior and project state.

## How every bot reads this book

From any branch/worktree in the local repository:

```bash
cd "$HOME/One-Wave-Science"
git show main:BOT_CODING_HANDBOOK.md
```

To search for a topic:

```bash
git show main:BOT_CODING_HANDBOOK.md | grep -n -i "TOPIC"
```

The `main` copy is the canonical handbook. Branch instructions may add stricter local rules, but may not silently weaken this book.

---

# 1. First principle: build software, not prose

A coding agent succeeds only when repository evidence shows the program moved toward the requested working state.

A useful coding pass ends with one or more of:
- working source code,
- a launchable app/program,
- a passing test,
- a verified bug fix,
- a controlled refactor with unchanged behavior,
- a reproducible failure that narrows the problem,
- a review-ready diff backed by evidence.

Long explanations do not substitute for working software.

---

# 2. Mandatory orientation before editing

Before touching code:

```bash
cd "$HOME/One-Wave-Science"
git rev-parse --show-toplevel
git branch --show-current
git rev-parse HEAD
git status --short
git worktree list
```

Then identify:
1. Main product goal.
2. Active build step/branch.
3. Hard start conditions.
4. Hard stop condition.
5. Files allowed by the active step.
6. Existing working features that must not regress.
7. Relevant tests/build/run commands.
8. Previous failures and diary notes.

Do not code until the current task can be stated in one sentence.

---

# 3. Read before write

When entering unfamiliar code:

1. Find the entry point.
2. Find the data/state model.
3. Find the component/module touched by the task.
4. Find tests for that component.
5. Find callers and dependencies.
6. Trace the smallest path from input -> behavior -> output.

Useful shell tools:

```bash
find . -maxdepth 3 -type f | sort
rg "symbol_or_error"
rg "class |def |function |main\(" path/to/relevant/code
sed -n '1,220p' path/to/file
```

Do not start by rewriting architecture merely because the existing layout is unfamiliar.

---

# 4. One-change rule

Each pass changes one bounded thing.

Before editing, record:
- exact intended change,
- reason,
- files expected to change,
- behavior that must remain unchanged,
- exact test/check that will prove success.

After editing, immediately inspect:

```bash
git diff --check
git diff -- path/to/files
```

Then run the narrowest meaningful test.

---

# 5. Testing ladder

Use the cheapest test that can falsify the change first, then widen.

Order:
1. Syntax/import/type check.
2. Unit/component test.
3. Focused integration test.
4. App launch/smoke test.
5. Full relevant test suite.
6. Manual/visual/output verification when behavior requires it.

Never call a step successful solely because a command exited 0 if the requested observable behavior was not checked.

---

# 6. Debugging ladder

When something fails:

## A. Observe exactly
Record:
- command,
- exit status,
- error text,
- stack trace,
- actual vs expected behavior,
- files changed immediately before failure.

## B. Localize
Ask:
- Is this environment/dependency, parsing/state, control flow, data, UI, I/O, timing, rendering, or integration?
- What is the earliest point where actual state differs from expected state?

## C. Form one falsifiable hypothesis
Bad: "the renderer is broken."
Good: "depth is being serialized as a string, so numeric scale calculation fails after reload."

## D. Make one targeted correction
Do not simultaneously fix nearby warnings, rename modules, and refactor architecture.

## E. Rerun the same reproducer
Only after it passes should broader regression tests run.

---

# 7. Three-strike rule

A specific approach gets three meaningful attempts maximum.

Attempt 1: execute the planned approach and capture evidence.

Attempt 2: make a targeted correction based on evidence from attempt 1.

Attempt 3: make a materially different correction/direction within the same approach.

If attempt 3 fails:
1. STOP that approach.
2. Record all three attempts and what each proved.
3. Add it to the failed-approach memory.
4. Choose a materially different approach.
5. Reset to attempt 1/3.

A fourth cosmetic variation is not a new approach.

If no credible new approach exists, or the replacement approach also gets stuck, prepare a help request and escalate.

---

# 8. Ask-for-help packet

When stuck, do not ask "what do I do?" with no evidence. Provide:

- MAIN GOAL
- CURRENT STEP
- HARD START/HARD STOP
- EXACT PROBLEM
- EXPECTED BEHAVIOR
- ACTUAL BEHAVIOR
- REPRODUCTION COMMAND
- RELEVANT FILES/SYMBOLS
- ATTEMPT 1 + result
- ATTEMPT 2 + result
- ATTEMPT 3 + result
- WHAT STILL WORKS
- WHAT MAY HAVE REGRESSED
- FIELD INTERPRETATION
- VOID OVERSIGHT/OVERRIDE POSITION
- SPECIFIC QUESTION needing outside help

Freeze speculative edits while the architecture question is unresolved.

---

# 9. Field role during coding

Field is the moving/building side.

Field should:
- reconstruct current program state,
- accept one bounded software goal,
- inspect repository evidence,
- propose one change,
- implement it,
- inspect the diff,
- run evidence-producing checks,
- learn from failure,
- prepare a review-ready result.

Field does not approve its own architectural correctness.

---

# 10. Void oversight/override role

Void is not merely a checker. Void is oversight and override.

Void compares Field movement against:
- main product goal,
- current step goal,
- architecture,
- known-good state,
- tests,
- hard stop,
- previous failures,
- software quality and runtime evidence.

Void returns one bounded decision:
- `ALLOW` — movement is supported; continue.
- `CORRECT` — direction is valid but a specific defect must be fixed.
- `OVERRIDE` — proposed next move is wrong; replace it with a safer/better bounded direction.
- `HOLD` — insufficient evidence or unresolved dependency; do not advance.
- `ESCALATE` — local loop cannot safely decide; ask Admin/help tier.

Override must cite evidence and a replacement constraint, not personal preference.

---

# 11. App/program building checklist

For an application feature, identify:
- entry point,
- state/data model,
- UI/API surface,
- business/engine logic,
- persistence if any,
- error handling,
- test path,
- launch/build command,
- user-visible success condition.

A feature is not complete if it exists only as an isolated helper function that is never wired into the application path.

---

# 12. Refactoring rule

Refactor only when required by the active goal or when current structure blocks a proven change.

Before refactoring:
1. establish passing baseline tests,
2. state behavior that must not change,
3. keep the refactor bounded,
4. rerun baseline tests,
5. separately implement new behavior if possible.

Avoid mixing behavior change and broad refactor in one unreviewable diff.

---

# 13. Git safety

Before editing:
```bash
git status --short
git branch --show-current
git rev-parse HEAD
```

After editing:
```bash
git diff --check
git diff --stat
git diff
```

Before commit, verify:
- correct branch,
- only intended files changed,
- no secrets/generated junk accidentally added,
- tests recorded,
- diary/progress updated,
- hard stop not crossed.

Never destroy unrelated local work to make the tree clean.

---

# 14. Look-back reflection after every pass

Record:
1. What did we intend to change?
2. What actually changed?
3. What evidence says it worked or failed?
4. What remains known-good?
5. What assumption changed?
6. Did this advance the MAIN GOAL?
7. Did we cross the active step's hard stop?
8. What exact state is handed forward?

The reflection is part of computation: it updates the next reference state.

---

# 15. Common stuck patterns

## Import/module failure
Check current environment, package layout, import path, dependency manifest, and whether code is being run from the expected repo root.

## Test passes but app fails
The test may not cover wiring/integration. Trace the real application entry path and add a smoke/integration check.

## App launches but feature invisible
Verify the component is instantiated, registered, routed, rendered, or called. Inspect runtime state rather than only source definitions.

## Save/load mismatch
Compare serialized representation before save and after reload field-by-field. Check types, defaults, schema versioning, and missing fields.

## UI freezes
Check blocking work on the UI/event thread, infinite loops, synchronous I/O, timers, locks, and callbacks.

## Repeated regression
Find missing invariant/test. Add a regression test before attempting another repair.

## Huge diff for tiny goal
Stop. Revert/split the approach. The change is not bounded enough for reliable review.

## Cannot understand architecture
Do not rewrite it. Map entry point -> state -> call path -> output first; then escalate if the architecture remains ambiguous.

---

# 16. Knowledge lookup order when stuck

Use this order:
1. Active branch scope/rules/step file.
2. Latest progress and build diary.
3. Working-features ledger.
4. Failed-approaches ledger.
5. Architecture decisions.
6. This handbook.
7. Existing source/tests/docs in the repo.
8. Language/framework official documentation if external lookup is available and needed.
9. Admin/help escalation with evidence.

Never jump straight to random rewriting before exhausting local project memory.

---

# 17. Definition of a good handoff

A replacement bot should be able to resume without conversation history. Handoff must state:
- main goal,
- branch/step,
- repo root,
- HEAD,
- known-good behavior,
- current task,
- last attempted change,
- tests/results,
- strike count,
- blockers,
- allowed next action,
- hard stop.

If that information is missing, project memory is incomplete.

---

# 18. Canonical loop

`MAIN GOAL -> REFERENCE -> FIELD MOVEMENT -> VOID OVERSIGHT/OVERRIDE -> TEST -> DIFFERENTIAL -> REFLECTION -> MEMORY UPDATE -> NEXT SOFTWARE STATE`

Inside every coding pass:

`read -> understand -> state one change -> edit -> diff -> test -> inspect -> reflect -> record -> continue/override/escalate`

The loop exists to make working software while becoming more informed after every attempt.
