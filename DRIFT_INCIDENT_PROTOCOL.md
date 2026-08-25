# DRIFT INCIDENT PROTOCOL

THIS NOTE PERTAINS TO THIS PAGE ONLY. It has nothing to do with rules or updates for any other page. It is the repository-wide incident procedure page only. It does not summarize, replace, inherit, or modify the local instructions on any other page.

## Purpose of this page
Define what must happen after a work action is identified as drift anywhere in this repository.

Drift means the worker moved away from the explicit current task, local page/file instructions, protected working behavior, or required test path and substituted another goal, architecture, demo, workflow, or assumption.

## Immediate response to drift
When drift is detected:
1. STOP the drifting action.
2. Do not defend it, hide it, rename it, or continue building on top of it.
3. Mark the current anti-drift streak as reset to 0 in the applicable ledger.
4. Preserve the last known-good state.
5. Create a drift incident report before resuming implementation.

## Required drift incident report
Every drift report must contain:
- date and local time;
- repository, branch/worktree, and HEAD if known;
- page/file/area where drift occurred;
- explicit task that should have been performed;
- actual action that drifted;
- exact mismatch between task and action;
- trigger: what assumption, generic pattern, shortcut, missing reference, or context failure caused the deviation;
- consequence: what was changed, wasted, confused, or put at risk;
- last known-good state;
- whether any incorrect files/code/data must be reverted, removed, or isolated;
- immediate corrective action;
- prevention actions;
- verification that proves the correction really returns to the intended path.

## Root-cause classification
Use one or more concrete causes. Do not write only "AI drifted."

Examples:
- generic-pattern substitution;
- wrong project/area assumed;
- local reference not read;
- user correction not carried forward;
- stale architecture reused;
- premature optimization;
- fake/placeholder acceptance test;
- external test substituted for real workflow;
- scope expansion;
- unverified assumption;
- conflicting notes treated as interchangeable;
- storage/data model silently changed;
- implementation started before inspecting current state.

Add a new cause when none of these accurately describes the event.

## Prevention action rule
A drift report is incomplete until at least one prevention action changes future behavior.

Possible prevention actions include:
- add or strengthen a local reference in the affected page/file/area;
- add a pre-action checklist item;
- add a regression/acceptance test;
- protect a known-good file/feature explicitly;
- remove or label a misleading obsolete path;
- require a real-workflow test instead of a mock;
- require asset/state inspection before implementation;
- split an overlarge step into smaller bounded actions;
- add a prohibited-substitution rule;
- add the failure pattern to the local failed-approach record.

Do not add busywork. The prevention action must directly target the identified cause.

## Resume gate
Work may resume only when:
1. the report names a concrete cause;
2. corrective action is defined;
3. at least one targeted prevention action is installed or explicitly queued as the next bounded action;
4. the worker rereads the local reference for the exact page/file/area being resumed;
5. the next action can be stated in one bounded sentence;
6. the verification method is known before the action starts.

## Feedback-loop law for this page
Use consequence as information:

`ACTION -> OBSERVED CONSEQUENCE -> COMPARE TO INTENT -> PASS OR DRIFT -> LEARN -> CORRECT/PREVENT -> NEXT ACTION`

The purpose is not punishment. The purpose is to make drift visible, learn why it happened, and change the process so the same failure becomes less likely.
