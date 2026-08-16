# One Wave Translation of Newtonian and Einsteinian Dynamics

## Status

- Brick sequence: Gray → 2D Yellow → 3D Yellow → audit.
- Newtonian mechanics and general relativity remain the anti-drift controls.
- One Wave changes the physical description and adds unresolved degrees of
  freedom; it does not alter established equations merely by renaming symbols.
- Any additional One Wave term must produce a separate receipt and must not
  double-count gravity already present in the Gray channels.

## Gray Brick — established definitions

### Newtonian field limit

For mass-energy density `rho`, define a gravitational potential `Phi`:

```text
Laplacian(Phi) = 4 pi G rho
a_N = -gradient(Phi)
```

For separated compact bodies this reduces to the familiar N-body interaction:

```text
a_i = G sum[j != i] m_j (r_j - r_i) / |r_j - r_i|^3
```

The field equation is the preferred One Wave translation. The point-body sum is
the numerical compact-source approximation, not the ontology.

### Einstein field equation

```text
G_mu_nu + Lambda g_mu_nu = (8 pi G / c^4) T_mu_nu
```

`T_mu_nu` carries energy density, momentum density, pressure, stress, and
energy flux. `g_mu_nu` is the spacetime metric and `G_mu_nu` its curvature
response. Free trajectories follow the metric geodesic equation.

The present solar control uses only the leading solar first-post-Newtonian
correction. It is not yet a full numerical-relativity solver.

## 2D One Wave interpretation

### One continuous measured surface

Let `Psi(x,y,t)` be the reduced One Wave Field and let `e[Psi]` be its measured
energy density. Extended excitation `A` is read through a normalized window
`W_A`, rather than declared as a mathematical point:

```text
E_A = integral W_A e[Psi] dA
q_A = integral x W_A e[Psi] dA / E_A
```

In the long-range, slowly changing limit, the measured energy distribution
supplies the Newtonian source:

```text
rho_2D = P_2D[e[Psi] / c^2]
Laplacian_2D(Phi) = projected source rule
```

The exact projection rule must be declared. A literal 2D Poisson law has a
different Green function from 3D gravity and cannot be silently substituted.

### Point–Path–Field description

- Point: the measured excitation center and its internal rotation receipt.
- Path: the relational history `q_A(t)` and transported wake.
- Field: the surrounding `Psi`, potential/metric response, stress, and flux.

These are three measurements of one state, not three independent fields.

### Four operators

- Differential `-`: contrast or gradient that localizes a response.
- Signal `+`: carried change accumulated along a path.
- Across `/`: transfer through or across a boundary.
- Amplification `×`: gain from resonance or repeated coherent transfer.

The operators describe transformations. They are not extra fundamental forces.

## 3D One Wave interpretation

### Standard geometry retained

The 3D/4D control remains Einstein's equation. One Wave interprets
`T_mu_nu` as the complete local measurement of one continuous Field:

```text
T_mu_nu[Psi] = energy + momentum + pressure + shear + flux
```

The metric response is then

```text
Geometry[T[Psi]] -> g_mu_nu
```

In the weak-field, low-speed limit, the metric response must reduce to the
Newtonian potential. That correspondence is a non-negotiable anti-drift gate.

### Extended excitations instead of point ontology

Planets, stars, atoms, protons, and other persistent structures are extended
regions of the measured Field. Compact centers may still be used for efficient
solar-system integration when their radius and internal dynamics are below the
required accuracy. Their positions are measurements of the Field state, not
separate substances outside it.

### Rotation at every scale

For every measured excitation, the state may contain:

```text
Point rotation: internal circulation/spin measurement
Path rotation: relational orbital or transported curvature history
Field rotation: curl/circulation of surrounding momentum or phase flow
```

Nested Point-PPF, Path-PPF, and Field-PPF descriptors are added only where the
data resolve them. They do not automatically modify orbital acceleration.

## Combined evolution used by the simulator

```text
a_total = a_Newton + a_1PN + a_OW_internal + a_OW_boundary
```

- `a_Newton` is the weak-field bulk response.
- `a_1PN` supplies the leading relativistic correction currently implemented.
- `a_OW_internal` is reserved for derived internal wake, phase, boundary, EM,
  or rotation exchange. Its net force and torque are closed to zero.
- `a_OW_boundary` is reserved for a declared external or larger-stratum Field
  boundary. It cannot be hidden inside the internal channel.

The One Wave terms default to zero. A description alone cannot activate them.

## What Newton and Einstein already account for

- gravitational attraction and orbital binding;
- motion of the barycenter;
- mutual N-body perturbations;
- weak-field relativistic perihelion correction;
- stress-energy as the source of spacetime curvature in the full theory;
- gravitational time and geometry effects in the full theory.

These effects must not be added again under the names wake, curvature, or
displacement.

## What remains missing from the present simulator

### 1. Canonical One Wave Field action

The framework needs a 3D/4D action `S[Psi,g,A,...]`. Its variation must produce
the Field equation, stress-energy tensor, boundary terms, and conserved
currents. Without this, the nonlinear potential and global kernel remain
candidate choices.

### 2. Moving-wake transport

A wake that follows an excitation requires a covariant transport/material
derivative derived from the same action. Screen-space trails are not physics.

### 3. Internal-to-external rotation transfer

The coupling between core rotation, EM structure, Field circulation, and path
motion needs a torque and energy-flux equation. Conservation closure prevents
creation of momentum but does not derive the transfer strength.

### 4. Electromagnetic coupling

The Maxwell field and charge/current four-vector must be included explicitly or
derived as a limit. Magnetic coupling cannot be represented by an unlabeled
visual shell.

### 5. Persistent-mode equation

The current complex Field bench does not yet preserve stable extended
excitations. A bounded mode equation and stability proof/test are required
before it can replace compact-body approximations.

### 6. Harmonic memory and lock feedback

Phase, frequency, hysteresis, and harmonic branches are measured, but a
dimensionally valid transfer law must define what energy/momentum moves during
Build, Hold, Break, and Loop.

### 7. Cross-scale projection

Micro, Small, Medium, Large, and Macro strata require declared characteristic
length, time, energy, and amplitude scales. Camera zoom does not couple quark,
atomic, planetary, and galactic equations.

### 8. Relativistic completeness

The implemented 1PN term is a solar weak-field approximation. Precision work
requires Horizons/SPICE state vectors, a full multi-body post-Newtonian model or
numerical relativity where appropriate, and clock/frame definitions.

### 9. Observation and falsification

The One Wave residual must be compared against held-out observations after the
Gray model, relativity, measurement errors, and numerical error are accounted
for. Parameter fitting to the same trajectory is not confirmation.

## Promotion gate

A nonzero One Wave term enters the production simulator only when it provides:

1. dimensions and declared variables;
2. derivation from the canonical action or an explicitly labeled ansatz;
3. energy, linear-momentum, and angular-momentum receipts;
4. correct Newtonian and relativistic limiting behavior;
5. convergence under timestep and spatial refinement;
6. a falsifiable prediction against data not used to tune it.
