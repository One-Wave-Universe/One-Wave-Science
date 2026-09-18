# Updated 30 - Ground Lattice Orbital-Restoring Simulation

Updated 30 adds the first real runnable Ground-lattice background for the physical simulation ladder.

## Added

- **D-413 Ground Lattice Orbital-Restoring Simulation**
- self-contained browser laboratory;
- reproducible Python batch validator;
- raw CSV receipts and JSON summary;
- comparison graph;
- Ground-fixed, displacement-fixed, and well-fixed camera views;
- actual triangular-lattice displacement and strain rendering;
- derived hexagonal-neighborhood overlay;
- imposed curvature depression;
- off-axis fall, orbital-restoring, and axial-torque tests;
- symmetric-shell, no-well, frozen-lattice, and zero-input controls.

## Locked mechanism tested

The moving feature is a bounded displacement shell, not a particle. Its center responds to the average restoring field. Its orientation responds to the torque produced by unequal restoring forces across the shell:

\[
\tau_Q=\frac1{N_s}\sum_a\mathbf r_a\times\mathbf f_a-c_\omega\omega.
\]

Therefore:

```text
off-center fall across curvature
-> unequal restoring response across the shell
-> translational correction plus torque
-> orbital path and axial spin candidate
```

Spin is calculated from state. It is not a renderer instruction.

## Finite reference results

- zero-input drift: passed below numerical tolerance;
- active pressure produced nonzero lattice strain;
- imposed well changed the displacement path relative to the no-well control;
- asymmetric shell maximum absolute spin: approximately `0.133612`;
- symmetric-shell ablation maximum absolute spin: approximately `7.18e-17`;
- off-axis drop approached the well and crossed away again rather than being falsely labeled a stable orbit.

These results validate the reduced code behavior only.

## What remains open

- the well is imposed rather than derived;
- the displacement shell is a collective coordinate rather than a derived Vortex Phase;
- full action-reaction work accounting remains incomplete;
- stable-orbit regions have not yet been mapped;
- no electrical shell, Mirror Gate, quark, proton, or Mass Effect is claimed;
- the current simulation is native 2D and cannot replace the 3D D-409 layer.
