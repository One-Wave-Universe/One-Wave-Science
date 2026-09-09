# One Wave Science — Initial Product Line

Working names only. Brand/trademark clearance is required before final launch naming.

## Platform: One Wave Circuit Lab

Shared qualified circuit-simulation core plus product-specific workspaces.

The platform should share:
- circuit solver;
- component model registry;
- measurement engine;
- fault reporting;
- save/load project format;
- test/receipt framework;
- installer/update framework.

Do not fork the physics engine independently for each product.

---

## Product 1 — Breadboard Lab

### User
Hobbyist, student, repairer, inventor or bench builder who wants to try a circuit before wiring the physical board.

### Core workflow

```text
NEW BUILD
  -> place parts
  -> wire
  -> power/simulate
  -> inspect
  -> scope/measure
  -> diagnose faults
  -> adjust
  -> save
  -> reopen
  -> export/share
  -> physical bench build
```

### Release-one promise

A human can install the desktop app and build/test ordinary low-voltage breadboard circuits without using GitHub, Node, npm or a terminal.

### Evidence already available

The repository contains conventional control/regression suites for resistor networks, RC/RL behavior, diodes/LEDs, MOSFETs, netlists, fault states and additional primitives. These validate the simulator controls; they do not make every possible circuit/model accurate automatically.

---

## Product 2 — Pedal Lab

### User
Guitarist/pedal builder who wants to design, compare and troubleshoot low-voltage effects circuits before soldering.

### Product-specific workspace

Use the same circuit core but provide a pedal-oriented bench:
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
- optional audio preview only after the electrical transfer path is correctly modeled.

### Required component-model expansion

Likely required for useful real pedal coverage:
- BJT NPN/PNP models;
- JFET models;
- common audio op-amp models;
- additional diode families including clipping diodes/LEDs;
- coupling capacitor behavior;
- potentiometer tapers;
- transistor/op-amp bias and supply limits.

A fixed-resistance or ideal-switch approximation must be labeled when used.

### First pedal controls

Use established circuits whose expected behavior is well documented as simulator qualification fixtures, for example:
- passive volume/tone network;
- simple diode clipper;
- transistor boost;
- op-amp gain stage after op-amp support exists;
- tone-control network;
- true-bypass switching.

Do not ship named commercial pedal clones without checking trademark/copyright/layout issues. Generic circuit classes are safer reference fixtures.

---

## Product 3 — Perfboard Amp Lab

### User
DIY amplifier builder who wants to convert a validated schematic into a physical perfboard layout and catch wiring, bias, loading and thermal mistakes before soldering.

### Product-specific workspace

Add a real perfboard topology layer:
- holes/pads;
- copper strips where applicable;
- cuts;
- jumpers;
- component leads;
- underside/topside views;
- continuity/net highlighting;
- collision/lead-reach checks;
- project BOM;
- test points.

The physical layout compiles into the same electrical netlist consumed by the qualified solver.

### Amplifier tests

For supported low-voltage amplifiers:
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

Tube amps, mains wiring and other hazardous-voltage designs remain out of scope until a separately designed high-voltage safety model, isolation rules and expert review exist.

---

## Product architecture rule

```text
QUALIFIED CIRCUIT CORE
       |
       +-- Breadboard workspace
       +-- Pedal workspace
       +-- Perfboard/Amp workspace
       |
       +-- shared measurements
       +-- shared fault system
       +-- shared project format
       +-- shared regression infrastructure
```

A product-specific UI may add a thin adapter. It must not silently create different physics for the same component.

## Possible commercial tiers — not yet priced

Keep pricing separate from code until the installable product is proven.

Potential structure:
- free/read-only or basic educational tier;
- paid builder tier with save/export/advanced instruments;
- Pedal Lab add-on;
- Perfboard Amp Lab add-on;
- later classroom/maker-space licensing.

No price is approved by this document.
