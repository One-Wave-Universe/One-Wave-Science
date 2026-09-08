# BALANCED FLASHLIGHT P0

## Purpose

Build a useful 9 V flashlight that serves as the first practical proof of balanced differential power control and selective reinjection.

The flashlight is not a conventional flashlight with experimental features bolted on. Its power, storage, control, and measurement sections are the reusable primitives for later One-Wave hardware.

## Core architecture

```text
9 V source
   |
center / balanced power stage
   |
storage stage
   |
reinjection gate
   |
LED light engine
   |
measurement + battery meter
```

### Balanced power

- establish a stable center reference
- expose `+ / CENTER / -` test points
- measure both rails relative to CENTER and measure the differential directly
- asymmetric loading must be visible; the simulator and physical circuit must not hide center sag

### Reinjection

The maintenance rule is:

`state -> decay/loss -> lower threshold -> reinject -> upper threshold -> disconnect -> coast`

Requirements:

- storage element may begin as capacitor, inductor, or LC depending on measured behavior
- lower and upper thresholds must be separate (hysteresis)
- source is disconnected between reinjection events where the topology allows it
- record pulse width, pulse frequency, source current, stored-node voltage, and total source energy
- compare against continuous drive at the same useful light output

Reinjection is not an energy source. It is a control strategy for replacing measured losses only when needed.

## Light engine

Working control axes:

- power axis: `low <- center -> high`
- color axis: `red <- neutral -> blue`

Color and power should remain independently measurable in P0. Cross-compensation may later be tested (for example, changing electrical drive while color shifts) only after the independent channels are characterized.

Use current limiting appropriate to the actual LED devices.

## Projected battery meter

Battery state should be visible in the projected beam only on demand.

P0 concept:

- 4 or 5 bar indicator
- small secondary LED(s)
- bar mask / stencil
- small projection/focusing lens
- momentary control
- meter wakes, reads battery state, projects bars for a short interval, then turns off
- automatic warning is allowed only at genuinely low/critical battery thresholds

The meter must not waste meaningful power during normal use.

## 3D printed body

Design the shell around experimentation:

- removable 9 V battery bay
- removable electronics tray
- modular LED head
- room for later ferrite/coil test module
- accessible scope/test points
- thermal path around the LED module
- no need to reprint the whole body when one electronics module changes

## Magnetic path toward later builds

The flashlight can become the first host for magnetic experiments, but those experiments must remain modular.

Progression:

1. pulse energy through one wound ferrite/inductive element
2. measure storage and release
3. add a second oriented winding / field axis
4. add a third independent axis
5. measure the actual resultant field with a 3-axis Hall sensor
6. test whether selective reinjection can maintain a chosen field-state band with less average source energy than continuous excitation

Do not assume the field is spherical from the coil layout. Measure `Bx`, `By`, and `Bz` and reconstruct the actual vector path.

## P0 measurements

At minimum log:

- battery voltage under load
- battery/source current
- average source current
- energy consumed over time
- center-reference movement
- `V+`, `V-`, and differential voltage
- storage voltage/current
- reinjection threshold crossings
- pulse width and duty cycle
- LED current
- relative / measured light output
- temperature where practical

## Reference comparison

Build or simulate a conventional reference light with the same battery, LED/load, and matched useful brightness.

P0 passes only if either:

1. balanced/reinjection operation gives a reproducible runtime or average-energy advantage at matched output, or
2. the measurements clearly identify why it does not, providing a concrete next correction.

## Parts strategy

Prefer reusable assortment inventory over one-off purchases where sensible:

- breadboard-friendly logic-level MOSFET assortment
- capacitor assortment
- diode / Schottky assortment
- resistor assortment for sensing, current limiting, bias, and tests
- magnet wire for user-owned ferrite cores
- comparators / Schmitt-trigger-capable parts
- Hall sensors later for field work
- perfboard and headers/connectors for permanent prototypes

Cheap legacy MOSFET assortments may contain parts that do not fully enhance at 3.3/5 V gate drive. Verify gate-drive requirements before treating a part as a low-voltage switch.

## Virtual Breadboard status — 2026-09-08

**SIMULATION RESULT — not a physical bench result.**

The Virtual Breadboard now has two flashlight test levels on `main`:

```text
Virtual_Breadboard/test/flashlight-calibration/
Virtual_Breadboard/test/run_flashlight_calibration.js
Virtual_Breadboard/test/flashlight-prototype.test.js
```

The calibration pack independently checks:

1. white LED + real current limiter;
2. MOSFET-switched LED;
3. real L/R coil step response;
4. flyback-clamped coil;
5. reversible H-bridge inductive load.

The integrated prototype then joins these already-qualified circuit primitives into one live simulation containing:

```text
5 V source
  -> buffered CENTER reference
  -> storage capacitor
  -> Schmitt hysteresis
  -> PMOS reinjection gate
  -> current-limited white LED load
```

The integrated simulation must prove all of the following before CI passes:

- storage does not collapse below 3.2 V;
- storage remains bounded below 4.6 V rather than rail-locking;
- hysteretic reinjection repeatedly cycles across the storage band;
- the PMOS has both conducting and disconnected/coast intervals;
- the white LED remains on through the coast interval;
- average LED current remains nontrivial for the modeled indicator-class LED;
- buffered CENTER remains a real midpoint under the integrated load;
- the solver reports no numerical failure.

The dedicated GitHub Actions workflow is:

```text
.github/workflows/breadboard-flashlight-tests.yml
```

It runs both the five-circuit calibration pack and the integrated prototype on every relevant change.

### Why the integrated simulator starts at 5 V

The Virtual Breadboard currently models an SN74HC14-class Schmitt trigger whose declared operating supply is 2–6 V. Driving that model directly from the P0 9 V battery would be an invalid circuit and must not be hidden by the simulator.

Therefore the current successful integrated run proves the **reinjection/light/control topology at a valid 5 V control rail**. It does **not** yet prove the complete 9 V P0 source architecture.

The next 9 V simulation step is to add a physically valid 9 V -> logic-rail supply/regulator path (or select a hysteretic controller genuinely rated for the 9 V rail), then repeat the exact same checks and add the matched-brightness continuous-drive energy comparison.

## Done for P0

The flashlight makes useful light, remains electrically stable around its center reference, performs measurable threshold-controlled reinjection, projects a momentary battery bar display, and produces a complete runtime/energy comparison against the conventional reference.
