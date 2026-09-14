---
node_id: "A-114b"
canonical_name: "Dispersion Trail — Next Ten Questions"
namespace: "NODE"
gate: "YELLOW"
lifecycle: "ACTIVE"
classification: "Trail / Compare-to-Repo"
claim_gate_detail: "YELLOW — questions scored against existing nodes 2026-09-14"
metadata_standard: "I-06"
---

# Node A-114b: Dispersion Trail — Next Ten Questions

Follows A-114 → A-114a → A-110a → C-324.
Compare column is the repo as of this commit. Update when a question moves.

## Q1. When is |z| = 1 for general γ?

**Need:** unit-circle condition on z_±(S,P).
**Repo before this node:** A-114 says general-γ not solved. A-114a gives z_± and notes product P = 1-γ.
**Status:** OPEN algebra. Sketch: |z+ z-| = |P| = |1-γ|. For both roots unimodular you need γ = 0 (or the pair split with one growing — illegal). For 0<γ<1, at least one |z| 
eq 1. Persistent undamped travel wants γ = 0.
**Update this turn:** recorded here. Closed form of arg(z) for γ
eq0 still open.

## Q2. Damped ω(γ,k) from the same quadratic?

**Need:** complex ω = -ln(z)/iΔt.
**Repo:** A-114 Future Work. A-114a points at arg and |z|.
**Status:** OPEN as a plotted formula. Recipe is in A-114a. Not numerically tabulated.

## Q3. Group velocity vs phase velocity?

**Need:** v_p = ω/k, v_g = dω/dk from exact ω(θ).
**Repo:** no hit on "group velocity".
**Status:** MISSING. Added sketch in this node (small-k): v_p ≈ v_g ≈ c_L sqrt(β/2). Exact v_g needs d(atan2)/dθ.

## Q4. Stability bound on β?

**Need:** β range where |z| ≤ 1 for all θ.
**Repo:** A-114 uses β=0.5 in a check. No bound theorem.
**Status:** PARTIAL. For γ=0, C∈[-2β,0], Δ=C(C+4)≤0 if β≤2. Candidate: 0<β≤2 on 1D two-neighbor line. Hex changes the 2.

## Q5. Hex / 2D neighbor C?

**Need:** <ψ_j>-ψ_i on six neighbors.
**Repo:** HEX-SPLIT geometry exists; A-114 is 1D. No C_hex in science nodes.
**Status:** MISSING as algebra. Sketch: six unit vectors, C_hex = β( (1/6)Σ e^{ik·e} - 1 ). Do not steal 1D ω(k).

## Q6. Finite ring (M4, N cells periodic)?

**Need:** k = 2π m / N, m = 0..N-1.
**Repo:** M4 ring is hardware language in RABBIT-HOPPING/build. A-114 infinite line.
**Status:** MISSING as spectrum. Rule: only those N values of θ. N=6 hex ring → six allowed k.

## Q7. Is A-112 Persistent Mode the |z|=1 locus?

**Need:** map ||ψ_{n+k}-ψ_n||<ε to |z|=1.
**Repo:** A-112 operational criterion only. Explicitly defers λ_max<0.
**Status:** PARTIAL. |z|=1 is the linear version of persist. A-112 allows nonlinear persist A-114 cannot see.

## Q8. Detector / source as a boundary, not a twin?

**Need:** drive term or cut at one site.
**Repo:** C-324 + NO_ENTANGLEMENT.md. No forced-site term in the update rule.
**Status:** PRINCIPLE YES, EQUATION NO. Next: ψ_{i0}^{n} forced or read, others follow A-114.

## Q9. Does Cell-0 obey this ω(k)?

**Need:** two FETs + ferrite ≠ a line of cells.
**Repo:** RABBIT-HOPPING/build/CELL0.md. A-114 1D lattice.
**Status:** NO. Cell-0 is one site / one pair. Dispersion starts at Q6 (a ring) or a line. Do not fit β from one D number.

## Q10. Conserved quadratic when γ=0?

**Need:** energy-like sum that stays put if |z|=1.
**Repo:** quadratic memory is in RABBIT-HOPPING software, not derived from A-114.
**Status:** MISSING. Candidate: sum of (ψ_i^n - ψ_i^{n-1})^2 plus neighbor mismatch. Not proven here.

## Score

| Q | In repo before? | After this node |
|---|---|---|
| 1 | mentioned open | sketched, not closed |
| 2 | future work | recipe pointed |
| 3 | absent | small-k v_p≈v_g written |
| 4 | numeric example only | β≤2 candidate 1D |
| 5 | absent in nodes | C_hex sketched |
| 6 | hardware M4 only | N-cell k grid named |
| 7 | A-112 operational | linear |z|=1 linked |
| 8 | C-324 principle | still no forced-site math |
| 9 | Cell-0 separate | explicit NO |
| 10 | software quadratic | candidate only |

Next work after this trail: close Q1/Q4 with a proof, or write C_hex properly in HEX-SPLIT, or put a forced site on the update (Q8). Do not start Q9 curve-fits.
