---
node_id: "G-779"
canonical_name: "Active Build Validation Matrix"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Engineering Build Status / Evidence Matrix"
claim_gate_detail: "YELLOW: canonical project structure or validation contract; empirical/domain-specific claims remain subject to stated tests and evidence boundaries."
metadata_standard: "I-06"
---

# G-779 — Active Build Validation Matrix

This matrix applies G-778 to the major active builds.

| Build family | Real reference / precedent | Current repo evidence | Current status | Smallest next proof |
|---|---|---|---|---|
| CELL_V1 midpoint/reference | TI TLE2426 rail splitter | bench documents + staged tests | BENCH-REALITY DESIGN, not physical pass | 5 V current-limited midpoint stiffness receipt |
| CELL_V1 stateful path | memristive devices, magnetic memory, MRAM are real separate precedents | design packet only unless a retained bench receipt exists | ONE-WAVE HYPOTHESIS | one A-axis stateful path with control, retention, rewrite, decay |
| CELL_V1 reinjection | regenerative inductive/DC-link energy recovery is established engineering | measurement plan exists | ONE-WAVE HYPOTHESIS for cell integration | energy-in / recovered / reused / loss ledger |
| three-phase motor/rotation | conventional three-phase bridge and six-step BLDC commutation | simulator/test notes; custom One-Wave mapping experimental | REFERENCE-REAL baseline + HYPOTHESIS mapping | compare measured custom field trajectory with conventional six-step case |
| Virtual Breadboard electrical solver | ngspice / SPICE analysis conventions | analytic regressions + ngspice cross-check suite documented | MODEL PASS for covered cases | keep coverage explicit; do not claim unsupported BSIM/Gummel-Poon parity |
| Virtual Breadboard magnetic/memory primitives | ordinary electromagnetics and component models | custom models | MODEL/HYPOTHESIS | cross-check each model against measured component or published transfer curve |
| Jetson Orin Nano runtime | NVIDIA Orin Nano developer-kit docs + Ubuntu/JetPack ecosystem | repo install/runtime/terminal tests | SOFTWARE BUILD, hardware assumptions must match actual carrier | run documented smoke test on exact Jetson and retain output |
| Hive Pipe / AI terminal bridge | HTTPS/MCP + systemd/user-space process controls | executable gateway, tokens, workflows, smoke-test instructions | SOFTWARE BUILD | authenticated terminal_pwd + harmless terminal_run + audit receipt |
| Proposed Android Brain | Hopfield associative memory; Boltzmann machine learning are real computational precedents | architecture proposal + software modules | PROPOSED / HYPOTHESIS | implement one closed sensor→candidate→evaluate→commit→feedback loop and compare flat controller |
| Learner App | parser/state-machine software patterns | deterministic generator/parser/verifier tests in repo | SOFTWARE MODEL PASS for documented phases | run full unit suite on current branch and retain CI receipt |
| One-Wave Animator | PySide6/Qt scene editor is real software framework | import/drag/resize/layer/save/reopen tests | SCENE EDITOR BUILD, not yet full frame animator | frame-by-frame timeline/playback/export acceptance path |
| Rabbit-Hop translators | exact integer arithmetic / reversible receipts | shared core + adapters/tests | SOFTWARE MODEL PASS | keep semantic domain mapping separate from numeric address equality |

## Reference links

### TLE2426
https://www.ti.com/product/TLE2426

### BLDC six-step commutation
https://onlinedocs.microchip.com/oxy/GUID-3AFF556D-77AD-488F-9A04-CD7AAB8F7DBC-en-US-1/GUID-A1DD3CA4-D59F-45CF-AA9F-EBBCB9EF37BA.html

### ngspice
https://ngspice.sourceforge.io/docs.html
https://ngspice.sourceforge.io/docs/ngspice-manual.pdf

### Jetson Orin Nano Developer Kit
https://docs.nvidia.com/jetson/orin-nano-devkit/user-guide/hardware_layout.html

### Hopfield associative memory
https://authors.library.caltech.edu/records/w41x7-8bn13
DOI: 10.1073/pnas.79.8.2554

### Boltzmann machines
https://onlinelibrary.wiley.com/doi/10.1207/s15516709cog0901_7

### Memristive computing
https://www.nature.com/articles/s41467-024-45670-9

### STT-MRAM
https://www.nature.com/articles/s44287-024-00111-z

## Interpretation rule

The presence of a real reference mechanism validates only the borrowed mechanism.

Example:
- real: TLE2426 generates a midpoint;
- not established: a CELL_V1 midpoint causes ternary cognition.

Example:
- real: Hopfield networks provide content-addressable associative memory;
- not established: the proposed Android architecture is biologically equivalent to a brain.

Every row advances only when its own acceptance receipt exists.
