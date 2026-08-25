# Branch-Step 02 — State-Machine Source Inventory

## MAIN GOAL

Make the established state-machine build clear and machine-checkable without changing its structure.

## CURRENT STEP GOAL

Inventory active state-machine sources and map them to bounded watchdog-node conversion units.

## HARD START

- Parent branch control receipt passed.
- Source branch is `canon/five-field-states` at `504b5239aab53fe5807e044688d10eefc5a2b63a`.
- PR #7 is open, draft, clean, mergeable, and has zero check runs.
- `BUILD_STRUCTURE_LOCK.yaml` is binding.

## ONE CHANGE

Add the source inventory only.

## RESULT

Thirteen structural units are mapped. The first conversion unit is SM-004 Field Lifecycle because every transition, Step-6 decision, and later validator depends on an exact lifecycle table.

## HARD STOP

Stop after the inventory and receipt are verified. Do not convert SM-004 in this branch.
