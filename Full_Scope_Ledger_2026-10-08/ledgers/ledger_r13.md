# Ledger r13

Slice: 1 file. Read in full (562 lines).

## W2 — Gravity as Lattice Deformation from Displacement Field psi   (`W2_GRAVITY_FROM_DISPLACEMENT.md`)
- Gate / lifecycle: Header says "Status: Core derivation of Einstein equations from One-Wave displacement" (L3), "Authority: psi is the only primitive; gravity emerges from div psi (compression)" (L4), dated 2026-10-04 (L5). Part 10 marks results as "What W2 Proves (After Derivation)" with check marks (L522-530), but every implementation step is unchecked (L534-538) and ends "Ready to implement Step 1 (coupled solver)?" (L561). So it is a proposal or derivation sketch with no bench or simulation result. It cites no node IDs (no A-/C-/E-/G- IDs anywhere in the file).
- Upstream: the One-Wave update rule `psi_i^{n+1} = psi_i^n + (1-gamma)(psi_i^n - psi_i^{n-1}) + beta(<psi_j^n> - psi_i^n)` (L18). Standard GR (Einstein equation, L137; Schwarzschild metric, L220).   Downstream / cites: Manuscript 2 (Q1 2027) "Gravitational Field Emergence from One-Wave Lattice: Resolving W2 Metric" (L542-543). It says Higgs and the particle spectrum "follow naturally from criticality and mode structure" (L559). The labels W2 and G1/G2/G3 (L466, L483, L500) are local prediction labels, not G-node IDs. External experiments named: LIGO/Virgo, ET, Vera Rubin, Roman, Euclid, Planck, Gravity Probe B.
- Core claim: "Gravity: div psi (divergence -> curvature)" (L24). "rho_i = div psi_i = (psi_{i+1} - psi_{i-1})/(2a)" (L35). "Curvature is the second derivative of compression" (L94). "Gravity emerges from psi deformation (no separate gravitational field)" (L524). "Cosmological constant is lattice tension (not mysterious)" (L529).
- Equations (verbatim):
  - Update rule (L18) as above.
  - E field = grad psi; mass = omega(k) from the characteristic equation (L22-23).
  - `rho_i = div psi_i = (psi_{i+1} - psi_{i-1})/(2a)` (L35)
  - `T^00 = (1/2)[|dpsi/dt|^2 + (beta/a^2)|grad psi|^2]` (L51). `T^0i = (dpsi/dt)(dpsi/dx^i)` (L61). `T^ij = (beta/a^2)[dpsi/dx^i * dpsi/dx^j - (1/2)delta^ij |grad psi|^2]` (L68)
  - `R_i = lap(div psi_i) = d2psi/dx2 + d2psi/dy2 + d2psi/dz2` (L98-99). `R_mu nu,i = d2psi/dx_mu dx_nu` (L116). `R_00,i = R_11,i = d2psi/dx2` (L121-122)
  - `[R_mu nu,i - (1/2)delta_mu nu R_i] + Lambda delta_mu nu = (8 pi G/c^4) T_mu nu,i` (L152)
  - `lap(div psi_i) - (1/2) lap psi_i + Lambda psi_i = (8 pi G/c^4)[kinetic + stress terms]` (L166)
  - Weak field: `psi_i = psi_0 + h_i`, `div h ~ phi`, `lap phi ~ rho_matter`, `phi = -GM/r`, `g = -grad phi = -GM/r^2` (L183-197)
  - Schwarzschild ds^2 (L220). `Lambda_bare ~ beta/a^2` (L237). `rho_dark = Lambda c^4/(8 pi G)` (L249). `w = -1 + O(1/a^2)`, `w ~ -1 +/- 0.01` (L263-265)
  - GW: `rho(x,t) = rho_0 + rho_GW cos(kx - omega t)` (L279). `d2rho/dt2 - c^2 lap rho ~ 0` (L287)
  - `A_breathing/A_plus ~ (beta - beta_crit) x correction_factor ~ 0.01` (L471-473). `Delta phi_OW ~ (1 - beta/beta_crit)^2 Delta phi_GR` (L489). `w = -1 + (lattice_corrections/Lambda)` (L507)
  - Code skeleton `GravityValidator` (L338-460). The gravity coupling is `geom * 1e-6` (L424), and Lambda is `beta/1.0**2` (L400).
- Point / Path / Field role:
  - Point: none stated. The file has no point rotation, spin, L, attitude, inertia or resistance.
  - Path: Mercury-like perihelion precession (G2, L483-496) and pulsar-black hole orbits are orbit-level (Path) effects. The file does not treat them as a ride or say whether they carry L.
  - Field: compression div psi (L35), the gradient grad psi as the E field (L22), and curvature as lap(div psi) (L98). "Shear waves (curl psi)" are named at L305 as independent of density waves. There is no curl or wake mechanism beyond that.
- Magnetism / gravity / rotation link:
  - Gravity: div psi compression is mapped to curvature, then to the Einstein equation and Poisson's equation, giving `g = -grad phi` with `phi = div h` (L189-197). There is no chi, no K_L, no kappa_R and no R (rotation) term.
  - Magnetism: none stated. Only the E field = grad psi is given (L22). Curl psi appears only as a shear-wave mode (L305).
  - Rotation: the only rotation link is "Frame-dragging corrections (Kerr black holes) might deviate from GR at <1%" (L226). No mechanism is given.
- Open / parked / not-set items:
  - All five implementation steps are open (L534-538).
  - The "metric correction term" in the update rule is unspecified (L331), and the code uses an arbitrary 1e-6 (L424).
  - beta_crit is not defined, and correction_factor is not set (L471).
  - Schwarzschild "emerges" is asserted without a solution (L224).
  - The numbers 1% breathing, w ~ -0.99 to -1.01 and <1% precession are not derived.
  - "Lambda emerges naturally from beta" (L158, L237) is asserted only.
- Conflicts (against the canonical rules):
  1. Gravity law: L189-197 defines gravity as `g = -grad phi`, with `phi = div h` and Poisson/Einstein from div psi compression. The canonical law is `g = -alpha K_L grad chi`, with `K_L = I + kappa_R R`, `R=0 -> A-115 baseline`, `grad chi = 0 -> g = 0`, and kappa_R not set. W2 has no chi, no K_L and no R=0 baseline. It replaces the canonical gravity form with GR/Newton, and its claim that gravity is "div psi" (L4, L24, L524) competes with the canonical one.
  2. Expansion / cosmological constant: L230-268 and L500-516 adopt a cosmological constant / dark energy with a w equation of state and "Standard LambdaCDM" comparison. They frame One-Wave as ΛCDM with a correction, against "w = -1 exactly", using supernova, CMB and BAO tests. The canonical rule is: no expansion, no scale factor, and redshift = E-528 path loss. Dark energy and w are expansion-model quantities. W2 never mentions E-528 or E-530 and implicitly sits inside an expanding-universe framework. (Note: `a` in W2 is lattice spacing, not a scale factor, L35/L237.)
  3. Rotation bookkeeping: L226 suggests frame-dragging (Kerr) as a gravity effect on rotation. That is mild: it is predicted only as a "<1% deviation" and does not explicitly say gravity starts or changes point rotation. It is flagged as an unreconciled link to the canonical rule "gravity does not start or affect point rotation". Frame dragging is not split into Point, Path and Field.
  4. Point, Path and Field are not separated. The node has only a Field (compression or curvature) and treats precession and orbits with no Point or Path split. Under the canonical rule it is incomplete (Point missing, Path not identified as a ride).
  5. Internal and math issues (not canonical rules, but recorded):
     - L98-99 equates lap(div psi) with `d2psi/dx2 + ...`, which is lap psi, not the Laplacian of the divergence.
     - L121-122 gives R_00 = R_11 identically.
     - L355 uses np.gradient(psi) as "compression", which in 1D is d psi/dx, fine. But L323 says `R_mu nu = lap(rho)` while L116 says R_mu nu = d2psi/dx dx.
     - L495 cites "Gravity Probe B" for pulsar or Mercury perihelion precision. That is a misattribution: GP-B measured geodetic and frame-dragging effects.
     - L491: `(1 - 0.99/beta_crit)^2 ~ 0.999` is inconsistent with the stated formula unless beta_crit is chosen specially.
     - Part 10 check marks claim "proves" with no runs executed (L522-538).

## Slice summary
(a) Nodes or chapters bearing on the topic list:
- W2 (`W2_GRAVITY_FROM_DISPLACEMENT.md`) bears on these topics:
  - Gravity: div psi compression, then curvature, then Einstein/Poisson.
  - Lattice: lattice tension as Lambda = beta/a^2, and lattice organization only as nearest-neighbor coupling beta.
  - Mass: omega(k) from the characteristic equation, asserted at L23.
  - Field: compression, gradient, and curl as a shear mode.
  - Path: perihelion precession and orbits.
  - Rotation: only Kerr frame-dragging at L226.
  - No Point (L, inertia, resistance), no magnetism, no locking or bound lattice.
  - The file cites no node IDs.

(b) Conflicts:
1. The gravity law g = -grad phi (phi = div h, Einstein/Poisson) replaces the canonical `g = -alpha K_L grad chi` (no chi, K_L, kappa_R or R=0 A-115 baseline) (L189-197, L4, L24, L524).
2. ΛCDM dark energy, w and the cosmological constant framing imply an expansion framework, against no expansion / no scale factor / redshift = E-528 (L230-268, L500-516).
3. Kerr frame-dragging is offered as a gravity-on-rotation effect with no Point/Path/Field split, unreconciled with "gravity does not start or affect point rotation" (L226).
4. The node is incomplete: Field only, with no Point and no Path-as-ride (whole file).
5. There are internal math or citation errors and overstated "proves" claims (L98-99, L121-122, L323 vs L116, L491, L495, L522-538).

(c) Cross-references outside the slice: none by node ID. The file references only the One-Wave update rule (L18), an unnamed "characteristic equation" for mass (L23), and a future "Manuscript 2". It also states that Higgs and the particle spectrum follow from criticality (L559). For reconciliation, these files are the relevant canonical owners: G-749/G-769 (Point/Path), the canonical gravity rule `g = -alpha K_L grad chi` / A-115, and E-528/E-530 (redshift, which bears on the Λ/dark-energy section).
