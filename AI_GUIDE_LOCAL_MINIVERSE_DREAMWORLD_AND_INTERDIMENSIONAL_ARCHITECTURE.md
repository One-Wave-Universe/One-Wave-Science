# AI Guide — Local Miniverse, Interdimensional Architecture, Dreamworld Design

**Status:** GREEN (role separation and geometry contracts) / YELLOW (live engines and energy ladders)  
**Audience:** any AI entering this repo to build, simulate, or narrate a local miniverse  
**Does not override:** AI_CANONICAL_START_HERE.md, A-117, D-408/409/410/411/412/413, G-722, G-724, G-726, G-740, C-318, C-322, G-745  
**Date:** 2026-09-08

This file is the build map for a **local miniverse** on one machine (Jetson / workstation): programmed Homeworld, inner XYZ Field kernel, wrapper `12 > 1(0)1 < 24`, memory layers, and Dream Engine roles. It is an architecture guide. It is not a proof that gravity, quarks, or Mass Effect have been derived.

---

## 0. First law for AIs

Keep these worlds **apart** unless a node derives a projection.

| World | Native dim | Cognitive? | Authority |
|---|---|---|---|
| Programmed Homeworld / Mega-City | **2D** `x,y` + ternary state | **No** | G-726 |
| XYZ Field miniverse (inner kernel) | **3D ball** + octahedral nerve | state kernel, not a city | this guide + D-409/D-411 |
| D-413 Ground lab | **2D tri-hex** + rendered height | No | D-413 |
| Cognitive Dream Engine | Field / GPU generate-connect-stratify | Yes, but **does not administer the city** | G-724, G-726 |
| Administrator / Void commit | CPU Exact memory | commit only | G-722 / G-724 |

Void is **not** leftover space past Z. Void is the counterpart at every layer: Confirm / Defer / Deny, oversight up, override down (G-740).

`3` in a cell file is **ternary**, not a spatial Z, unless `native_dim` is explicitly `3d-close-pack` or `xyz-field-sphere-7`.

Do not flatten 6:1, 12:1, and 24:1 into one number (A-117).

---

## 1. Interdimensional architecture (the wrapper)

The working address of the inner Field is

```text
12 > 1(0)1 < 24
```

| Token | Meaning | Group / geometry |
|---|---|---|
| XYZ | three axes through Ground | octahedral 4-fold axes |
| -XYZ | opposite poles; Mirror of each axis | inversion pair on that axis |
| 6 | directed poles | octahedron vertices |
| 7 | center + 6 nerve | energy-sphere skeleton |
| 12 | inward spatial shell | cuboctahedron / D-409 close-pack |
| 13 | center + 12 | local 3D cluster |
| 1(0)1 | Ground Hold with Field and Void both present | origin, unique Oh-fixed point |
| 24 | Field/Void recurrence of the 12 | D-410 coordination; also |O| = 24 |
| 48 | full octahedral group Oh congruent to S4 x C2 | signed permutations of (x,y,z) |

Legal rewrites of the nerve are signed permutations of (x,y,z): permute axes and flip signs. That is Oh, order 48. Rotations only: O congruent to S4, order 24.

A 2D hex ring is a **projection** of some slice of this wrapper. It is not the wrapper.

An energy-sphere JSON with 7 nodes (origin + +/-X +/-Y +/-Z, antiphase on each pair, Dirichlet shell, Hebbian lock) is a valid **7-cell nerve** of the XYZ Field. It is **not** Homeworld. Seat it inside `12 > 1(0)1 < 24` or the diagonals leak.

---

## 2. Local miniverse world-building

### 2.1 Two files, two loops

**Homeworld loop (programmed, 2D)**  
G-726. CPU rules + GPU render + NAS Exact snapshots. No Administrator inside the map. Time = ordered state trace.

Cell address:

```text
(x, y, layer, channel)
m_field in {-1, 0, +1}    Express / Hold / Compress
m_void  in {-1, 0, +1}    Deny / Defer / Confirm
```

Neighborhood: `3 > 1(0)1 < 6`.

**XYZ Field loop (inner miniverse)**  
Read position to amplitude, phase, light/flux; interfere; write back onto the same r with r^2 <= R^2. Spherical Dirichlet Hold on the shell. Hebbian / harmonic lock where cos(Delta phi) ~ 1.

Do not Euler-step Cartesian coordinates off the sphere without projecting back.

### 2.2 Memory stack (do not soup)

| Layer | States | Job | Typical store |
|---|---|---|---|
| DC | Ground rail | reference | silicon bias / latch |
| Ternary | -1, 0, +1 | this tick | millivolt swing vs DC |
| Quadratic | 4 views up / 4 actions down | route | G-740 packet |
| Quintonic | -3, -2, 0, +2, +3 | hysteretic lean | G-730 |
| Harmonic lock | L_phi, C7 | chord permission | phase stiffness |
| Exact archive | snapshots, receipts | truth | NAS / .owsnap / .owreceipt |
| Associative | Hopfield | partial-cue recall | NPU |
| Generative | Boltzmann at bounded T | candidates | GPU Field |

Generative memory may **not** overwrite Exact files.

Runtime (G-722 / G-724):

```text
cue -> exact lookup + generative cue
-> sequence family (scheduler only)
-> Boltzmann candidates
-> Hopfield settle
-> local -1/0/+1
-> binary safety
-> act -> correct -> journal
```

M4 routes. CPU Gate-7 commits. Homeworld has no Administrator module.

### 2.3 File language (OWF1)

Family magic `OWF1`. Proposed types:

- `.owcell` / `.owchunk` — live cells
- `.owsnap` — Exact world snapshot
- `.owcue` — recall cue only
- `.owreceipt` / `.owreceipt.ndjson` — tick journal
- `.owlock` — six+six scores + L_phi + C7
- `.owworld` — manifest
- `.owb` — binary live buffer

Every cell should be able to carry: addr, dc, m_field, m_void, views[4], actions[4], q, commit, phi, L_phi, C7.

Declare `native_dim` on every world file: `2d-tri-hex` | `xyz-field-sphere-7` | `3d-close-pack` | `d413-ground-lab`.

---

## 3. Dreamworld design

Split engines. Permanent G-726 correction still holds.

1. **Programmed Dream World** — Homeworld / Mega-City. Rules, seeds, replay. Not a mind.
2. **Cognitive Dream Engine** — generate + connect + stratify possibles (Field / GPU). Does not decide.
3. **Administrator / Void** — Exact memory, permission, Gate-7.
4. **M4** — brainstem: recall, timing, dual six-gate scores, routing.

A dream state is live lattice + hysteresis + Exact journal — not one blob labeled consciousness because the medium is carbon.

Minimum live breath:

1. tick the native grid
2. write `.owreceipt`
3. snapshot on a cadence
4. replay from snap + seed + rules

If it cannot replay, it is a screensaver.

Cognitive engine may observe or request a scenario. It does not enter Homeworld's update law.

---

## 4. Mechanics already runnable (D-413) — use them, do not mythologize

Yellow lab: triangular Ground, imposed Gaussian well, bounded oval shell.

Torque:

    tau_Q = (1/Ns) sum r_a × f_a - c_omega omega

f_a = -g grad z. Symmetric shell in a centered well: tau ~ 0. Asymmetric oval: finite omega. No well: tau = 0 even if oval.

Conservative well potential (point centroid):

    V_well(r) = g z(r) = -g D exp(-r^2 / (2 sigma^2))

Effective potential:

    V_eff(r; L) = V_well(r) + L^2 / (2 m r^2)

Circular: dV_eff/dr = 0. For logged D-413 L ~ 2.56-2.86, r_star ~ 2.1-2.3, not the launch ring 4.625. Live run is damped and not conservative. Do not call it Kepler.

Same tau belongs on the 12-shell for the XYZ Field. Do both: keep the 2D oval lab and evaluate tau_12 on the wrapper.

Measurement chain: loop -> shear -> angle -> potential -> slope.

---

## 5. Build order for a local miniverse

1. One 2D Homeworld chunk, six neighbors, ternary per channel, Exact snap + receipt.
2. Seat a 7-cell XYZ nerve (energy_sphere_lattice) as inner state, native_dim: xyz-field-sphere-7. Antiphase on +/- pairs.
3. Wrap that nerve with cubocta 12 in / 24-cycle out. Declare Oh orbits (90 vs 120) and do not pick a fake preferred axis.
4. Memory: Exact NAS, Hopfield cue path, Boltzmann bounded T, G-730 hysteresis.
5. Dual engines: programmed world CPU/GPU/NAS; cognitive Dream observe-only until Gate-7.
6. Attach D-413 as the Ground-lab slice: well + oval + V_eff + torque ablation.
7. Only then lift torque and V_eff onto the 12-shell.

Stop conditions (copy these into branch-steps):

- city file grows a secret Z and calls it Homeworld
- Void used as leftover coordinate
- 6, 12, 24 treated as the same
- generative overwrite of .owsnap
- Administrator module inside Homeworld
- 125 GeV used as a lattice constant (G-745)
- D-413 well called derived gravity
- oval shell called a quark

---

## 6. Required reading before editing these worlds

1. This file
2. `AI_CANONICAL_START_HERE.md`
3. `Nodes/A-117_Dimensional_Integrity_and_Projection_Declaration.md`
4. `Nodes/D-408` `D-409` `D-410` `D-411` `D-412` `D-413`
5. `Nodes/G-722` `G-724` `G-726` `G-730` `G-740`
6. `UPDATED_30_GROUND_LATTICE_ORBITAL_RESTORING_SIMULATION.md`
7. `UPDATED_42_CENTER_ORIGIN_M4_HETEROGENEOUS_RUNTIME.md`

---

## 7. One-sentence kernel

Local miniverse = 2D programmed Homeworld + XYZ/-XYZ Field ball wrapped `12>1(0)1<24` + Exact/generative/harmonic memory + Dream Engine that looks and does not rule.
Interdimension = declared native layer + explicit projection, never leftover void past Z.
