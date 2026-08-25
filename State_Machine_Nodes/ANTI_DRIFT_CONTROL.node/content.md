# State-Machine Nodesification Anti-Drift Control

## Main goal

Convert every active state-machine definition, transition, gate, action, view, scale, lifecycle rule, and validation rule into a canonical node graph without rewriting the established architecture.

Ordinary explanations, history, superseded material, and archived records are not executable nodes. They may reference canonical nodes but may not silently redefine them.

## Required node folder

Each converted state-machine unit uses a `.node` watchdog folder containing:

- `node.yaml`
- `content.md`
- `logic_chain.yaml`
- `dependencies.yaml`
- `node.watchdog.yaml`
- `telemetry/`
- `receipts/`
- `notes-to-self.md`

A `.node` folder is a watchdog folder type, not a separate executable per node.

## One-change loop

For every conversion unit:

1. Record the exact source and current canonical meaning.
2. Convert one bounded unit.
3. Run its structural and semantic checks immediately.
4. Compare the result with the active goal and protected canon.
5. Record drift, even when drift is zero.
6. Write the receipt and notes-to-self before advancing.
7. After three failures of the same approach, stop it, record what was learned, and switch approaches.
8. Stop at the branch-step hard stop.

## Anti-drift receipt law

A conversion is incomplete without a receipt recording:

- date/time;
- branch, worktree, and HEAD before and after;
- main goal and current bounded goal;
- source files read;
- files changed;
- canonical meanings preserved;
- tests/checks and exact results;
- intended versus actual diff;
- drift found or `NONE`;
- what worked and failed;
- attempt/strike count;
- Field notes;
- Void oversight decision;
- next permitted action;
- hard-stop status.

## Notes-to-self law

Before and after every bounded conversion, update `notes-to-self.md` with:

- what must not change;
- what is still uncertain;
- what evidence would falsify the current mapping;
- failed approaches not to repeat;
- protected working behavior;
- the exact next permitted action;
- a direct check that the work still serves the main goal.

## Protected separation

The five Field lifecycle states are:

`Idle -> Primed -> Executing -> Vectoring -> Resolving`

They are not the five modulation levels and not the six recursion steps:

`Begin -> Build -> Hold -> Build -> Break -> Loop`

No conversion may merge these three layers.
