# Balanced Cell Family — P0 Index

Status: **proposed build contracts; not physical proof**  
Date: 2026-09-11

This directory separates four things that must not be collapsed into one vague
"cell":

| File | Job | May command an actuator? |
|---|---|---:|
| `BALANCED_CELL_P0.md` | Preserve and expose a differential state around one reference | No |
| `SENSOR_CELL_P0.md` | Turn measurements into balanced Views Up | No |
| `ACTION_NERVE_CELL_P0.md` | Turn an admitted action into local three-winding motion | Yes, within a bounded local envelope |
| `../brain/BRAIN_CELL_P0.md` | Compare views, choose/defer/deny, and issue bounded Actions Down | Only through the authority boundary |

## Shared law

Every cell carries the same four quantities at every handoff:

1. **Direction** — which side of the reference the change points toward.
2. **Phase** — where the measured cycle or relationship is now.
3. **Strength** — magnitude inside a declared envelope.
4. **Reference** — the exact center/baseline used to interpret the first three.

Every packet also carries quality, validity, sequence, and time. A packet
without its reference is incomplete.

Views Up and Actions Down use the **same bidirectional gate/interconnect**. They
are opposite directions of one referenced relationship, not separate one-way
gate families. Direction identifies the signal's role:

```text
measured return / View Up  <== same bilateral gate ==>  admitted Action Down
```

Sharing the gate does not merge authority. An upward measurement cannot
authorize its own downward action; the brain/controller still resolves the
turnaround.

The recurrence is:

```text
old View Up -> resolved Action Down -> physical change
            -> NEW View Up describing the result of that last action
```

The new View Up is not the old view reflected back. It is the newly measured
state, registered against the same reference and linked to the last action's
sequence identifier.

The shared gate may alternate direction fast enough that the exchange appears
continuous at the device scale. This is a time-shared/half-duplex recurrence,
not proof of zero delay. Record the full cycle rate, turnaround time, worst-case
latency, and jitter; they must be comfortably inside the controlled device's
stability budget.

`HOLD` means **no new differential correction**. It does not mean power off,
motor zero, light off, or speaker volume zero. The presently admitted operating
state continues unless a higher safety authority replaces it.

## Scale-up rule

Prove one cell, then one sensor-to-action loop, then a small network. Do not
claim that a cube, sphere, brain, or flight system works because the drawings
line up. Each added layer must preserve the reference and pass its own recorded
test.

## Is another primitive cell missing?

Not for P0. These four cover state, observation, decision, and action. The
following are required functions inside or between them, not new primitive cell
types yet:

- power and protected energy distribution;
- the shared reference and its independent measurement;
- HOLD/persistent state and history;
- bidirectional communication plus M4 timing and routing;
- higher-level oversight, override, and emergency energy removal.

Create another cell type only when a test shows that one of those functions
needs an independently powered, measured, replaceable boundary. Until then,
keep it as a named module or packet field so the architecture does not grow by
labels alone.
