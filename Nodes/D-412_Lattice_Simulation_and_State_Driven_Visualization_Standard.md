---
node_id: "D-412"
canonical_name: "Lattice Simulation and State-Driven Visualization Standard"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Simulation Governance / Wiki Laboratory Standard / Dimensional Visualization"
claim_gate_detail: "BRONZE (simulation standard) / YELLOW (physical implementations pending)"
metadata_standard: "I-06"
---

# Node D-412: Lattice Simulation and State-Driven Visualization Standard

**Dependencies**  
Upstream: A-102 Displacement, A-103 Differential, A-105 Restoring Response, A-117 Dimensional Integrity, C-317 Boundary-Tension Weave, D-408, D-409, D-410, D-411  
Lateral: I-02 proof lifecycle, G-706 Validation  
Downstream: D-413 Ground-lattice orbital-restoring lab, circulation-emergence, Vortex-Phase, Three-Vortex-Knot, electrical-shell, Mirror-Gate, and Mass-Effect simulations

## Purpose

A moving picture is not automatically a simulation. A valid One-Wave simulation must evolve declared state variables under a reproducible update law, calculate measurements from those states, expose failure conditions, and render only quantities actually present in the run.

\[
\boxed{\text{simulation state}\rightarrow\text{measured fields}\rightarrow\text{visualization}}
\]

The prohibited reversal is

\[
\boxed{\text{desired picture}\rightarrow\text{animation pretending to be evidence}}.
\]

## Native Geometry

- native 2D tests use the D-408 triangular connection lattice and hexagonal cell/neighborhood view;
- native 3D physical tests use the D-409 volumetric twelve-neighbor candidate;
- D-410 supplies recurrence/state-history requirements and is not silently rendered as ordinary 3D space;
- every view declares whether it is native, sliced, projected, or derived.

## Stationary Ground

Stationary means zero net motion at equilibrium, not frozen nodes:

\[
\mathbf u_i=0,\qquad \mathbf v_i=0,\qquad \Delta X_i=0.
\]

Every site must remain capable of displacement, transfer, restoring response, and return.

## Minimum State Interface

A physical lattice run should declare at least:

\[
X_i(t)=\left(\mathbf u_i,\mathbf v_i,\phi_i,\chi_i,\mathbf q_i,B_i\right),
\]

where candidate meanings are:

- displacement `u`;
- local motion `v`;
- recurrence phase `phi`;
- compression state `chi`;
- circulation/rotation state `q`;
- boundary/weave state `B`.

The exact update law remains a separate derivation. The interface does not prove the physics.

## Required State-Driven Views

A serious wiki laboratory page should be able to display synchronized views of one run:

1. **deformed lattice:** actual displaced site positions and connections;
2. **triangle-edge view:** relative strain, shear, and transfer along edges;
3. **hexagonal-cell view:** area change, pressure, circulation, leakage, and center drift;
4. **velocity/vector view:** local flow and directional reconstruction;
5. **vorticity view:** circulation calculated from the velocity field;
6. **resistance/restoring view:** calculated local pushback, not generic damping color;
7. **Boundary-Tension Weave view:** strain and confinement derived from the boundary model;
8. **internal/external electrical view:** shown only if the update produces a derived differential shell response;
9. **Mirror-Gate view:** hold, approach, crossing, and return conditions calculated from the declared gate variable;
10. **graph panel:** live measurements from the same arrays.

Flower-of-Life and Metatron-style overlays may visualize overlap radius or declared connection maps. They may not add couplings absent from the update law.

## Required Measurements

At minimum, record:

- total numerical energy/work balance;
- maximum and RMS displacement;
- compression ahead and release behind a moving recurrence;
- edge strain and cell-area change;
- circulation and vorticity concentration;
- boundary leakage;
- recurrence error;
- recovery time after perturbation;
- center drift and residual wake;
- applied work, velocity-dependent drag, and acceleration-dependent response;
- parameter values, grid spacing, time step, seed, and code version.

## Required Failure Tests

Every model must be capable of failing. Required tests include:

1. zero-input drift;
2. time-step and spatial-refinement convergence;
3. energy injection from numerical error;
4. perturbation recovery versus collapse;
5. parameter sweeps that produce stable and unstable regions;
6. interaction ablations;
7. dimensional projection-loss measurement;
8. comparison against periodic, random, or simpler control models where relevant.

## Physical Simulation Ladder

The canonical dependency order is

```text
stationary responsive Ground
-> displacement and recovery
-> compression / shear / rotational input
-> bounded excitation
-> circulation emergence
-> persistent confined Vortex Phase candidate
-> three-phase coupling
-> Three-Vortex Knot / proton candidate
-> electrical-shell and Mirror-Gate response
-> controlled translation
-> four-interaction Mass-Effect measurement
```

The Mass Effect is measured after a complete stable recurrence exists. It is not inserted as an initial parameter.


## First Runnable Implementation

D-413 is the first implementation governed by this standard. It supplies a triangular Ground background, synchronized Ground-fixed and displacement-fixed cameras, an imposed curvature depression, off-axis restoring/orbital tests, torque-based axial spin, a symmetric-shell ablation, a no-well control, zero-input drift checks, CSV receipts, and batch graphs.

D-413 remains Yellow because the well is imposed and the bounded displacement shell is a reduced collective coordinate.

## Wiki Laboratory Requirement

A Silver-candidate physical wiki page requires:

- runnable code or an exact executable reference;
- declared native dimension and projection;
- parameter table;
- raw machine-readable results;
- graphs;
- stable and failed examples;
- interpretation separated from output;
- explicit falsifiers.

An illustration or artistic reconstruction is welcome only when labeled as art and grounded in a specific simulation receipt.

## Failure / Revision Conditions

This standard fails if it permits an animation to be promoted without state equations, raw results, failure cases, or reproducibility; or if it forces a renderer to display a theoretical feature that the underlying update never calculated.
