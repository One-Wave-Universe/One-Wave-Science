# SiC International — Initial Product Line

Working names only. Brand/trademark clearance is required before final launch naming.

## Shared platform principle

Products may reuse one qualified conventional circuit-simulation core where that is technically appropriate.

Shared infrastructure may include:
- circuit solver;
- conventional component-model registry;
- measurement engine;
- fault reporting;
- project format;
- test/receipt framework;
- installer/update framework.

Do not fork the same conventional component into contradictory physics across products.

Research-only models and experimental hypotheses must not be silently exposed inside classroom products.

---

## Product 1 — Breadboard Lab

### Product role

**Breadboard Lab is a normal electronics education product.**

It is for students, teachers, introductory electronics classes, STEM programs, maker-space education, and beginners learning how conventional breadboard circuits work.

It is **not** the One-Wave research sandbox and is not marketed as an experimental electronics platform.

### What belongs in Breadboard Lab

- Ohm's law;
- series and parallel circuits;
- voltage/current/resistance;
- LEDs and current limiting;
- ordinary diodes;
- switches and pushbuttons;
- potentiometers/dividers;
- capacitors and RC timing;
- inductors and RL behavior where qualified;
- conventional AC lessons;
- conventional transistor/MOSFET lessons where qualified;
- conventional comparator/op-amp lessons only after those models are qualified;
- scope/measurement practice;
- shorts, open circuits, polarity mistakes and other normal fault lessons;
- safe low-voltage breadboard practice before a physical build.

### What does not belong in Breadboard Lab

- One-Wave theory experiments;
- ternary research cells;
- magnetic-memory architecture experiments;
- MTJ research demonstrations;
- lattice/AI-hardware experiments;
- unverified energy or field claims;
- speculative physics;
- internal qualification/calibration fixtures presented as student lessons.

Those remain in separate research/development tooling.

### Core student workflow

```text
OPEN LESSON OR NEW BOARD
  -> place normal parts
  -> wire
  -> simulate
  -> inspect
  -> scope/measure
  -> identify mistake or expected behavior
  -> adjust
  -> save/share when edition permits
  -> reproduce on a physical low-voltage breadboard
```

### Free edition

A useful classroom demo, not crippleware:
- one editable board;
- beginner conventional parts;
- live voltage/current inspection;
- basic scope;
- fault warnings;
- LED current-limiting lesson;
- RC charge/time-constant lesson.

### Paid classroom edition

Expands educational capability:
- larger conventional component/lesson library;
- multi-board classroom projects;
- save/reopen/project library;
- export/share for homework or teacher review;
- advanced scope/measurement tools;
- guided lessons/challenges;
- reporting/BOM/worksheet support;
- teacher/classroom features when implemented.

Paid Breadboard Lab still does **not** unlock experimental One-Wave research content.

### Release-one promise

A student or teacher can install the desktop app and build/test supported ordinary low-voltage educational circuits without GitHub, Node, npm, or a terminal.

---

## Product 2 — Pedal Lab

### Product role

A separate specialist product for guitarists and pedal builders who want to design, compare and troubleshoot conventional low-voltage effects circuits before soldering.

### Product-specific workspace

Use the qualified conventional circuit core where possible, with:
- guitar/input signal generator;
- input/output jack representation;
- 9V/18V pedal supply presets;
- potentiometers shown as pedal controls;
- footswitch/bypass wiring;
- oscilloscope;
- frequency response / sweep;
- gain meter;
- clipping view;
- current draw;
- optional audio preview after the electrical path is correctly modeled.

### Required model expansion

For useful real pedal coverage:
- BJT NPN/PNP models;
- JFET models;
- common audio op-amp models;
- additional diode families;
- coupling capacitor behavior;
- potentiometer tapers;
- transistor/op-amp bias and supply limits.

Approximations must be labeled.

---

## Product 3 — Perfboard Amp Lab

### Product role

A separate specialist tool for DIY amplifier builders converting validated low-voltage schematics into physical perfboard layouts.

### Product-specific workspace

- holes/pads;
- copper strips where applicable;
- cuts;
- jumpers;
- component leads;
- underside/topside views;
- continuity/net highlighting;
- collision/lead-reach checks;
- BOM;
- test points.

The physical layout compiles into the same qualified conventional electrical netlist where possible.

### Amplifier checks

- DC bias / quiescent current;
- input impedance;
- output impedance where modeled;
- voltage gain;
- frequency response;
- clipping/output swing;
- load behavior;
- component power dissipation;
- thermal warning;
- supply sag;
- grounding/current-return inspection.

### Safety boundary

Initial Perfboard Amp Lab is **low-voltage only**.

Tube amps, mains wiring and other hazardous-voltage designs remain out of scope until separately designed and reviewed high-voltage safety handling exists.

---

## Research/development tools

Experimental One-Wave, ternary, magnetic-memory, lattice, AI-hardware, and other exploratory work stays in research/development tooling.

It may reuse internal engineering code where appropriate, but it is **not a Breadboard Lab edition or paid classroom unlock**.

This separation protects students and teachers from confusing established electronics with exploratory claims.

## Product architecture

```text
SiC International
       |
       +-- Breadboard Lab Free        (classroom)
       +-- Breadboard Lab Paid        (classroom)
       +-- Pedal Lab                  (specialist conventional electronics)
       +-- Perfboard Amp Lab          (specialist conventional electronics)
       +-- Research / Experimental    (separate, clearly labeled)
```

## Pricing

Pricing stays outside circuit-engine source. No price is approved by this document.
