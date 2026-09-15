# CELL_V1 Board #1 - Baseline Physical Test Harness

**Status:** current experimental build harness. This file defines the first board used to prove the electrical and magnetic functions before closing the three-core nerve ring or enabling reinjection.

**Architecture authority:** this board lives **inside one CELL_V1 hex**. It does not replace the locked six-edge hex, seven-cell flower, or scale recurrence.

```text
ONE CELL_V1 HEX
 -> identical flat-edge neighbor
 -> seven-cell flower
 -> path / rotation / field
 -> volume
 -> next-scale point
```

Canonical external edge order remains:

```text
A+ -> B+ -> C+ -> A- -> B- -> C-
```

All external ports are centered on the flat sides, never the corners.

---

## 1. Why Board #1 exists

The purpose of Board #1 is to turn the proposed A/B/C magnetic cell into an instrumented physical test harness in which each claim is isolated before the next loop is connected.

The order is mandatory:

```text
power/reference foundation
 -> differential drive
 -> open-circuit sense characterization
 -> independent memory threshold measurement
 -> one A Sense -> B Memory transfer
 -> complete A->B->C->A nerve ring
 -> controlled reinjection
```

Do not close the full analog ring before the individual transfer has been demonstrated.

---

## 2. 18-terminal experimental magnetic layout

The current experimental fixture uses three magnetic elements: A, B, and C.

Each element exposes three functional winding pairs:

```text
DRIVE + / -
MEMORY + / -
SENSE + / -
```

That gives:

```text
6 terminals per magnetic element
x 3 magnetic elements
= 18 external magnetic-element terminals
```

This 18-terminal count belongs to the **bench magnetic fixture**, not to the six external CELL_V1 hex ports.

Keep the distinction explicit:

```text
6 CELL_V1 EDGE PORTS
!=
18 BOARD #1 MAGNETIC TERMINALS
!=
MOSFET COUNT
```

Exact winding count remains experimental. The three-pair fixture is a testable implementation, not a permanent law of CELL_V1.

---

## 3. Board zones

Physically divide the board into four functional zones.

### Zone A - Power perimeter

- +5 V current-limited DC link;
- local DC-link decoupling;
- switching stages for A, B, C Drive windings;
- current measurement;
- intentional inductive-energy clamp/recovery paths;
- gate-drive protection and dead time where required.

### Zone B - Magnetic center

- Core/element A;
- Core/element B;
- Core/element C;
- documented winding dot convention;
- mechanically fixed orientation so repeated measurements are comparable.

### Zone C - Quiet reference and measurement

- electrical 2.5 V reference;
- Sense breakout headers;
- Memory breakout headers;
- oscilloscope/test points;
- no intentional high-current drive return through this reference.

### Zone D - Energy reservoir

- DC-link / reinjection capacitor;
- steering/clamp path;
- independent reservoir voltage test point;
- no direct dumping of flyback energy into the 2.5 V reference node.

---

## 4. Power and reference foundation

Start with a protected/current-limited +5 V source.

The first reference implementation may be a simple unloaded midpoint used only as a measurement reference:

```text
+5 V
 |
10 kOhm
 |
 +------ VREF ~= 2.5 V
 |        |
10 kOhm  10 uF
 |        |
0 V     100 nF
          |
         0 V
```

### Important interpretation

With a true floating H-bridge across a Drive winding, the 2.5 V node is **not** the drive-current return path. The winding floats between two bridge outputs.

VREF is used as a quiet electrical reference for:

- sensing;
- comparison;
- biasing where explicitly required;
- measurement of common-mode movement.

The magnetic substrate, ferrite, geometric center, earth ground, and VREF are not interchangeable.

### Reference acceptance test

Before connecting magnetic cross-coupling, measure VREF during every drive pulse.

Record:

- unloaded VREF;
- drive-induced transient movement;
- settling time;
- noise relative to the Sense waveform being measured.

If the measurement circuitry loads the divider enough to move VREF materially, add a suitable buffer/rail-splitter stage. Do not assume the divider is a power source.

---

## 5. Differential Drive architecture

A true Drive + / Drive - pair requires a switching topology that can reverse current through the winding.

Preferred Board #1 interpretation:

```text
                 +5 V DC LINK

             A H-BRIDGE
          OUT_A1     OUT_A2
             |          |
             +-- DRIVE A+
             |   winding   |
             +-- DRIVE A-

             B H-BRIDGE
          OUT_B1     OUT_B2
             |          |
             +-- DRIVE B+
             |   winding   |
             +-- DRIVE B-

             C H-BRIDGE
          OUT_C1     OUT_C2
             |          |
             +-- DRIVE C+
             |   winding   |
             +-- DRIVE C-
```

A single ordinary half-bridge has only one switching node. Therefore `Drive +` and `Drive -` must not both be described as independent half-bridge outputs unless a center-tapped or other explicitly defined winding topology is used.

### Required protection

- current limiting;
- shoot-through prevention/dead time;
- deliberate inductive-energy path;
- gate pull-downs/pull-ups as appropriate;
- thermal observation;
- no hot-plugging unknown winding configurations.

---

## 6. Breakout header layer

During Board #1 bring every Sense and Memory terminal to accessible headers or jumper blocks.

```text
A Sense +     o
A Sense -     o
A Memory +    o
A Memory -    o

B Sense +     o
B Sense -     o
B Memory +    o
B Memory -    o

C Sense +     o
C Sense -     o
C Memory +    o
C Memory -    o
```

Leave all Sense and Memory pairs floating during the first Drive characterization.

This is deliberate. The board must allow the ring to be opened, one link inserted, polarity reversed, or an impedance-matching stage added without cutting traces.

---

## 7. Required test points

Provide test points for:

```text
TP_5V        DC-link supply
TP_0V        supply return
TP_REF       2.5 V electrical reference
TP_DC        DC-link / reinjection capacitor

TP_A1 / A2   both ends of Drive A
TP_B1 / B2   both ends of Drive B
TP_C1 / C2   both ends of Drive C

TP_AS+ / AS- A Sense pair
TP_AM+ / AM- A Memory pair
TP_BS+ / BS- B Sense pair
TP_BM+ / BM- B Memory pair
TP_CS+ / CS- C Sense pair
TP_CM+ / CM- C Memory pair
```

Where floating bridge nodes are measured, use a measurement method that does not short the node through an earth-referenced oscilloscope ground clip.

---

## 8. Phase 1 - Drive and open-circuit Sense characterization

Start with Core A only.

1. Leave A Sense and A Memory unloaded.
2. Apply a controlled Drive pulse in one direction.
3. Record both Drive terminals and the Sense pair.
4. Reverse the Drive polarity and repeat.
5. Repeat with identical pulse settings.

Record:

- pulse amplitude;
- pulse width;
- winding current;
- raw Sense amplitude;
- Sense polarity;
- ringing frequency;
- decay constant / settling behavior;
- flyback tail;
- VREF movement;
- DC-link movement;
- core and switch temperature.

The open Sense waveform is the baseline against which all later loading/cross-coupling is compared.

---

## 9. Phase 2 - Independent Memory threshold

Do not use the Sense winding to drive Memory yet.

Drive each Memory pair from a separately controlled, current-limited source or pulse stage and determine whether a retained magnetic state can be written.

Sequence:

```text
known initial condition
 -> Memory write pulse
 -> remove write current completely
 -> wait defined interval
 -> weak standardized read/probe
 -> record response
 -> reverse write
 -> repeat identical probe
```

Measure the minimum write current/pulse area that produces a reproducible retained-state difference.

Do not call ordinary inductive ringing or residual charge memory.

The hard memory criterion is:

> After all write drive has been removed, the prior write direction/state changes a later standardized response reproducibly.

---

## 10. Phase 3 - First nerve-transfer experiment: A -> B

Only after Phase 1 and Phase 2 are characterized, close one candidate cross-coupling path:

```text
A SENSE +  ---- candidate link ----> B MEMORY +
A SENSE -  ---- candidate link ----> B MEMORY -
```

Then:

1. place B in a known baseline state;
2. pulse A with a standardized Drive event;
3. allow A Drive and transient ringing to settle;
4. remove A Drive completely;
5. interrogate B with the same standardized weak probe used during Phase 2;
6. compare B with and without the A->B link/event.

### Hard transfer criterion

A nerve transfer passes only if:

```text
A event
 -> measurable energy/current reaches B Memory path
 -> after A drive is gone
 -> B retains a reproducible changed state
 -> B's later standardized response differs from baseline
```

A simultaneous voltage spike in B is not sufficient. That proves coupling, not retained memory transfer.

---

## 11. Direct Sense-to-Memory wiring is a candidate

The candidate three-link nerve ring is:

```text
A Sense +/- -> B Memory +/-
B Sense +/- -> C Memory +/-
C Sense +/- -> A Memory +/-
```

This ring is **not yet locked as a direct copper connection**.

Reason:

- a Sense winding can generate useful voltage but insufficient magnetizing current;
- directly loading the Sense winding can collapse or distort the waveform;
- the source/load impedance may require transformation, buffering, controlled gain, or another passive/active coupling stage;
- polarity and turn ratio matter.

Therefore test direct coupling first. If it fails, measure why before adding a buffer.

Possible later coupling implementations include:

```text
DIRECT      Sense -> Memory
PASSIVE     Sense -> transformer / resonant match -> Memory
CONTROLLED  Sense -> analog buffer/current stage -> Memory
MAGNETIC    coupled magnetic path with measured transfer
```

The chosen implementation must preserve continuous analog causality and be measurable.

---

## 12. Phase 4 - Close the three-element nerve ring

Only after one A->B transfer passes, duplicate the same proven coupling mechanism:

```text
A -> B
B -> C
C -> A
```

Test each link separately before closing the ring.

Then close the ring and distinguish:

- one-pass propagation;
- damped ringing;
- unstable positive feedback;
- stable oscillation;
- directional/circulating propagation;
- retained state affecting later circulation.

Do not label oscillation as field rotation without phase-resolved evidence around A/B/C.

---

## 13. Phase 5 - Controlled reinjection

Reinjection comes **after** Drive, Sense, Memory threshold, and nerve transfer are understood.

Correct energy path:

```text
inductive / magnetic return
 -> steering / synchronous recovery
 -> DC-link or local reservoir capacitor
 -> measured controlled release
 -> later permitted Drive/Memory event
```

Incorrect path:

```text
flyback -> 2.5 V VREF
```

The electrical reference must remain a reference, not an energy dump.

Measure separately:

```text
E_in
E_returned_to_reservoir
E_later_delivered
losses
```

Memory/state return and energy return are related but distinct tests:

```text
STATE RETURN:
old magnetic organization changes the next event

ENERGY RETURN:
measurable field energy is recovered and reused later
```

---

## 14. Relationship to One-Wave lattice/memory hypothesis

Board #1 does not prove the One-Wave substrate model. It tests a hardware analogue of the proposed sequence:

```text
electrical differential
 -> magnetic rotation / magnetic-state change
 -> reorganization of available local pathways
 -> persistent hysteretic organization
 -> old organization changes a later event
 -> physical history / memory
```

For the One-Wave architecture, the long-term hypothesis is that recursive CELL_V1 structures manipulate and read a persistent medium rather than merely storing digital symbols.

The engineering proof required here is narrower and measurable:

```text
write
 -> remove drive
 -> retain
 -> read
 -> rewrite
 -> show prior state changes later response
```

Only measured magnetic/electrical behavior is promoted to hardware canon.

---

## 15. Relationship to the hex and scale recurrence

Board #1 is an internal implementation of **one** CELL_V1.

It must eventually expose the locked six external edge interfaces:

```text
          A+
      __________
     /          \
 C- /            \ B+
   /              \
   \              /
 B- \            / C+
     \__________/
          A-
```

After the internal cell passes its tests:

```text
ONE HEX
 -> identical neighbor
 -> 2/3-cell path
 -> closed rotation
 -> seven-cell flower
 -> smallest depth coupling
 -> volume
 -> mirrored/history volume candidate
 -> next-scale point
```

The Board #1 fixture must never become a one-off assembly that cannot map back into the repeatable hex.

---

## 16. Board #1 pass gates

### Gate 1 - reference integrity

PASS if the reference is characterized and does not masquerade as the signal being measured.

### Gate 2 - reversible Drive

PASS if Drive current can be deliberately reversed through each magnetic element without shoot-through or unintended reference current.

### Gate 3 - measurable open Sense

PASS if repeated identical Drive events produce repeatable Sense waveforms with known polarity and loading behavior.

### Gate 4 - retained Memory

PASS if an independently written state persists after the write source is removed and changes a later standardized response.

### Gate 5 - A->B retained transfer

PASS if an A event writes a reproducible retained change into B after A has settled and been disconnected from active drive.

### Gate 6 - complete nerve ring

PASS only after A->B, B->C, and C->A each work independently and the closed ring behavior is measured.

### Gate 7 - reinjection

PASS if returned energy is captured in a reservoir and intentionally contributes to a later event with explicit energy accounting.

---

## 17. Build receipt

For every test record:

```text
test_id
date / board revision
magnetic element / winding
core material / geometry
turn counts and polarity/dot convention
5 V supply and current limit
VREF unloaded and during pulse
bridge topology
Drive pulse amplitude / width / current
open Sense waveform
Memory write pulse / current
retained-state readback
A->B / B->C / C->A link configuration
reservoir waveform
energy accounting
temperature
PASS / FAIL
unexpected behavior
next single change
```

Standing rule:

```text
change one thing
 -> test immediately
 -> compare to active gate
 -> check for drift
```

After three repeats of the same failing approach, change the coupling or measurement angle instead of repeating the same assumption.
