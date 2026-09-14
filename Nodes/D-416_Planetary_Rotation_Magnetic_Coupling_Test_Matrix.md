---
node_id: "D-416"
canonical_name: "Planetary Rotation-Magnetic Coupling Test Matrix"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE_HYPOTHESIS"
classification: "Cross-Scale Falsification / Planetary Rotation and Magnetism"
claim_gate_detail: "GREEN (observational control matrix and falsification rules) / BROWN (One-Wave magnetic-lock prediction not yet derived)"
metadata_standard: "I-06"
---

# Node D-416: Planetary Rotation-Magnetic Coupling Test Matrix

**Dependencies**  
Upstream: A-115 Unified Compression Field, C-306 Torque, C-307 Angular Momentum, C-311 Electric-Magnetic Duality, C-319 Magnetic Lattice Reorganization, C-320 Magnetic-Compression Path Coupling, D-409 Twelvefold 3D Close-Packed Coordination, D-412 Lattice Simulation and State-Driven Visualization Standard, D-413 Ground Lattice Orbital-Restoring Simulation  
Lateral: D-401 Flux, E-505 Coupling  
Downstream: future source-derived 3D planetary coupling simulation and body-by-body parameter-free comparison

## Purpose

D-416 prevents planetary examples from becoming free-form stories. It is the required falsification matrix for any claim that parent-field coupling, magnetic lattice reorganization, gravity/compression, spin, orbit, or tidal locking share one One-Wave mechanism.

The rule is simple:

> One coupling law must face the awkward bodies as well as the convenient ones.

Moon, Mercury, Venus, Uranus, and Neptune are deliberately kept together because they occupy very different rotation and magnetic regimes.

## Observational Controls

These are external observations used as controls. They are not One-Wave conclusions.

| Body | Rotation/orbit control | Magnetic control | Constraint on C-319/C-320 |
|---|---|---|---|
| Moon | Synchronous rotation: one face remains directed toward Earth on average. | No present global magnetic field; localized crustal magnetic regions exist. | A model requiring a present global lunar dipole to maintain synchronous rotation fails. Magnetic coupling, if relevant, must be secondary, historical, induced, parent-field-mediated, or unnecessary in this case. |
| Mercury | 3:2 spin-orbit resonance: three rotations for every two solar orbits. | Weak intrinsic magnetic field, strongly weaker than Earth's and offset along the spin axis. | The model must produce or preserve 3:2 rather than forcing every close body toward 1:1. |
| Venus | Extremely slow retrograde rotation. | No internally generated global magnetic field; solar-wind interaction produces an induced field. | A universal intrinsic-dipole locking rule fails. Any coupling must distinguish intrinsic, induced, and absent global fields. |
| Uranus | Rapid rotation with extreme axial orientation. | Magnetic dipole is tilted about 59-60 degrees from the rotation axis and offset by about one-third planetary radius. | A simple magnetic-axis-equals-spin-axis rule fails. The model must tolerate or predict a strongly misaligned rotating field. |
| Neptune | Rapid rotation. | Magnetic axis is tilted about 47 degrees from the rotation axis and is significantly offset from the center. | The same law used for Uranus must address a second strongly misaligned ice-giant field without body-specific switches. |

## Source References

Authoritative starting references for the control facts:

- NASA Moon solar-wind/magnetic-field overview: https://science.nasa.gov/moon/solar-wind/
- NASA Earth/Moon magnetic-shield history and tidal-lock overview: https://www.nasa.gov/solar-system/earth-and-moon-once-shared-a-magnetic-shield-protecting-their-atmospheres/
- NASA Mercury facts: https://science.nasa.gov/mercury/facts/
- NASA BepiColombo overview noting Mercury's 3:2 resonance: https://science.nasa.gov/mission/bepicolombo/
- NASA Venus facts: https://science.nasa.gov/venus/venus-facts/
- NASA Uranus facts: https://science.nasa.gov/uranus/facts/
- NASA Voyager Uranus history: https://www.nasa.gov/history/35-years-ago-voyager-2-explores-uranus/
- NASA Neptune facts: https://science.nasa.gov/neptune/neptune-facts/

## Required State Vector

A planetary comparison must at minimum track

\[
\mathcal P
=
\left(
\omega_{spin},
 n_{orb},
 e,
 \theta_{spin},
 \theta_B,
 \delta_B/R,
 B_{int},
 B_{ind},
 \chi,
 \nabla\chi,
 \mathbf R,
 \mathbf K_L
\right),
\]

where:

- `omega_spin`: spin rate;
- `n_orb`: mean orbital rate;
- `e`: orbital eccentricity;
- `theta_spin`: spin-axis orientation relative to the orbital reference;
- `theta_B`: magnetic-axis misalignment;
- `delta_B/R`: normalized magnetic-field offset;
- `B_int`: intrinsic magnetic component;
- `B_ind`: induced/externally driven magnetic component;
- `chi`, `grad(chi)`: A-115 compression state and gradient;
- `R`, `K_L`: C-319 reorganization and path-accessibility states.

A missing quantity must be marked unknown. It may not be silently fitted.

## Locking Is an Output, Not an Input

For a parent/child system define the spin-orbit phase

\[
\Delta\phi_{p:q}=q\,\phi_{spin}-p\,\phi_{orb}.
\]

A `p:q` lock requires bounded libration of this phase under the modeled dynamics. It is not enough to initialize the body at the observed ratio.

Examples:

- Moon synchronous lock: `p:q = 1:1`;
- Mercury resonance: `p:q = 3:2`.

The simulation must start away from the target state in at least one test and show whether the target is dynamically approached, retained, escaped, or never reached.

## Required Ablations

Every planetary magnetic-coupling run must include:

1. baseline gravity/tidal model with C-319/C-320 OFF;
2. C-319 lattice reorganization ON but C-320 gravity coupling OFF;
3. C-319 and C-320 ON;
4. intrinsic magnetic component removed;
5. induced/parent-field component removed where applicable;
6. magnetic-axis tilt removed while keeping field magnitude fixed;
7. field offset removed while keeping tilt fixed;
8. parameter-identical cross-body run where dimensional scaling permits it.

A magnetic claim is useful only if ON/OFF or geometry ablations predict a measurable residual beyond the baseline model.

## Anti-Retrofit Rule

Do not tune one private coefficient set per planet and then call the common diagram a law.

Before a multi-body run, freeze:

- the form of C-319's reorganization law;
- the form of C-320's path-weighted restoring law;
- which coefficients are universal;
- which parameters are measured body inputs;
- the scaling rule, if any.

Only then compare bodies.

## Direct Failure Conditions

The planetary magnetic-lock hypothesis fails in its current form if:

- it requires the Moon to have a present global intrinsic magnetic field;
- it forces Mercury toward 1:1 when the same inputs should permit the observed 3:2 state;
- it cannot represent Venus without inventing an unobserved intrinsic global field;
- Uranus or Neptune require their observed magnetic-axis tilts to be erased by hand;
- the magnetic channel produces no measurable prediction beyond the baseline gravitational/tidal model;
- each body requires unrelated coupling constants with no derived scaling rule;
- apparent locking is created only by initial conditions, damping chosen after the fact, or renderer constraints.

## Status

D-416 makes Moon/Mercury/Venus/Uranus/Neptune a permanent joint test set. Their unusual differences are not exceptions to hide; they are the pressure test for whether C-319 and C-320 describe anything real.
