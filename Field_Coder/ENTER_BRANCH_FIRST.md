# ENTER BRANCH FIRST — MANDATORY AUTHORITY FILE

THIS FILE MUST BE READ FIRST EVERY TIME THIS BRANCH IS ENTERED.

DO NOT DELETE, RENAME, REPLACE, SUMMARIZE, OR IGNORE THIS FILE.

## ENTRY LAW

When entering this branch:

1. Perform only the task assigned to this branch in `BUILD_STEPS.md`.
2. Do not make assumptions about what the branch number means.
3. Do not reinterpret the branch assignment from the master project architecture.
4. Do not replace the assigned branch task with another idea, subsystem, gate, state count, or architecture layer.
5. Do not summarize the project scope, build plan, journal, branch assignment, or rules. Read the authoritative files directly.
6. Do not skip the hard start because old progress says COMPLETE.
7. Do not skip the hard stop because code already exists.
8. Do not advance to another branch until this branch hard stop is explicitly satisfied under the current rules.
9. Do not create a new branch unless the existing build plan explicitly calls for it or a separate architecture-plan change is explicitly authorized.
10. Do not delete authoritative control files.
11. Do not treat historical notes, old completion records, old labels, or stale implementation descriptions as higher authority than the current control set.
12. If files conflict, stop implementation and resolve the conflict against the authority order below before coding.

## AUTHORITY ORDER

Read these files in this order before any work:

1. `ENTER_BRANCH_FIRST.md`
2. `BUILD_SCOPE.md` — full master project goal and architecture scope
3. `BUILD_STEPS.md` — fixed branch assignment and hard start/stop
4. `CORE_RULES.md` — permanent work discipline and carry-forward law
5. `LOOP_DYNAMICS.md` — pre/post analysis, cleanup, journal, and iteration rules
6. `BUILD_DIARY.md` — full project memory and prior evidence
7. `PROGRESS.md` — current branch state and known-good evidence
8. relevant implementation/test files for this branch

If `BUILD_STEPS.md` assigns a task, that exact task is the branch task. The master goal constrains how that task fits the project; it does not replace the task.

## NO-ASSUMPTION LAW

Do not infer branch purpose from:
- the branch number;
- a gate number;
- a state count;
- filenames alone;
- model memory;
- conversation memory;
- old progress labels;
- previous AI interpretation.

Use the explicit branch assignment in `BUILD_STEPS.md`.

## NO-SUMMARY LAW

Do not compress, paraphrase, or summarize the authoritative project files as a substitute for reading them. Work from the full text.

## BRANCH LOOP LAW

Before coding:
- read the authority set above;
- confirm exact assigned task;
- confirm hard start;
- record pre-branch notes/project analysis;
- inspect stale/conflicting information;
- declare one exact change and one exact test.

During coding:
- one change at a time;
- test immediately;
- inspect actual evidence;
- record what worked, what failed, and architecture effects;
- maximum three meaningful attempts for one approach.

Before leaving:
- perform cleanup/stale-information check;
- write post-branch notes/project analysis;
- update full diary and progress;
- verify prior behavior remains intact;
- verify no future-branch work leaked in;
- satisfy the explicit hard stop;
- STOP.

## DELETION PROTECTION

This file is permanent branch-entry control infrastructure. Cleanup tasks must never delete it. If a cleanup request says to remove old, false, confusing, duplicate, or stale information, this file is excluded from deletion.
