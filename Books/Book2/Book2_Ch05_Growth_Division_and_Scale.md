# ONE-WAVE FRAMEWORK
## Book 2 — Small
## Chapter 5: Growth, Division, and Scale

**Status:** GRAY reference / YELLOW One-Wave comparison  
**Dependencies:** A-107 Bounded Motion, A-108 Local Stability, A-111 Recursion, B-220 scale hierarchy  

---

## Gray

Cells grow, duplicate molecular components, replicate genetic material, and divide. Growth and division are not simple geometric doubling. They are regulated processes constrained by resource supply, surface area, volume, DNA replication, cytoskeletal mechanics, checkpoints, and environment.

For an ideal spherical cell,

$$
A=4\pi r^2,
\qquad
V=\frac{4}{3}\pi r^3.
$$

If radius doubles,

$$
A\rightarrow4A,
\qquad
V\rightarrow8V.
$$

Therefore

$$
\frac{A}{V}=\frac{3}{r}
$$

falls as size increases. This simple scaling already shows why a larger cell is not merely a small cell multiplied uniformly in every functional sense.

## 2D — growth as an explicit state trajectory

Let $M(t)$ represent biomass or another clearly defined size proxy. Exponential growth under unconstrained proportional production is

$$
\frac{dM}{dt}=\mu M,
$$

with solution

$$
M(t)=M_0e^{\mu t}.
$$

A resource-limited population is often represented phenomenologically by logistic growth,

$$
\frac{dN}{dt}=rN\left(1-\frac{N}{K}\right).
$$

These two equations describe different objects—single-cell mass and population count in this example. The book must keep variable identity explicit rather than using the same curve to imply a universal law.

## 3D — division and conservation bookkeeping

At ideal symmetric division, one parent state becomes two daughter states. For a conserved inventory $Q$ with no production or loss during the division event,

$$
Q_{parent}=Q_{d1}+Q_{d2}.
$$

Symmetry would give

$$
Q_{d1}=Q_{d2}=\frac{Q_{parent}}{2},
$$

but real division can be asymmetric. The conservation equation is more general than the equal-halves special case.

A state vector can be written

$$
\mathbf x=(M,V,A,D,E,\ldots),
$$

where every coordinate is named. Division is then a mapping

$$
\mathbf x_p\rightarrow(\mathbf x_{d1},\mathbf x_{d2}).
$$

That is the proper place to ask which quantities are conserved, copied, partitioned, rebuilt, or newly synthesized.

## Mathematics — dimensionless scale comparisons

Cross-scale comparisons become safer when expressed using dimensionless quantities instead of raw size alone. Examples include normalized deviation

$$
\epsilon_x=\frac{x-x_*}{x_*},
$$

relative growth rate

$$
g=\frac{1}{M}\frac{dM}{dt},
$$

and a diffusion timescale estimate

$$
t_D\sim\frac{L^2}{D}.
$$

That last relation is especially important: if characteristic length $L$ increases by a factor of 10 while $D$ stays fixed, the diffusion timescale rises by about a factor of 100. Scale changes dynamics.

For surface-mediated exchange with characteristic flux $J$,

$$
\frac{1}{V}\frac{dQ}{dt}\propto J\frac{A}{V}.
$$

The surface-to-volume term supplies a direct measurable scaling constraint.

## One-Wave comparison

B-220 provides the Micro → Small → Medium → Large → Macro organizational ladder. Book 2 should use that ladder as an indexing system until an actual transformation law is derived.

A legitimate cross-scale law must state what changes under a scale factor $s$:

$$
L' = sL,
$$

and then derive or measure the corresponding transformation for time, coupling, amplitude, energy, or other variables. It is not enough to observe a repeated picture at two scales.

For example, geometric similarity alone gives

$$
A' = s^2A,
\qquad
V' = s^3V.
$$

Those exponents are derived from geometry. A proposed One-Wave scaling relation deserves the same level of explicitness.

## Graph requirement

This chapter should always travel with figures showing:

1. $A$, $V$, and $A/V$ versus radius;
2. growth curve with units and fitted parameters;
3. parent-to-daughter inventory accounting;
4. diffusion timescale versus characteristic length on log axes when multiple decades are compared.

## Predictions / tests

1. Test any claimed scale invariance against known surface-to-volume and diffusion scaling first.
2. Separate geometric similarity from dynamical similarity.
3. For division, measure partition variance rather than assuming equal halves.
4. Require every cross-scale claim to specify the transformed variables and exponents.
5. Reject a repeated ratio if changing units, normalization, or sampling destroys it.

## Yellow Audit

- The scale hierarchy is organizational; it is not itself a biological scaling law.
- Surface/volume and diffusion scaling are established controls.
- No universal One-Wave transform currently maps a cellular equation into an organismal or planetary equation with calibrated parameters.
- Visual resemblance across scales is hypothesis generation, not validation.

## Future Work

Build a scale table for every book: characteristic length, time, dominant measured variables, control equations, and proposed One-Wave mappings. Cross-book equations should link only after the dimensions and transformations are explicit.

## Closing Thoughts

Scale is where loose analogies usually break. A larger object has different surface-to-volume ratio, transport times, inertial scales, and interaction ranges. If One-Wave really survives scale changes, it should survive those equations too. That is a stronger and more useful claim than saying two pictures look alike.
