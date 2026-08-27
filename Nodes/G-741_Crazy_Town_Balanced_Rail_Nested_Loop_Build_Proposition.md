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
binary polarity oscillation, ternary mirrored direction, quadratic Views up,
and quadratic Actions down. This node is an experiment plan, not a claim that
the circuit has been built or shown to compute.

## Protected logical boundary

The physical candidate must preserve the settled address space:

\[
b\in\{-1,+1\},\qquad d\in\{-1,0,+1\},\qquad 2\times3=6.
\]

No analog threshold, mirror path, quadratic measurement, or confirmation stage
may silently create a seventh route or exchange Field and Void identities.

## Build stack

| Build | Candidate physical function | State retained | Measured output |
|---|---|---|---|
| P0 | balanced `+ / (0) / -` reference spine | local virtual zero | rail balance, drift, noise |
| B1 | binary polarity AC oscillator | sign and phase | first polarity decision |
| B2 | DC extraction/decision loop | averaged or latched binary result | stable decision receipt |
| T1 | ternary differential oscillator | Left / Stay / Right | mirrored rotational path |
| Q1 | quadratic sensing | Direction / Phase / Strength / Reference | paired Field/Void Views up |
| C1 | command computation | nested receipt | proposed brain command |
| R1 | unresolved return resolver | to be determined experimentally | return-control packet |
| Q2 | quadratic action decoder | four action coordinates | paired Field/Void Actions down |
| V1 | Void outcome | Confirm / Defer / Deny | permit, Hold, or Override |

## P0 — balanced rails and local reference

Every stage receives three explicit connections:

\[
+V,\qquad V_0,\qquad -V.
\]

Every information voltage is a differential relative to the local reference:

\[
v_{state}=v_{signal}-V_0.
\]

The receipt at every step records signed displacement, local-reference drift,
noise, amplitude, phase, threshold, and previous state. Virtual ground is not
assumed to be earth ground and must not be treated as an actuator-current sink.
Millivolt information paths remain separated from motor and switching returns.

## B1/B2 — binary AC loop plus DC decision loop

The first decision is polarity:

\[
b\in\{-1,+1\}.
\]

The candidate AC loop repeatedly crosses the reference:

\[
+\rightarrow(0)\rightarrow-\rightarrow(0)\rightarrow+.
\]

A separate DC loop measures and retains the decision without pretending the
oscillation stopped:

\[
b_{DC}=\operatorname{Latch}(\operatorname{Measure}(v_{AC},V_0)).
\]

A six-pin dual-gang potentiometer is a candidate experimental control for two
mechanically coupled mirrored thresholds. It is not assumed to be the complete
six-route cell; that correspondence must be demonstrated by measurement.

## T1 — ternary mirrored rotational loop

The next differential is:

\[
d\in\{-1,0,+1\}=\{\text{Left},\text{Stay},\text{Right}\}.
\]

T1 carries the B1/B2 polarity, phase, and retained decision into the selected
mirrored path. Its receipt also retains mirror-path identity and the new
differential. The complete route remains `(b,d)`.

Asymmetric voltage admission is a comparator/threshold function. A candidate
bidirectional switch uses back-to-back MOSFETs or an appropriate transmission
gate so a body diode cannot silently pass the blocked polarity. MOSFET gates do
not establish the information threshold by themselves.

## Q1 — paired quadratic Views up

The accumulated differential is measured as:

\[
Q_{up}=(\text{Direction},\text{Phase},\text{Strength},\text{Reference}).
\]

Field and Void Views travel upward together. Oversight is the Void View:

\[
(F_Q,V_Q)_{views}\xrightarrow{up}\text{brain command}.
\]

## Q2 — paired quadratic Actions down

After command resolution, Field and Void Actions travel downward together:

\[
\text{brain command}\xrightarrow{down}
(F_Q,V_Q)_{actions}.
\]

The four action coordinates are Inward, Outward, Across, and Over. Override is
the Void Action produced when the resolved Void state is Deny. Defer preserves
Hold and must not fabricate an Override.

## Intentionally unresolved return stage

The hardware between command computation and Q2 has not been built. Three
candidate orderings must be compared instead of choosing by vocabulary:

1. Void ternary only: Confirm / Defer / Deny;
2. ternary resolution followed by binary Commit / Block; or
3. binary authorization around a second ternary return differential.

The minimum valid topology is the smallest one that independently represents
valid continuation, insufficient-evidence Hold, invalid-boundary Override,
four distinct downward Actions, and retained six-route identity.

## Staged experiment

1. Build and characterize P0 without oscillators or loads.
2. Add B1; measure crossing, polarity, frequency, phase, drift, and noise.
3. Add B2; verify that the DC receipt is stable while B1 continues oscillating.
4. Add T1; demonstrate all six unique `(b,d)` routes and no seventh route.
5. Add Q1 instrumentation; reconstruct all four Views from measured traces.
6. Compare the three unresolved return-stage candidates using identical inputs.
7. Add Q2 only after the return packet is distinguishable and repeatable.
8. Connect no motor until electrical fault, Hold, and Override tests pass into a
   dummy load.

## Minimum receipts

Each step records rail voltages, local `V0`, timestamp, route address, Field and
Void state, differential, phase, threshold, hysteresis, switch state, proposed
command, Void resolution, action result, measured consequence, and provenance.

## Pass conditions

- all six and only six binary-by-ternary routes are distinguishable;
- millivolt states remain resolvable above measured noise and drift;
- blocked bidirectional paths do not conduct through body-diode leakage beyond
  the declared bound;
- View packets travel up and Action packets travel down in the receipt;
- Defer, Deny, and Confirm remain experimentally distinguishable;
- Override occurs only from Deny; and
- removing power or losing reference forces a safe, observable Hold.

## Failure conditions

Reject or revise the topology if virtual-ground motion masquerades as state,
the DC loop stops the AC loop, two routes collapse into one, an undeclared route
appears, MOSFET leakage determines the decision, the quadratic cannot be
reconstructed from measurements, or the final stage requires labels that have
no distinct electrical observables.

