# Intrinsic Ternary Language Mapping

The language names physical transitions; it does not control passive hardware from a CPU.

```text
choice      = -1 | 0 | +1
level       = Floor | Low | Middle | High | Ceiling
handedness  = CCW | HOLD | CW
memory      = MAINTAIN | WRITE
route       = RECEIVE | ISOLATE | EXCHANGE
```

Primitive operations:

```text
SET_VREL
READ_MIRROR
HOLD
CHOOSE_NEG
CHOOSE_POS
SHIFT_LEVEL
PASS_PHASE
FLIP_PHASE
ROTATE_POINT
ROTATE_PATH
ROTATE_FIELD
LATCH_STATE
MAINTAIN_STATE
WRITE_STATE
REFRESH_RC
EXCHANGE
ISOLATE
LOOP
```

Every instruction must correspond to a measurable transition inside the cell.
