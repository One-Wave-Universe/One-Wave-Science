---
node_id: "G-778"
canonical_name: "Build Logic Research and Reference Validation Standard"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Engineering Validation / Build Qualification"
metadata_standard: "I-06"
---

# G-778 — Build Logic, Research, and Reference Validation Standard

Every One-Wave build, simulator, hardware packet, runtime bridge, motor/control experiment, and proposed physical architecture is subject to this node.

## 1. Claim ladder

Use exactly these levels:

- **REFERENCE-REAL** — mechanism is established in published engineering, vendor documentation, or a known real build.
- **MODEL PASS** — the repo model/simulator produces the expected result.
- **BENCH-REALITY PASS** — parts, supply, reference, current, drive, thermal, protection, and measurement topology are physically plausible.
- **PHYSICAL PASS** — measured on actual hardware with a retained receipt.
- **ONE-WAVE HYPOTHESIS** — project-specific interpretation not established by the reference mechanism.

Do not promote one level into the next.

## 2. Mandatory build record

Every active build must identify:

1. **Purpose** — what is being tested.
2. **Reference mechanism** — real engineering/research precedent.
3. **What is copied from the reference** — topology, part role, control law, measurement method, etc.
4. **What is new / One-Wave-specific** — the actual experiment.
5. **Inputs and limits** — voltage, current, temperature, timing, load, dimensions.
6. **Measured outputs** — not adjectives.
7. **Control build** — conventional baseline or null case.
8. **Acceptance criteria**.
9. **Failure/falsifier criteria**.
10. **Receipt** — parts, schematic/netlist, software commit, measurements, date.

## 3. Physical-build reference floor

### Virtual midpoint / reference

TI TLE2426 is a real precision rail-splitter designed to generate one-half the supply for analog reference use. It is specified for 4–40 V input and approximately 20 mA typical source/sink capability.

Reference:
https://www.ti.com/product/TLE2426

Rule:
A TLE2426 midpoint is a **signal/reference node**, not a motor/coil power return or energy reservoir.

### Three-phase motor / rotating stator field

Conventional three-phase BLDC six-step commutation uses a three-phase bridge and six sectors per electrical cycle. Standard six-step schemes normally energize two of three phases in each sector.

Reference:
https://onlinedocs.microchip.com/oxy/GUID-3AFF556D-77AD-488F-9A04-CD7AAB8F7DBC-en-US-1/GUID-A1DD3CA4-D59F-45CF-AA9F-EBBCB9EF37BA.html

Rule:
One-phase A→B→C stepping may demonstrate a **stepped field-direction sequence**, but is not automatically equivalent to a conventional balanced three-phase rotating-field drive.

### Circuit simulation

ngspice is the parity reference for circuit-solver behavior. Its transient analysis and integration options include trapezoidal and Gear methods.

References:
https://ngspice.sourceforge.io/docs.html
https://ngspice.sourceforge.io/docs/ngspice-manual.pdf

Rule:
A Virtual Breadboard solver result earns model status only. Cross-check representative circuits against ngspice before claiming SPICE-like parity.

### Jetson Orin Nano Developer Kit

NVIDIA's official hardware layout is the authority for developer-kit ports and power topology. The documented USB-C port is data-only; power is via the DC power jack on the reference developer kit.

Reference:
https://docs.nvidia.com/jetson/orin-nano-devkit/user-guide/hardware_layout.html

Rule:
Do not infer hardware connector capabilities from a different Jetson generation.

### Fluxgate magnetic sensing

Fluxgate sensors are established magnetic sensors using magnetic cores with excitation and sensing windings.

Reference review:
https://www.mdpi.com/1424-8220/21/4/1500

Rule:
A fluxgate is a sensing precedent. It is not evidence that CELL_V1's memory/reinjection architecture works.

### Magnetic nonvolatile memory / spintronics

STT-MRAM is established nonvolatile magnetic memory; SOT-MRAM remains an active development direction.

References:
https://www.nature.com/articles/s44287-024-00111-z
https://www.nature.com/articles/s44306-024-00044-1

Rule:
Reserve **spintronic** for hardware whose state/action actually depends on electron spin / magnetic tunnel junction / spin-torque physics. Hall sensors, coils, encoders, and ordinary magnetic feedback are magnetic/electromechanical feedback, not automatically spintronics.

### Memristive processing-memory

Memristive devices are established research devices for nonvolatile state and in-memory/neuromorphic computation, with significant device-variability and integration challenges.

References:
https://www.nature.com/articles/s41467-024-45670-9
https://www.nature.com/articles/s41578-022-00434-z

Rule:
Memristor literature supports testing a stateful path. It does not prove a One-Wave processing-memory law or muscle-memory mechanism.

### Historical transfluxor precedent

Multi-aperture ferrite transfluxor memories demonstrated remanent magnetic state and nondestructive-readout architectures.

Reference:
https://www.bitsavers.org/pdf/afips/1959-03_%2315.pdf

Rule:
Use as historical magnetic-memory precedent only; do not claim a modern CELL_V1 implementation is a transfluxor unless its geometry and pulse/read/write behavior actually match.

## 4. Software/runtime build rules

A software/runtime build must have:
- exact supported platform/version;
- install/start command;
- smallest smoke test;
- expected output;
- failure mode;
- rollback/restart path;
- no invented access path or credential;
- versioned dependencies or a documented compatibility range.

## 5. Architecture analogy rule

Biology, music, social systems, cosmology, or neural analogy may suggest a test, but cannot substitute for an engineering reference.

Use:
**analogy -> hypothesis -> measurable implementation -> control -> result**

Never:
**analogy -> therefore build is correct**

## 6. Energy accounting

No reinjection/recovery claim may exceed conservation accounting.

Record:
- source energy;
- load/storage change;
- recovered energy;
- reused energy;
- losses and measurement uncertainty.

A virtual ground/reference node is not counted as an energy source.

## 7. Motor and inductive-load rule

Early CELL_V1 logic tests use resistive/dummy loads at low current.

Actual motor/coil power testing moves to a proper half-bridge / three-phase driver or PCB/module with:
- current limiting;
- flyback/freewheel paths;
- dead time where required;
- measured VGS;
- thermal monitoring;
- separate power return from delicate reference nodes.

## 8. Repository enforcement

Current build authorities must cite G-778. Archived builds may remain as history but must not be presented as current instructions without requalification.
