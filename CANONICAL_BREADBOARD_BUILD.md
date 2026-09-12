# CANONICAL BREADBOARD BUILD

**Status:** Single current bench-build handoff. This file is the one place to read before changing or rebuilding the One-Wave breadboard primitive. Older breadboard/build notes remain historical support, but this file owns the current combined build.

## 0. Reference first

Everything is measured against one explicit local reference:

```text
+V
 V0   <- baseline / zero / reference
-V
```

Do not invent a new zero between stages. Every local voltage, state, phase, and direction must remain reference-resolved to `V0`.

## 1. Core primitive

The current primitive is one coordinated cell, not several unrelated experiments:

```text
BC-DC / X  ----\
TC-AC / Y  ----- > TERNARY BALANCE LOCK
QC-RC / Z  ----/
```

Working roles:

- **BC-DC / X** = steady bias / engagement / translation relation.
- **TC-AC / Y** = oscillatory / alternating relation.
- **QC-RC / Z** = retained recursive magnetic-state relation; candidate magnetic/memristive memory layer.

These three remain coupled around the same `V0` reference.

## 2. Mirrored magnetic rotation is structural

The rotational path is not a single one-way ring.

```text
forward rotational path
+
mirrored return path
=
paired rotational magnetic loop
```

The relaxed target is a balanced center condition. A controlled imbalance selects direction while the mirrored return remains part of the same physical loop.

Do not claim 3D field shape from the drawing. When magnetic hardware exists, measure `Bx`, `By`, and `Bz`.

## 3. Reinjection is the extra loop

Reinjection is not assumed to come from the three primary branches by themselves.

```text
coordinated state change
 -> stored / returning energy
 -> EXTRA REINJECTION LOOP
 -> local energy bus
 -> next allowed state / maintenance cycle
```

Measure:

```text
energy in
energy stored
energy returned
energy delivered back locally
losses
```

No unexplained net gain is allowed in the claim.

## 4. Magnetic / memristive memory

Retained state and active refresh are separate mechanisms.

### Passive retained state

A magnetic, hysteretic, magnetoresistive, memristive, or equivalent element retains a state because present state depends on drive history.

### Maintained state

If retained state drifts outside an allowed band, the extra loop may selectively reinject measured available energy to restore it.

A memory claim requires demonstrated:

```text
write -> retain -> read -> rewrite -> repeat
```

and a measured state margin.

## 5. Build flow

The bench sequence is one continuous build:

```text
P0  reference spine
 -> B1 first binary lean around V0
 -> B2 second-loop admission / coupled AC recurrence
 -> T1 ternary direction: - / 0 / +
 -> M1 three physical mirror gates / six logical positions
 -> Q1 View up
 -> higher resolution
 -> Q2 Action down
 -> N1 bidirectional nerve-gate flip
 -> R1 resulting NEW local state
 -> upward recurrence again
```

The return is not a reset. The resulting physical configuration becomes the next upward state.

## 6. Canonical number stack for this build

```text
0 Reference
1 Field
2 Choice
3 Direction
4 View / Action
5 State
6 Loop
```

These are different jobs, not competing state counts.

- **0 Reference** = baseline all relations are measured from.
- **1 Field** = active local condition/context around the reference.
- **2 Choice** = binary engage / do-not-engage relation.
- **3 Direction** = `- / 0 / +` around reference.
- **4 View / Action** = the same four-slot interface used bidirectionally: View up, Action down.
- **5 State** = resolved local state layer; do not confuse with a lifecycle list unless explicitly mapped.
- **6 Loop** = the recurring six-position / six-gate oscillator cycle.

Do not create a seventh route.

## 7. M4 boundary

M4 is the fast bidirectional relay/router between lower body/nerve layers and higher brain layers.

```text
local result -> VIEW UP through M4 -> higher relation
higher relation -> ACTION DOWN through M4 -> local change
```

View and Action are not separate architectures. They are opposite traversal directions through the same four-slot interface.

## 8. Local telemetry

The cell may expose physical measurements such as:

```text
active / engaged
activity level / strength
actual local direction
phase
temperature
available local energy
sensor state
memory readback
reinjection-loop voltage/current
```

These are measurements. They are not automatically extra logical states.

## 9. First breadboard proof

The first valid proof is deliberately small.

Demonstrate, in order:

1. stable `V0` reference and measured noise/drift;
2. repeatable positive/negative first lean around `V0`;
3. second-loop admission and repeatable AC recurrence around the same `V0`;
4. three resolvable direction outcomes: `- / 0 / +`;
5. forward and mirrored return paths both observable;
6. retained magnetic/memristive state if claimed;
7. measurable energy return through the extra reinjection loop if claimed;
8. View up / Action down receipts through the same interface;
9. return produces a distinguishable new state rather than restoring the previous state;
10. the new state can become the next upward relation for at least two consecutive recurrences.

## 10. Minimum measurement receipt

```text
time
reference_id / V0
+V and -V rails
command / choice
Dx, Dy, Dz drive differentials
phase / timing
selected direction
mirror-path state
Bx, By, Bz when magnetic sensing exists
retained-memory readback
temperature
available local energy estimate
reinjection-loop voltage/current/returned-energy estimate
previous state
resulting new state
sensor faults / unknowns
```

Unknown stays unknown. Do not synthesize missing measurements.

## 11. Current physical candidates

Candidates only; none are canon until bench measurements support them:

- six-pin mechanically ganged potentiometer for coupled mirrored threshold experiments;
- back-to-back MOSFETs or another true bidirectional switch for nerve-gate isolation;
- SiC MOSFETs as a later nerve/power switching candidate where appropriate;
- magnetic, magnetoresistive, hysteretic, or memristive element for retained state;
- coils / three-axis magnetic sensing for field-vector tests;
- oscilloscope test points at every stage.

A power MOSFET gate is not assumed to resolve millivolt information directly; gate drive remains an engineering problem to solve and measure.

## 12. Fail conditions

Reject or revise the build if:

- `V0` motion is mistaken for signal state;
- the first loop cannot reproducibly admit the second;
- the paired loops do not create repeatable recurrence;
- the mirrored return path is only drawn but not physically observable;
- two routes collapse together or an undeclared seventh route appears;
- memory cannot be written, retained, read, and rewritten reproducibly;
- reinjection accounting requires unexplained energy gain;
- blocked bidirectional paths leak enough to determine the state;
- View and Action require unrelated packet architectures;
- return only resets the old state when a new retained state is required.

## 13. Source relationship

This file consolidates the current build content from:

- `Nodes/G-741_Crazy_Town_Balanced_Rail_Nested_Loop_Build_Proposition.md`
- `UPDATED_50_BALANCED_CELL_MIRRORED_ROTATION_AND_TELEMETRY.md`
- the current M4 / View-up Action-down architecture

For bench work, **start here first**. Use the older files only for derivation/history or deeper supporting detail.
