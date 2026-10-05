# CELL_V1 Safe Bring-Up

Current-limited. Low voltage. One observable at a time. **Do not populate all three stations and then debug the pile.**

Full wiring is in `../CELL_V1_FULL_BUILD.md`.

## P0 — power OFF

- Label NET_P / NET_G / NET_N.
- Verify no P-to-N short.
- Verify G is not tied to N.
- Verify every MOSFET pair is source-to-source using the actual device pinout.
- Verify each tied gate has a 100 k gate-to-common-source OFF pull.
- Verify electrolytic polarity.

Stop on any ambiguity.

## P1 — midpoint host only

Apply 5 V with a 10–20 mA supply limit.

Measure:

```text
V(P-N)
V(P-G)
V(G-N)
V(G-home)
V(G-far)
```

Expected: P-G and G-N are each approximately half the supply. G-far minus G-home should be close to zero.

## P2 — midpoint stiffness

Momentarily test a roughly 1 mA load in each direction using 2.2 k:

```text
P -> 2.2k -> G
then remove
G -> 2.2k -> N
then remove
```

G must recover and remain inside its belt both sourcing and sinking.

## P3 — passive G0

No MOSFETs yet:

```text
P -> 1k -> G0_TAP -> 1k -> N
G0_TAP -> 10 ohm -> G
```

Balanced receipt across 10 ohm should be near zero.

## P4 — deliberate lean

Temporarily make the upper arm about 680 ohm (1 k parallel 2.2 k is ~688 ohm). Measure:

```text
V(G0_TAP)-V(G)
I_G0 = [V(G0_TAP)-V(G)] / 10 ohm
V(G)-half_supply
```

The local receipt must move; G itself should remain stiff.

## P5 — upper bilateral MOSFET pair

Restore 1 k / 1 k. Insert only the G0 upper source-to-source pair.

OFF: leakage-scale current; no simple body-diode clamp.

ON: low-mA conduction; no heating. Record pair voltage drop and current.

## P6 — lower bilateral MOSFET pair

Add the lower pair. Enable both legs. G0 now has the full physical mirrored station shape. Balance should return its 10-ohm receipt near zero.

Repeat the deliberate lean and verify the receipt sign/value.

## P7 — RC

Add:

```text
G0_TAP -> 1k -> HOLD0
HOLD0 -> 10uF -> G
HOLD0 -> 100k -> G
```

Drive a lean for >=30 ms, return to balance, and measure the decay. A 1 k / 10 uF branch targets about 10 ms tau. Record actual tau.

## P8 — copy G0

Copy the proven G0 station unchanged to G+ and then G-. Re-run P3/P4 balance and lean checks after each new station.

## P9 — slow bidirectional cycling

Begin with manual polarity changes. Only then increase frequency. Watch:

```text
G-home
G-far
station tap
10-ohm receipt
HOLD node
supply current
```

If G oscillates or drifts, stop. That is reference failure, not a useful state.

## P10 — whole-cell quadratic memory, sense only

Route the resolved A/B/C differential state into the one whole-cell memory
plane. Measure its Hall/sense and memristive state outputs relative to NET_G.
No active reinjection yet. Run positive/negative/control/drive-off receipts per
`../07_MAGNETICS/ROTATIONAL_HOLD_TEST.md` and prove that different ternary
histories yield distinguishable, repeatable whole-state readings.

## P11 — manual bounded reinjection

Use the measured whole-state differential to identify LOW and HIGH belts.
Manually connect the current-limited reinjection path at LOW and disconnect it
at HIGH. Verify polarity, source current, NET_G stiffness, state restoration,
and coast decay before adding automatic feedback.

## P12 — analog reinjection loop

Enable the analog hysteretic controller. It must:

```text
LOW crossing  -> bounded source connection
HIGH crossing -> source disconnect
between belts -> retain the previous switch state without chatter
```

Compare integrated source energy against continuous excitation at the same
state/output tolerance. Stop if NET_G leaves its belt, either reinjection side
conducts illegally, the controller chatters, or any device heats.

## Mandatory receipt per step

Record:

```text
supply voltage/current limit
rail voltages
G-home and G-far
station arm values
gate drive state and actual VGS
upper/lower branch currents
10-ohm receipt voltage/current
RC values and measured tau
frequency / polarity / phase where applicable
temperature or heating observation
magnetic sense values only when present
whole-state memory value and preceding A/B/C history
LOW/HIGH threshold crossings and reinjection switch state
integrated reinjection energy and matched continuous-drive control energy
PASS / FAIL and exact reason
```

Do not advance on a FAIL. Fix the failed observable first.
