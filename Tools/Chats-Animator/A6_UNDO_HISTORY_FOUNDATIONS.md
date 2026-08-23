# A6 — Undo / History Foundations

**Status: PASS**

A6 adds the reversible edit foundation for the shared One-Wave Video Maker project state.

## Locked behavior

- Human and AI edits use the same transaction format.
- A transaction contains one or more explicit path-addressed edits.
- Every edit stores its `before` and `after` value.
- Undo reverses edits in reverse order.
- Redo reapplies the same transaction.
- A new committed edit clears the redo stack.
- History is bounded by a configurable maximum.
- Conflict checks refuse to silently apply a transaction when the current state no longer matches the transaction's expected baseline.
- The history layer does not implement scene, animation, playback, scale, audio playback, or rendering behavior.

## Transaction shape

```text
transaction
  id
  label
  actor: human | ai | other
  createdAt
  metadata
  edits[]
    op: set | delete
    path[]
    before
    after
```

This gives later human tools and bounded AI operations the same reversible project-edit mechanism.

## A6 hard stop

A6 stops after reversible project-state history passes its tests.

The canonical master plan says the next phase is:

**PHASE B — BACKGROUND / SCENE**

and the next brick is:

**B1 — Background loading**
