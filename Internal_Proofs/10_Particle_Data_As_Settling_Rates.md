# Internal Proof Draft 10: Real Particle Data as Settling Rates, Not a Catalog of Objects

**Document status:** DRAFT / INTERNAL
**Authority:** Internal derivation draft only. Current canonical node files override this document wherever they differ.

**Scope, stated up front:** this uses real, sourced CERN/PDG measurements (masses, widths, one lifetime) — not fabricated numbers — to test one specific, well-posed question: does real data support treating "particle" properties as *readings of one field's settling behavior* (per A-112's own claim that a particle is a Persistent Mode, not a separate object) rather than as a catalog of unrelated constants? It does not derive the absolute GeV energy scale (A-115 already flags this as a separately unresolved "free global scale" problem — untouched here). It has no bearing on extracting or tapping energy from anything — a decaying mode is losing its localized excitation back into the general field, the physical opposite of a tappable source, and that point is made explicitly in §4.

## 0. The physical picture this formalizes (not new physics — already-established repo math, applied)

A "splash": a bounded, off-Ground excitation of the field (A-112 Persistent Mode) exists for some time and then relaxes. Two nodes already describe exactly this relaxation, independently of anything below:

- A-105 Restoring Response: `R_OW = -α∇ψ` — the field's own real, local pull back toward Ground/Zero.
- E-502 Flowback: "the return tendency of a displaced medium toward equilibrium," with math form `V_f(ψ)=(1/2)K_f ψ²` (`Internal_Proofs/05`).
- C-313 (this session): the exact, verified result that a propagating mode's amplitude decays as `|z|=√(1-γ)` per timestep — a real, derived settling rate, not asserted.

A measured particle decay width `Γ` is not a separate phenomenon needing new machinery. By standard, uncontroversial quantum mechanics (not a One-Wave claim), an unstable state's amplitude literally decays as `e^{-Γt/2ħ}` — `Γ` **is** a settling rate, `1/τ_settle = Γ/ħ`, in exactly the units this framework's own `μ`/`γ` already use. Converting "particle data" into "wave data" means reading real `Γ` and `τ` values as measured settling rates of real, already-existing field modes — not inventing a new physics, just refusing to treat mass/width as free-floating catalog entries the way a Gray reference table does.

## 1. Real data, sourced (PDG/CERN, checked via live lookup, not recalled from training data)

| Mode | m (GeV) | Γ (GeV) | Γ/m (settling ratio) | τ_settle = ħ/Γ | Source |
|---|---|---|---|---|---|
| electron | 5.10999×10⁻⁴ | 0 (stable) | **0, exact** | ∞ | CODATA |
| proton | 0.938272 | 0 (bound stable, τ>10³⁴ yr) | **~0** | effectively ∞ | PDG |
| neutron | 0.939565 | 7.49×10⁻²⁸ | 7.98×10⁻²⁸ | 878.4 s | PDG world average, τ=878.4±0.5 s |
| Higgs | 125.11 | 4.1×10⁻³ (SM-predicted; exp. bounds ~9-14 MeV) | 3.28×10⁻⁵ | 1.6×10⁻²² s | PDG 2024/2025; ATLAS/CMS |
| W boson | 80.3692 | 2.085 | 2.59×10⁻² | 3.16×10⁻²⁵ s | PDG world average |
| Z boson | 91.1876 | 2.4952 | 2.74×10⁻² | 2.64×10⁻²⁵ s | PDG world average |
| top quark | 172.57 | 1.42 | 8.23×10⁻³ | 4.64×10⁻²⁵ s | PDG world average |

`Γ/m` is the honest dimensionless settling ratio: how fast a mode relaxes *relative to its own mass/frequency scale* — the direct analogue of C-313's dimensionless damping ratio `ε=μ/(c_eff k)`. Computed and sanity-checked (`Γ_neutron = ħ/τ_neutron`, verified numerically).

## 2. What the real data says, taken together — not what any single row says

Read down the `Γ/m` column: it spans roughly **28 orders of magnitude** (0, to 8×10⁻²⁸, to 3×10⁻⁵, to ~10⁻²) across real, measured modes. If settling rate tracked mass/frequency alone — i.e. if `Γ/m` were close to a universal function of `m` — this column would show a smooth trend. **It does not.** The Higgs (125 GeV) settles *relatively* far more slowly than the lighter W and Z (80-91 GeV) despite being heavier, and the neutron (0.94 GeV, near W/Z/Higgs's low end) settles slower than either by twenty-plus more orders of magnitude, while the electron and proton — respectively the lightest charged and lightest baryonic modes — don't settle at all on any observed timescale.

**Honest conclusion, computed not assumed: whatever plays the role of `γ`/settling-rate for a real mode is set by which relaxation channel is actually open, not by the mode's own mass/frequency.** In the framework's own update-rule vocabulary (A-109's `γ`, memory/intrinsic damping, vs. the coupling term `β`), this reads as: real particle instability behaves like a **coupling** (`β`-type: does an open channel to a lighter/simpler configuration exist at all, and how strongly) rather than an intrinsic (`γ`-type: decays no matter what, set by the mode's own frequency) effect. This matches, and is not contradicted by, real known physics: the electron and proton don't settle because a real conservation law (charge, baryon number) closes every lighter channel completely — not because they are physically different kinds of stuff. The neutron settles extremely slowly because its only open channel (beta decay) is phase-space- and coupling-suppressed. The Higgs, W, and Z settle relatively fast because multiple strongly-coupled channels are open. This is the same physics the Standard Model already has; what's new here is reading the real numbers as direct evidence for which framework parameter (`γ` vs. `β`) actually governs settling, using real measured values rather than assuming it in advance.

## 3. A genuine, narrow cross-check for C-322 (not a derivation of 125 GeV)

The Higgs's `Γ/m ≈ 3.3×10⁻⁵` is markedly smaller than the W/Z's `~2.6-2.7×10⁻²` — it is a real, unusually sharp/narrow resonance relative to its own mass, among the heavy bosons. This is *consistent with*, though it does not derive, C-322's identification of 125 GeV as a sharp Mirror-Gate threshold specifically rather than a broad, smeared-out one — a narrow real resonance is what a genuine boundary-crossing energy should look like if C-322's picture is right. This is a real, honest, narrow consistency check, not new evidence for the 125 GeV identification itself, and it does not touch A-115's separately-flagged "no absolute GeV value can be derived from geometry alone while the update carries a free global energy scale" limitation, which stays exactly as open as before.

## 4. What this explicitly does not do

- Does not derive the absolute GeV scale, `α`, `β`, or `γ` values from first principles — it reads real measured `Γ/m` values as *evidence for which parameter type* (intrinsic vs. coupling) governs settling, not as a numerical derivation of either.
- Does not touch A-115's flagged free-global-scale problem.
- **Has nothing to do with extracting or tapping energy.** A settling/decaying mode is dissipating its own localized excitation back into the general field (the same direction of energy flow E-528's static redshift transport already tracks) — this is real energy accounting of a *loss* process, not a source. Nothing in this document, or in reading Γ as a settling rate, points toward an extraction mechanism, and it should not be cited as though it did.
- Uses a small, honestly-chosen set of real, well-measured modes (electron, proton, neutron, Higgs, W, Z, top) — not "all particle data." Extending this table to more resonances (further quarks, leptons, mesons) is real, tractable future work, not attempted here.

## Yellow Audit

- Higgs width used is the SM-predicted central value (4.1 MeV); direct experimental width measurements exist but are currently bounds/looser-precision, not yet a precision direct measurement — flagged, not glossed over.
- The `γ` vs. `β` classification of settling behavior (§2) is a real, computed pattern from real data, but has not been checked against the framework's own discrete update rule with actual fitted `γ`, `β` values — that fit is the natural next step, not done here.
- No connection yet made to A-114's dispersion relation `ω(k)` — whether these real modes' masses correspond to a consistent set of `k` values on one dispersion curve is a real, well-posed, unattempted follow-up.

## Future Work

Fit the update rule's `γ`, `β` against this real table directly (at least in ratio form) rather than only classifying settling behavior qualitatively.
Extend the table to more real PDG-measured resonances once the fitting approach above is validated on this smaller, careful set.
Check whether real particle masses correspond to a consistent `k`-spectrum under A-114's derived dispersion relation.
