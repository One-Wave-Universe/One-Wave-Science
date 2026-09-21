# VTC Zero Logic — Interface Mapping

**Status:** experimental software/UI mapping; not a replacement for CELL_V1 canon

## Authority
For physical geometry and hardware, `CELL_V1_ANTI_DRIFT.md` and the current CELL_V1 build packet win.

## Zero/reference rule
```text
+ <-> (0) <-> -
```

`(0)` is the declared reference/pivot. It is not automatically absence, power ground, or an energy reservoir.

## Logical layers
The UI may expose:
- binary choice;
- ternary movement around reference;
- views/state moving upward;
- actions/conditioning moving downward;
- Field/Void roles;
- lifecycle state;
- exact receipt/history.

These are software/state descriptors. They must not create extra physical gates.

## CELL_V1 projection
Physical primitive remains:
```text
A+ <-> A-
B+ <-> B-
C+ <-> C-
```

Three physical bidirectional mirrors produce six directed edge interfaces.

## UI state schema
Recommended fields:
```text
reference
field_or_void
binary_choice
ternary_move
view
action
lifecycle
strength
phase
direction
receipt_id
```

## Guardrails
- no six-separate-Mirror/Action hardware interpretation;
- no corner ports;
- no automatic mapping of symbolic zero to electrical ground;
- no promotion of unmeasured memory/reinjection behavior to validated hardware.
