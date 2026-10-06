# What holds, what spreads: One-Wave recurrence domain and harmonic check

**Outcome: the recurrence equations hold; localization weakens with domain size.**
The same small-amplitude state can be refined to much smaller harmonic defect,
then embedded in a larger Ground region and resolved. Its central activity drops
from 64.55% to 31.07%. The spectrum identifies a near-linear upper-band branch,
not demonstrated holding by a complete boundary mechanism.

Reference: PR #193 at `db26b983afa25dc938162c2ca78c73186271781f`.
Current main comparison `d89ebdca606b26089267b7ff5903eb5c940cf3dc`;
AGENTS, General Reference Rules, canonical start and Reality Database specification
are unchanged from `b897fa2cb50d5be39100b4265bf95dbf97a2ec15`.
Scientific execution is in the isolated workspace, not a Jetson simulation run.

## Adjustment and reproducible contract

The [previous direct solve](PERIODIC_ORBIT_SOLVE.md) provides the A=.2 state.
The native [constitutive law](native_compression_bridge.py) and coefficients
beta=shear=k=a_c=1, eta=2 stay fixed. The full retained state remains real
excitation psi, vector displacement u, their velocities and chi=-div(u).
This is native 3D FCC twelve-neighbor geometry. It does not substitute 2D sixfold
coordination or turn the 24-state Field/Void shell into 24 spatial neighbors.

- Increase psi harmonics from {1,3} to {1,3,5}, and displacement harmonics from
  {0,2,4} to {0,2,4,6}; use 64 temporal quadrature points.
- Resolve the original 32-site box with the .2 center anchor and zero-mean DC
  displacement gauge. The anchor is only a solve condition, not a physical force.
- Embed its centered coefficients into Ground on 108 sites (side 6), subtract
  the uniform DC displacement gauge, and resolve with the same conditions.
- Keep radius-1 localization fixed; also report radius 2 for comparison.
- Check full, unprojected force defect, exact extended recurrence, analytic
  Jacobian, and ten-cycle direct evolution. Halve the larger-box timestep.

The domain lift is discrete and can select another branch: it does not prove
continuous branch identity. Before re-solving, the embedded larger state has
full relative equation defect .23968. Re-solving changes its shape rather than
pretending the old periodic box was already an isolated physical boundary.
Periodic numerical boundaries are not Knot Lock, a bounded-void surface law,
Mirror coupling or Boundary-Tension Weave. No boundary penetration is forced.

```sh
OPENBLAS_NUM_THREADS=1 python solvers/recurrence_domain_check.py > solvers/recurrence_domain_results.json
```

[Executable](recurrence_domain_check.py) · [Raw measurements and coefficients](recurrence_domain_results.json).
NumPy/SciPy required. Requires the previous solver and its committed results.
Successful exit means implementation controls passed, not physical closure.

## Observed refinement and domain response

| State | Sites | Full equation defect | Activity inside radius 1 | Activity inside radius 2 | Effective active sites | RMS activity radius |
|---|---:|---:|---:|---:|---:|---:|
| Previous harmonics, side 4 | 32 | 5.36e-8 | 64.55% | 98.55% | 8.618 | 1.101 |
| Increased harmonics, side 4 | 32 | 8.74e-12 | 64.55% | 98.55% | 8.618 | 1.101 |
| Increased harmonics, side 6 | 108 | 5.74e-12 | 31.07% | 75.05% | 23.757 | 1.660 |

The higher harmonics correct the equation truncation; they do not restore
localization. The larger state still misses the .8 radius-1 screen. Even the
radius-2 diagnostic drops below .8 after the domain lift. Activity is the temporal
mean of psi²+v_psi², not conserved energy or a physical particle count.
Effective active sites is (sum activity)²/sum(activity²).

Both exact extended controls have equation defect below 2.6e-16. Directional
Jacobian errors are 1.49e-12 and 2.61e-12. Direct integration uses matrices assembled
from the original native operators; its initial forces and energy are asserted
against those operators before every evolution. The update law is unchanged.

| Side-6 direct evolution | Max scaled energy error | Full-state return error after ten fitted periods |
|---|---:|---:|
| 400 steps per period | 5.28263e-5 | .00182696 |
| 800 steps per period | 1.32066e-5 | .000456742 |

Both complete ten periods. Halving dt improves both errors by approximately four.
There is no resetting, recentering, phase fitting or repeated displacement
relaxation during evolution. Ten cycles do not prove perturbation stability.

## Why this branch repeats but does not hold tightly

At Ground, the scalar lattice symbol is

    ell(K)=6-2(xy+xz+yz),  x=cos(Kx), y=cos(Ky), z=cos(Kz).

The identity

    1+xy+xz+yz = [(1+x)(1+y)(1+z)+(1-x)(1-y)(1-z)]/2 >= 0

gives ell<=8. Equality requires one cosine to be +1 and another to be -1;
the remaining wavevector component is free. These are reciprocal-space lines,
not an isolated maximum. On an even side-s grid, 6s-6 full-grid wavevectors have
ell=8. The even-parity FCC representation identifies K and K+(pi,pi,pi), giving
upper-eigenspace dimension **3s-3**. Each line gives spatial patterns that can vary
along one axis while extending across the other two. Superpositions can focus
activity near the center while retaining broad tails.

The measured fundamental fractions in this eigenspace are 99.99869% (side 4)
and 99.99043% (side 6). Their overlaps with the upper-eigenspace projection of a
center-site disturbance are .99358 and .98905. This is direct numerical evidence
that the solved states are near upper-band focusing patterns. It does not identify
these disturbances as Propagating Light Modes or Vortex Phases.

A sharper localization check uses the projector P_top. For any vector in its
range, the largest possible fraction inside a fixed region R is

    lambda_max( R P_top R^T ).

The executable constructs this restricted matrix from the FFT projection kernel
and evaluates its eigenvalues. The following are numerical evaluations of that
operator bound, not an assertion that every nonlinear state lies in this space.

| Side | Sites | Upper-eigenspace dimension | Maximum radius-1 fraction in that space | Radius-1 fraction of projected center disturbance |
|---|---:|---:|---:|---:|
| 4 | 32 | 9 | .750000 | .656250 |
| 6 | 108 | 15 | .407407 | .324074 |
| 8 | 256 | 21 | .250000 | .191406 |
| 10 | 500 | 27 | .168000 | .126000 |
| 12 | 864 | 33 | .120370 | .089120 |

The 8/10/12 rows are **linear spectral audits**, not larger nonlinear recurrence
solves. All audit projections satisfy the eigenvector equation to floating-point
precision and vanish on the inactive parity sublattice. The maximum single-site
fraction is exactly (3s-3)/(s³/2), which shrinks with domain size.

If epsilon of the total mean activity lies outside the upper eigenspace, a
conservative radius-1 bound is

    [sqrt(b)*sqrt(1-epsilon)+sqrt(epsilon)]²,

capped at 1, where b is the restricted-projector eigenvalue. This follows from
the triangle inequality on the weighted Fourier coefficient vectors. Actual
epsilon and the resulting near-band bounds are retained in the raw measurements.
They rule out the .8 central-activity gate for these measured near-band states;
they do not rule out other nonlinear branches or the full One-Wave architecture.

## Compression shifts this small-amplitude branch into the Ground band

The observed omega values, 2.82703446 and 2.82707673, are just below sqrt(8).
This direction can be explained without changing coefficients. Let f lie in the
upper scalar eigenspace and write psi=A f cos(omega t)+O(A³). Set C=-div,
D=C^T(f²), and M=blockdiag(L,L,L)+C^T C on zero-mean displacement. To order A²,
the density drive has DC and twice-frequency components:

    u_DC/A² = (eta/2) M^-1 D,
    u_2/A²  = (eta/2) (M-32 I)^-1 D.

Projecting the excitation equation onto its fundamental gives the necessary
leading frequency shift

    delta(omega²)/A² = -eta² D^T [M^-1 + .5(M-32 I)^-1] D / (f^T f).

The inverse at zero eigenvalues is understood on the zero-mean subspace; D has
no uniform component. This is a perturbative solvability relation, not a full
nonlinear existence theorem in a degenerate eigenspace. The retained a_c rho
stiffness enters at higher order here.

The earlier Ground analysis gives M eigenvalues <=14. For every nonzero
lambda<=14, 1/lambda-.5/(32-lambda)>0. Therefore the leading shift is negative
when D is nonzero. If D=0, the single upper eigenvector with u=0 has no compression
drive and remains an exact extended linear recurrence. Increasing small-amplitude
compression in this branch does not lift its fundamental above the Ground band.

Using the measured fundamentals projected into the upper eigenspace and normalized
to unit central amplitude gives:

| Side | Leading delta(omega²)/A² | Predicted omega at A=.2 | Solved omega |
|---|---:|---:|---:|
| 4 | -.19758195 | 2.82702966 | 2.82703446 |
| 6 | -.19053146 | 2.82707954 | 2.82707673 |

The approximate agreement is evidence for this perturbative explanation; it
is not a calibration or an independent prediction of physical Mass Effect.
The fundamental remains inside a Ground propagation band. Periodic-box repetition
alone does not demonstrate cancellation of outgoing channels.


## A second missing closure: compression does not generate rotation here

The owner check reads [C-317 Boundary-Tension Weave](../Nodes/C-317_Boundary_Tension_Weave.md),
[C-319 Magnetic Lattice Reorganization](../Nodes/C-319_Magnetic_Lattice_Reorganization.md),
[C-320 Magnetic-Compression Path Coupling](../Nodes/C-320_Magnetic_Compression_Path_Coupling.md)
and [D-412 state-driven simulation](../Nodes/D-412_Lattice_Simulation_and_State_Driven_Visualization_Standard.md).
The mechanisms remain part of the intended architecture; this reduced law lacks
their coupled dynamical closure.

| Owner | Declared mechanism | What the current recurrence law still lacks |
|---|---|---|
| C-317 | Closed volumetric boundary, surface energy, phase locking and twist energy | Evolving boundary geometry, separate Vortex Phase components and their reciprocal force terms; coefficients remain unknown |
| C-319 | Symmetric reorganization R, positive path accessibility K_L=I+kappa_R R and rotational history | An evolved R state, its work ledger and coupling back into rotation/compression |
| C-320 | Path-weighted restoring response -alpha_g K_L grad(chi), recovering isotropic A-115 | Reciprocal integration with the retained displacement energy and reorganization state |
| D-412 | Displacement, velocity, phase, compression, rotation and boundary/weave state | The present real scalar excitation and u are only a reduced subset; a scalar angular seed is not vortex evidence |

There is an exact obstruction in the baseline equation:

    ddot(u) = -L u - grad[(1+psi²)chi - 2psi²].

On this periodic graph, the central gradient components commute, curl(grad f)=0,
and curl commutes with L. Thus

    ddot(curl u) = -L(curl u).

Starting with curl u=0 and curl v_u=0 cannot create displacement/velocity
circulation through this compression coupling. Rotation can be seeded and then
propagates freely in this model; there is no nonlinear compression-to-curl source.
The solved displacement harmonic curls are below 2.2e-19. Random-state checks of
curl(force_u)=L curl(u) agree below 6.3e-15. This explains precisely why the scalar
angular seed and the existing compression recurrence do not test C-319's full
magnetic reorganization mechanism. It does not refute that mechanism.

C-320's K_L is a proposed response law, not permission to multiply the current
unit-kinetic force by an arbitrary tensor and keep its old energy ledger. For the
positive constant example K_L=diag(1.2,.9,.9), corresponding to traceless
R=diag(.2,-.1,-.1) when kappa_R=1, the naive linear compression derivative becomes

    K_L C^T C.

Its transpose is C^T C K_L, generally different. The executable records a nonzero
Jacobian asymmetry for this example. That naive substitution is not a reciprocal
potential force in the current unit kinetic coordinates. A constant K could be
represented with a different kinetic metric; an evolving R would then need its
own energy, reciprocal coupling and appropriate metric terms. Those are new
constitutive choices, not measured Mass Effect and not yet derived here.

The smallest useful next construction must therefore define a common work/energy
law for boundary, rotation and path reorganization before solving for persistence.
A direct -K_L grad(chi) insertion, an imposed reflecting wall or an extra label
would each leave the missing closure unresolved.

## Field/Void receipt and adjusted next action

Main goal: derive a self-held One-Wave recurrence and eventually its carrying/time
response. Choice: one bounded harmonic and domain check on the smallest solved
branch, plus spectral and perturbative explanation of the observed outcome.
Allowed: new executable, raw report, this explanation, laboratory pointer and
an additive C-319 implementation-gap receipt; no node metadata or gate change.
Protected: native law, previous data, node gates, timing interpretation, hardware,
complete architecture and dirty Jetson checkout.

Field proposed harmonic refinement and a larger Ground region. Void required
unprojected equation defect, unchanged spatial operators, fixed localization
radii, gauge control, direct evolution and spectral discrimination. Same assistant
performed both: this is not independent-model corroboration. The first run
completed both solves; the final run repeats them with spectral, frequency-shift
and rotation/reciprocity receipts. No physical coefficient was tuned.

State: equation refinement and finite-domain check RESOLVED; persistent localization
PARTIAL/failed for this branch. Scale: retain near-periodic branches as numerical
results; do not promote to Persistent Modes, Knot Lock, Mass Effect, clocks or
physical nonexistence. The full knot, shell, Mirror and Boundary-Tension Weave
architecture is retained as the required next mechanism closure.

Adjusted next action: stop treating this weak upper-band branch as a held mode.
Reference the owner equations for the missing boundary/rotation coupling and
identify the smallest reciprocal operator that can supply confinement or a
nonradiating structure under reflection, deflection, tangential redistribution
and Mirror phase coupling. Derive its energy/force pair and check dimensional
geometry before inserting it into this recurrence solver. A new assumed potential
must not be dressed as the complete Boundary-Tension Weave. A separately located
strong nonlinear branch of the existing law remains possible, but is not supplied
by this weak-amplitude continuation or by simply adding harmonics.
