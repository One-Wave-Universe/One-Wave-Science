---
node_id: "E-534"
canonical_name: "Redshift–Time-Dilation Shared-Transport No-Go and Derivation Target"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Cosmology / Transport Constraint"
metadata_standard: "I-06"
---

# E-534 — Redshift–Time-Dilation Shared-Transport No-Go and Derivation Target

## Purpose

Attack E-528 and E-533 together instead of fitting redshift and timing independently. The target is one frozen transport law derived from the existing lattice dynamics and then confronted with independent data.

## Baseline Zero references

Owning repo: `One-Wave-Science`. Baseline Zero remains the full `One-Wave-Universe` organization.

Primary chain:
- `Nodes/E-528_Static_Redshift_Transport.md`
- `Nodes/E-533_Superfluid_Transport_Time_Dilation.md`
- `Nodes/A-114_Dispersion_Relation.md`
- `Nodes/C-309_Friction_Limit.md`
- `Nodes/E-509_Propagation_Limit.md`
- I-06 metadata rules.

## Exact A-114 branch

Start with

```
z_step^2 - (2 - gamma + C) z_step + (1 - gamma) = 0
C = beta [cos(k dx) - 1]
```

Define `A = 2 - gamma + C` and `q = 1 - gamma`. Then

```
z_± = [A ± sqrt(A^2 - 4q)] / 2.
```

On an oscillatory branch, `A^2 < 4q`:

```
z_± = sqrt(q) exp(± i theta)
cos(theta) = A / [2 sqrt(q)]
omega(k) = theta / dt.
```

Therefore the present constant-coefficient recurrence naturally separates:
- magnitude `|z| = sqrt(1-gamma)`: damping/growth;
- phase `theta`: dispersion and phase advance;
- `d omega/dk`: group transport.

This extends A-114 without changing its small-k result.

## No-go for the current static homogeneous implementation

A linear time-translation-invariant recurrence maps a temporal Fourier component to the same temporal frequency multiplied by a transfer factor. Constant `beta`, `gamma`, `dx`, and `dt` can attenuate amplitude and alter phase/group delay, but do not by themselves translate a monochromatic carrier continuously to lower temporal frequency with path length.

Accordingly, the E-528 candidate

```
d nu / d ell = -kappa_gamma nu
1 + z_cos = exp(integral kappa_gamma d ell)
```

is **not yet derived from A-114**.

This is a no-go for the narrow implementation "static + linear + homogeneous A-114 alone", not a falsification of every possible One-Wave redshift mechanism.

## Required extension

A successful mechanism must derive frequency conversion from the medium dynamics. Candidate classes to test, not assume:

1. state-dependent or spatially evolving coefficients;
2. nonlinear coupling between propagating mode and medium state;
3. genuinely nonstationary local reference/update dynamics.

Any extension must state exactly which symmetry is broken and conserve/account for energy and information explicitly.

## Shared-law target

Let a derived accumulated interaction be

```
K = integral kappa_gamma(chi, grad chi, ...) d ell.
```

E-528 gives the candidate spectral mapping

```
nu_obs / nu_emit = exp(-K)
1 + z_cos = exp(K).
```

The hard E-533 target is that the **same frozen medium law**, without a separately fitted timing function, predict the transient-duration mapping. The strongest simple target is

```
Delta t_obs / Delta t_emit = exp(K) = 1 + z_cos.
```

That equality is a test target, not an established One-Wave result.

## Field map to derive

- `beta`: coupling/dispersion control in A-114.
- `gamma`: recurrence memory damping; C-309 prohibits treating damping itself as the propagation ceiling or Mass Effect.
- `k, dx, dt`: mode and lattice scales; E-509 supplies the local propagation bookkeeping.
- `chi, grad chi`: candidate E-528 medium-state inputs to `kappa_gamma`.
- `Xi`: E-533 timing-state placeholder. It must be reduced to the same underlying state variables rather than becoming an independent cosmology fit function.

Target derivation:

```
(beta, gamma, k, dx, dt, chi, grad chi, ...)
        -> one local transport operator
        -> {d ln nu/d ell, d ln Delta_t/d ell}
```

with both outputs fixed by that operator.

## Falsification gates before fitting

FAIL this implementation if any of the following holds:

1. the derived operator has no frequency-conversion term;
2. redshift requires one free path function while timing requires an independent free path function;
3. one frozen parameter set cannot predict both spectral redshift and transient stretch;
4. the mechanism produces unavoidable chromatic distortion inconsistent with the data domain being tested;
5. parameters are retuned separately for the held-out geometric test.

## Data attack order

Only after the mechanism is derived:
1. supernova redshift/duration and Pantheon+ distance/covariance products;
2. freeze the law and nuisance treatment;
3. use DESI BAO/AP as an independent geometric held-out test.

No cosmological dataset may be used to invent the missing frequency-conversion term.

## Council review receipt

Brain Buddy Gemini independently agreed with the narrow no-go: the current static linear homogeneous recurrence supplies damping/dispersion, not secular carrier-frequency translation. DeepSeek did not return a scientific review in that run; its relay returned HTTP 500 from the browser backend. Therefore no DeepSeek scientific agreement is claimed.

Receipt produced by the recovery Council run:
`External_Work/brain_buddy/outbox/council-both-000001.md`.

## Status

- Exact A-114 root algebra: DERIVED from repo recurrence.
- Static-LTI frequency-conversion no-go: ESTABLISHED mathematical constraint on this implementation.
- E-528 shared transport mechanism: HYPOTHESIS / NOT DERIVED.
- E-533 shared timing mechanism: HYPOTHESIS / NOT DERIVED.
- Equality of redshift factor and transient stretch from one `K`: TARGET TEST.
- Cosmological fit: NOT RUN.

## Next smallest proof step

Introduce the smallest explicit state-coupling extension to A-114 that can transfer frequency while retaining the repo's propagation constraints. Derive `d ln nu/d ell` and `d ln Delta_t/d ell` from it symbolically before touching cosmological fit parameters.
