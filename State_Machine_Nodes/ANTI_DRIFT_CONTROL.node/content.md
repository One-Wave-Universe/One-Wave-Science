# State-Machine Nodesification Anti-Drift Control

## Main goal

Turn the active state-machine build into a clear, traceable node graph without changing the build structure.

Nodesification is an organizational conversion. It exposes the build that already exists: what each part is, where it connects, what it depends on, and how it is checked. It is not permission to redesign the machine.

## Meaning of no drift

**No drift means do not alter the established build structure.**

A conversion must not reorder, rename, merge, split, add, remove, replace, or reinterpret any established build component. The locked structure is recorded in `BUILD_STRUCTURE_LOCK.yaml`.

Allowed work:

- expose an existing component as a node;
- connect it to its existing dependencies;
- make its place in the build easier to follow;
- add validation, telemetry, receipts, indexes, and navigation;
- remove duplicate hard-coded definitions only after they point to the same locked canonical node.

Forbidden work:

- invent a cleaner architecture;
- move a component to a different layer;
- combine distinct layers;
- replace established names or order;
- change behavior while calling it nodesification;
- use a local optimization to reshape the whole build.

If a proposed node makes the build behave differently, changes its order, or changes what a component means, the watchdog must return `HOLD` or `OVERRIDE`.

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

1. Read `BUILD_STRUCTURE_LOCK.yaml`.
2. Record the exact source, structural position, connections, and canonical meaning.
3. Convert one bounded unit without altering any of them.
4. Run structural and semantic checks immediately.
5. Compare the resulting node graph to the locked build.
6. Record `NO_STRUCTURAL_DRIFT` only when the build is unchanged.
7. Write the receipt and notes-to-self before advancing.
8. After three failures of the same approach, stop it and use a materially different approach.
9. Stop at the branch-step hard stop.

## Anti-drift receipt law

A receipt must show, with evidence:

- which locked build components were touched;
- their before and after order, names, layer, connections, and meaning;
- whether runtime/build behavior changed;
- how clarity improved;
- exact checks and results;
- `NO_STRUCTURAL_DRIFT` or `STRUCTURAL_DRIFT_DETECTED`;
- the next permitted action.

A receipt may never report no drift merely because work stayed inside the task scope.

## Protected separation

The five Field lifecycle states remain:

`Idle -> Primed -> Executing -> Vectoring -> Resolving`

They remain distinct from five-level modulation and from:

`Begin -> Build -> Hold -> Build -> Break -> Loop`

Nodesification must make those relationships clearer without changing them.
