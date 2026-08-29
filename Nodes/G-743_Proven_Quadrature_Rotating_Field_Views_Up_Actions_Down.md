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

Lock the two established quadrature hardware constructions that map cleanly onto
G-740's paired quadratic routing contract:

```text
rotating relation
    |
    +-> quadrature sensing / resolver-style readout -> Views UP
    |
    +-> two-phase quadrature stator drive          -> Actions DOWN
```

This node does **not** claim that either established technology proves the full
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

The drive stage acts; it is not the sensing/View stage.

## 3. Locked Direction Separation

G-740 remains authoritative:

```text
(Field Views + Void Views)
          UP
          |
      brain / command
          |
         DOWN
(Field Actions + Void Actions)
```

Therefore the proven hardware roles are kept distinct:

| One-Wave leg | Established hardware pattern | Physical role |
|---|---|---|
| Views UP | resolver / quadrature magnetic angle sensor | sense rotating relation as orthogonal components |
| Actions DOWN | two-phase quadrature stator / sine-cosine stepper drive | create commanded rotating magnetic vector |

No View/Action cross-switch is allowed.

## 4. Three-Winding Exclusion

The three-winding / three-phase construction is **not** the quadratic hardware
pair defined by this node.

Within the current One-Wave build program, the three-winding construction is
reserved for the **ternary nerve-reaction layer**. Do not replace the two-axis
quadrature Views-up or Actions-down implementations with a three-phase motor
simply because three-phase rotation is also established engineering.

This distinction is architectural, not a claim that conventional three-phase
machines are invalid.

## 5. Integration With the Three-Physical-Structure Cell

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
its signal margins may be millivolt-scale. Commercial resolver or motor-drive
excitation voltages are implementation details of the external hardware and
must not be confused with the cell's local information amplitude.

## 6. Bench Translation

### Views-up bench target

Demonstrate that one rotating magnetic relation can be reconstructed from two
orthogonal channels without ambiguity over a complete electrical cycle.

Minimum recorded quantities:

```text
sin channel
cos channel
phase
amplitude / strength
local reference
rotation direction
reconstructed angle
```

### Actions-down bench target

Demonstrate that two orthogonal drive channels commanded in quadrature produce
a repeatable rotating magnetic/current vector in both directions.

Minimum recorded quantities:

```text
I_A
I_B
commanded phase
measured phase
strength
rotation direction
local reference
```

Do not connect a mechanical load until the field/current behavior is measured
and the local information reference is shown not to be dragged by actuator
return current.

## 7. External Engineering Basis

Established engineering references supporting the physical mechanisms:

1. Analog Devices, "Precision Resolver-to-Digital Converter Measures Angular Position and Velocity" — resolver primary excitation and two secondary windings displaced by 90 degrees producing sine/cosine outputs:
   https://www.analog.com/en/resources/analog-dialogue/articles/precision-rtdc-measures-angular-position-and-velocity.html

2. Microchip AN1307, "Stepper Motor Control with dsPIC DSCs" — two-phase stepper driven by two sine waves shifted 90 degrees apart:
   https://ww1.microchip.com/downloads/en/AppNotes/AN1307-Stepper-Motor-Control-with-dsPIC-DSCs-DS00001307B.pdf

3. Oriental Motor, "Stepper Motor Basics" — two-phase construction with phase/pole geometry arranged in 90-degree relationships:
   https://www.orientalmotor.com/stepper-motors/technology/stepper-motor-basics.html

These sources establish the resolver/quadrature sensing and two-phase
quadrature drive mechanisms. The mapping of those mechanisms to One-Wave
Views-up and Actions-down remains a proposed build integration to be tested.

## 8. Pass Conditions

The mapping survives only if bench measurements show:

1. Views-up sensing reconstructs direction, phase, strength, and reference from
   the rotating relation without acting as the drive stage;
2. Actions-down drive creates a distinguishable commanded rotating vector in
   both directions without masquerading as sensory evidence;
3. Field and Void remain paired on both legs;
4. the shared local reference remains measurable and stable;
5. the three physical structures still yield six and only six logical positions;
6. no three-winding quadratic substitution is introduced; and
7. the measured consequence can return as the next reference/receipt.

## Anti-drift statement

```text
Resolver / quadrature sensor = Views UP.
Two-phase quadrature stator / sine-cosine drive = Actions DOWN.
Three-winding construction = ternary nerve-reaction work, not this quadratic pair.
```
