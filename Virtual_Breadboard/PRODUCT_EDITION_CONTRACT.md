# Breadboard Lab — Classroom Product Contract

Status: product-boundary contract for the human-facing desktop app. One codebase, Free and Paid classroom editions. **Breadboard Lab is a conventional electronics teaching product. It is not an experimental or One-Wave research workspace.**

## Product identity

Breadboard Lab exists for normal electronics education: students learning what real parts do, teachers demonstrating circuits, and beginners practicing safe low-voltage breadboard work before touching a physical board.

It must teach and simulate established circuit behavior using conventional component models and clearly documented approximations.

Breadboard Lab must not expose or market:

- One-Wave experimental circuits;
- ternary research cells;
- magnetic-memory research builds;
- MTJ / speculative architecture experiments;
- experimental lattice or AI-hardware concepts;
- unverified energy, field, gravity, or physics claims;
- research-only calibration builds as student lessons.

Research work stays in a separate research/testing environment and is never silently mixed into the school product.

## Core rule

The Free and Paid editions use the **same qualified circuit engine, same conventional component models, same fault logic, and same regression suite**.

Edition gating may control classroom features, project limits, instruments, lessons, export, or teacher tools. It must never make the same circuit produce different physics depending on payment status.

## Intended users

- middle-school / high-school electronics classes where appropriate;
- introductory college electronics;
- STEM and maker-space classrooms;
- teachers and tutors;
- students learning breadboarding at home;
- beginners who want a safe practice environment before building physically.

## Free Demo

Purpose: let a student or teacher install the app, complete real beginner circuits, change values, and observe conventional electrical behavior without GitHub, Node, npm, or a terminal.

### Free Demo must include

- one large breadboard workspace;
- editable blank build mode;
- ordinary low-voltage beginner parts:
  - jumper wire;
  - resistor;
  - LED;
  - ordinary diode;
  - capacitor;
  - DC power supply / battery;
  - switch / pushbutton;
  - potentiometer;
  - scope probe / voltage readout;
- live conventional simulation;
- inspector voltage/current readouts;
- warnings for obvious short/fault conditions;
- clear/reset;
- two one-click teaching demos;
- all free-demo circuit types backed by the same release regression tests as Paid.

### Free teaching demos

1. **LED Lamp — current limiting**
   - 5 V supply;
   - current-limiting resistor;
   - LED;
   - ordinary wiring;
   - learner changes resistor value and observes current change;
   - lesson target: voltage, resistance, current, polarity, and why the resistor protects the LED.

2. **RC Charge / Delay — time constant**
   - supply;
   - switch;
   - resistor;
   - capacitor;
   - scope probe;
   - learner toggles the switch and watches the RC transient;
   - learner changes R or C and observes the time constant change;
   - lesson target: stored charge and the relationship tau = R*C.

A short-circuit example may remain as an explicitly labeled **safety lesson**, not a showcase experiment.

### Free Demo limits

Initial limits should be obvious and non-destructive:

- one board at a time;
- beginner component subset;
- limited scope channels/features;
- small built-in lesson/demo library;
- limited project persistence;
- no advanced classroom library;
- no teacher assignment/class management tools;
- no Pedal Lab;
- no Perfboard Amp Lab;
- no research/experimental components or presets.

Do **not** use artificial solver inaccuracies, fake delays, or deliberately broken parts as a paywall.

## Paid — Breadboard Lab Classroom

Purpose: the complete conventional electronics learning and teaching product.

Paid expands the classroom, not the experimental scope.

Paid may unlock:

- larger conventional component library;
- multiple breadboards / larger classroom projects;
- unrestricted save/reopen;
- project library;
- export/share for homework and teacher review;
- full oscilloscope controls and multiple probes;
- differential measurements;
- AC source and conventional frequency-response lessons;
- conventional RC/RL/filter lessons;
- conventional transistor/MOSFET lessons where the model is qualified;
- conventional comparator/op-amp lessons only after those models are qualified;
- continuity, fault, power, and diagnostic views;
- BOM / worksheet / report output;
- guided lessons and challenge circuits;
- teacher answer/reference builds kept separate from student-facing tasks;
- classroom/maker-space licensing and teacher features when implemented.

### Explicit Paid exclusion

Paying does **not** unlock experimental One-Wave research inside Breadboard Lab. Those builds belong elsewhere.

## Separate products

SiC International may sell other electronics products, but they remain separate products/workspaces:

```text
SiC International
      |
      +-- Breadboard Lab Free — classroom electronics
      +-- Breadboard Lab Paid — classroom electronics
      +-- Pedal Lab — guitar-pedal design/testing
      +-- Perfboard Amp Lab — low-voltage amp/perfboard design/testing
      +-- Research tools — separate from classroom releases
```

Pedal Lab and Perfboard Amp Lab may reuse the same qualified conventional circuit core, but their specialist features do not turn Breadboard Lab into a research sandbox.

## Entitlement implementation

Use one Breadboard Lab codebase where practical.

Recommended capability model:

```text
edition = free | paid
capabilities = {
  board_count,
  allowed_conventional_component_types,
  scope_channels,
  advanced_scope,
  save_projects,
  export_projects,
  lesson_library,
  teacher_tools
}
```

The UI asks the capability layer whether a classroom feature is available. Circuit-engine code must not read `edition` and must not branch its physics based on entitlement.

A separate build/profile should define research-only parts and presets. They are not merely hidden paid features.

## Human acceptance — Free

```text
install
-> open
-> load LED Lamp lesson
-> inspect voltage/current
-> change resistor
-> see expected conventional result change
-> load RC lesson
-> toggle switch
-> observe charge curve
-> change R or C
-> observe tau change
-> make a small blank-board student circuit
-> close/reopen without corruption
```

## Human acceptance — Paid

```text
install
-> activate paid classroom entitlement
-> open blank board
-> build supported conventional circuit
-> simulate
-> inspect/scope
-> diagnose/adjust
-> save
-> close
-> reopen
-> reload project exactly
-> export/share for teacher or student review
```

## Release gate

Neither edition ships until:

1. the full supported **conventional basic-circuit** suite is green;
2. the Electron launch smoke test is green;
3. both teaching demos are present in the installed UI and usable without a terminal;
4. Free/Paid capability tests prove gating does not change solver output;
5. all student-visible parts are conventional and have an explicit qualification status;
6. no research/experimental presets or terminology appear in the classroom build;
7. Linux x64 and Jetson/ARM64 package paths are verified for intended launch platforms;
8. Paid save/reopen/export is exercised end-to-end by a human.

## Pricing

Do not hard-code a price into the simulator source.

Pricing belongs in company/configuration/release metadata so it can change without touching circuit physics. Initial pricing should be decided after teachers/students have exercised the installable classroom build and we know which paid teaching features carry real value.
