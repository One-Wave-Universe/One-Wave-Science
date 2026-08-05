---
node_id: "D-409"
canonical_name: "Twelvefold 3D Close-Packed Coordination"
namespace: "NODE"
gate: "GREEN"
lifecycle: "ACTIVE"
classification: "Native 3D Geometry / Volumetric Simulation Foundation"
claim_gate_detail: "YELLOW (geometry) / GREEN (canonical physical-lattice candidate)"
metadata_standard: "I-06"
---

# Node D-409: Twelvefold 3D Close-Packed Coordination

**Dependencies**  
Upstream: A-116 Three-Dimensional Spherical Default, A-117 Dimensional Integrity, D-408 Sixfold 2D Lattice, D-411 Mirrored Axis Pairs, D-412 Lattice Simulation Standard, C-317 Boundary-Tension Weave  
Downstream: bounded-excitation simulation, Vortex-Phase simulation, Three-Vortex-Knot simulation, electrical-shell simulation, Mass-Effect response simulation

## Definition

The native physical layer is three-dimensional and volumetric. The current canonical lattice candidate uses close-packed local coordination, where a center has twelve nearest neighbors:

\[
\boxed{12{:}1}.
\]

This is a distinct 3D coordination shell, not two flat six-cell rings pasted together and called a volume.

## Local Neighbor Shell

One convenient normalized twelve-neighbor shell is the cuboctahedral set

\[
\mathcal N_{12}
=
\frac{a}{\sqrt2}
\left\{
(\pm1,\pm1,0),
(\pm1,0,\pm1),
(0,\pm1,\pm1)
\right\}.
\]

The twelve directed neighbor positions may be organized into six opposite coordinate pairs for a declared shell mapping. This gives a `6:1` mirrored-pair view and a `12:1` directed-neighbor view, controlled by D-411. It does not make every six-count mechanism identical.

Each point lies at distance \(a\) from the center. The complete local cluster therefore contains

\[
1\text{ center}+12\text{ nearest neighbors}=13\text{ sites}.
\]

Face-centered cubic and hexagonal close-packed arrangements share this local coordination number while differing in their longer-range stacking. The repository must test stacking rather than quietly treating FCC and HCP as identical.

## Relationship to the 2D Sixfold Layer

A 2D slice or projection of a 3D close-packed neighborhood may expose sixfold rings, triangles, hexagons, seven-center clusters, or thirteen-center diagrams. Such a picture is a projection/indexing view.

The native 3D state includes out-of-plane neighbors and gradients that the 2D view omits.

Therefore

\[
P_{3\rightarrow2}(\mathcal N_{12})
\neq
\mathcal N_{12}
\]

as a full dynamical object, even when the projection preserves sixfold visual symmetry.

## Volumetric State Variables

A 3D lattice site or cell may carry:

\[
X_i^{(3)}
=
\left(
\mathbf u_i,
\mathbf v_i,
\phi_i,
\chi_i,
\mathbf q_i,
B_i
\right),
\]

where candidate meanings include:

- \(\mathbf u_i\): 3D displacement,
- \(\mathbf v_i\): 3D local motion,
- \(\phi_i\): recurrence phase,
- \(\chi_i\): compression state,
- \(\mathbf q_i\): rotational/circulation state,
- \(B_i\): boundary or weave state.

The exact physical update law remains to be derived and tested. These variables are a simulation interface, not proof of mechanism.

## Required 3D Behaviors

The 3D lattice must be capable of displaying and measuring:

- volumetric compression and release,
- shear in multiple planes,
- rotational flow and vorticity,
- bounded recurrence,
- internal/external shell differentiation,
- Boundary-Tension Weave strain,
- Mirror-Gate approach and crossing,
- translation by sequential displacement and reconstruction,
- front compression, side transfer, and rear recovery.

## Relation to Flower-of-Life and Metatron Views

Flower-of-Life, Fruit-of-Life, and Metatron-style diagrams may be used as 2D coordinate, overlap, or connection projections of selected centers. They are not the native 3D object.

A thirteen-center 2D diagram may index the one-plus-twelve local shell, but the mapping must specify which projected point corresponds to which 3D neighbor and which lines represent actual couplings.

## Quark and Proton Boundary

A Vortex Phase must be simulated in this 3D layer. A planar circulation in D-408 is only a precursor test.

A proton candidate requires one continuous volumetric bounded excitation containing three persistent Vortex Phases coupled by the Boundary-Tension Weave. It cannot be validated in a single 2D ring.

## Required First 3D Tests

1. equilibrium hold of the twelve-neighbor shell;
2. isotropy test under impulses in many directions;
3. compression pulse and recovery;
4. rotational perturbation and vorticity retention;
5. localized bounded-excitation formation;
6. perturbation recovery;
7. FCC versus HCP stacking comparison;
8. 2D slice/projection comparison with measured information loss.

## Failure / Falsification

The close-packed candidate fails if:

- another 3D coordination produces demonstrably better isotropy and stable recurrence under the same laws;
- twelvefold local coordination cannot preserve bounded modes without imposed hard walls;
- the claimed 2D/3D correspondence cannot be defined without losing the quantities used by the physical interpretation.
