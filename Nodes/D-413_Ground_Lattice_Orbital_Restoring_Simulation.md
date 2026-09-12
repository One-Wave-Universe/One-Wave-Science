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
Upstream: A-101 Ground Zero, A-102 Displacement, A-103 Differential, A-105 Restoring Response, A-109 Inertial Memory, A-115 Unified Compression Field, A-117 Dimensional Integrity, C-319 Magnetic Lattice Reorganization, C-320 Magnetic-Compression Path Coupling, C-317 Boundary-Tension Weave, D-408, D-411, D-412  
Lateral: B-202 Pressure, C-306 Torque, C-307 Angular Momentum, D-409 Twelvefold 3D Close-Packed Coordination, E-502 Flowback, E-503 Pressure, E-506 Stability  
Downstream: D-416 Planetary Rotation-Magnetic Coupling Test Matrix, bounded excitation, circulation emergence, Vortex Phase, quark, proton knot, electrical shell, Mirror Gate, and Mass Effect simulations

## Canonical Node Graph Linkage

D-413 is the runnable gravity/compression laboratory attached to [A-115 Unified Compression Field](A-115_Unified_Compression_Field.md). It is also listed in the repository-level [`00_MASTER_INDEX.md`](../00_MASTER_INDEX.md), so the lab is part of the canonical node graph rather than a standalone demo.

The gravity-only baseline path is:

```text
A-101 Ground / Zero
-> A-102 Displacement
-> A-104 Gradient / A-105 Restoring Response
-> A-115 Unified Compression Field
-> D-413 Ground Lattice Orbital-Restoring Simulation
```

The canonical magnetic extension is:

```text
C-311 Electric-Magnetic Duality
-> C-319 Magnetic Lattice Reorganization
-> C-320 Magnetic-Compression Path Coupling
-> D-413 ON/OFF laboratory controls
-> D-416 planetary falsification matrix
```

The runnable files live in [`D-413_Ground_Lattice_Orbital_Restoring_Simulation/`](D-413_Ground_Lattice_Orbital_Restoring_Simulation/). Results from the lab must be interpreted through this node and A-115; they must not silently promote the imposed curvature well into a derived gravity law.

**Current implementation boundary:** the existing D-413 runnable lab does not yet implement C-319/C-320. Those nodes are upstream requirements for the next magnetic/gravity experiment, not a claim that the current code already tests magnetic coupling.

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

D-408 owns this planar geometry. D-409 remains mandatory before a planetary physical claim, including any D-416 result.

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

The curvature well is **imposed**, not derived. D-413 therefore tests the consequences of a curvature/restoring field but does not claim to derive gravity. The direct A-115 integration target is to replace this imposed Gaussian with a source-derived compression field \(\chi(\mathbf x,t)\) and its baseline gravity view \(\mathbf g_0=-\alpha_g\nabla\chi\).

## Magnetic-Lattice Coupling Target

After the A-115 baseline is source-derived and reproduces the gravity-only controls, D-413 must add C-319/C-320 as a separately switchable experiment.

C-319 supplies

\[
\mathbf K_L=\mathbf I+\kappa_R\mathbf R,
\]

and C-320 proposes

\[
\mathbf g_{\rm OW}=-\alpha_g\mathbf K_L\nabla\chi.
\]

The required order is:

```text
SOURCE-DERIVED BASELINE:
chi -> grad(chi) -> g0 -> trajectory/torque

MAGNETIC EXTENSION:
B/rotation -> R -> K_L
                  +
               grad(chi)
                  -> g_OW -> trajectory/torque
```

The magnetic channel must have an explicit OFF state with `R=0`, `K_L=I`, and exact recovery of the baseline within numerical tolerance. It may not be used to repair a baseline gravity run that already fails its own controls.

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

C-306 and C-307 remain the authority for torque/angular accounting whether the restoring field comes from the baseline or the later C-320 extension.

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

These results validate the declared reduced code path only. They do not validate One-Wave gravity, C-319 magnetic reorganization, C-320 magnetic/gravity coupling, planetary locking, quark identity, proton structure, electrical-shell emergence, or Mass Effect.

## Required Next Tests

Before promotion, D-413 must add in this order:

1. replace the imposed Gaussian well with an A-115 source-derived \(\chi\) field and test \(\mathbf g_0=-\alpha_g\nabla\chi\);
2. prove the source-derived baseline reproduces or explains the existing gravity-only controls before adding magnetism;
3. implement C-319 `R` and `K_L` with ON/OFF/reversal/rotation controls;
4. implement C-320 `g_OW=-alpha_g K_L grad(chi)` and verify `K_L=I` reproduces the baseline;
5. record trajectory, torque, capture, orbit, work, and drift differences with C-319/C-320 ON versus OFF;
6. time-step refinement;
7. lattice-radius refinement;
8. boundary-reflection and periodic-boundary comparisons;
9. full work accounting for imposed/source field, damping, lattice reaction, and magnetic reorganization;
10. a field-only displacement with no collective shell coordinate;
11. derived circulation and vorticity from the lattice state;
12. stable-orbit windows versus capture, escape, and collapse;
13. 3D D-409 translation;
14. only after 3D translation, hand results to D-416 for planetary tests.

## Failure / Revision Conditions

D-413 fails if:

1. camera mode changes the physical trajectory or measurements;
2. spin remains when the shell is symmetric and all torque sources are removed;
3. the zero-input lattice drifts or injects energy;
4. the renderer displays compression, curvature, orbit, spin, or magnetic reorganization not calculated from state;
5. the visible well surface, contour geometry, displacement height, and restoring gradient do not come from the same lattice state;
6. the curvature well is described as derived gravity;
7. the bounded shell is mislabeled as a quark or particle;
8. a visually attractive orbit is promoted without convergence, ablation, and work-ledger tests;
9. C-319/C-320 are claimed as tested before their state variables exist in the runnable code;
10. enabling the magnetic extension changes the supposedly identical baseline even when `R=0` and `K_L=I`.
