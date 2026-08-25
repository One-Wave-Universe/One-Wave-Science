# Notes to Self

## Permanent correction

- Anti-drift does not mean only staying inside the assigned task.
- Anti-drift means **do not fuck with the established build structure**.
- Nodesification must make the existing build clearer, easier to trace, and easier to test.
- Do not redesign, reorder, rename, merge, split, add, remove, replace, or reinterpret build components.
- Read `BUILD_STRUCTURE_LOCK.yaml` before converting any state-machine unit.
- A receipt must compare names, order, layers, connections, semantics, and behavior before and after.
- Report `NO_STRUCTURAL_DRIFT` only when all of those are unchanged.
- If clarity improves but structure changes, the conversion fails.
- If structure is preserved but the build is not clearer, the conversion is incomplete.
- Preserve `Idle -> Primed -> Executing -> Vectoring -> Resolving` exactly.
- Keep Field lifecycle, modulation, and six-step recursion separate.
- Do not make each node a separate executable.
- Change one thing, test immediately, compare against the structure lock, then write the receipt.
- After three failed attempts, stop that approach.
- Next permitted action: inventory the existing build exactly as-is, mapping each active source to its structural position without changing it.
