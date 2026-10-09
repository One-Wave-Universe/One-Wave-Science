---
node_id: "C-301-X"
canonical_name: "Two-Sided Cross-Coupled Star Reference"
namespace: "NODE"
gate: "BROWN"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Applied Mechanics and Boundary Structure"
claim_gate_detail: "Proposed two-face Field/Void cross-routing and shared star reference; physical switching, energy paths, stability and magnetic coupling unverified"
metadata_standard: "I-06"
---

# C-301-X — Two-Sided Cross-Coupled Star Reference

## Authority and scope
Research extension of [C-301 Mirror Gate](C-301_Mirror_Gate.md), **not** a replacement or a proven physical circuit. Respect `GENERAL_REFERENCE_RULES.md`, `AI_CANONICAL_START_HERE.md` and the current CELL_V1 geometry authority. Do not promote this hypothesis without tests.

## Proposed structure
- One hex cell, two opposed physical faces (A/B); **each face carries Field and Void**, with views/state travelling up and actions/conditioning travelling down.
- Three physical bidirectional mirror axes: A+ ↔ A−, B+ ↔ B−, C+ ↔ C−. Six directed edge interfaces, **not** six distinct mirror gates. Flat edges only; canonical clockwise order A+, B+, C+, A−, B−, C−.
- Preserve C-301's logical cycle: Mirror1 → Action1 → Mirror2 → Action2 → Mirror3 → Action3 → loop. Do not confuse the physical A/B/C axes with additional logical gates.
- Two opposing star faces route sensor-cell relationships toward the central motor cell. All ternary comparisons must specify the **same measurable virtual-ground reference**; a star reference is not by itself a power-current return conductor.
- Cross-coupled information routes are allowed in both directions: Face A ↑ → Face B ↓, Face B ↑ → Face A ↓, as well as A ↑ → A ↓ and B ↑ → B ↓. Both Field and Void participate in each direction; the crossed routes are **logical candidate paths**, not demonstrated conductive circuits.
- Machine candidate: two round outer magnetic structures, six windings each, opposite intended polarities, surrounding a distinct central transfluxor nucleus. A possible work/drive face and recovery/energy-management face are function labels, **not** proof of Maxwell-gradient formation or energy recovery. The transfluxor aperture geometry and winding mapping remain open.
- Biological analogy is separate: work/metabolism/feedback may have similar organizational roles, but ATP chemistry, membranes, and cellular energy handling are not literal winding or inductive-reinjection circuits.
- The Jetson remains an optional, on-demand external scientific metadata/evidence source, not part of the cell's intrinsic state mechanism.

## Candidate signal graph
```text
sensor cells -> Face A Field/Void ↑ --\
                                     shared star reference -> central state
sensor cells -> Face B Field/Void ↑ --/
central state -> three mirrored bidirectional axes -> A Field/Void ↓
                                                \--> B Field/Void ↓
candidate cross routing: A↑ -> B↓ ; B↑ -> A↓
```

## Required evidence gates
1. Draw an explicit two-face electrical schematic with reference, supply, winding currents, switch body diodes, and closed return paths. No implicit current through virtual ground.
2. Specify physical gate topology and polarities; test both crossed routes and local routes independently.
3. Measure whether a shared reference remains stable under simultaneous sensing, drive and reinjection.
4. Model coupled magnetic flux with appropriate B-H/hysteresis curves, geometry, winding direction, and leakage; compare with independent prior art.
5. Test energy balance (input, delivered work, recovered energy, losses) and feedback stability. Reinjection is never assumed gain.
6. Keep established measurements, proposed mechanisms, and unverified One-Wave mappings separately labelled.
7. Preserve no-clock/no-forced-internal-time requirement for the proposed cell; external instrumentation may timestamp measurements.

## Open questions
- One electrical central reference node or two physically separated star nodes tied to one reference potential?
- Exact physical cross-routing and MOSFET gate drive?
- Central nucleus: two-aperture, three-aperture or other magnetic geometry?
- Which winding positions and current directions generate the intended gradient, if any?
- How do both faces share retained magnetic state without unintended feedback?

## Reference relationships
- Parent: [C-301 Mirror Gate](C-301_Mirror_Gate.md)
- Canonical geometry: `AI_CANONICAL_START_HERE.md` CELL_V1 gate and its named authority chain.
- Governance: `Governance_I_Series/I-06_Canonical_Node_Metadata_and_Alias_Resolution.md`
- Status: **BROWN / ACTIVE_HYPOTHESIS**, awaiting design and experimental validation.
