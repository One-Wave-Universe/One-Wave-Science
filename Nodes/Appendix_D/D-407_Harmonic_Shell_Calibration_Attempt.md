---
node_id: "D-407"
canonical_name: "Harmonic Shell / Two-Shell Neutron Calibration Reanalysis"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Active Calibration and Model-Definition Audit"
claim_gate_detail: "YELLOW — PARTIAL RESOLUTION"
metadata_standard: "I-06"
---

# Node D-407: Harmonic Shell / Two-Shell Neutron Calibration Reanalysis

Dependencies:
Upstream: D-405 Harmonic Shell, A-114 Dispersion Relation, Book 1 Ch5 The Neutron
Downstream: quantitative carbon-12/Hoyle-state work remains blocked, but the false two-candidate fork is removed

Purpose:
Re-examine whether the neutron two-shell parameters can calibrate D-405's
nuclear wavelength. The earlier version treated two quantities as competing
measurements of the same shell spacing:

- center separation: R_minus - R_plus;
- fitted shell width: sigma.

That comparison was not valid. A profile width and a center-to-center spacing
are different geometric quantities unless a separate equation explicitly
identifies them.

## Input provenance and role

Repository parameters:

- R_plus = 0.7331 fm — center radius of the positive inner profile;
- R_minus = 0.8409 fm — center radius of the negative outer profile;
- sigma = 0.210 fm — radial width parameter attached to the profiles.

The repository repeats these as fitted parameters but does not currently
include their source fit, covariance matrix, or uncertainties. They must be
treated as internal model-fit inputs, not independent measured constants.

For a Gaussian-style shell profile,

rho_plus(r) = A_plus exp[-(r-R_plus)^2/(2 sigma_plus^2)]
rho_minus(r) = A_minus exp[-(r-R_minus)^2/(2 sigma_minus^2)]

R_plus and R_minus locate profile centers. sigma controls spread around a
center. Therefore:

DeltaR_center = R_minus - R_plus = 0.1078 fm
sigma / DeltaR_center = 1.9481

The numerical near-factor-of-two is an overlap/width statement, not a second
wavelength calibration.

## Resolution of the earlier candidate fork

### Former Candidate B — rejected as a role conflation

The earlier step

DeltaR = sigma
lambda = 2 pi sigma

is not licensed by the shell model. It equates profile width with adjacent
shell-center spacing without a derivation. Candidate B is removed from the
calibration competition.

This does not prove sigma is irrelevant. It remains necessary for overlap,
self-energy, and coupling calculations. It simply cannot be used as shell
spacing by definition.

### Adjacent-shell hypothesis — sharpened, not proved

Assume R_plus and R_minus are adjacent integer shells n and n+1 of one
wavelength lambda:

R_n = n lambda/(2 pi)
R_(n+1) = (n+1) lambda/(2 pi)

Then the radii alone imply

n_est = R_plus/(R_minus-R_plus) = 6.800557

The unique nearest adjacent integer assignment is therefore

n_plus = 7
n_minus = 8.

The two independent wavelength estimates are

lambda_plus = 2 pi R_plus/7 = 0.658029 fm
lambda_minus = 2 pi R_minus/8 = 0.660441 fm.

They differ by 0.366%.

The least-squares common wavelength for the fixed integer pair (7,8) is

lambda_star = 2 pi (7 R_plus + 8 R_minus)/(7^2+8^2)
            = 0.659395 fm.

It predicts

R_7_star = 0.734622 fm, residual R_plus-R_7_star = -0.001522 fm (0.208%)
R_8_star = 0.839568 fm, residual R_minus-R_8_star = +0.001332 fm (0.158%).

This is a substantially cleaner consistency result than the former
"8/7 is suggestive" note. Under the adjacency assumption, 7 and 8 are not
an arbitrary rational approximation; they are the nearest integer shell
labels selected by n_est.

However, this is still not a completed calibration because:

1. adjacency of the positive and negative profile centers has not been derived;
2. the parameter uncertainties and covariance are absent, so the residuals
   cannot be assigned statistical significance;
3. the radii are internal fit parameters whose source derivation is not stored;
4. higher non-adjacent integer pairs can approximate a radius ratio unless
   adjacency is physically established.

Provisional geometric result:

lambda_nuclear,candidate = 0.659395 fm, conditional on the 7/8 adjacent-shell model.

This value may be used only as a labeled sensitivity-test parameter, not as a
measured or calibrated One-Wave constant.

## Deeper shell-number / energy result

D-405 currently uses a variable-radius, fixed-wavelength family:

R_n = n lambda/(2 pi).

For an angular phase mode on a circle, the tangential wavenumber is

k_n = n/R_n.

Substitution gives

k_n = n/[n lambda/(2 pi)] = 2 pi/lambda,

which is independent of n.

Therefore A-114's dispersion relation omega(k) does not, by itself, produce
an energy ladder across D-405's current shell family. If energy is only
E_n = hbar omega(k_n), then all n share the same k and the same omega, giving
DeltaE_(n+1,n) = 0.

This resolves A-114's former generic "n to k mapping" question negatively
for the present D-405 geometry. The repository must choose and derive one of
these distinct models before predicting shell energies:

A. fixed boundary radius R with k_n=n/R;
B. variable radius with fixed lambda plus an independently derived per-wavelength
   action/energy rule E_n=n epsilon_lambda;
C. radial eigenmodes k_(r,n) from a real boundary-value equation;
D. nonlinear/coupled shell energy depending on curvature, overlap, pressure,
   or junction terms rather than omega(k) alone.

A-114 has already narrowed omega(k) to existing lattice parameters in its
small-k regime. The remaining energy blocker is not an arbitrary missing
proportionality constant; it is the absent physical map from shell geometry
to mode energy.

## Carbon/Hoyle consequence

The earlier factor-of-two calibration fork is closed as a false comparison.
The carbon calculation is still blocked by three explicit items:

1. establish whether the neutron profile centers really are adjacent n=7,8 shells;
2. recover or independently reproduce the fit and its uncertainties;
3. derive the shell-geometry-to-energy map listed above, then connect it to
   the carbon-12 collective mode rather than inserting the 7.65 MeV target.

No Hoyle-state number is produced here.

## Yellow Audit

Resolved:
- sigma is a width, not a second shell-spacing measurement;
- the factor-of-two disagreement is not evidence of two incompatible lambdas;
- the unique nearest adjacent assignment is n=7,8;
- conditional best-fit lambda is 0.659395 fm;
- D-405's current variable-radius family has k_n independent of n, so its
  energy ladder cannot come from dispersion alone.

Still open:
- physical derivation of adjacency;
- provenance and uncertainty of R_plus, R_minus, sigma;
- full radial profile and overlap-energy derivation;
- shell-geometry-to-energy rule;
- carbon-12 collective-mode mapping.

## Future Work

1. Recover the original neutron-profile fit or refit the charge distribution
   with stated uncertainties and covariance.
2. Derive whether opposite-sign shell centers must occupy consecutive radial
   indices; do not assume adjacency merely because 7/8 fits well.
3. Use sigma in the overlap/coupling integral where it belongs.
4. Select one shell-energy model A-D and derive it from existing One-Wave
   equations.
5. Only then run a held-out carbon/Hoyle calculation.
