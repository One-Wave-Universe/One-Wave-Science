# FIELD CODER — BRANCH MEMORANDUM STANDARD

Every coding branch must contain a branch memorandum that can stand on its own without conversational memory.

## FULL PROJECT SCOPE — REQUIRED IN EVERY MEMORANDUM

Every branch memorandum must include the complete current project scope, including project name, purpose, complete main goal, required final behavior, software/app/program-building purpose, Field role, Void oversight/override role, M4/controller role where applicable, CPU role, GPU role where applicable, persistent memory/state requirements, local repo location, interfaces, inputs, outputs, test requirements, rollback rules, branch-loop rules, three-attempt rule, architecture-change rule, final integration criteria, and final project hard stop.

Do not replace this with `see master plan`, `same as previous branch`, `inherits prior scope`, or another abbreviated reference. A reference may verify the source, but the operative full scope must also exist inside the branch memorandum.

## BUILD METHOD — REQUIRED AT THE BEGINNING

State explicitly that the full coding plan is designed first, broken into ordered programming steps, and those steps are created ahead of time as branches. The current branch is one preplanned coding stage. Code only its assigned subsystem. Make one controlled change at a time. Test each change before the next one. Preserve verified prior behavior. Stop immediately at the branch hard stop. Do not implement future branch work early.

## COMPLETE PRIOR JOURNAL HISTORY — REQUIRED

Every branch memorandum must carry forward the complete prior project journal history available when the branch begins, in chronological order. Include every prior pre-branch entry, every prior post-branch entry, material attempts, failures that affected future decisions, Void corrections/overrides, known-good checkpoints, accepted architecture decisions, rejected/deferred architecture proposals still relevant, and unresolved issues.

Do not reduce prior journal history to a recap. Preserve historical branch identity and meaning.

## CURRENT PROGRESS — REQUIRED

Include completed branches, active branch, future branches, verified working features, known-good reference, passing tests, failing tests, blockers, current attempt, relevant failed approaches, open architecture concerns, and next permitted action.

## CURRENT BRANCH CONTRACT — REQUIRED

Include branch name/order, plan version, exact subsystem, why it exists, dependencies, required inputs, required outputs, expected files/modules, allowed scope, forbidden scope, forbidden future work, first permitted code change, exact test, all success criteria, rollback point, branch-specific hard start, branch-specific hard stop, and next branch.

## HARD START BLOCK

Before coding, explicitly verify:

- full project scope present;
- complete prior journal history present;
- current progress present;
- plan version correct;
- local repo verified;
- branch verified;
- previous branch complete;
- previous hard-stop evidence present;
- known-good state identified;
- required inputs available;
- allowed scope explicit;
- forbidden scope explicit;
- first code change explicit;
- first test explicit.

If any required item fails, coding must not begin.

## ACTIVE BRANCH RECORD

For each controlled change append: order/timestamp, attempt, approach ID, intended change, reason, expected files, actual files, diff reference, exact test, exact result, what worked, what failed, what was learned, Void decision, next permitted movement, and rollback action if used.

## HARD STOP BLOCK

Before leaving the branch verify:

- assigned subsystem implemented;
- required outputs exist;
- required tests pass;
- previous verified behavior still passes;
- changes stayed inside scope;
- no future branch work was implemented;
- attempts and failures are recorded;
- what worked is recorded;
- what did not work is recorded;
- future architecture evidence is recorded;
- Void decision is recorded;
- progress is updated;
- post-branch journal is appended;
- known-good reference is preserved;
- rollback point is preserved;
- next branch is identified;
- next branch hard start is explicit.

If any required item fails, the branch is not complete.

## BUILD METHOD — REQUIRED AT THE END

End every memorandum by stating that this branch was one preplanned step in the full coding plan, only its assigned subsystem was permitted, coding stops at hard stop, complete project scope and complete accumulated journal history carry into the next branch memorandum, the next branch already exists as the next work slot, and the next branch must pass its own hard start before coding begins.

The project must never depend on an AI remembering these rules from conversation.