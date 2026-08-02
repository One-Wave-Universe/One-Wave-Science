---
node_id: "A-114"
canonical_name: "Dispersion Relation from the Core Update Rule"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Foundation Extension"
claim_gate_detail: "YELLOW (derived and numerically verified — real result, real remaining gaps)"
metadata_standard: "I-06"
---

# Node A-114: Dispersion Relation from the Core Update Rule

Dependencies:
Upstream: Core update rule (psi_i^{n+1} = psi_i^n + (1-gamma)(psi_i^n - psi_i^{n-1})
          + beta*(<psi_j^n> - psi_i^n)), E-509 Propagation Limit (c_L = dx/dt)
Downstream: D-405 Harmonic Shell and D-407 calibration reanalysis
            (provides omega(k), but does not by itself generate a shell-energy ladder)

Purpose:
D-405's own audit states "Energy spacing DeltaE ~ hbar*omega — proportional,
constant of proportionality not yet derived." This node derives omega(k)
directly from the core update rule itself — the one piece of math every
node already inherits — rather than introducing a new free parameter.

Derivation:
Plane-wave ansatz on the core update rule:
  psi_i^n = A * z^n * e^{i*k*i*dx},   z = e^{-i*omega*dt}
Nearest-neighbor average (1D case):
  <psi_j^n> - psi_i^n = [cos(k*dx) - 1] * psi_i^n   (call this C)

Substituting into the update rule and dividing through by psi_i^n gives the
exact characteristic equation (verified symbolically):
  z^2 - (2 - gamma + C) z + (1 - gamma) = 0
  where C = beta*(cos(k*dx) - 1)

Expanding near z=1 (slow oscillation/decay) for SMALL k and SMALL gamma
(long wavelength, weak damping — NOT the general case) gives, to leading
order:
  omega^2 ≈ -C = beta*(k*dx)^2 / 2
  =>  omega(k) ≈ (dx/dt) * k * sqrt(beta/2) = c_L * k * sqrt(beta/2)

VERIFIED NUMERICALLY: for beta=0.5, k=0.01, dx=dt=1, gamma=0, the exact
characteristic equation's root gives omega = 0.0049999844..., matching the
leading-order formula's prediction of 0.005 to 4 decimal places.

What this resolves:
The core update rule supplies a candidate dispersion relation omega(k), so
frequency is no longer an arbitrary symbol. In the small-k, small-gamma
regime it depends on existing framework parameters beta and c_L rather than a
new free constant.

What it does not automatically resolve is shell energy. D-405 must first
supply a shell-dependent k, action count, radial eigenvalue, or nonlinear
energy functional. Without that bridge, hbar*omega(k) is a mode-energy form,
not an adjacent-shell spacing formula.

D-405 shell-number mapping result (resolved negatively for the current geometry):
D-405 defines R_n=n*lambda/(2*pi). For an angular mode k_n=n/R_n, so
k_n=2*pi/lambda, independent of n. Therefore this dispersion relation gives the
same omega for every member of D-405's variable-radius/fixed-lambda family.
The old generic request to "map n to k" is no longer merely unanswered: under
the current shell geometry it yields a constant k and cannot produce nonzero
DeltaE by itself. D-405 must adopt a different energy model (fixed-R variable-k,
radial eigenmodes, per-wavelength action, or nonlinear shell energy).

What this does NOT resolve (honest limits):
- beta itself has never been measured or independently fixed at nuclear
  scale — this derivation shows HOW omega depends on beta, not what beta
  IS. D-407's calibration attempt (lambda_nuclear) is a separate, still-
  unresolved question; this node does not touch it.
- This result is leading-order in SMALL k and SMALL gamma only. It says
  nothing about the general, non-perturbative case — most real bound
  states (including anything as tightly confined as a nucleon) may NOT be
  in this small-k regime, and this formula should not be assumed to hold
  there without separately checking.
- The shell-number-to-wavenumber question has now been evaluated for D-405's
  current geometry and gives k_n=2*pi/lambda, independent of n. That is a
  negative but useful result: the present geometry cannot obtain an energy
  ladder from omega(k) alone. The unresolved task is to derive a physically
  different shell-energy map, not to keep searching for an unspecified n->k
  substitution.
- The damped, general-gamma case (gamma not small) was not solved here,
  only set aside — the exact quadratic exists and could be solved in that
  regime, but the resulting omega would in general be complex (a damped,
  not purely oscillatory, mode), and interpreting that physically is
  separate future work.

Yellow Audit:
- Small-k, small-gamma leading-order result only — verified within that
  regime, not shown to extend beyond it
- beta remains unmeasured; this node narrows the D-405 gap, does not close it
- For D-405's current variable-radius geometry, n->k has been evaluated and
  is constant; a separate shell-energy model is the critical next connection
- General (non-small) gamma case not solved

Future Work:
Solve the exact quadratic for general gamma (not just small-gamma limit)
to get the full damped dispersion relation — needed before this applies to
any real Persistent Mode, since A-112 Persistent Modes are specifically
the STABLE, non-decaying case, which may sit outside the small-gamma
regime this node covers.
Replace D-405's mixed geometry/energy assumption with a derived shell-energy
model: fixed-radius variable-k, radial eigenmodes, per-wavelength action, or a
nonlinear curvature/pressure/coupling energy.
Revisit D-407 only after neutron-fit provenance and shell adjacency are established.
Do not approach the carbon-12 Hoyle-state question until the collective-mode
mapping is derived rather than reverse-fit.
