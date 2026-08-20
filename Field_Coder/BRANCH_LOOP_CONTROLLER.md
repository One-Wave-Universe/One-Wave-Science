# FIELD CODER — BRANCH LOOP CONTROLLER

## ROLE

The Branch Loop Controller is the automatic machine-control mechanism that moves the Field coding project through the pre-created programming branches one stage at a time.

It does not invent the programming plan while running.
It does not create a new build order while running.
It does not skip branches because a later feature looks useful.
It does not require the human to manually perform routine Git, test, progress, or transition operations.

The programming plan is defined first.
The branches are created ahead of time.
The controller executes that plan.

---

# MASTER REFERENCE

Before doing anything, the controller must load:

- `Field_Coder/MASTER_CODE_PLAN.md`
- `Field_Coder/BUILD_SCOPE.md`
- `Field_Coder/CORE_RULES.md`
- `Field_Coder/BUILD_STEPS.md`
- `Field_Coder/PROGRESS.md`
- latest `Field_Coder/BUILD_DIARY.md`
- coding handbook/reference material when needed

The controller must treat `MASTER_CODE_PLAN.md` as the permanent branch main-goal reference.

---

# LOCAL PROJECT LOCATION

Primary local working repository:

`$HOME/One-Wave-Science`

At the beginning of every branch cycle the controller automatically determines and records:

- repository root;
- active worktree;
- active branch;
- HEAD;
- working-tree status;
- current branch step;
- previous completed branch;
- current allowed files/subsystem;
- known-good test state.

If the local repository cannot be verified, the controller must HOLD rather than guess.

---

# BRANCH LOOP STATE

The controller maintains an explicit machine-readable state containing at least:

- `project_id`
- `main_goal_reference`
- `current_branch`
- `current_step`
- `previous_branch`
- `next_branch`
- `branch_status`
- `hard_start_status`
- `current_task`
- `allowed_scope`
- `forbidden_scope`
- `attempt`
- `max_attempts`
- `last_change`
- `last_test`
- `last_result`
- `void_decision`
- `hard_stop_status`
- `known_good_head`
- `candidate_head`
- `blocker`
- `escalation_packet`

Allowed `branch_status` values:

- `NOT_STARTED`
- `HARD_START`
- `ACTIVE`
- `TESTING`
- `CORRECTING`
- `WAITING_FOR_VOID`
- `HARD_STOP`
- `COMPLETE`
- `HOLD`
- `BLOCKED`
- `ESCALATE`

---

# AUTOMATIC BRANCH CYCLE

For each pre-created Field branch, execute this sequence exactly:

`LOAD PLAN`
-> `LOCATE LOCAL REPO`
-> `SELECT CURRENT PREPLANNED BRANCH`
-> `ENTER HARD START`
-> `VERIFY PREVIOUS STEP`
-> `LOAD CURRENT STEP CONTRACT`
-> `DECLARE ONE CODE CHANGE`
-> `FIELD IMPLEMENTS ONE CHANGE`
-> `CAPTURE ACTUAL DIFF`
-> `RUN EXACT TEST`
-> `CAPTURE EVIDENCE`
-> `VOID OVERSIGHT/OVERRIDE`
-> `DECIDE NEXT STATE`
-> `UPDATE DIARY/PROGRESS`
-> `CHECK HARD STOP`
-> `COMPLETE BRANCH OR LOOP CURRENT BRANCH`
-> `MOVE TO NEXT PRE-CREATED BRANCH ONLY AFTER COMPLETION`

---

# HARD START GATE

A branch may not become `ACTIVE` until all required hard-start conditions in `MASTER_CODE_PLAN.md` and `BUILD_STEPS.md` are satisfied.

The controller must automatically verify:

1. correct local repository exists;
2. correct pre-created branch exists;
3. previous required branch is complete;
4. previous success evidence exists;
5. known-good behavior is still valid;
6. main goal has been loaded;
7. current branch assignment has been loaded;
8. allowed scope is explicit;
9. forbidden future work is explicit;
10. exact test for the next code change is explicit.

If any required item fails, branch state becomes `HOLD` or `BLOCKED`.

No coding occurs before hard start passes.

---

# ONE-CHANGE INNER LOOP

Inside one active branch:

1. Field reads the current branch goal and evidence.
2. Field declares exactly one intended code change.
3. Controller records files expected to change.
4. Field applies that one change.
5. Controller captures actual changed files and diff.
6. If actual diff exceeds declared scope, stop and send to Void.
7. Controller runs the exact declared test.
8. Controller captures stdout, stderr, exit code, timeout and relevant runtime evidence.
9. Field may interpret the evidence, but cannot self-approve architectural correctness.
10. Void receives reference + proposal + actual diff + test evidence.

No second code change begins until the first change has completed this loop.

---

# VOID CONTROL OUTPUT

Void returns exactly one control decision:

- `ALLOW` — candidate movement is acceptable; continue toward hard stop or next declared change.
- `CORRECT` — remain in the current branch and make one evidence-targeted correction.
- `OVERRIDE` — reject Field's proposed next movement and replace the next action/state with the bounded corrective direction selected by Void.
- `HOLD` — preserve current state and do not modify code until a required condition/reference becomes available.
- `ESCALATE` — stop autonomous branch work and produce a complete escalation packet for higher-level review.

Void oversight controls the next movement. It does not become an unrestricted second Field coder.

---

# THREE-ATTEMPT MECHANISM

For a failing objective within the current branch:

- Attempt 1 = planned approach.
- Attempt 2 = targeted correction using Attempt 1 evidence.
- Attempt 3 = materially different evidence-based correction/direction.

After three failures:

- no Attempt 4 is permitted;
- current approach is marked failed;
- failure evidence is written to project memory;
- Void selects `OVERRIDE`, `HOLD`, or `ESCALATE`;
- if a genuinely different approved approach exists, attempt counter may reset for that new approach only;
- otherwise autonomous coding stops.

---

# HARD STOP GATE

The branch cannot become `COMPLETE` until its explicit hard-stop requirements are verified automatically.

The controller must check:

1. this branch's assigned subsystem is implemented;
2. branch success tests actually passed;
3. previously verified behavior still passes;
4. actual diff stayed inside allowed branch scope;
5. no future branch subsystem was implemented early;
6. attempt/failure evidence is recorded;
7. Field notes are recorded;
8. Void decision is recorded;
9. progress is updated;
10. look-back reflection is recorded;
11. known-good/candidate state is identified;
12. next branch hard-start requirements are known.

Once all required hard-stop conditions pass:

`branch_status = COMPLETE`

The controller stops coding that branch immediately.

---

# NEXT-BRANCH TRANSITION

Only after current branch status is `COMPLETE` may the controller select the next branch listed in the fixed programming plan.

Transition behavior:

1. preserve completed branch evidence;
2. identify next pre-created branch;
3. move/prepare the working implementation according to the project's approved Git/worktree strategy;
4. load the next branch's explicit contract;
5. set next branch state to `HARD_START`;
6. do not code until that hard start passes.

The existence of a later branch is not permission to work on it early.

---

# LOOP TERMINATION

The branch loop stops automatically when any of the following occurs:

- final planned branch reaches `COMPLETE`;
- Void returns `HOLD` with an unmet external requirement;
- Void returns `ESCALATE`;
- repository safety cannot be established;
- project references conflict materially;
- three-attempt handling produces no approved different approach;
- an architecture change would alter the preplanned master build.

Routine failure does not call the human automatically if Field/Void can resolve it inside the existing plan.

---

# ESCALATION PACKET

When escalation is required, automatically produce:

- main goal reference;
- current branch and step;
- exact branch assignment;
- hard-start state;
- starting known-good reference;
- current task;
- Attempt 1 action/evidence;
- Attempt 2 action/evidence;
- Attempt 3 action/evidence;
- actual diffs;
- tests and outputs;
- Void decisions;
- failed approaches already ruled out;
- unresolved question;
- safest preserved repository state.

Higher-level review receives evidence, not a vague request for help.

---

# CONTROLLER PSEUDOCODE

```text
load_master_plan()
load_project_state()

while project_not_complete:
    branch = next_planned_branch()
    enter(branch)

    if not hard_start_passes(branch):
        hold_or_escalate()
        break

    while not hard_stop_passes(branch):
        change = field.propose_one_change(branch, state, evidence)
        declare(change)
        apply_one_change(change)

        diff = capture_actual_diff()
        test = run_declared_test(change)
        evidence = collect(diff, test, state)

        decision = void.oversight_override(
            reference=known_good,
            goal=main_goal,
            branch_contract=branch.contract,
            candidate=change,
            evidence=evidence
        )

        persist_everything()

        if decision == ALLOW:
            continue
        if decision == CORRECT:
            increment_attempt()
            continue
        if decision == OVERRIDE:
            set_next_action(void.override_action)
            increment_attempt_or_reset_for_new_approach()
            continue
        if decision == HOLD:
            preserve_state()
            break
        if decision == ESCALATE:
            build_escalation_packet()
            break

        enforce_three_attempt_limit()

    if hard_stop_passes(branch):
        close_branch()
        set_next_planned_branch()
    else:
        stop_loop()
```

---

# NON-NEGOTIABLE RULE

The Branch Loop Controller executes the preplanned code project. It does not replace the code project with its own orchestration system.

Its job is to keep the actual Field/Void coding engine moving through the planned implementation stages accurately, automatically, and without branch drift.