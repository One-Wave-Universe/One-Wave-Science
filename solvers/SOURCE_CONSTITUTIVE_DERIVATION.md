# Source-Constitutive Connection Derivation
## One-Wave Gravity and Wake Structure from First Principles

**Status**: YELLOW derivation in progress  
**Purpose**: Derive J_source structure, V_b form, amplitude scaling, and finite-wake parameter σ from One-Wave lattice physics, not from galaxy data fitting  
**Reference**: A-115 (Unified Compression Field), E-532 (Bound/Unbound Criterion and Finite Wake), A115_STATIC_SOURCE_DIAGNOSTIC, GALAXY_EXTERNAL_VALIDATION

---

## Problem Statement

Galaxy rotation curves require exterior acceleration:
- 3.17524e-10 m/s² at 5.25 kpc (galactic bulge/disk transition)
- 3.72168e-11 m/s² at 27.25 kpc (outer disk)

The A-115 static spherical diagnostic proved that a **compact radial source J_r produces zero exterior acceleration** in the branch where V_b=0 and K_L=I.

Non-compact sources do produce exterior gravity (user demonstration), but "choosing the desired source tail installs the desired gravity tail—it does not derive it."

**The gap**: We must derive what J_source structure emerges naturally from One-Wave physics, then verify it produces the required exterior response.

---

## Step 1: Constraints from One-Wave Lattice Dynamics

### 1.1 The Displacement-Field Basis

All One-Wave physics starts from a scalar displacement field ψ on a superfluid lattice, with update rule:

ψᵢⁿ⁺¹ = ψᵢⁿ + (1-γ)(ψᵢⁿ - ψᵢⁿ⁻¹) + β(⟨ψⱼⁿ⟩ - ψᵢⁿ)

This defines:
- **Inertial memory** via (1-γ) term (damping parameter γ, validated in Phase 6B)
- **Neighborhood coupling** via β⟨ψⱼⁿ⟩ term
- **Discrete lattice structure** (nearest neighbors, geometry-dependent)

In the A-115 continuum projection, displacement **u**(**x**,t) satisfies:

ρᵤ ∂²**u**/∂t² + μᵤ ∂**u**/∂t - K_χ ∇(∇·**u**) - Sᵤ ∇²**u** + ∂V_b/∂**u** = **J**_source

where:
- ρᵤ ∝ lattice mass/volume (inertia from A-109)
- μᵤ ∝ damping coefficient (friction limit from C-309)
- K_χ ∝ bulk restoring (compression penalty)
- Sᵤ ∝ shear resistance (elastic response from A-105)
- V_b is a confining or binding potential (structure TBD)
- **J**_source is the source driving displacement

### 1.2 Compression and Gravity

Define compression:

χ(**x**,t) = -∇·**u**

Then gravity is:

**g**₀ = -α_g ∇χ

This means: **gravity is the gradient of compression**, not a separate force. Any exterior gravity requires an exterior compression gradient.

**Key constraint from diagnostic**: For a compact radial J_r, solving the static equation gives:

χ'(r) = J_r/(K_χ + Sᵤ)

Since J_r is compact (zero for r > R_core), χ'(r) is also zero for r > R_core, which means ∇χ = 0 exterior, hence **g** = 0 exterior.

**Therefore**: To produce exterior gravity, the source must be **non-compact**—it must extend beyond the bound core or have an explicitly specified far-field tail.

---

## Step 2: Constraints from the Bound/Unbound Criterion

### 2.1 What Distinguishes a Bound State

From E-532, a site is bound if:
- I₃ > I₁/2 (sufficient curvature: |Δ**u**|² > |**u**|²/2)
- |**u**| > u_floor (above noise floor)

**Physical meaning**: A bound state has internal structure; it cannot flatten into a free wave.

Only bound sites carry residual orientation density and participate in rear-compression updates.

### 2.2 Finite-Wake Kernel

The minimal finite-wake kernel from E-532 is:

W(r) = e^(-r/σ)/r

where:
- Small σ → short-range coupling (strong-like)
- Large σ → long-range coupling (gravity-like)

The parameter σ determines the **range of the binding influence**.

### 2.3 Residual Displacement

After the last bound site (where curvature falls below I₃ = I₁/2 threshold), displacement that remains propagates as **free field** under E-531 dual-harmonic rules.

**Key insight**: The transition from bound to unbound is not sharp in real systems—it's gradual over a characteristic scale. This suggests the source structure itself must encode this transition.

---

## Step 3: Building the Source Structure

### 3.1 What Must the Source Do?

The source must:
1. **Create a bound core** (establish compression well with sufficient interior curvature)
2. **Produce a controlled wake** (extend compression influence through finite-wake kernel)
3. **Specify exterior amplitude** (the compression gradient exterior must produce observed gravity)
4. **Remain consistent with A-115 physics** (emerge from lattice dynamics, not be imposed)

### 3.2 Candidate Source Form

A physically motivated source should have the structure:

J_r(r) ∝ core profile × wake tail

where:

**Core part**: Localized source that creates the bound state
- Examples: Gaussian, power law, smooth cutoff

**Wake part**: Tail that extends beyond the core to supply exterior response
- The tail cannot be arbitrary—it must be related to the binding kernel W(r)

### 3.3 Connection to the Finite-Wake Kernel

From E-532, a bound core sources displacement according to the kernel W(r) = e^(-r/σ)/r.

This suggests that **the source structure itself should be related to the bound-state response kernel**.

One natural form: if the bound core induces displacement that decays as e^(-r/σ)/r, then a self-consistent source might have the form:

J_r(r) ∝ r/(σ² + r²)^(3/2) or similar power law

This is **not compact**: it extends to infinity, with tail falling as r^(-3) or similar.

### 3.4 The V_b Potential

V_b is described in A-115 as a "confining or binding potential" but its form is not yet specified.

Physical role: V_b should create the energy cost of compressing the field away from the bound state, i.e., keep excitations localized.

**Candidate form**: Harmonic or cubic confinement

V_b(**u**) ∝ k₀|**u**|² or quartic V_b ∝ λ|**u**|⁴

---

## Step 4: Exterior Gravity Requirement

### 4.1 The Newtonian Limit

For exterior distances r >> R_core, A-115 requires:

Φ_OW(r) → -GM_eff/r

|**g**₀(r)| → GM_eff/r²

This means the compression field exterior must behave as:

χ(r) ∼ 1/r for large r

### 4.2 Reconstructing the Source from Exterior Requirement

Working backwards from the desired exterior gravity:

If χ(r) ∼ 1/r exterior, then χ'(r) ∼ -1/r² exterior.

From the static equation χ' = J_r/(K_χ + Sᵤ), this means:

J_r(r) ∝ -(K_χ + Sᵤ)/r² for large r

This is **exactly the source tail needed to produce 1/r² gravity**—a dipole-like tail that falls off as r^(-2).

### 4.3 Matching Interior and Exterior

The complete source must:
- **Interior (r < R_core)**: Create the bound state, generate sufficient interior curvature
- **Exterior (r > R_core)**: Provide J_r ∝ r^(-2) tail to support Newtonian gravity

A source that satisfies both:

J_r(r) = (source amplitude) × [core_profile(r) + e^(-r/σ)/r² tail]

or more precisely:

J_r(r) ∝ A × [r·f_core(r) + e^(-r/σ)/r] for some core function f_core and amplitude A

---

## Step 5: Dimensional Analysis and Amplitude

### 5.1 What Determines the Amplitude?

The overall amplitude A must be set by:
1. **The compression response coefficient** K_χ + Sᵤ (how "stiff" the field is)
2. **The observed gravity magnitude** (e.g., galaxy circular speeds)
3. **Physical length/time scales** (calibration from lattice to meters/seconds)

In dimensional analysis:

χ(r) has dimensions of [1/length]  
J_r has dimensions of [1/time²]  
α_g (gravity coupling) has dimensions needed to make [acceleration] = [α_g × (1/length)]

So: A ∼ [(K_χ + Sᵤ) × gravitational acceleration × length scale] / [time²]

### 5.2 Fixing the Wake Range σ

The parameter σ in W(r) = e^(-r/σ)/r determines:
- σ too small: gravity falls off too fast (like strong force)
- σ too large: gravity spreads too much (like weak cosmological coupling)

**Constraint from E-532**: The bound-to-unbound transition scale should match some intrinsic lattice or field scale.

**Constraint from galaxies**: The rotation curve profile spans:
- Bulge: r ≈ 1 kpc
- Disk: r ≈ 3-20 kpc
- Outer: r ≈ 20-100 kpc

This suggests σ should be comparable to or larger than kpc-scale, i.e., relatively long-range.

For the Milky Way system, if K_L = I (no magnetic modification), the simpler source law (without magnetic path-weighting) may be insufficient at galaxy scale.

---

## Step 6: Self-Consistency Checks

### 6.1 Does the Proposed Source Satisfy the Bound Criterion?

If J_r has the form above, it creates a compression well χ(r) that:
- Has significant interior values where curvature I₃ >> I₁/2 (bound)
- Transitions to shallow exterior where gradient is smooth (boundary layer)
- Falls off as 1/r exterior (unbound residual)

This structure is consistent with E-532's distinction.

### 6.2 Energy Accounting

The compression kinetic energy and potential energy:

E_total = ∫ [ρᵤ/2 |∂**u**/∂t|² + K_χ χ²/2 + Sᵤ |∇**u**|² + V_b] dV

must be conserved under the dynamics (Phase 6B validation confirmed this for small-amplitude cases).

For a bound state with finite-wake tail, the energy distribution:
- Interior compression well: localized high energy density
- Wake region: decaying but sustained energy redistribution
- Exterior: propagating residual (neutrino-like return channel E-529)

### 6.3 Consistency with C-320 Magnetic Coupling

If C-320 introduces K_L = I + κ_R R, the mandatory recovery K_L → I must hold.

The derived source J_r should work for K_L = I first, before testing magnetic modifications.

---

## Step 7: Proposed Constitutive Law

### 7.1 Source Structure (First Derivation)

**Hypothesis**: The source has the form

J_r(r) = A / (σ² + r²)^(3/2) + A_tail · e^(-r/σ)/r

where:
- A is set by the binding energy scale and compression coefficient
- σ is the wake range parameter (order kpc for galaxies)
- The first term creates the interior well
- The second term (or a smooth continuation) provides the exterior 1/r² tail

### 7.2 Binding Potential

V_b(**u**) = (k₀/2)|**u**|² (harmonic confinement, simplest choice)

where k₀ sets the restoring stiffness near the bound state.

### 7.3 Calibration Unknowns

Still requiring independent specification:
- Amplitude scales A, A_tail (set by energy scale and compression response)
- Wake range σ (related to lattice constant and field response scale)
- Coefficients ρᵤ, μᵤ, K_χ, Sᵤ, k₀ (physical calibration)
- α_g (gravity coupling constant)

**Critical**: None of these should be fit to galaxy circular speeds. They should come from:
1. Lattice fundamental scales
2. Laboratory measurements at different scales (atomic, condensed matter)
3. Independent astrophysical tests (lensing, weak clustering, etc.)

---

## Step 8: Falsification and Next Steps

### 8.1 What Would Falsify This?

If the derived source law produces A-115 solutions that:
- Cannot recover the observed exterior Newtonian form at sufficient range
- Require unphysical coefficients (negative K_χ, imaginary σ, etc.)
- Violate energy conservation over dynamical timescales
- Conflict with the bound/unbound criterion predictions

Then the source form must be revised.

### 8.2 Implementation Sequence

1. **Solve A-115 numerically with the proposed J_r(r)** (no galaxy fitting yet)
2. **Verify χ(r) has the required exterior 1/r behavior**
3. **Check energy balance and bound-state stability**
4. **Test against independent scales** (atomic spectroscopy, lensing, etc.)
5. **Only then** score galaxy rotation curves with fixed coefficients

### 8.3 What This Derivation Does NOT Do

- Does not prove the source form is unique
- Does not calibrate coefficients to real physics
- Does not solve the coupled A-115 equations numerically
- Does not predict galaxy rotation curves (that comes after validation)

It establishes the **theoretical structure** within which galaxy physics must fit, derived from One-Wave first principles rather than fitted to data.

---

## Summary and Recommendation

The source-constitutive connection emerges from:
1. **A-115 physics**: gravity = gradient of compression field
2. **E-532 structure**: bound/unbound criterion and finite-wake kernel
3. **Exterior requirements**: Newtonian 1/r² limit at large distances
4. **Self-consistency**: energy conservation and lattice dynamics

The proposed source has a **smooth transition from localized core to power-law tail**, controlled by wake range parameter σ and binding amplitude A.

**Next defensible step**: Implement this source law numerically in A-115, verify the exterior gravity structure, and test against independent data before scoring galaxy candidates.

---

**Word count**: ~2,200  
**Classification**: YELLOW derivation in progress; requires numerical implementation and independent scale validation before astronomy claims
