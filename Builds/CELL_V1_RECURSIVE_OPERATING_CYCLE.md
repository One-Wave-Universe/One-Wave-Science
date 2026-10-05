# CELL_V1 — RECURSIVE OPERATING CYCLE

**Status:** target architecture / recursion rule  
**Date:** 2026-10-03  
**Authority:** preserve this chart and the nested Begin/Loop relationship when translating the operating cycle into hardware, simulation, documentation, or later diagrams.

## Outer cycle

```text
BEGIN (void established)
    ↓
BUILD (charge)
    ↓
    BEGIN (sub-void forms — nested)
        ↓
    LOOP (sub-recovery — nested)
    ↓
HOLD (loaded)
    ↓
    BEGIN (trigger void — nested)
        ↓
    LOOP (trigger recovery — nested)
    ↓
BUILD (trigger armed)
    ↓
BREAK/RELEASE (flip)
    ↓
LOOP (recovery)
    ↓
(back to BEGIN)
```

Begin and Loop are not only endpoints. They recur inside phase transitions and at larger/smaller supported scales.

## Transition map

| Transition | Nested Begin | Nested Loop |
|---|---|---|
| Void → Build | Sub-void forms | Sub-recovery |
| Build → Hold | Hold-void forms | Hold-recovery |
| Hold → Build | Trigger-void forms | Trigger-recovery |
| Build → Break | Break-void forms | Break-recovery |
| Break → Loop | Recovery-void forms | Recovery-loop |

## Full nested chart — preserve verbatim

```text
BEGIN ─────────────────────────────────────────────┐
  ↓                                                │
BUILD ─────────────────────────────────────────┐   │
  ↓                                            │   │
  BEGIN (sub) ─────────────┐                   │   │
    ↓                      │                   │   │
  LOOP (sub) ──────────────┘                   │   │
  ↓                                            │   │
HOLD ──────────────────────────────────────────┤   │
  ↓                                            │   │
  BEGIN (sub) ─────────────┐                   │   │
    ↓                      │                   │   │
  LOOP (sub) ──────────────┘                   │   │
  ↓                                            │   │
BUILD (trigger) ───────────────────────────────┤   │
  ↓                                            │   │
  BEGIN (sub) ─────────────┐                   │   │
    ↓                      │                   │   │
  LOOP (sub) ──────────────┘                   │   │
  ↓                                            │   │
BREAK/RELEASE ─────────────────────────────────┤   │
  ↓                                            │   │
LOOP ──────────────────────────────────────────┴───┘
  ↓
(back to BEGIN)
```

## Recursive heartbeat

- Outer cycle = cell heartbeat.
- A supported phase/transition may expose the same Begin/Loop interface as a nested heartbeat.
- BEGIN = establish or re-establish the local Void/reference/null.
- LOOP = return, reconcile, recover, and expose the reference for the next transition.
- Recovery is therefore a candidate continuous/nested behavior, not only an end-of-cycle event.
- The same grammar may recur at cell, flower, lattice, and other physically supported scales.

Do not interpret recursion as requiring a physically infinite regress. The architecture is recursively composable; actual recursion depth is set by physical structure and must be measured.

## Maxwell mapping

```text
BEGIN          Maxwell null/reference established
  ↓
BUILD          Field/Void imbalance develops
  ↓
HOLD           field/hysteretic state retained
  ↓
BUILD          trigger differential develops
  ↓
BREAK/RELEASE  null tips / flip / actuator expression
  ↓
LOOP           recoil + reinjection + reference recovery
  ↓
BEGIN          recovered null becomes next reference
```

## Testable consequence

If nested recovery is physically real, measurements should not show only one recovery signature after the major BREAK/RELEASE. The experiment should search for smaller reference-return/recovery signatures around intermediate transitions.

That prediction remains **unproven until measured**.

## Anti-drift rule

Do not reduce the operating cycle to a purely linear six-item checklist.

The canonical grammar is:

```text
BEGIN → BUILD → HOLD → BUILD → BREAK/RELEASE → LOOP → BEGIN
```

with Begin/Loop recursion available at phase transitions and supported scales.

The nested ASCII chart above is part of the architecture record and must not be discarded when this rule is summarized.
