# FIELD CODER — BRANCH LOOP CONTROLLER

## PURPOSE

The Branch Loop Controller is the automatic AI-controlled mechanism that takes a software project from an explicit project goal through a preplanned sequence of coding branches, one coded subsystem at a time.

The controller must never invent the build sequence while coding.

Before implementation begins, the project must be broken into explicit coding stages. Each stage becomes a pre-created branch. Those branches are the fixed coding roadmap for the project.

The controller executes that roadmap one branch at a time.

Routine repository operations, branch transitions, journal updates, progress updates, test execution, evidence collection, retry accounting, handbook lookup, and branch completion checks are AI-controlled and automatic.

The human supplies or approves the project-level goal and major architecture changes. The human is not required to manually perform routine loop operations.

---

# REQUIRED PROJECT REFERENCE

Every project controlled by this mechanism must have a project-level reference file equivalent to:

`MASTER_CODE_PLAN.md`

That file must explicitly define:

- project name;
- project purpose;
- complete main goal;
- required final behavior;
- intended users or calling agents;
- software/app/program being built;
- Field responsibilities;
- Void oversight/override responsibilities;
- CPU responsibilities;
- GPU responsibilities where applicable;
- M4/controller responsibilities where applicable;
- persistent memory/state requirements;
- repository/local-project location;
- required interfaces;
- required inputs;
- required outputs;
- required tests;
- required safety boundaries;
- required rollback behavior;
- required logging/journal behavior;
- required progress reporting behavior;
- required architecture-decision recording;
- final integration criteria;
- final project hard stop.

No coding branch may begin unless this project reference exists and is readable.

---

# PROJECT PLANNING PHASE — MUST HAPPEN BEFORE CODING

Before any implementation branch is coded, the AI must break the project into an ordered coding plan.

Each coding-plan step becomes one pre-created branch.

Each planned branch must define, before coding starts:

- branch name;
- branch number/order;
- exact subsystem assigned to that branch;
- why that subsystem exists;
- dependency on previous branches;
- required inputs from previous branches;
- outputs that this branch must produce for later branches;
- files/modules expected to be created or modified;
- allowed scope;
- forbidden scope;
- future work explicitly forbidden on this branch;
- branch-specific hard start;
- branch-specific success criteria;
- branch-specific required tests;
- branch-specific hard stop;
- rollback point;
- required pre-branch journal entry;
- required post-branch journal entry;
- required progress update;
- required architecture notes;
- next planned branch.

All planned branches must be created before implementation begins unless the master plan explicitly states that a later branch cannot yet be known.

Creating the branches does not mean coding them early.

A branch existing ahead of time is only a reserved work slot in the project roadmap.

---

# PLAN VERSION LOCK

At project start, record a plan version and plan reference.

Every branch must record which plan version it is executing.

The project plan may not be silently rewritten during implementation.

If evidence shows that the architecture or coding plan must change:

1. stop the active branch at a safe state;
2. write the reason to the architecture-change ledger;
3. record evidence that caused the proposed change;
4. identify which future branches are affected;
5. preserve previous plan version;
6. create a new plan version;
7. update affected future branch contracts explicitly;
8. do not rewrite completed historical branch records.

Completed evidence remains historical truth even when future architecture changes.

---

# LOCAL PROJECT LOCATION

Primary local working repository for the current project:

`$HOME/One-Wave-Science`

The controller must verify the actual local project root automatically before coding.

At every branch hard start it records:

- repository root;
- worktree path;
- active branch;
- HEAD;
- working-tree status;
- known-good commit/reference;
- current plan version;
- current branch contract;
- previous completed branch;
- next planned branch.

If the local repository cannot be verified, the controller must HOLD rather than guess.

---

# REQUIRED PROJECT MEMORY

The controller must maintain durable project memory, not rely on AI conversational memory.

Required memory categories:

- master project goal;
- master coding plan;
- branch contracts;
- branch order;
- branch dependencies;
- current progress;
- pre-branch journal entries;
- post-branch journal entries;
- working features;
- known-good behavior;
- failed approaches;
- attempt history;
- test evidence;
- architecture decisions;
- architecture-change proposals;
- unresolved blockers;
- handoff state;
- final integration state.

Future AI workers must be able to reconstruct the project from repository memory alone.

---

# PRE-BRANCH JOURNAL — REQUIRED BEFORE EVERY BRANCH

Before coding begins on every branch, automatically write a journal entry containing:

- project name;
- complete main project goal;
- plan version;
- current branch;
- exact branch goal;
- why this branch exists;
- previous branch result;
- known-good starting state;
- current HEAD/reference;
- branch dependencies;
- inputs available to this branch;
- outputs this branch must create;
- allowed files/modules;
- forbidden files/modules;
- forbidden future work;
- branch hard start requirements;
- confirmation that hard start passed;
- exact first coding change;
- exact test for that change;
- attempt number;
- known risks;
- unresolved questions;
- expected branch hard stop.

No code change may occur before this entry exists.

---

# HARD START — REQUIRED FOR EVERY BRANCH

Every branch has its own explicit hard start.

A branch may not become ACTIVE until the controller verifies all branch-specific requirements plus these global requirements:

1. complete main project goal is loaded;
2. current plan version is loaded;
3. correct local project is verified;
4. correct pre-created branch exists;
5. previous required branch is complete;
6. previous branch post-journal exists;
7. previous progress update exists;
8. previous required tests passed or an explicit accepted exception exists;
9. known-good reference is identified;
10. current branch dependency requirements are satisfied;
11. current branch inputs exist;
12. current branch outputs are explicit;
13. allowed scope is explicit;
14. forbidden scope is explicit;
15. forbidden future work is explicit;
16. exact first coding change is explicit;
17. exact test for that change is explicit;
18. pre-branch journal entry exists.

If any required condition fails, do not code.

State becomes HOLD, BLOCKED, or ESCALATE according to the evidence.

---

# ONE-CHANGE CODING LOOP

Within an active branch, execute one controlled code change at a time.

For every change:

1. reload branch goal and master project goal;
2. inspect current known-good state;
3. declare exactly one intended code change;
4. declare files expected to change;
5. declare expected behavior change;
6. declare behavior that must remain unchanged;
7. declare exact verification/test;
8. make the one code change;
9. capture actual changed files;
10. capture actual diff;
11. run the declared test;
12. capture stdout/stderr/exit status/runtime evidence;
13. compare expected result against actual result;
14. record what worked;
15. record what did not work;
16. record what was learned for future architecture or implementation;
17. send evidence to Void oversight/override;
18. receive next-state decision;
19. persist state before another code change begins.

No second code change begins before the first change completes this cycle.

---

# FIELD ROLE

Field is the software-building side of the engine.

Field may:

- inspect project evidence;
- propose a bounded code change;
- implement the declared change;
- run or request required tests;
- interpret implementation evidence;
- learn from failed implementation attempts;
- propose a corrected implementation.

Field may not silently broaden branch scope or approve its own architecture as correct.

---

# VOID OVERSIGHT / OVERRIDE ROLE

Void observes the same project goal, plan version, branch contract, known-good reference, proposal, actual diff, tests, progress evidence, and failure history.

Void controls whether the next software movement is permitted.

Void returns one of:

- `ALLOW`
- `CORRECT`
- `OVERRIDE`
- `HOLD`
- `ESCALATE`

`OVERRIDE` means Void may replace Field's proposed next movement with a bounded corrective next action consistent with the project goal and current branch contract.

Void does not silently turn itself into an unrestricted second implementation agent.

---

# THREE-ATTEMPT RULE

For one failing approach inside the current branch:

- Attempt 1: planned implementation.
- Attempt 2: targeted correction based on Attempt 1 evidence.
- Attempt 3: materially different evidence-based correction.

There is no hidden Attempt 4.

After Attempt 3 fails:

- mark that approach failed;
- write failure evidence to durable memory;
- write what was learned;
- search coding handbook/reference material;
- search previous failed approaches;
- search repository for related working patterns;
- Void chooses OVERRIDE, HOLD, or ESCALATE;
- a genuinely different approach may begin only if explicitly recorded as a new approach.

Repeatedly changing small details of the same failed approach does not reset the counter.

---

# AUTOMATIC REFERENCE LOOKUP WHEN STUCK

When an implementation is stuck, the controller automatically searches available project references before escalating.

Lookup order:

1. current branch contract;
2. master code plan;
3. previous branch journals;
4. working-features ledger;
5. failed-approaches ledger;
6. architecture decisions;
7. bot coding handbook;
8. repository code containing related working behavior;
9. tests and fixtures;
10. higher-level escalation if still unresolved.

The AI must not guess when durable project evidence exists.

---

# PROGRESS REPORT — REQUIRED THROUGHOUT THE PROJECT

Progress must be updated after every meaningful branch event and at branch close.

Progress records must include:

- current project;
- complete project goal reference;
- plan version;
- current branch;
- current branch goal;
- branch status;
- current attempt;
- completed branches;
- verified working behavior;
- current known-good reference;
- tests currently passing;
- tests currently failing;
- blockers;
- failed approaches;
- architecture concerns;
- next permitted action.

Progress is evidence for future agents, not conversational commentary.

---

# WHAT WORKED / WHAT DID NOT WORK — REQUIRED

Every branch must leave explicit evidence useful to future architecture work.

Record separately:

## WHAT WORKED

- implementation patterns that behaved correctly;
- interfaces that proved stable;
- tests that provided useful evidence;
- performance behavior that met requirements;
- assumptions supported by evidence;
- reusable code or patterns.

## WHAT DID NOT WORK

- failed approaches;
- failing assumptions;
- unstable interfaces;
- misleading tests;
- performance failures;
- platform-specific failures;
- dead ends;
- approaches that must not be casually repeated.

## FUTURE ARCHITECTURE EVIDENCE

Record observations that may matter to later architecture changes without automatically changing the current plan.

An observation is evidence, not permission to rewrite architecture.

---

# ARCHITECTURE CHANGE LEDGER

Any possible architecture change must be recorded with:

- current plan version;
- branch where evidence appeared;
- exact observed problem;
- supporting test/diff/runtime evidence;
- proposed architecture change;
- expected benefit;
- affected branches;
- risk to verified behavior;
- decision: ACCEPT / REJECT / DEFER / ESCALATE;
- new plan version if accepted.

Architecture changes must never erase old evidence.

---

# POST-BRANCH JOURNAL — REQUIRED AFTER EVERY BRANCH

Before leaving a branch, automatically write a closing journal entry containing:

- complete main project goal;
- plan version;
- branch name;
- branch goal;
- starting known-good reference;
- final candidate/known-good reference;
- every meaningful change made;
- files changed;
- tests run;
- exact results;
- attempts used;
- Void decisions;
- what worked;
- what did not work;
- what was learned;
- architecture evidence discovered;
- failed approaches that should not be repeated;
- branch outputs produced;
- confirmation that required outputs exist;
- confirmation previous verified behavior remains intact;
- confirmation future branch work was not implemented early;
- branch hard-stop evidence;
- next branch name;
- next branch hard-start requirements.

The branch cannot close without this entry.

---

# HARD STOP — REQUIRED FOR EVERY BRANCH

Every branch has its own explicit hard stop.

The controller must verify the branch-specific hard stop plus these global conditions:

1. assigned subsystem is implemented to the branch contract;
2. required branch outputs exist;
3. required branch tests pass;
4. previous verified behavior still passes;
5. diff stayed inside allowed scope;
6. forbidden future work was not implemented;
7. attempts/failures are recorded;
8. what-worked evidence is recorded;
9. what-did-not-work evidence is recorded;
10. future-architecture evidence is recorded;
11. architecture decisions/changes are recorded if applicable;
12. progress report is updated;
13. post-branch journal exists;
14. known-good reference is identified;
15. rollback point is preserved;
16. next branch exists;
17. next branch hard start is known.

When the hard stop passes, stop coding that branch immediately.

Do not begin the next branch's implementation from the current branch.

---

# BRANCH TRANSITION

After hard stop passes:

1. preserve current branch evidence;
2. preserve known-good reference;
3. mark current branch COMPLETE;
4. load next pre-created branch from the plan;
5. transfer only approved project state/implementation according to the project's Git strategy;
6. create next branch pre-journal entry;
7. enter next branch HARD START;
8. verify all next-branch hard-start requirements;
9. only then permit coding.

---

# ROLLBACK / KNOWN-GOOD CONTROL

Before each implementation change, the controller must know how to return to the current known-good state.

Failed changes must not destroy the last verified implementation.

The controller records:

- known-good HEAD/reference;
- candidate reference;
- changed files;
- rollback action;
- whether rollback was required;
- whether rollback restored verified behavior.

No branch is allowed to destroy the only known-good state.

---

# MACHINE-READABLE CONTROLLER STATE

The controller maintains at least:

- `project_id`
- `project_goal_reference`
- `plan_version`
- `branch_plan`
- `current_branch`
- `previous_branch`
- `next_branch`
- `branch_goal`
- `branch_dependencies`
- `required_inputs`
- `required_outputs`
- `allowed_scope`
- `forbidden_scope`
- `forbidden_future_work`
- `branch_status`
- `hard_start_status`
- `hard_stop_status`
- `attempt`
- `max_attempts`
- `approach_id`
- `known_good_reference`
- `candidate_reference`
- `last_change`
- `last_diff`
- `last_test`
- `last_result`
- `what_worked`
- `what_failed`
- `architecture_evidence`
- `void_decision`
- `blocker`
- `rollback_state`
- `pre_branch_journal_state`
- `post_branch_journal_state`
- `progress_state`
- `escalation_packet`

---

# ESCALATION PACKET

If autonomous work cannot continue safely, produce evidence containing:

- complete project goal reference;
- plan version;
- current branch contract;
- hard-start state;
- current known-good state;
- current candidate state;
- current task;
- branch inputs and required outputs;
- attempts and approach IDs;
- diffs;
- tests and outputs;
- Void decisions;
- what worked;
- what did not work;
- architecture evidence;
- references already searched;
- failed approaches already ruled out;
- unresolved question;
- safest preserved repository state.

---

# PROJECT COMPLETION

The project is not complete merely because the last branch was visited.

The final planned branch must verify the master project's explicit final integration criteria and final project hard stop.

The controller stops the project only when the final hard stop in the master code plan is satisfied or when the project enters HOLD/BLOCKED/ESCALATE.

---

# NON-NEGOTIABLE PROJECT LAW

Before every software project:

`DEFINE COMPLETE PROJECT GOAL`
-> `BREAK CODING WORK INTO EXPLICIT ORDERED STEPS`
-> `TURN THOSE STEPS INTO PRE-CREATED BRANCHES`
-> `GIVE EVERY BRANCH ITS OWN CONTRACT + HARD START + HARD STOP`
-> `CODE ONE BRANCH AT A TIME`
-> `JOURNAL BEFORE`
-> `MAKE ONE CONTROLLED CHANGE`
-> `TEST`
-> `RECORD WHAT WORKED / WHAT DID NOT`
-> `VOID OVERSIGHT / OVERRIDE`
-> `UPDATE PROGRESS`
-> `JOURNAL AFTER`
-> `VERIFY HARD STOP`
-> `ONLY THEN MOVE TO THE NEXT PRE-CREATED BRANCH`

The Branch Loop Controller exists to execute the software project's preplanned coding architecture. It must never replace the actual project with an orchestration project of its own.