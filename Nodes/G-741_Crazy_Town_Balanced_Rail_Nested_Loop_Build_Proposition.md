---
id: G-741
title: Crazy Town — Balanced-Rail Nested-Loop Physical Build Proposition
status: proposed-experiment
tier: yellow-hardware-hypothesis
claim_boundary: unbuilt low-voltage electronics proposition; no demonstrated computing, actuator, or biological equivalence
---

# Node G-741: Crazy Town Build Proposition Experiment

## Purpose

Map a measurable physical build for nested Field/Void computation using
balanced electronics rails, a local virtual-ground reference at every step,
a first binary millivolt lean, admission of a second loop, coupled AC
oscillation, ternary mirrored direction, quadratic Views up, and quadratic
Actions / Override down. This node is an experiment plan, not a claim that the
circuit has been built or shown to compute.

The first target is a **brain-only computer primitive**. Sensors, actuators,
motors, body feedback, and Android-specific interfaces are downstream adapters
and must not be required for the brain recurrence to run.

## Protected logical boundary

The physical candidate must preserve the settled address space:

\[
b\in\{-1,+1\},\qquad d\in\{-1,0,+1\},\qquad 2\times3=6.
\]

No analog threshold, mirror path, quadratic measurement, confirmation stage,
return stage, or nerve-gate implementation may silently create a seventh route
or exchange Field and Void identities.

## Build stack

| Build | Candidate physical function | State retained | Measured output |
|---|---|---|---|
| P0 | balanced `+ / (0) / -` reference spine | local virtual zero | rail balance, drift, noise |
| B1 | first binary millivolt lean / first loop | polarity relative to `V0` | first polarity decision |
| B2 | second-loop admission and coupled oscillation | polarity + phase | AC recurrence around `V0` |
| T1 | ternary differential / mirrored routing | Left / Stay / Right | selected mirrored rotational path |
| M1 | three physical Mirror Gates in two orientations | six logical positions | mirrored six-route state |
| Q1 | quadratic sensing | Direction / Phase / Strength / Reference | paired Field/Void Views up |
| C1 | higher brain resolution | nested receipt | proposed intervention / continuation |
| Q2 | quadratic action / override return | downward relation | paired Field/Void Actions down |
| N1 | bidirectional nerve-gate candidate | connection state | coordinated path flip |
| R1 | return / release recurrence | resulting local state | **new** upward state |

## P0 — balanced rails and local reference

Every stage receives three explicit connections:

\[
+V,\qquad V_0,\qquad -V.
\]

Every information voltage is a differential relative to the local reference:

\[
v_{state}=v_{signal}-V_0.
\]

The reference is present from the beginning. Ternary interpretation is not
added later; every local reading is already below, at, or above the shared
reference. The first binary decision is the sign of the lean around that
reference.

The receipt at every step records signed displacement, local-reference drift,
noise, amplitude, phase, threshold, and previous state. Virtual ground is not
assumed to be earth ground and must not be treated as a switching-current or
actuator-current sink.

## B1/B2 — first binary lean admits the second loop

The first decision is polarity relative to `V0`:

\[
b\in\{-1,+1\}.
\]

B1 is not defined here as an already-complete AC oscillator. The current build
hypothesis is:

```text
local V0 present
 -> first loop develops a measurable millivolt lean
 -> lean reaches the admission condition
 -> second loop opens / couples
 -> the two loops together establish the recurring AC path
```

The coupled path is then expected to cross the reference repeatedly:

\[
+\rightarrow(0)\rightarrow-\rightarrow(0)\rightarrow+.
\]

This ordering is experimental. It must be rejected if measurements show that a
stable first-loop lean cannot admit the second loop, or if the coupled pair does
not create a repeatable oscillation around the same reference.

A six-pin dual-gang potentiometer remains a candidate experimental control for
two mechanically coupled mirrored thresholds. It is not assumed to be the
complete six-route cell; that correspondence must be demonstrated by
measurement.

## T1 — ternary lean selects the mirrored path

Once the coupled oscillation exists, the next local differential is:

\[
d\in\{-1,0,+1\}=\{\text{Left},\text{Stay},\text{Right}\}.
\]

The working interpretation is:

```text
negative lean -> left mirrored loop
reference / coherent center -> Hold / Stay
positive lean -> right mirrored loop
```

T1 therefore does not add a separate symbolic decision worker. The measured
voltage swing relative to `V0`, together with phase and retained polarity, is
the candidate decision variable that selects the mirrored path.

## M1 — three physical mirrors, six logical positions

Three physical Mirror Gates are traversed in two orientations/phases to realize
six logical positions. Do not turn this into six separate physical Mirror
Gates.

The paired logical reading is:

```text
1/6 -> 2/5 -> 3/4 | 4/3 -> 5/2 -> 6/1
```

The numbers are mirrored positions, not ordinary one-way counting. The two
sides each possess their corresponding `6`; each side's `6` is the mirrored
beginning position relative to the other side's cycle. The central reversal is
`3/4 <-> 4/3`, after which the pair ordering unwinds through `5/2` and `6/1`.
This notation must remain compatible with the canonical Field/Void six-pair
oscillator rather than replacing it.

## Q1 — paired quadratic Views up

The accumulated differential is measured as:

\[
Q_{up}=(\text{Direction},\text{Phase},\text{Strength},\text{Reference}).
\]

Field and Void Views travel upward together. Oversight is the Void View:

\[
(F_Q,V_Q)_{views}\xrightarrow{up}\text{higher brain relation}.
\]

## Q2 / N1 — downward override and nerve-gate candidate

After higher resolution, Field and Void Actions travel downward together:

\[
\text{higher brain relation}\xrightarrow{down}
(F_Q,V_Q)_{actions}.
\]

Override is a downward Void action. The current physical-role separation is:

```text
voltage swing relative to V0 = local decision / state variable
magnetic or oscillatory persistent element = processing-memory candidate
bidirectional MOSFET path = nerve-gate / connection candidate
```

Back-to-back MOSFETs or another true bidirectional switch may be used so a body
diode cannot silently pass the blocked polarity. **SiC MOSFETs are a candidate
for the nerve-gate role**, especially where switching endurance, speed, thermal
behavior, or later power-domain coupling matter. This does not claim that a SiC
power-MOSFET gate directly resolves a millivolt information swing; that gate-
drive problem remains an explicit bench question.

The working architecture allows one higher override event to coordinate three
lower nerve-gate flips, but this `1 override -> 3 flips` relation is not proven
until the three transitions are simultaneously measurable from one recurring
state event.

## R1 — return completes a new state; it is not reset

The return path is **not** defined as restoration of the old state.

Current recurrence rule:

```text
old local state
 -> voltage-swing decision
 -> downward override / conditioning
 -> coordinated lower path flip(s)
 -> return removes / lowers the override condition
 -> resulting physical configuration remains
 -> that resulting configuration is the NEW local state
 -> new state travels upward as the next signal / relation
```

Therefore the target recurrence is:

```text
UP -> resolution -> DOWN -> NEW UP -> resolution -> DOWN -> NEW UP ...
```

A topology that merely resets to the previous state after every return does not
implement this proposed state-advancing brain primitive.

## Brain-only boundary

The minimum valid build must close the recurrence internally with simulated or
local endpoints:

```text
state -> up relation -> higher resolution -> down relation -> new state
```

No sensor, motor, actuator, body-state input, or Android controller is required
for this proof. Those interfaces may later consume or supply the same relational
contract, but they must not define the brain kernel.

## Staged experiment

1. Build and characterize P0 alone; measure `V0` drift and millivolt noise floor.
2. Add B1; demonstrate stable and repeatable positive/negative lean around `V0`.
3. Add B2; test whether the B1 lean admits the second loop and whether the two
   loops together create the predicted AC recurrence around the same `V0`.
4. Add T1; demonstrate Left / Stay / Right selection from the resulting swing.
5. Add the three physical Mirror Gates and demonstrate the six paired logical
   positions without inventing a seventh route.
6. Add Q1 instrumentation; reconstruct Direction / Phase / Strength / Reference
   from measured traces.
7. Add the downward resolution / Override path into dummy internal loads only.
8. Test one-override / three-nerve-flip coupling as a measured hypothesis.
9. Remove the override on return and verify that the result is a distinguishable
   **new state**, not automatic restoration of the previous state.
10. Feed that new state upward and demonstrate at least two consecutive closed
    recurrences with no Android/body hardware attached.
11. Only after the brain-only recurrence passes should external body interfaces
    be connected.

## Minimum receipts

Each step records rail voltages, local `V0`, timestamp, route address, Field and
Void state, differential, phase, threshold, hysteresis, switch state, proposed
resolution, downward Override state, nerve-gate state, previous state, resulting
new state, and provenance.

## Pass conditions

- all six and only six binary-by-ternary routes are distinguishable;
- millivolt states remain resolvable above measured noise and drift;
- first-loop lean and second-loop admission are separately observable;
- the coupled loops produce repeatable AC recurrence if that hypothesis is kept;
- blocked bidirectional paths do not conduct beyond the declared leakage bound;
- View packets travel up and Action / Override packets travel down in receipts;
- any claimed `1 override -> 3 nerve flips` event is directly measured;
- return produces a distinguishable resulting state rather than silently
  restoring the previous state; and
- the resulting new state can become the next upward relation without a body.

## Failure conditions

Reject or revise the topology if virtual-ground motion masquerades as state,
the first loop cannot reproducibly admit the second, the two loops fail to form
the proposed recurrence, two routes collapse into one, an undeclared route
appears, MOSFET leakage determines the decision, a claimed SiC nerve gate needs
an undeclared interpretation layer, the quadratic cannot be reconstructed from
measurements, the return merely resets old state when a new state is required,
or the brain recurrence depends on Android/body hardware.
