# P0 — build this, not another node

## What you assemble this week

One nerve cell. One brain cell. They talk once. No Jetson. No words.

### Nerve (mV, three windings, one ground)

- Two rails: +V and -V. Start at ±1.5 V coin cells or a split bench supply. Stay millivolt-to-low-volt. Not mains.
- Virtual ground: two equal resistors between rails, midpoint is `(0)`. That midpoint is HOLD.
- Three windings: three coils or three resistor+LED stand-ins labeled U V W.
- Each winding is a bidirectional half-bridge to the two rails, source/source or back-to-back N/P as you have. SiC later. 2N7000 / BSS84 is enough to prove the law.
- Drive law for P0: only one winding UP, one DOWN, one HOLD. Admin picks the pair. M4 does not.

If the midpoint drifts, you do not have ternary. You have a mess.

### Brain (CPU, mute)

Run `mute_cycle.py`.

```text
Dream proposes a move
M4 may only copy the proposal to Admin
Admin writes HOLD / DOWN / UP onto the three windings
STOP is Admin VOID + all HOLD
```

No command string. If you type "follow" you failed P0.

### Done when

1. Midpoint stays put at rest.
2. One UP/DOWN/HOLD pattern appears when Admin says UP.
3. Mute cycle prints one receipt with `committed` only on STOP.
4. M4 cannot change a winding in code.

That is closer. G-756 is the dictionary on the wall. This file is the bench.
