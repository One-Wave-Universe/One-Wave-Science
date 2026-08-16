# D-415 Simulation Audit — Where New Mathematics Is Required

## Result

The current update is numerically stable under the first timestep-refinement
check, but it does not yet produce persistent, rotating, phase-locked
three-excitation motion.  This is a useful Yellow result: the failure is
visible and attributable instead of being hidden by a prescribed orbit.

The first 120-step sweep used a 32×32 six-neighbor triangular lattice.

## Observed behavior

- Timestep runs at `dt = 0.02, 0.04, 0.08` produced hyperradius ratios of
  approximately `0.412, 0.413, 0.415` at equal physical time.  The integrator
  is not the dominant source of the current failure.
- Across the factor sweep, measured excitation-weight retention ranged from
  roughly `0.12` to `0.41`.  The seeded structures disperse or lose measured
  identity rather than acting as persistent modes.
- The baseline hyperradius contracted to about `0.41` of its initial value.
- Baseline Field-vorticity RMS fell to about `0.074` of its initial value.
- No run produced a completed harmonic lock return.  Locking currently exists
  only as a diagnostic and does not feed back into the Field equation.
- Kernel-length changes materially changed hyperradius, coherence, weight, and
  vorticity receipts.  The global kernel cannot remain an arbitrary visual or
  numerical choice.
- Raw lattice-size runs are not physically comparable yet because `n`, window
  width, kernel length, and domain extent are not tied through a declared
  dimensionless scaling law.

## Required new mathematics

### 1. Persistent-mode potential

The current positive linear/cubic response does not preserve three localized
excitations.  A bounded nonlinear potential must be derived with a stability
condition and conserved-energy ledger.  Parameter fitting alone is not a
derivation.

### 2. Rotation generation and transfer

The complex-scalar current supplies a useful diagnostic, but smooth phase
gradients are predominantly curl-free.  Persistent distributed rotation needs
either derived topological defects, a multi-component order parameter, or an
explicit transport/circulation state coupled to `Psi`.

### 3. Harmonic feedback operator

The simulator measures frequency, phase, and hysteretic lock strength, but
`Lambda_ab` does not yet alter the Field update.  A dimensionally valid
coupling must specify what is transferred when a lock builds, holds, breaks,
and loops.

### 4. Derived nested nonlocal kernel

The strictly positive kernel proves the global numerical path, not its physical
form.  The next kernel must encode Micro→Macro stratum relationships, Field
timing, dimensional projection, and normalization without introducing an
arbitrary cutoff or independent superposed body fields.

### 5. Moving-wake equation

The current Field evolves globally but lacks a material derivative or derived
transport velocity.  A wake cannot remain attached to a moving source until
the one Field carries deformation through a covariant transport rule.

### 6. Conserved transfer ledger

Point, Path, Field, EM, boundary, and nonlocal channels need one ledger.  No
rotation, amplification, or orbital response may appear without a matching
Field exchange.

### 7. Dimensionless scale law

Before comparing 2D, 3D, planetary, or galactic runs, define dimensionless
groups connecting lattice spacing, timestep, kernel scale, excitation width,
wave speed, damping, and nonlinear response.

### 8. Measurement identity

The windows currently track three regions, but merge, split, crossing, and
temporary disappearance can exchange identities.  The measurement layer needs
an explicit continuity and reassignment rule before capture/ejection labels can
be trusted.

## Reproduction

```bash
python sweep_math_gaps.py
```

This produces `math_gap_audit/sweep_results.csv` and `findings.json`.
