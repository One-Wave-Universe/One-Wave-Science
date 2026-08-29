---
node_id: "G-743"
canonical_name: "Proven Quadrature Rotating-Field Hardware — Views Up / Actions Down"
namespace: "NODE"
gate: "GREEN"
lifecycle: "PROPOSED_BUILD"
classification: "Quadratic Routing / Established Hardware Analogy / Sensor-Actuator Pair"
claim_gate_detail: "GREEN (external hardware principles) / YELLOW (One-Wave integration mapping)"
metadata_standard: "I-06"
---

# Node G-743: Proven Quadrature Rotating-Field Hardware — Views Up / Actions Down

## Purpose

Lock the established rotating-field hardware roles that map onto G-740's paired
quadratic routing contract while preserving the three-winding reflex controller
as a fast local nerve layer:

```text
three-winding ternary reflex state
        |
        +---- contributes reflex state to Views UP
        |
rotating relation
        |
        +-> quadrature sensing / resolver-style readout -> Views UP
        |
        +-> two-phase quadrature stator drive          -> Actions DOWN
                                                        |
                                                        +-> Override / correction returned to nerve controller
```

The reflex controller remains locally autonomous and fast. The quadratic layer
must be able to observe its state on the upward leg and send a bounded downward
override/correction without turning the brain into the ordinary source of every
nerve action.

This node does **not** claim that any established technology proves the full
One-Wave architecture. It records proven physical mechanisms that can be reused
inside the proposed build without inventing new rotating-field hardware.

## 1. Views Up — Resolver / Quadrature Magnetic Position Sensing

Established resolver hardware uses two orthogonal secondary axes to resolve a
rotating magnetic relation into sine and cosine components. The secondary axes
are mechanically displaced by 90 degrees. Their outputs carry angular relation
as orthogonal components:

```text
SINE   ~ sin(theta)
COSINE ~ cos(theta)
```

Commercial resolver and resolver-to-digital systems use these signals to recover
angular position and velocity. Equivalent magnetic angle sensors can likewise
produce orthogonal sine/cosine outputs from a rotating magnetic field.

### One-Wave mapping

This is the physical precedent for the **quadratic Views-up** leg:

```text
rotating / accumulated differential
        |
orthogonal magnetic sensing
        |
Direction / Phase / Strength / Reference
        |
paired Field + Void Views UP
```

The upward packet must also include the current three-winding reflex-controller
state so higher oversight sees what the fast nerve layer is already doing rather
than receiving a detached sensor picture.

Minimum reflex contribution to the upward receipt:

```text
reflex ternary state      -1 / 0 / +1
active winding / phase
rotation direction
local reference
reflex confidence / strength
whether local reflex action is already in progress
```

The resolver is a sensing/readout device. In this architecture it must not be
silently repurposed as the actuator stage.

## 2. Actions Down — Two-Phase Quadrature Stator / Sine-Cosine Drive

Established two-phase stepper and quadrature motor drive hardware places two
phase windings on orthogonal axes. In a two-phase stepper the A and B phase
windings form a 90-degree spatial relationship. Driving those windings with
sine/cosine current commands produces a controllable rotating magnetic vector.

A standard sine-cosine microstepping relation is:

```text
I_A = I * sin(theta_cmd)
I_B = I * cos(theta_cmd)
```

Changing `theta_cmd` rotates the commanded stator field; changing amplitude
changes commanded field strength. Reversing the progression reverses rotation.

### One-Wave mapping

This is the physical precedent for the **quadratic Actions-down** leg:

```text
resolved command
      |
quadrature sine/cosine drive
      |
rotating magnetic/current vector
      |
Inward / Outward / Across / Over
      |
paired Field + Void Actions DOWN
```

One of those downward actions may be a Void Override. That Override must be
communicated back to the three-winding nerve controller as a distinct control
condition, not hidden inside an ordinary ternary reflex state.

The drive stage acts; it is not the sensing/View stage.

## 3. Three-Winding Reflex Controller — Local Fast Layer

The three-winding / three-phase construction is retained as the **ternary nerve
reaction / reflex controller**.

Its ordinary local choice remains:

```text
-1 = counter / reverse / reduce
 0 = active Hold / maintain
+1 = express / advance / increase
```

The reflex controller is permitted to react before higher command resolution,
provided that its state and consequence are included in the next upward View
packet.

Its required communication loop is:

```text
local sensory differential
        |
three-winding ternary reflex controller
        |
fast local reflex action
        |
reflex state + consequence
        |
        +-----------------------> quadratic Views UP
                                      |
                                  oversight / command
                                      |
                           quadratic Actions DOWN
                                      |
                           Void Override if required
                                      |
                           three-winding controller
```

This preserves local reflex autonomy while keeping the reflex visible to higher
oversight.

## 4. Override Contract Back to Nerve Control

Override is a **Void Action** on the downward leg. It is not a fourth ternary
state and it must not overwrite the meaning of `-1 / 0 / +1`.

The nerve controller therefore needs two logically separate inputs:

```text
reflex ternary command: -1 / 0 / +1
override line/state:     no-override / override
```

The minimum safe override behaviors to test are:

```text
Override + local +1 -> force Hold or commanded counter-action
Override + local  0 -> retain safe Hold
Override + local -1 -> force Hold or commanded counter-action
```

The exact electrical arbitration between Hold and counter-action remains a
bench question and must be recorded explicitly. A downward override may stop,
reverse, reroute, or clamp the reflex response only if the chosen behavior is a
distinct measured state.

Override must not erase the prior reflex receipt. The system must retain what
the nerve controller attempted, what higher oversight commanded, and what
physical consequence followed.

## 5. Locked Direction Separation

G-740 remains authoritative:

```text
(Field Views + Void Views + reflex-state contribution)
                    UP
                    |
                brain / command
                    |
                   DOWN
        (Field Actions + Void Actions)
                    |
              reflex override
```

Therefore the hardware roles are kept distinct:

| One-Wave leg | Established hardware pattern | Physical role |
|---|---|---|
| Reflex local | three-winding rotating-field controller | fast ternary nerve reaction |
| Views UP | resolver / quadrature magnetic angle sensor | sense rotating relation and report reflex state |
| Actions DOWN | two-phase quadrature stator / sine-cosine drive | create commanded rotating magnetic vector |
| Override return | distinct Void Action input to reflex controller | interrupt, clamp, reverse, or reroute reflex response |

No View/Action cross-switch is allowed.

## 6. Three-Winding Inclusion Boundary

The three-winding construction is **not** a replacement for the quadratic
sensor/actuator pair. It is instead integrated with that pair through
communication:

```text
three-winding reflex -> included in Views UP
quadratic Actions DOWN -> Override communicated to three-winding reflex
```

This distinction allows the nerve layer to remain faster than conscious or
higher oversight while still making its current action observable and
interruptible.

## 7. Integration With the Three-Physical-Structure Cell

The current VTC physical interpretation retains:

```text
3 physical mirrored structures
x 2 traversal orientations / phases
= 6 logical positions
```

Those six logical positions are not six separate quadratic machines. The
quadrature sensing and drive layers observe or act on the resolved rotational
relation produced by the cell.

The cell-level information reference remains the shared local `(0)` / `V0` and
its signal margins may be millivolt-scale. Commercial resolver, reflex-motor, or
motor-drive excitation voltages are implementation details and must not be
confused with the cell's local information amplitude.

## 8. Bench Translation

### Reflex-to-Views-up target

Demonstrate that the three-winding controller can execute a local ternary reflex
and simultaneously expose enough state for the quadratic sensing layer to
report what it is doing.

Minimum recorded quantities:

```text
reflex -1 / 0 / +1
active phase / winding state
rotation direction
local V0
reflex strength
measured consequence
```

### Views-up bench target

Demonstrate that one rotating magnetic relation can be reconstructed from two
orthogonal channels without ambiguity over a complete electrical cycle while
retaining the reflex-controller contribution.

Minimum recorded quantities:

```text
sin channel
cos channel
phase
amplitude / strength
local reference
rotation direction
reconstructed angle
reflex state
```

### Actions-down / override target

Demonstrate that two orthogonal drive channels commanded in quadrature produce
a repeatable rotating magnetic/current vector in both directions, and that a
separate Void Override reaches the three-winding reflex controller and changes
its behavior in a measurable way.

Minimum recorded quantities:

```text
I_A
I_B
commanded phase
measured phase
strength
rotation direction
local reference
reflex state before override
override state
reflex state after override
measured consequence
```

Do not connect a mechanical load until the field/current behavior is measured
and the local information reference is shown not to be dragged by actuator
return current.

## 9. External Engineering Basis

Established engineering references supporting the physical mechanisms:

1. Analog Devices, "Precision Resolver-to-Digital Converter Measures Angular Position and Velocity" — resolver primary excitation and two secondary windings displaced by 90 degrees producing sine/cosine outputs:
   https://www.analog.com/en/resources/analog-dialogue/articles/precision-rtdc-measures-angular-position-and-velocity.html

2. Microchip AN1307, "Stepper Motor Control with dsPIC DSCs" — two-phase stepper driven by two sine waves shifted 90 degrees apart:
   https://ww1.microchip.com/downloads/en/AppNotes/AN1307-Stepper-Motor-Control-with-dsPIC-DSCs-DS00001307B.pdf

3. Oriental Motor, "Stepper Motor Basics" — two-phase construction with phase/pole geometry arranged in 90-degree relationships:
   https://www.orientalmotor.com/stepper-motors/technology/stepper-motor-basics.html

These sources establish the resolver/quadrature sensing and two-phase
quadrature drive mechanisms. Three-phase rotating-field control is established
engineering as well; its One-Wave assignment here is specifically the fast
ternary reflex layer. The complete cross-layer mapping remains a proposed build
integration to be tested.

## 10. Pass Conditions

The mapping survives only if bench measurements show:

1. the three-winding controller can produce distinguishable local ternary reflex
   behavior;
2. its current reflex state is included in the Views-up receipt;
3. Views-up sensing reconstructs direction, phase, strength, and reference from
   the rotating relation without acting as the drive stage;
4. Actions-down drive creates a distinguishable commanded rotating vector in
   both directions without masquerading as sensory evidence;
5. a Void Override travels downward as a separate condition and measurably
   changes or arrests the reflex controller;
6. the prior local reflex state remains in the receipt after Override;
7. Field and Void remain paired on both legs;
8. the shared local reference remains measurable and stable;
9. the three physical structures still yield six and only six logical positions;
10. the measured consequence returns as the next reference/receipt.

## Anti-drift statement

```text
Three-winding rotating field = fast ternary reflex control.
Reflex state contributes to quadratic Views UP.
Resolver / quadrature sensor = Views UP.
Two-phase quadrature stator / sine-cosine drive = Actions DOWN.
Void Override travels DOWN and is communicated back to the reflex controller.
Override never becomes a fourth ternary state.
```
