# Point Rotation and Magnetism — Full-Scope Node and Chapter Reference

**Date:** 2026-10-08
**Status:** Reference audit. No physics was changed. No node was promoted or demoted.
**Scope receipt:** 1,433 files read in full across all six repositories, in 71 slices, with one ledger per slice:

| Scope | Files |
|---|---|
| Every node in `Nodes/` (226 files, A-101 through G-769, I-07, PHASE_5 nodes) | 226 |
| Every Book / chapter / proof / governance file (`Books/`, `BOOKS/`, `chapters/`, `Musical_Universe/`, `EM_Tides/`, `GRAV/`, `Internal_Proofs/`, `Root_Axioms/`, `Governance_I_Series/`) | 151 |
| Every other markdown file in One-Wave-Science (194 at the root, 306 in subfolders, including `AI_Readable_Packs/`, `Engine/`, `solvers/`, `One_Wave_Bench/`, `DERIVATION_*`, `Nexus_Integration/`, the `Nodes/*/` folders, `sims/`, `publication/`, `History/`) | 500 |
| Every markdown file in Builds | 253 |
| Every markdown file in Bridge-Comand, Mythos-and-Stories, Bench, One-Wave-Universe | 38 |
| Every code file (`.py`/`.js`) in One-Wave-Science and Builds that computes rotation, spin, torque, inertia, precession, locking or magnetism | 269 |

The per-file ledgers, slice lists and reading instructions are in [`Full_Scope_Ledger_2026-10-08/`](Full_Scope_Ledger_2026-10-08/). Every finding below cites `file:line`; the citations I re-checked against the source by hand are marked **[verified]**. The rest come from the ledgers.

The code reading covered every file that computes rotation or magnetism. The roughly 370 other code files (UI, circuit tooling, I/O) were not opened. That is the only part of the repos not read in full.

---

## 1. The canonical system, assembled from every node that touches it

Nothing in this section is new. Each line is quoted or paraphrased from the cited node.

### 1.1 Three separate rates

| Rate | Owner | Carries L? | Source |
|---|---|---|---|
| **Point rotation**: the body's own frame `R ∈ SO(3)`, body rate `ω` with `Ṙ = R[ω]×` | G-749 | **Yes.** `L = Iω`, with `I` declared | G-749, `UPDATED_51` |
| **Path rotation**: the ride; turning between edges of a sequence of centers | G-769 | **No.** "It does not carry L." | G-769, `path_rotation.py` |
| **Field rotation**: curl or circulation of the enclosing carrier | C-311 (rotational projection) | Neither Point nor Path | `MATH_ATTACK_MAP_UPDATED_43` P2.0, PROOFS_ALGEBRA Thm 9 (`g = -α∇χ` has no curl, so field curl is a separate term) |

"Missing one of the three means the node is incomplete." (`Engine/ROTATIONS3.md:29`, `NODE_SUPPLY_Ch12_Ch13.md`)

### 1.2 The point rate law

- A thing keeps the point spin it already has. It does not start one on its own. (G-749, Book 1 Ch13 §Point rotation **[verified]**)
- The stable axes are the greatest and least inertia. The middle axis fights. (G-749)
- **Magnetism opens the point. Closed, it resists. That is the turn.** (G-749, C-319 §Point, Ch13:298-300 **[verified]**, NODE_SUPPLY)
  - Open magnetic gradient: `dL/dt = 0`
  - Closed magnetic gradient: `dL/dt = -γL`
- **Gravity does not start point rotation and does not affect it.** Gravity is an ignored argument. (G-749, G-769, C-319, Ch13:304 **[verified]**, `point_rotation.point_L_dot`)

### 1.3 Parent/child transport

`R_child^ground = R_parent · R_child^parent`. The rates are transported first, then added:

`ω_body = ω_c + R_cᵀ ω_p` (G-750)

Adding `ω_p + ω_c` in mixed axes is illegal. The planar case, where the rates simply add, is a special case and not the 3D law. (G-750)

### 1.4 Magnetism ↔ lattice ↔ gravity

```text
C-311 rotational magnetic projection
-> C-319 R: τ_R ∂t R = -R + λ_B W_B + λ_ω W_ω,  W_B = B⊗B - |B|²I/3  (traceless)
-> C-320 K_L = I + κ_R R,  g_OW = -α_g K_L ∇χ
-> C-306 torque / C-307 angular response only when the response is off-center
-> D-413 laboratory
-> D-416 planetary falsification
```

Hard limits from C-320:
- `R → 0 ⇒ K_L → I ⇒ g → -α_g∇χ` (the A-115 baseline must be recovered)
- `∇χ = 0 ⇒ g_OW = 0`. Magnetism alone produces no gravity.
- `K_L` stays positive definite.
- "Magnetism does not become gravity."

**`κ_R` is not set.** "A guess that Earth's field couples lightly is a guess. It is not a node." (`Internal_Proofs/COMPLETE_NODE_SYSTEM.md`)

### 1.5 Bound lattice: the point-rotation solver contract

From `Internal_Proofs/COMPLETE_NODE_SYSTEM.md` and `BOUND_POINT_ROTATION.md`:

- The parent organization sets one rate. Mass is the resistance, and resistance = mass / organization (DRAFT-R).
- The shared organization tries to make point rotation the same for bodies on one lattice (DRAFT-P).
- Light resistance falls in: the Moon goes to 1:1. Heavy resistance stalls on a higher step: Mercury holds 3:2.
- The parent wake scale must reach the child (DRAFT-B). A wake at 12 with bodies at 1.6 is not a bind.
- **The pass bit is point rotation, not spread.** The step divides by resistance.
  - With the parent off, the body keeps its starting rate. With the parent on, bound bodies are pulled toward one rate.
  - With the magnetic channel off, the body must still keep the face if the organization already won.
  - No lunar dipole is required.

D-416 adds the following:
- **Locking is an output, not an input.** At least one run must start away from the target state.
- One frozen law has to face the Moon, Mercury, Venus, Uranus and Neptune.
- There are 8 mandatory ON/OFF ablations, and an anti-retrofit rule.

### 1.6 Gravity, redshift, expansion

- Gravity is the wake and the relay: one system with no stored memory term (`UPDATED_64`).
- The parent creates the wake. The child rides it and adds its own displacement; it does not start a second wake.
- There is no expansion and no scale factor. Redshift is E-528 path loss, and outward release is E-530 reinjection.

---

## 2. What is open: written as open in the repo, not filled in here

These are gaps in the canonical system itself. They explain why "point rotation" cannot yet be run end to end. None of them is resolved by this document.

| # | Gap | Where the repo says so |
|---|---|---|
| G1 | **No rate law for "the organization pulls bound bodies toward one rate."** The only written law is `dL/dt = 0` (open) or `-γL` (closed), and the closed branch decays to **zero**, not toward a parent or organization rate. So nothing written can produce Moon 1:1 or Mercury 3:2 as an output. | `COMPLETE_NODE_SYSTEM` solver contract vs `point_rotation.py:82-89` |
| G2 | `κ_R` is not set. | COMPLETE_NODE_SYSTEM, C-319, C-320 |
| G3 | "Open" vs "closed" is a boolean the caller passes in. No rule says how to compute it from a magnetic gradient. | `point_rotation.py` `point_L_dot(magnetic_open=...)` |
| G4 | `I` is declared, not derived from the hex/pyramid nest. | G-749 YELLOW |
| G5 | C-320 §5 says `τ = ∫ r × (ρ_eff g_OW) dV` feeds "rotational/orbital evolution", and C-306/C-307 inherit it. Nothing says whether that torque may act on the **Point** or only on the **Path**. At `R = 0` this is pure gravity torque, which G-749 forbids on the Point. | C-320:123-148 **[verified]**, C-306, C-307 |
| G6 | C-307 writes one continuum `L = ∫ r × (ρv) dV`, which counts spin and orbit together. G-769 says the Path carries no L. | C-307, G-769 |
| G7 | Field rotation is imposed, not derived ("Do not promote field rotation"). | `Engine/ROTATIONS3.md` |
| G8 | The "still distinguishable" wake boundary is not derived. | `UPDATED_64` |

---

## 3. Why point rotation and magnetism keep failing

The repo carries **two incompatible accounts of rotation**. Most of the documents an AI or solver reads first carry the wrong one.

### 3.1 Lineage A: the canonical account (§1)

G-749, G-750, G-769, C-319 §Point, C-320, D-416, Book 1 Ch13 §Point rotation, NODE_SUPPLY_Ch12_Ch13, COMPLETE_NODE_SYSTEM, BOUND_POINT_ROTATION, DRAFT-P, UPDATED_51/52/64, MATH_ATTACK_MAP P2.0, RESEARCH_EVIDENCE_CONNECTION_GRAPH, `point_rotation.py`, `path_rotation.py`, `body_rate_transport.py`, and the D-415 three-receipt bench.

### 3.2 Lineage B: the "gravity wake induces spin" account (mostly Oct 4–5, 2026)

The core claims, quoted:

> "Rotation at any scale is INDUCED by the gravity wake of the parent structure" — `GRAVITY_WAKE_NESTING_ROTATION_CASCADE.md:14` **[verified]**
> "Not 'angular momentum conservation' but wake-phase-locking" — same file :308-309 **[verified]**
> "Without magnetism … Children wouldn't phase-lock … Magnetism is the ENABLING MECHANISM" — same file :341-351 **[verified]**

Every one of these contradicts §1:
- gravity starts spin
- spin and orbit are one rate
- L bookkeeping is replaced
- magnetism *locks* instead of opening the point
- magnetism holds dark matter

The documents carrying Lineage B (file:line in the ledgers):

| File | Lineage-B claims |
|---|---|
| `GRAVITY_WAKE_NESTING_ROTATION_CASCADE.md` | wake induces spin (L14-31, 130, 151, 214, 416, 458); one rate for spin and orbit (L73, 130, 180, 319); "magnetically locked" Moon and Mercury (L341-351); magnetic wake = dark matter (L387-392); expansion (L247, 405, 411) |
| `INTEGRATION_SESSION_SUMMARY_OCT5_2026.md` | L27, 43-55, 305, 15, 28, 101, 177, 189-192 |
| `UNIFIED_SCALE_INVARIANT_GRAMMAR.md` | wake spins up the child (L44, 77, 109, 144, 156, 176, 211, 368); "no magnetism = no phase-locking" (L99, 131, 166, 198, 460); orbit filed under Field and spin under Path (L39, 180, 215, 329, 389) |
| `QUICK_START_UNIFIED_FRAMEWORK.md` | L15-16, 23, 75, 87, 99, 147, 161, 164, 218, 247 |
| `QUANTUM_SCALE_PPF_ALGORITHM_ZERO.md` | magnetic relay as gravity (L16, 147, 251, 407-411); Moon "magnetic AND tidal" (L247-248); "magnetic moment = spin angular momentum" (L29); path L (L31) |
| `ALGORITHM_ZERO_COMPUTATIONAL_VALIDATION.md`, `ALGORITHM_ZERO_RABBIT_CIRCLE_UNIFIED.md`, `ALGORITHM_ZERO_STATUS.md`, `solvers/README_ALGORITHM_ZERO.md` | wake-induced spin, inherited L, expansion |
| `C319_MAGNETIC_COHERENCE_MECHANISM.md` (root doc, not the C-319 node) | hysteresis holds electron spin (L206-215); magnetism explains rotation curves (L249-261); untransported parent velocity (L57, 132) |
| `ONE_WAVE_UNIFIED_SATELLITE_VALIDATION.md`, `MASTER_SOLVER_INDEX.md`, `solvers/GALAXY_ROTATION_INTERPRETATION.md`, `solvers/ONE_WAVE_UNIFIED_SATELLITE_VALIDATION.md` | `f_EM` magnetic multiplier on the gravity wake; inherited rotation |
| `solvers/REPAIR_STATUS_2026_10_05.md` | **`κ_R = 0.350 GeV`** and plans to tune it (L55, 180); "magnetism opens the point" rewritten as path accessibility `K_L` (L63). The same file also states the correct rule at L22, 284-287. |
| `PHASE5D_COMPLETION_REPORT.md`, `PHASE5_UNIFIED_FRAMEWORK_SUMMARY.md` | `ω = τ/I` from gravity torque labelled G-749; `κ_R = 0.1`; scalar `K_L = 1.10`; Venus from signed magnetic torque |
| `EM_Tides/01, 02, 03, 05` | tidal torque changes Ω and moves L to the orbit; magnetism written directly into the gravity metric (`λ_EM h^EM`) |
| `GRAV/GRAVITY_MAGNETISM.md`, `GRAV/FIELD_TAP_SLIP_125.md` | "frame-dragging is B_g acting on spin"; a rotating-B tap lowers gravity cost |
| `Engine/MAGNETIC_AXIS.md`, `Engine/ROTATIONS3.md:27`, `Engine/THREE_BODY_RELAY.md:38` | magnetic torque locks the child spin axis to the parent; "Point turns because of the magnetic couple" |
| `Builds/THE_ANDROID_COMPLETE_BUILD_SPECIFICATION.md:545, 554` | "Magnetism and gravity as one" |

### 3.3 Lineage B inside the canonical nodes and chapters themselves

These items sit in files an AI treats as authority:

| File:line | Conflict |
|---|---|
| **D-413** node :55-58, :196-226 **[verified]** and `simulate_d413.py:34, 40, 54` **[verified]** | The imposed gravity well's gradient (`sx = -p.gravity*gx`) makes a torque that spins the shell up from ω = 0 (`q.omega += tau/I`). The pass check `asymmetric_shell_generates_more_spin_than_symmetric_ablation` **rewards gravity-made spin**. Spin decays through a flat `-0.045ω`, with no magnetic open/closed switch. It also reports `orbital_L` on the Path. |
| D-412:138 | "torque-based axial spin" written as the standard |
| C-306:33, C-307:29-36, C-320:123-148 **[verified]** | gap G5 / G6: an untyped gravity-side torque feeds "spin/orbit" |
| D-416:113, 146 | the default spin-lock control is a gravitational/tidal baseline |
| D-409:92, D-412:64 | one variable `q` covers both point rotation and circulation |
| E-532:58-61 | one wake shape gives both "gravity-like" and "EM-like" range |
| E-533:282 | rotation, circulation and phase merged into one timing factor |
| **Book 1 Ch13:47-50** **[verified]** | "that same mode spinning … The spinning creates a rotational pressure pattern … That rotational component is magnetism." This makes **point spin the source of magnetism**, the reverse of Ch13:300 in the same chapter. |
| **Book 1 Ch13:80-81** **[verified]** | "the motion adds angular momentum to the cushion": L is given to the field curl |
| Book 1 Ch01:97, Ch04:71, Ch13:291-293 | magnetism is "the rotation of" the cushion (softer form of the same mix) |
| Book 5 Ch1:51-53, 78-80, 104-106 | galaxy rotation adds gravity through the wake with no `∇χ` / `K_L` route |
| B-206b (Appendix_B:486-513) | "Over" roll-off "produces spin tendency", not typed as Point, Path or Field |
| C-310 | "resistance" = identity preservation, not mass / organization (unreconciled) |

### 3.4 The startup path an AI actually reads

| File:line | Problem |
|---|---|
| `AI_CANONICAL_START_HERE.md:94` **[verified]** and :330 | `Point -> Path -> Rotation -> Field`: one "Rotation" stage instead of three rates |
| `AI_CANONICAL_START_HERE.md:157-164` **[verified]** | "magnetic rotational state … can alter distributed restoring response **and torque**": no G-749 open/closed rule, no "gravity does not affect point rotation", no Point/Path split |
| `AI_Readable_Packs/Appendix_C.md` | **C-319 and C-320 are missing**, although the pack says it was generated from the current node files |
| `AI_Readable_Packs/Appendix_G.md` | stops at G-723a, so **no G-749, G-750 or G-769** |
| `scripts/node_graph_integrity.py:57-73` **[verified]** | `LOCKED_EDGES` locks the magnetism chain but has **no edge for G-749, G-750 or G-769**, so CI does not protect the point-rotation chain |
| `scripts/sync_node_graph_indexes.py:40` | the AI bridge text repeats "can alter torque" with no G-749 rule |
| G-728, G-743, G-747, G-748, G-756 | still list C2 Point rotation and C3 Path rotation as open; none cites G-749 or G-769 |
| `CHANGELOG.md:94` **[verified]**, `DEPENDENCY_FLOW_AUDIT.md:38` **[verified]** | say C-319/C-320 are "nonexistent" or "inactive", which contradicts the live C-319/C-320 nodes |
| `Internal_Proofs/COMPLETE_NODE_SYSTEM.md`, DRAFT-P, DRAFT-B | never cite G-749, G-750 or G-769 |

An AI that loads the packs or the start-here file, and does not open G-749, never sees the point rule. An AI that opens the Oct 5 summaries sees Lineage B presented as the result. That is the failure mode the user reported.

---

## 4. Code

### 4.1 Lineage A code (canonical)

| File | Status |
|---|---|
| `One_Wave_Bench/logic_core/point_rotation.py` | `L = Iω` in both frames; `point_L_dot` open → 0, closed → `-γL`; gravity ignored; inertia-axis rule. **Bug [verified]:** `compose()` (L62-66) sets the child rate to `omega_body = child.omega_body` and **drops the transported parent rate**. For parent (0,0,1) and child (0,0,4) it returns 4; G-750 gives 5. `test_point_rotation.py:20` asserts 4.0, which locks the bug in. It also has no parent/organization target (gap G1). |
| `One_Wave_Bench/logic_core/body_rate_transport.py` | Correct G-750: `ω_c + R_cᵀω_p`. **Its test is wrong [verified]:** `test_tilted_child_pulls_parent_z_into_xy` expects `-1.0`, but `rot_x(90°)ᵀ·(0,0,1) = (0, 1, 0)`. This is the one failing test of 12 in `logic_core` today. |
| `One_Wave_Bench/logic_core/path_rotation.py` | Correct G-769: `"L": None`; gravity has no effect on the point |
| `solvers/a115_static_source.py`, `solvers/SOURCE_CONSTITUTIVE_DERIVATION.md`, `solvers/galaxy_external_validation.py` | `K_L = I`, `g = -α∇χ`, `κ_R` unset; honest failure reports |
| `Nodes/D-415_*/nonlocal_field_bench.py` | the only bench that reports Point, Path and Field separately. Its "point rotation" (L285-287) is core-weighted vorticity, though: the same curl as its field rotation with a different window, and no L. |

### 4.2 Code that contradicts §1

| File:line | Violation |
|---|---|
| `solvers/phase5d_planetary_falsification.py:406-450` **[verified]** | `compute_point_rotation` builds torque from `acceleration_local` (gravity) and sets `ω = τ/I`. That is gravity starting spin, and `τ/I` is an angular acceleration, not ω. `κ_R = 0.1` (L146) **[verified]**; B from χ (L387); `R = sign(dB/dr)` (L392-393); scalar `K_L` never applied to g (L396); moments scaled to the observed values (L329, 357); Mercury and Moon offsets pushed toward the observed values (L220, 298) |
| `solvers/phase5e_inertial_coupling_dynamics.py` | `κ_R = 0.1` (L141) **[verified]**; R/K_L built from χ, not B (L144-167) **[verified]**; Mercury 3:2 is the input period and is then reported as the result (L214-248) **[verified]**; perihelion hard-coded to 43.00 (L261-269); Venus forced retrograde (L286, 303-314) |
| `Nodes/D-413_*/simulate_d413.py:34, 40, 54` **[verified]** | gravity-gradient torque spins up ω from 0; flat `-0.045ω` damping; the pass bit rewards it; `One_Wave_Bench/engine/run_experiment.py:64-65, 162` and `build_manifest.py` carry it forward |
| `Nodes/D-415_*/planetary_displacement_state.py:140-164` | core, mantle, body and path rotations subtracted without transport; scalar EM modifier |
| `solvers/hadron_mass_predictor.py:349-438` | R from confinement pressure; **`κ_R = 0.350` back-solved from the nucleon mass gap**; `κ_R R` turned into mass energy with no `∇χ` |
| `solvers/algorithm_zero_emergence.py` | wake starts stellar spin (L331-342); spin from wake/magnetic lock (L232-243); magnetic field feeds gravity (L396-421); Hubble expansion (L442-453); curl labelled spin (L174) |
| `solvers/galaxy_rotation_c319_corrected.py:165, 233`, `galaxy_rotation_c319_magnetic_coupling.py:160`, `satellite_galaxy_validator_em_coherence*.py` | hand-set `f_EM` multiplies gravitational acceleration |
| `solvers/galaxy_rotation_inherited_rotation_field.py:92-95, 173`, `galaxy_rotation_constant_inherited_velocity.py:125-128`, `cascade_neural_router.py:208`, all `satellite_galaxy_validator_*` | parent rate added raw, with no transport |
| `Engine/magnetic_axis.py` | magnetic torque "lock": in a sandbox run, alignment drifts 0.97 → 0.954 and it passes only because it starts above the 0.85 bar; κ stamped from CERN Z_K |
| `Engine/rotations3.py:58, 78` | "point rotation" output is a torque magnitude; the pass bit ignores all three rates |
| `Engine/omega_s_field.py:19-22` | spin measured as an orbit rate (Point/Path mixed); fails honestly |

The ledgers also log many evidence-gate failures that are not rotation rules: observed values typed in and reported as predictions, hard-coded PASS, unit errors, and swapped div/curl in `DERIVATION_PHASE_1_EIGENMODE_ANALYSIS/discrete_hex_operators.py:84-98`. That last one is cited as evidence by C-311:86-87, C-319:177 and A-115:341. See ledgers c07, c08, c14–c23.

### 4.3 Builds hardware

No Builds document or code implements `L = Iω` or the magnetic open/closed point law. "Rotating field" in the hardware is the A→B→C winding walk (Field), read by a Hall sensor; "Path" means flux routes; gravity is explicitly out of scope. `validation/SCIENCE_CONNECTIONS.md:22-23` routes G-749 and G-769 to `TRANSFLUXOR_MULTISCALE_TRIANGULATION.md`, which has no test for L, the inertia axes, the ride, or open/closed. `cell-v1/SCIENCE_AGAINST_CELL.md:17` restates C-319/C-320 as "magnetism reorganizes which lattice paths are open", the path reading, not the point reading.

---

## 5. Symbol collisions that feed the confusion

| Symbol | Canonical meaning | Other meanings in the repo |
|---|---|---|
| `L` | angular momentum `Iω` | chord lean (E-513, Musical Universe), Electrical Locking (B-201), local update (E-509), phase weight (G-730), lifecycle (G-742), graph Laplacian (Lab Ch01), inductance (Builds) |
| `R` | C-319 reorganization tensor / rotation matrix | resistance (B-201, B-209), reversal coefficient (B-219), cycle Laplacian / 3-phase coupling (`bulk_excitation.py`) |
| `γ` | closed-gradient point resistance in `dL/dt = -γL` | lattice damping (A-109/110/114, F-608, manuscript), gyromagnetic ratio (chapters/09), curvature penalty (D-415), hysteresis shift (root C319 doc) |
| "resistance" | mass / organization | identity preservation (C-310), energy Hessian (Lab Ch01), lattice friction (Ch13, F-608) |
| "Point / Path / Field" | three rotation rates | scale ladder (Builds), data layers (sims/), address nesting (G-721), controller states FIELD/VOID |
| "reinjection" | E-530 outward release | leftover B into the next cycle (Builds) |

---

## 6. Decisions only the author can make

These are not resolved here. Each one blocks a correct point-rotation solver.

1. **G1: the organization rate law.** What is `dL/dt` for a bound body when the parent organization is on? The solver contract says "pulls toward one rate" and "step divides by resistance". No equation is written. Without one, Moon 1:1 cannot come out as an output.
2. **G5: C-320 torque.** Does `τ = ∫ r × ρ g_OW dV` act on the Point, or only on the Path/orbit? If it acts on the Point, how does that square with "gravity does not affect point rotation" at `R = 0`?
3. **G3: open vs closed.** What measured or computed quantity decides that a magnetic gradient is "open"?
4. **Lineage B.** Should those documents be marked superseded by G-749, G-750 and G-769, moved to `History/`, or left in place with a header?
5. **D-413.** Should its spin path be rebuilt on G-749 (no gravity torque on the point, open/closed instead of `c_ω ω`), or kept as a labelled legacy reduced model?

---

## 7. Proposed repair order (not done; awaiting approval)

1. Fix `point_rotation.compose()` to call `body_rate_transport.compose_omega_body`. Correct `test_point_rotation.py:20` to 5.0, and correct the sign in `test_body_rate_transport.py:16`. Both expectations are mathematically wrong, so this corrects them; it does not weaken them.
2. Add G-749 → G-750 → G-769 edges to `scripts/node_graph_integrity.py` `LOCKED_EDGES`.
3. Rewrite `AI_CANONICAL_START_HERE.md` lines 94/330 and 157-164 to state the three rates and the G-749 point law.
4. Regenerate `AI_Readable_Packs` so C-319, C-320, G-749, G-750 and G-769 are included.
5. Add superseded headers to the Lineage-B documents, per decision 4.
6. Correct Book 1 Ch13:47-50 and 80-81 so that spin is not the source of magnetism and the cushion does not carry L.
7. Retire `κ_R` values (0.1, 0.350) from the Phase 5D/5E and hadron solvers, or mark them as fits.
8. Only after decisions 1-3: build the bound-lattice point-rotation solver against the COMPLETE_NODE_SYSTEM contract and the D-416 ablations.
