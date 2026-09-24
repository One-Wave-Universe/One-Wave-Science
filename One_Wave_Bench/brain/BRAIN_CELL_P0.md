# Brain Cell P0 — Views Up, Decisions, Actions Down

Status: **software-first architecture; integrated runtime unvalidated**

## Purpose

The brain cell is a bounded decision-and-memory recurrence. It receives
referenced Views Up, compares them with the held goal and prior state, and emits
an admitted Action Down. It contains no motor winding.

```text
View Up  <= shared bidirectional gate => Action Down
              brain resolves direction/turnaround
              Dream -> M4 -> Administrator
              measured return -> new held state
```

The first build is software on the existing Jetson/host stack. Custom magnetic
brain hardware is not required to test the contract.

## Roles and authority

| Role | Job | May commit an action? |
|---|---|---:|
| Dream / Field | Produce candidate interpretations and leans | No |
| M4 | Fast routing, timing, association, and handoff | No |
| Administrator / Void | Confirm, defer, deny, or override from evidence | Yes |
| Executor adapter | Translate an admitted action to the target controller | No new choice |

The local nerve loop uses the working `3:1` relationship: **three complete
nerve cycles for one higher-brain function**. Each local cycle contains Action
Down, physical response, and a new View Up. The higher function compares those
three returned views and resolves the next larger step. Higher oversight uses
the working `6:1` neighborhood/override relationship. These are architecture
ratios to test, not claims that biological brains literally use the proposed
hardware.

## One gate, two directions

The upward signal and downward signal are opposite uses of the same
bidirectional gate. `View Up` and `Action Down` name direction and authority,
not two different gate types. The brain resolves the turnaround: it receives a
referenced view, makes the admission decision, and then reverses the same route
for the action. Direction, reference, sequence, and expiry must remain explicit
so the returned view cannot be mistaken for a new command.

Canonical recurrence:

```text
View Up(n) -> resolved Action Down(n) -> measured physical result
           -> NEW View Up(n+1), referenced to Action Down(n)
```

This is why the return is the new view of the last action. It does not reset to
the pre-action state and does not merely echo `View Up(n)`.

Rapid direction flipping can make the loop appear simultaneous, but the brain
contract retains explicit phases and timestamps. Apparent continuity is
accepted only when measured round-trip latency and jitter stay below the
declared limit for the controlled process.

The 3:1 scheduler must not turn into blind batching. Every nerve cycle is
measured and locally bounded. A fault or explicit override may preempt the group
before cycle three; the receipt must record the incomplete group and reason.

The higher brain changes the **held target**, not the raw actuator balance. Fast
nerve cycles keep the system balanced around that target while the admitted
higher function adds lift or a directional lean. HOLD leaves the target in
place and lets the fast loop continue correcting disturbances.

## Lifecycle

The canonical five states are process states, not five voltage levels:

```text
Idle -> Primed -> Executing -> Vectoring -> Resolving -> Idle/new cycle
```

- **Idle:** safe, no unhandled command.
- **Primed:** inputs and reference validated.
- **Executing:** an admitted bounded action is active.
- **Vectoring:** direction/phase/strength are tracked against the reference.
- **Resolving:** measured return is compared, logged, and committed as the new
  held state or corrected/overridden.

Quinary `-2/-1/0/+1/+2` remains a possible magnitude grammar only if a later
test needs and validates two distinct magnitudes on each side. It is not the
meaning of this five-state lifecycle.

## Input contract — Views Up

Each view includes:

- direction;
- phase;
- strength;
- reference and units;
- quality/validity;
- source, coordinate frame, sequence, and timestamp;
- the last measured action response when available.

## Output contract — Actions Down

An action packet includes:

```text
target + axis + lean(-1/0/+1) + magnitude limit + slew limit
+ expiry + allowed mode + sequence + reason + approving authority
```

`HOLD` keeps the admitted target and permits the lower controller to keep doing
the work required to maintain it. For example, a hovering drone still produces
stabilizing thrust and a playing speaker retains its selected volume setting.

## Memory and growth

Store the relationship between view, candidate, decision, action, measured
return, and new state. Do not substitute a giant undifferentiated transcript
for this state history. Any learned preference or weight must remain inspectable,
reversible, and subordinate to hardware limits and explicit human override.

## Acceptance tests

- Reject a view that lacks reference, units, frame, quality, sequence, or time.
- Demonstrate Confirm, Defer/HOLD, Deny, and Override paths.
- Prove Dream and M4 cannot authorize an actuator command.
- Prove one shared gate carries a view upward and an admitted action downward
  without reflection, collision, or role confusion.
- Replay the same recorded views and reproduce the same decision under the same
  declared state.
- Show that return becomes the next state rather than automatically restoring
  an earlier zero.
- Prove `View Up(n+1)` contains the measured result and sequence reference for
  `Action Down(n)` rather than a copy of `View Up(n)`.
- Prove one higher-brain function consumes three completed nerve-cycle receipts,
  or an explicitly marked preempted group during override/fault handling.
- Interrupt the output stream and confirm the target controller's native
  recovery behavior.
- Preserve a complete decision/response log without hidden state changes.

## Further development needed

- Freeze machine-readable view and action schemas.
- Connect the existing triad-brain, command-memory, and three-winding contracts
  into one runnable headless loop.
- Define how competing sensor views are registered and resolved.
- Define shared-gate direction control, turnaround timing, and collision rules.
- Set per-device minimum cycle rate and maximum latency/jitter from stability
  tests rather than human perception.
- Implement the 3:1 scheduler, three-receipt comparison, and preemption tests.
- Implement bounded learning with reversible state snapshots and explicit
  Administrator approval.
- Add deterministic replay, timeout, duplicate-sequence, and override tests.
- Demonstrate the complete loop in simulation, then on the rover, before flight.
