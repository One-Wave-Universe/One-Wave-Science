---
node_id: "D-413"
canonical_name: "Ground Lattice Orbital-Restoring Simulation"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Ground-Lattice Laboratory / Orbital-Restoring Candidate / State-Driven Visualization"
claim_gate_detail: "YELLOW (reduced coupled simulation; physical derivation open)"
metadata_standard: "I-06"
---

# Node D-413: Ground Lattice Orbital-Restoring Simulation

**Dependencies**  
Upstream: A-101 Ground Zero, A-102 Displacement, A-103 Differential, A-105 Restoring Response, A-109 Inertial Memory, A-117 Dimensional Integrity, C-317 Boundary-Tension Weave, D-408, D-411, D-412  
Lateral: B-202 Pressure, E-502 Flowback, E-503 Pressure, E-506 Stability  
Downstream: bounded excitation, circulation emergence, Vortex Phase, quark, proton knot, electrical shell, Mirror Gate, and Mass Effect simulations

## Purpose

D-413 is the first runnable Ground-lattice background for later physical simulations. It provides a responsive native-2D triangular connection lattice, a derived hexagonal-neighborhood view, an imposed curvature depression rendered directly through the deformed triangular surface, and a bounded displacement region that moves on and responds to that same surface.

The model is deliberately lower than a quark. It asks whether a declared lattice can visibly and measurably:

- remain stationary at zero input without being frozen;
- deform, bunch, resist, and restore;
- carry a bounded displacement region across the Ground;
- display the same physical run in Ground-fixed and displacement-fixed camera frames;
- turn an off-center fall through a curvature well into orbital motion;
- generate axial torque when unequal restoring forces act across an asymmetric bounded shell.

A camera change must never change the state equations:

\[
\boxed{\text{Ground-fixed view}\equiv\text{displacement-fixed scrolling view}}
\]

The equivalence is observational only. The physical state remains one run.

## Native Dimension and Geometry

```text
native dimension: 2D lattice coordinates with a rendered height/depression field
connection geometry: triangular, six directed nearest-neighbor routes
cell/neighborhood view: derived hexagonal rings
axis-pair count: 3 mirrored pairs
centered local count: 6 directed routes + 1 reference
projection: oblique 2D rendering of x,y,z state
omitted: full 3D twelve-neighbor coordination and 4D recurrence shell
```

The lattice is not square and does not use four-neighbor Cartesian propagation.

## Ground State

Each site has rest location

\[
\mathbf X_i^0=(x_i^0,y_i^0,0)
\]

and dynamic state

\[
\mathbf X_i=\mathbf X_i^0+\mathbf u_i,
\qquad
\dot{\mathbf u}_i=\mathbf v_i.
\]

Nearest-neighbor edges supply a provisional elastic work law:

\[
\mathbf F_{ij}
=
\left[k_s(\ell_{ij}-\ell_0)
+c_e\left((\mathbf v_j-\mathbf v_i)\cdot\hat{\mathbf e}_{ij}\right)\right]
\hat{\mathbf e}_{ij}.
\]

Each site also has local return and resistance:

\[
\mathbf F_{i,\mathrm{Ground}}
=-k_0\mathbf u_i-c_0\mathbf v_i.
\]

These are numerical candidate work laws. They do not assert that the physical One-Wave Ground is literally made of mechanical springs.

## Imposed Curvature Depression

The first gravitational-well test uses a declared Gaussian target depression:

\[
z_G(x,y)
=-D\exp\left[-\frac{(x-x_G)^2+(y-y_G)^2}{2\sigma_G^2}\right].
\]

Lattice sites are initialized on this target depression when the well is enabled, then continue evolving under lattice coupling, restoring response, resistance, and well-follow forces. The well is therefore visible from the first frame rather than existing only as an invisible force calculation.

The browser renderer triangulates the actual displaced lattice sites and shades those calculated faces. Curved contour rings sample the same interpolated height field used by the moving bounded region. A Ground-to-bottom depth marker reports the current sampled depression. Vertical exaggeration changes only the projection and never the state equations.

The bounded displacement centroid and its shell samples use the same surface interpolation for displayed height and restoring-gradient calculation:

\[
\boxed{z_{\rm display}(\mathbf q)=z_{\rm force}(\mathbf q)=\mathcal I[\{z_i\}](\mathbf q)}
\]

If the visible depression and the sampled restoring surface disagree, the renderer fails.

The curvature well is **imposed**, not derived. D-413 therefore tests the consequences of a curvature/restoring field but does not claim to derive gravity.

## Bounded Displacement Region

The moving structure is represented as a collective bounded shell, not a particle. Its reduced state is

\[
Q(t)=\left(\mathbf q,\dot{\mathbf q},\theta,\omega\right),
\]

where \(\mathbf q\) is the displacement centroid, \(\theta\) is shell orientation, and \(\omega\) is axial spin.

The shell is sampled at points \(\mathbf r_a\) around an ellipse. Each sample feels the local restoring field:

\[
\mathbf f_a=-g_R\nabla z(\mathbf q+\mathbf r_a).
\]

The translational restoring response is

\[
\mathbf F_Q=\frac{1}{N_s}\sum_a\mathbf f_a-c_Q\dot{\mathbf q}.
\]

The axial torque is

\[
\boxed{
\tau_Q
=
\frac{1}{N_s}\sum_a
\mathbf r_a\times\mathbf f_a
-c_\omega\omega
}
\]

and

\[
I_Q\dot\omega=\tau_Q.
\]

For a perfectly symmetric shell in a symmetric central well, the finite reference ablation produces approximately zero axial torque. With shell asymmetry or off-axis loading, unequal restoring forces can produce nonzero torque.

This is the precise simulation version of:

```text
displacement falls across the depression
-> restoring force is unequal across the shell
-> different shell regions correct by different amounts
-> torque appears
-> orbit and axial spin may emerge
```

Spin is not inserted as an animation command.

## Lattice Coupling

The bounded region deforms the actual lattice through a localized pressure field. The pressure is biased toward the direction of travel so the renderer can measure:

- bunching ahead;
- side strain;
- depression beneath the region;
- release and wake behind.

The lattice reaction is included only as a weak reduced feedback in this first version. A later promotion must derive a complete action-reaction work ledger.

## Camera Modes

The browser laboratory provides:

1. **Ground fixed:** the lattice remains visually fixed while the displacement crosses it;
2. **Displacement fixed:** the displacement stays centered and the lattice scrolls beneath it;
3. **Well fixed:** the curvature center remains fixed.

These are renderer transforms only:

\[
\mathbf X_i^{\mathrm{screen}}
=\mathcal P\left(\mathbf X_i-\mathbf C_{\mathrm{camera}}\right).
\]

Changing camera mode must leave every saved metric unchanged.

## Runnable Artifacts

```text
Nodes/D-413_Ground_Lattice_Orbital_Restoring_Simulation/index.html
Nodes/D-413_Ground_Lattice_Orbital_Restoring_Simulation/simulate_d413.py
Nodes/D-413_Ground_Lattice_Orbital_Restoring_Simulation/results/
```

The browser laboratory includes live controls, camera changes, top-down and curved-surface projections, adjustable view-only vertical exaggeration, shaded triangular curvature faces, sampled depth contours, a visible well-depth marker, lattice-freeze ablation, strain and velocity overlays, orbital trail, metrics, and CSV export.

The batch validator runs five finite cases:

1. off-axis drop;
2. asymmetric orbital shell;
3. symmetric-shell torque ablation;
4. no-well travel control;
5. zero-input drift.

## Current Finite Results

The reference run reports:

- zero-input drift below numerical tolerance;
- nonzero lattice strain when pressure coupling is active;
- a changed path under the well compared with the no-well control;
- nonzero axial spin for the asymmetric shell;
- approximately zero axial spin for the symmetric-shell ablation.

These results validate the declared reduced code path only. They do not validate One-Wave gravity, quark identity, proton structure, electrical-shell emergence, or Mass Effect.

## Required Next Tests

Before promotion, D-413 must add:

- time-step refinement;
- lattice-radius refinement;
- boundary-reflection and periodic-boundary comparisons;
- full work accounting for imposed well, damping, and lattice reaction;
- a field-only displacement with no collective shell coordinate;
- derived circulation and vorticity from the lattice state;
- stable-orbit windows versus capture, escape, and collapse;
- 3D D-409 translation after the 2D mechanism is understood.

## Failure / Revision Conditions

D-413 fails if:

1. camera mode changes the physical trajectory or measurements;
2. spin remains when the shell is symmetric and all torque sources are removed;
3. the zero-input lattice drifts or injects energy;
4. the renderer displays compression, curvature, orbit, or spin not calculated from state;
5. the visible well surface, contour geometry, displacement height, and restoring gradient do not come from the same lattice state;
6. the curvature well is described as derived gravity;
7. the bounded shell is mislabeled as a quark or particle;
8. a visually attractive orbit is promoted without convergence, ablation, and work-ledger tests.
