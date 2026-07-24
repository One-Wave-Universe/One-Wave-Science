---
node_id: "D-406"
canonical_name: "Isotope Stability via Outer-Shell Coupling Density"
namespace: "NODE"
gate: "GREEN"
lifecycle: "BLOCKED"
classification: "Extension Node"
claim_gate_detail: "GREEN (nuclear coupling hypothesis) / BLOCKED pending an inter-nucleon bridge"
metadata_standard: "I-06"
---

# Node D-406: Isotope Stability via Outer-Shell Coupling Density

Grounding note: Book 1 Ch5 already states the actual mechanism this
node needs — a free neutron's outer shell "loses its coupling when it
has no neighbors," which is offered there as the reason free neutrons
decay while bound neutrons don't. This node does nothing more than
take that stated mechanism seriously as a function of NEIGHBOR COUNT
and RATIO, since isotopes (same Z, different neutron count) are
precisely a question of how many neighbors each outer shell has.
Nothing here is new physics — it is making an implicit dependency
explicit and asking what it predicts.

Dependencies:
Upstream: Book 1 Ch5 The Neutron (two-shell model, R+/R-, sigma),
          A-108 Local Stability, A-112 Persistent Mode
Conditional geometry input: C-321 only after an inter-nucleon coupling bridge is derived
Downstream: none yet (proposed) — needed for carbon-12 vs carbon-14
            comparison specifically

Definition:
Ch5 establishes that a neutron's outer shell (R- = 0.8409 fm) requires
COUPLING to a neighboring structure to remain in the shell-balance
state; without a neighbor, the outer shell decouples and the two-shell
structure collapses (beta decay: proton + electron + neutrino).

This node proposes: coupling is not binary (present/absent) but has a
DENSITY, set by how many other nucleons are within coupling range and
how that coupling is distributed. For a fixed proton count Z, adding
neutrons changes this coupling density in two competing ways:

1. Each added neutron is itself a potential coupling partner for
   existing neutrons' outer shells — more neutrons, more mutual
   support, tending to stabilize.
2. Each added neutron changes the number and geometry of possible inter-nucleon couplings. C-321 cannot yet supply those couplings because it is only a reduced neck model derived from the intra-proton Boundary-Tension Weave. A separate bridge must establish whether intact proton/neutron knots form comparable necks at nuclear scale.

This gives a genuine hypothesis: there should be a coupling-density
OPTIMUM at some neutron-to-proton ratio for each Z, not a simple
monotonic "more neutrons = more stable" or "fewer = more stable." This
matches the real observed pattern (light stable nuclei cluster near
N≈Z; carbon-12 is Z=6,N=6; carbon-14 with Z=6,N=8 is beta-unstable) —
but this node does NOT derive that pattern from the mechanism, it only
identifies that the mechanism as stated in Ch5 is consistent with a
non-monotonic result and names the missing derivation.

Mathematics:

Coupling density (PROPOSED FORM, not derived from first principles —
built to have the right qualitative shape given Ch5's stated
mechanism, coefficients unknown):

CouplingDensity(i) = sum over neighbors j of [coupling_strength(i,j)] / ExpectedCoupling(shell type of i)

Decay condition (direct extension of Ch5's stated trigger):
IF CouplingDensity(i) < CouplingThreshold  THEN  outer shell of
nucleon i decouples => beta-decay-like event (matching Ch5's actual
described mechanism for the free-neutron case, generalized here to
the in-nucleus case)

Stability requirement for the WHOLE nucleus (composite of A-108's real
condition, applied per-nucleon rather than globally):
Nucleus is stable IFF, for all nucleons i: CouplingDensity(i) >= CouplingThreshold

Isotope comparison (what this node is actually FOR):
For fixed Z, as neutron count (A-Z) increases from N≈Z:
- Near N≈Z: neutrons and protons mutually support coupling density —
  CONSISTENT with observed stability clustering, not yet DERIVED from
  a specific coupling_strength(i,j) form
- Beyond some N/Z ratio: excess neutrons' outer shells are increasingly
  coupled only to OTHER neutrons (weaker/different coupling than to
  protons, per Ch5's shell-type distinction) — CouplingDensity per
  excess neutron falls, predicting eventual decay, CONSISTENT with
  carbon-14's real beta-instability, but again not yet DERIVED
  quantitatively

Operational Chain:
Ch5's single-neutron decoupling proposal => derive an inter-nucleon coupling law => define CouplingDensity(i) => require CouplingDensity(i) >= threshold for every nucleon => vary neutron count at fixed Z and test the resulting stability curve

Yellow Audit:
- coupling_strength(i,j) has no derived functional form — this is
  asserted to exist and to differ by shell type (proton-proton,
  proton-neutron, neutron-neutron), following Ch5's own shell-type
  distinction, but the actual VALUES are not derived
- CouplingThreshold is not derived — it is the same category of gap
  as Ch5's own undetermined kappa+/- (equilibrium stiffness)
- This node predicts a QUALITATIVE pattern (stability optimum near
  N≈Z, falling off with excess) that happens to match real nuclear
  physics, but "predicts the right shape" is not the same as "derives
  the right shape" — this must not be overclaimed
- C-321's N=3 junction geometry does not establish an inter-nucleon force. This node is blocked until that physical bridge is derived.
- Formation and stability requirements are taken directly from C-318 and Book 1 Ch14.

Future Work:
Derive coupling_strength(i,j) for the three shell-type cases
(proton-proton, proton-neutron, neutron-neutron) from Ch5's real
R+/R-/sigma values, rather than treating it as a free function.
Derive the missing inter-nucleon coupling bridge before importing any C-321 network geometry. Then test candidate nuclear geometries against C-318/A-112 stability requirements.
Once coupling_strength has a real form, compute CouplingDensity(i)
for carbon-12 (Z=6,N=6) and carbon-14 (Z=6,N=8) explicitly and check
whether the predicted stability difference matches the real, known
difference (carbon-12 stable, carbon-14 beta-decays with ~5730 year
half-life) — this is the actual validation target for this whole node.
