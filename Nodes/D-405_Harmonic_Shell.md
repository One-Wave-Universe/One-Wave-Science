---
node_id: "D-405"
canonical_name: "Harmonic Shell"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Geometry, Resonance, and Simulation"
claim_gate_detail: "YELLOW — GEOMETRY FORMALIZED; MODEL 2 IDENTIFIED AS THE OPERATIVE NUCLEAR GEOMETRY (MODEL 1 RETAINED FOR ATOMIC SHELLS); CONSTANT-SPACING ENERGY LADDER SUPPORTED BY TWO INDEPENDENT DERIVATIONS, STILL UNCALIBRATED; CALIBRATION BLOCKED ON C-318'S OWN OPEN MASS-EFFECT NUMBERS, NOT A ROUTABLE GAP"
metadata_standard: "I-06"
---

# Node D-405: Harmonic Shell

Dependencies:
Upstream: D-402 Resonant Mode, A-110 Oscillation
Downstream: Books — atomic shells, electron orbital model, proton charge radius;
            D-407 calibration reanalysis; CCD-01; Book5_Ch5_Stellar_Nucleosynthesis.md
            (blocked on this node's missing energy ladder for its product-stability
            "availability condition" -- see that chapter's Mathematics/Yellow Audit)

Definition:
A Harmonic Shell is a bounded standing-wave geometry whose closed path contains
an integer number of wavelengths.

Shell condition:

2 pi R = n lambda,  n in Z+

where:
R = shell radius,
lambda = wavelength along the closed path,
n = integer winding/shell count.

Mathematics — variable-radius, fixed-wavelength family:

R_n = n lambda/(2 pi)
DeltaR = R_(n+1)-R_n = lambda/(2 pi).

This defines equally spaced shell-center radii if lambda is held fixed.

## Critical model distinction

There are two different quantization problems that must not be mixed:

1. Variable radius, fixed lambda:
   R_n = n lambda/(2 pi).
   Here n counts how many copies of the same wavelength fit around successively
   larger closed paths.

2. Fixed boundary radius, variable wavenumber:
   k_n = n/R.
   Here n changes the allowed wavenumber and can generate a dispersion-based
   frequency/energy ladder.

The original node used Model 1 geometry but borrowed Model 2 energy intuition.
For Model 1:

k_n = n/R_n = 2 pi/lambda,

so k_n is independent of n. Therefore E_n=hbar omega(k_n) alone gives no
nonzero adjacent-shell energy spacing.

A nonzero energy ladder requires an additional derived model, for example:

- E_n = n epsilon_lambda from an action/energy per wavelength;
- radial eigenvalues k_(r,n) from a boundary-value equation;
- curvature/pressure/surface/coupling energy depending on R_n;
- nonlinear collective-mode energy.

D-405 currently quantizes geometry. It does not yet quantize energy.

## Candidate energy ladder (derived, not yet calibrated)

A-114 already tried the obvious route -- feeding Model 1's own k into the
core update rule's dispersion relation -- and got a documented negative
result: Model 1 gives `k_n = n/R_n = 2*pi/lambda`, independent of n, so
`E_n = hbar*omega(k_n)` is the same for every shell. An energy ladder is
not obtainable from Model 1 by this route. That rules one thing out; it
does not supply the ladder.

Switching to **Model 2** (fixed boundary radius R, `k_n = n/R`) and using
A-114's own already-derived, numerically-verified small-k dispersion
relation `omega(k) ~= c_L * k * sqrt(beta/2)` gives, for the first time, a
nonzero, derived (not invented) energy ladder:

```text
omega_n = c_L * sqrt(beta/2) * (n/R)
E_n     = hbar * omega_n = [hbar * c_L * sqrt(beta/2) / R] * n = epsilon * n
```

This is exactly D-405's own first-listed candidate form, `E_n = n*epsilon_lambda`,
now with `epsilon` expressed in already-existing quantities (`hbar`, `c_L` from
E-509, `beta` from the core update rule, `R` the fixed confinement radius)
rather than left as an undefined symbol.

Adjacent-shell spacing is therefore **constant**, independent of n:

```text
Delta E = E_(n+1) - E_n = epsilon = hbar * c_L * sqrt(beta/2) / R
```

An independent second candidate exists from a completely different
mechanism -- Ch6's already-real surface-energy formula (`E_surface = sigma
* 4*pi*R^2`) applied to Model 1's own `R_n = n*lambda/(2*pi)`:

```text
E_n = sigma * 4*pi*R_n^2 = (sigma * lambda^2 / pi) * n^2
Delta E_n = E_(n+1) - E_n = (sigma * lambda^2 / pi) * (2n + 1)
```

Here spacing **grows linearly with n** instead of staying constant. These
two candidates make genuinely different, mutually falsifiable predictions
about the shape of the shell-energy ladder (flat vs. widening gaps) --
that difference is itself a future test target, not something to force
into agreement now.

### Third route: breathing-mode oscillation (A-106)

A-106's own Derrick-theorem rescaling analysis already proves a localized
solution sits in a genuine potential well as a function of its size
(`d^2E/dlambda^2 > 0` at the stable point) -- a real, already-derived
"oscillates around a center" structure, not asserted from the oscillation
language used elsewhere in the repo. See A-106 section 12a for the full
derivation. If quantized (pending one still-missing ingredient: an
effective mass/kinetic term for the size coordinate, from A-109 or C-303,
not yet supplied), it gives `E_n = hbar*omega_breathe*(n+1/2)` --
**equally spaced**, the same qualitative shape as the Model-2/A-114
candidate above, reached by a completely independent route. Two
independent derivations landing on the same shape is real supporting
evidence for constant spacing over the surface-energy candidate's growing
spacing, though neither is calibrated and A-106's breathing-mode n is not
established to be the same quantum number as this node's winding number n
(see A-106 12a's explicit caveat on that point).

**Attempting to compute omega_breathe hits a hard, permanent wall, not a
temporary gap.** The missing effective mass would have to come from
Mass Effect (C-318), and C-318 explicitly and permanently forbids
deriving mass from a propagation-ceiling/speed shortcut ("a previous
draft incorrectly treated propagation status as a source of inertia...
it is false, permanently erased, and prohibited from re-entry under
alternate wording") -- which is exactly the kind of shortcut a fixed-R
confinement problem invites (mass from a confinement-scale/c_L
combination). C-318 itself is GREEN only on mechanism identity; its
actual coefficients and numerical spectrum are YELLOW. So this
candidate's normalization is not blocked on "nobody has done the
algebra yet" -- it is blocked on the repository's own central,
still-open Mass-Effect derivation, and must wait on that rather than
route around it.

### Reconciling Model 2 with Ch6's magic-number picture (resolved)

D-405's own Downstream line already names two different application
domains: atomic shells/electron orbitals, and nuclear magic numbers.
These are not the same physical situation, and on inspection they
actually want D-405's two different models separately, rather than
needing to be forced into one:

- **Atomic electron shells genuinely sit at different average radii**
  around one nucleus (principal quantum number n, Bohr-radius-like
  scaling with n). A picture where shell radius grows with n --
  **Model 1** -- is the physically appropriate one here.
- **Nuclear shells do not work this way.** Nucleons in different
  shells (1s, 1p, 1d2s, ...) all sit within the SAME confining nuclear
  volume (empirically, nuclear radius scales with mass number A, not
  with which shell a given nucleon occupies -- Ch6's own `R_nucleus ~
  R_0 * A^(1/3)`). Ch6's own magic-number language -- "all modes are
  fully coupled, no dangling ends," a count of how many internal
  coupling slots are filled -- describes occupancy of internal modes
  within one fixed container, not a container that grows with each
  new shell. That is **Model 2**'s picture (fixed R, internal mode
  index n), not Model 1's.

So D-405 applying Model 1's geometry to the *nuclear* magic-number
story was a category mismatch: it borrowed the right formula (shell
condition) for the wrong domain (Model 1 fits atomic shells, not
nuclear ones). This does not mean Model 1 is wrong everywhere -- it is
likely still right for D-405's atomic-shell downstream use -- it means
the *nuclear*/carbon-nucleosynthesis question this node keeps getting
asked to answer (Book5_Ch5, D-406) should have been reaching for Model
2 all along, not Model 1 + Ch6 surface energy.

This also answers the "is breathing-mode n the same as winding number
n" question, at least for the nuclear case specifically: once Model 2
is recognized as the right nuclear picture, its n (internal excitation
index of one fixed-size confined system) and A-106's breathing-mode n
(radial excitation index of one localized solution) are playing the
same role -- counting internal excitation quanta of one fixed object --
even though neither is proven numerically identical to the other yet.
For the atomic-shell case, where Model 1 is likely correct instead,
this correspondence is not expected to hold, and is not claimed to.

**Net effect on the three candidates:** this is an argument, not a
disproof -- it does not mathematically forbid a real growing-spacing
mechanism from existing by some other route. But it removes the
surface-energy candidate's own geometric justification for the
specific nuclear/carbon question this repository actually needs D-405
for, while the two constant-spacing candidates (Model 2 + A-114, and
A-106's breathing mode) turn out to describe the same kind of picture
for the right reason, not by coincidence. Constant spacing is now the
better-supported candidate for the nuclear case on three independent
grounds (two derivations plus this domain-matching argument); it is
still not calibrated, and is still not proof.

### Honest limits of the Model-2/A-114 ladder specifically

- A-114's `omega(k)` formula is a **small-k, small-gamma leading-order**
  result, verified numerically only in that regime. Model 2 sets
  `k_n = n/R`, so k grows with n -- at large enough n this ladder leaves
  the regime the dispersion relation was actually verified in. Treat
  `E_n = epsilon*n` as a low-n approximation, not a claim about the full
  spectrum.
- `beta`, `c_L` (equivalently dx/dt), and R are not calibrated at nuclear
  (or any physical) scale. This derivation fixes the *functional form*
  (linear ladder) and expresses its slope in terms of existing symbols;
  it does not produce a number in MeV or any other physical unit.
- Model 2 requires reinterpreting what "R" and "n" mean: R becomes a
  *fixed* confinement radius (e.g. the physical size of one nucleus or
  lattice cell), and n indexes internal excitation modes within that
  fixed boundary -- not, as in the existing Ch6/2D magic-number prose, a
  family of shells nested at successively larger radii. These are
  different pictures of what a "shell" is, and this node does not yet
  reconcile Model 2's fixed-R excitation-mode picture with Ch6's
  variable-radius nested-shell picture used to explain magic-number
  closure ("no dangling coupling ends"). Both may be capturing real,
  different things (which configurations exist geometrically, versus how
  much energy separates them) rather than actually conflicting, but that
  reconciliation has not been done.
- Neither candidate above says which physical nucleon count (or Z, A) a
  given n corresponds to. D-407's attempted n=7,8 assignment is a
  separate, already-flagged-as-conditional attempt at that mapping and is
  not used or assumed here.

## Connection to D-407

D-407 removes a false calibration fork: neutron-profile width sigma is not
shell-center spacing. Under an unproved adjacent-shell assumption, the neutron
radii select a provisional n=7,8 assignment and lambda approximately 0.6594 fm.
This is a conditional sensitivity-test value, not a measured constant.

## CCD-01 relationship

The shell condition may contribute to a minimum-action derivation only after the
energy/action assigned to one closed wavelength is derived. Geometry alone does
not establish S_min=hbar.

Operational Chain:
Resonant Mode + closed-path wavelength condition => Harmonic Shell geometry
=> Model 2 (fixed-R, k_n=n/R) + A-114 dispersion relation => candidate linear
energy ladder E_n = epsilon*n (functional form only, uncalibrated)
=> [calibration + n-to-nucleon-count mapping still required] => quantitative
atomic/nuclear structure

Yellow Audit:
- closed-path geometry and uniform center spacing are explicit;
- variable-radius versus fixed-radius quantization is now separated;
- Model 1's geometry does not create an n-dependent k spectrum (A-114,
  confirmed here again while deriving the ladder below);
- RESOLVED IN PART: a candidate energy ladder now exists via Model 2 +
  A-114's dispersion relation (E_n = epsilon*n, constant spacing), plus an
  independent second candidate via Ch6's surface energy + Model 1's R_n
  (E_n proportional to n^2, growing spacing), plus a THIRD independent
  route via A-106's own Derrick-theorem stability analysis treated as a
  breathing-mode oscillator (also constant spacing). Two of three
  independent routes now agree on constant spacing, which is real
  supporting evidence, not proof; the surface-energy candidate's
  growing-spacing prediction has not been mathematically ruled out, though
  see the domain-matching argument below, which weakens its own geometric
  justification for the nuclear case specifically;
- CLOSED (permanent wall, not a gap): the breathing-mode candidate's
  effective mass cannot be supplied from a propagation-ceiling/speed
  shortcut -- C-318 explicitly and permanently forbids exactly that
  derivation. It must wait on C-318's own still-open (YELLOW) numerical
  Mass-Effect derivation rather than route around it;
- lambda is not independently measured;
- D-407's 0.6594 fm candidate is conditional on an unproved 7/8 adjacency;
- beta and c_L (the inputs the new linear ladder's slope depends on) are
  not measured at nuclear scale (A-114's own Yellow Audit);
- RESOLVED: the Model-2 fixed-R excitation-mode picture and Ch6's
  variable-radius nested-shell picture were never actually competitors --
  Model 1 fits D-405's atomic-shell downstream use (electron shells do
  sit at growing radii), Model 2 fits the nuclear/magic-number use (all
  nucleon shells share one fixed nuclear volume). D-405 had been applying
  Model 1's geometry to the nuclear case, which was the mismatch. See the
  new "Reconciling Model 2 with Ch6's magic-number picture" section;
- radial stability hierarchy is not established;
- relationship to the neutron two-profile model remains conditional.

Future Work:
Do not attempt to supply the breathing-mode candidate's effective mass
from a propagation-ceiling/speed shortcut -- C-318 permanently forbids
it. Wait on C-318's own Mass-Effect numerical derivation instead.
For the nuclear/carbon question specifically, treat Model 2 (fixed-R,
k_n=n/R) as the operative geometry rather than Model 1 -- Model 1 remains
the right picture for D-405's separate atomic-shell downstream use.
Now that constant spacing has two independent derivations plus the
domain-matching argument above, actively look for a reason the
surface-energy (growing-spacing) candidate could still be right for some
other regime, rather than treating it as ruled out by weight of numbers.
Derive the physical boundary-value problem that decides between fixed-R
wavenumber quantization, variable-R winding shells, or radial eigenmodes,
now that both extremes have an explicit candidate ladder to compare against.
Solve A-114's exact (non-small-k) dispersion relation before trusting the
linear ladder at anything but low n.
Recover the neutron-profile fit and uncertainties before treating D-407 as a
calibration.
Derive or measure beta, c_L, and R at nuclear scale, and only then attempt
an n-to-nucleon-count (Z, A) mapping -- do not reverse-fit one from Hoyle
or magic-number data, per A-114's own Future Work.
Apply only the derived model to atomic and carbon calculations.
