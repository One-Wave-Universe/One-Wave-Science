# BRANCH MEMORANDUM — TEMPLATE

## COMPLETE PROJECT SCOPE

[PASTE THE FULL CURRENT PROJECT SCOPE HERE. DO NOT ABBREVIATE.]

## COMPLETE CODING PROJECT ROADMAP

[PASTE THE FULL ORDERED CODING PLAN HERE. DO NOT ABBREVIATE OR OMIT FUTURE BRANCHES.]

For every branch in the coding project, state explicitly:

- branch number/order;
- branch name;
- exact subsystem that branch owns;
- what code is supposed to be created or changed there;
- why that subsystem is needed by the complete program;
- what earlier branch output it depends on;
- what it must hand to later branches;
- CPU responsibility for that branch;
- GPU responsibility for that branch, if any;
- Field responsibility for that branch;
- Void oversight/override responsibility for that branch;
- expected files/modules;
- required tests;
- branch-specific hard start;
- branch-specific hard stop;
- forbidden future work.

The roadmap must make the current branch's exact position in the complete coding project unmistakable.

## COMPLETE ACCUMULATED JOURNAL HISTORY

[PASTE/CARRY FORWARD EVERY PRIOR PRE-BRANCH AND POST-BRANCH JOURNAL ENTRY IN CHRONOLOGICAL ORDER. DO NOT CONDENSE.]

## CURRENT PROJECT PROGRESS

- Plan version:
- Completed branches:
- Current branch:
- Future branches:
- Known-good reference:
- Verified working features:
- Passing tests:
- Failing tests:
- Open blockers:
- Current attempt:
- Relevant failed approaches:
- Open architecture concerns:
- Next permitted action:

## BUILD METHOD — BEGINNING OF STEP

The complete coding plan was designed before implementation began and broken into ordered programming steps. Those steps were created ahead of time as branches. This branch is one preplanned coding stage. Only this branch's assigned subsystem may be coded here. Make one controlled change at a time, test it before the next change, preserve verified prior behavior, record evidence, and stop immediately when this branch's hard stop is satisfied. Do not implement future branch work early.

## THIS BRANCH'S POSITION IN THE CODING PROJECT

This section must be filled in explicitly before coding. Do not use vague wording such as "continue engine work" or "next component."

- Current branch number:
- Current branch name:
- Previous branch:
- Next branch:
- Complete program being built:
- Exact subsystem this branch owns:
- Exact code this branch must add/change:
- Why this subsystem belongs at this point in the build order:
- What already-working code this branch builds on:
- Inputs inherited from earlier branches:
- Outputs this branch must provide to later branches:
- Interfaces this branch must expose:
- State/data this branch reads:
- State/data this branch writes:
- CPU work assigned here:
- GPU work assigned here:
- Field work assigned here:
- Void oversight/override assigned here:
- Files/modules expected to exist when this branch closes:
- Tests that prove this branch's piece works:
- What later branches are waiting on this branch:
- Work that absolutely belongs to later branches and must not be coded here:

A future AI opening only this memorandum must be able to tell exactly what part of the complete software architecture this branch is responsible for coding.

## CURRENT BRANCH CONTRACT

- Branch name:
- Branch number/order:
- Exact subsystem:
- Why this subsystem exists:
- Dependencies:
- Required inputs:
- Required outputs:
- Expected files/modules:
- Allowed scope:
- Forbidden scope:
- Forbidden future work:
- First permitted code change:
- Exact first test:
- Success criteria:
- Rollback point:
- Branch-specific hard start:
- Branch-specific hard stop:
- Next branch:

## HARD START CHECK

- Full project scope present: YES/NO
- Full coding-project roadmap present: YES/NO
- Current branch position in roadmap explicit: YES/NO
- Complete prior journal history present: YES/NO
- Current progress present: YES/NO
- Correct plan version loaded: YES/NO
- Local repo verified: YES/NO
- Correct branch verified: YES/NO
- Previous branch complete: YES/NO
- Previous hard-stop evidence present: YES/NO
- Known-good state identified: YES/NO
- Required inputs available: YES/NO
- Required outputs explicit: YES/NO
- CPU/GPU responsibilities explicit: YES/NO
- Field/Void responsibilities explicit: YES/NO
- Allowed scope explicit: YES/NO
- Forbidden scope explicit: YES/NO
- Forbidden future work explicit: YES/NO
- First code change explicit: YES/NO
- First test explicit: YES/NO

If any required item is NO, do not code.

## ACTIVE-BRANCH JOURNAL

For every controlled change append:

- Order/timestamp:
- Attempt:
- Approach ID:
- Intended change:
- Reason:
- Expected files:
- Actual files:
- Diff reference:
- Exact test:
- Exact result:
- What worked:
- What did not work:
- What was learned:
- Effect on later branch architecture:
- Void decision:
- Next permitted movement:
- Rollback action if used:

## HARD STOP CHECK

- Assigned subsystem implemented: YES/NO
- Required outputs exist: YES/NO
- Required interfaces exist: YES/NO
- Required tests pass: YES/NO
- Previous verified behavior still passes: YES/NO
- Changes stayed inside allowed scope: YES/NO
- No future branch work was implemented: YES/NO
- Later branches received the expected handoff outputs: YES/NO
- Attempts recorded: YES/NO
- Failures recorded: YES/NO
- What worked recorded: YES/NO
- What did not work recorded: YES/NO
- Future architecture evidence recorded: YES/NO
- Void final decision recorded: YES/NO
- Progress updated: YES/NO
- Post-branch journal appended: YES/NO
- Known-good reference preserved: YES/NO
- Rollback point preserved: YES/NO
- Next branch identified: YES/NO
- Next branch hard start explicit: YES/NO

If any required item is NO, the branch is not complete.

## POST-BRANCH JOURNAL

[APPEND THE COMPLETE POST-BRANCH ENTRY HERE BEFORE LEAVING THE BRANCH.]

The post-branch entry must explicitly state what piece of the complete program now exists because of this branch, what later branch can use it, and any architecture evidence discovered while coding it.

## BUILD METHOD — END OF STEP

This branch was one preplanned step in the complete coding plan. Only this branch's assigned subsystem was permitted here. Coding stops at this branch's hard stop. The complete project scope, complete coding-project roadmap, current project progress, and complete accumulated journal history must carry into the next branch memorandum. The next branch already exists as the next planned work slot and must pass its own hard start before coding begins.