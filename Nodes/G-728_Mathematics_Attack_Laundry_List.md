# G-728 — Mathematics Attack Laundry List

**Status:** Active execution queue  
**Gate:** Tasks inherit the gate of their evidence  
**Dependencies:** Updated 43, G-727, A-114, B-216, C-313, C-318, D-408–D-410, E-523, G-713, G-724–G-727  
**Authority:** `MATH_ATTACK_MAP_UPDATED_43.md`

## How to use this list

Every checked item must produce:

1. equations with symbols and units declared;
2. executable code and deterministic configuration;
3. raw results and plots;
4. comparison against the strongest applicable control;
5. failed cases and parameter limits;
6. a Brick recommendation: Gray, Yellow, Green, Brown, or Red.

A simulation picture alone does not complete a task. A matching number or
visual pattern alone is not a derivation.

## A. Primitive logic and commitment

- [x] **A1 — Six-route finite set:** implement `2 choices x 3 moves = 6`.
  Artifact: `One_Wave_Bench/logic_core/six_route_logic.py` and six tests.
- [x] **A2 — Six-route transition graph:** candidate laws, reachability,
  reversibility, absorbing states, and topology are executable. Current result:
  product graph = 7 edges/diameter 3; center-gated flip = 5 edges/diameter 3;
  movement-only = 4 edges and disconnects YES from NO. Physical law selection
  remains open. Artifacts: `route_transition_graph.py` and its tests.
- [x] **A3 — Mirror operator:** implemented as a continuous phase rotation with
  a finite six-route projection. The projection preserves YES/NO, reverses
  DOWN/UP over a half-cycle, fixes projected Hold, and is involutive. A full
  phase cycle returns to reference. Center crossing and Hold are independent
  measurements. Artifact: G-729 and `mirror_operator.py` with eight tests.
- [x] **A4 — Commitment map:** implemented a bounded latent coordinate with
  phase-gated signed drive and Schmitt hysteresis, producing only
  `{-3,-2,0,+2,+3}`. Single weak receipts cannot create full commitment;
  repeated aligned history can. Choice-oriented versus absolute-axis movement
  semantics remains an explicit comparison task. Artifact: G-730 and
  `commitment_map.py` with nine tests.
- [x] **A5 — Ground and Hold separation:** logical Ground `(0,0)`, YES/HOLD,
  NO/HOLD, center residence, center crossing, turning-point Hold, and coherent
  phase-locked Hold now emit separate receipts. Zero speed alone is not a
  coherent Hold. Artifact: G-731 and `ground_hold_classifier.py` with nine tests.
- [x] **A6 — Hysteresis noise audit:** seeded Monte Carlo tests quantify
  chatter and false full-entry events. Hysteresis sharply reduces partial-state
  chatter but cannot prevent rare excursions accumulated over long windows;
  full commitment needs dwell/multi-sample confirmation. Artifact: G-733 and
  `noise_hysteresis_audit.py` with seven tests.

## B. Center-origin oscillation and six recursive gates

- [ ] **B1 — Asymmetric oscillator:** solve and sweep
  `x_ddot+2*zeta*omega0*x_dot+a*x^3-b*x-h=u(t)`.
- [ ] **B2 — Center geometry:** test whether the shared middle is a point,
  finite band, crossing surface, limit-cycle section, or slow manifold.
- [ ] **B3 — Six-gate extraction:** derive Begin, coherent Build, Hold/Mass
  Effect, unstable Build/heat, Break, and Loop from measured trajectories.
- [ ] **B4 — Build-before-Break condition:** calculate minimum stored state,
  threshold, and phase required for a valid Break.
- [ ] **B5 — Delayed noisy threshold:** extend B-216 with delay,
  quantization, stochastic input, and hysteresis; report stability regions.
- [ ] **B6 — Phase-shifted return:** measure return-to-reference error and
  distinguish Loop from exact reset.

## C. Recursive Point–Path–Field mathematics

- [ ] **C1 — PPF state schema:** implement
  `X_s={P_s,gamma_s,F_s;X_(s-1,1),...,X_(s-1,n)}` with units and frames.
- [ ] **C2 — Point rotation:** derive intrinsic/local orientation and its
  carried angular-momentum receipt.
- [ ] **C3 — Path rotation:** derive turning, orbit, circulation, curvature,
  and transport of the Point frame along a Path.
- [ ] **C4 — Field rotation:** derive Field circulation/curl and its boundary
  conditions without replacing it with Path rotation.
- [ ] **C5 — Point-containing-PPF:** calculate nested internal PPF inside a
  localized structure.
- [ ] **C6 — Path-containing-PPF:** calculate transported subpaths and their
  connection/frame terms.
- [ ] **C7 — Field-containing-PPF:** calculate multiple contained PPF systems
  and their aggregate Field receipt.
- [ ] **C8 — Nested rotation ledger:** prevent intrinsic, orbital, frame, and
  enclosing-Field rotations from being counted twice.
- [ ] **C9 — PPF scale maps:** define Micro, Small, Middle, Large, and Macro
  transfer operators and projection errors.
- [ ] **C10 — PPF ablation:** remove Point, Path, and Field rotation one at a
  time and measure which observables fail.

## D. Dimensional Mirror Gates

- [ ] **D1 — 2D graph:** construct adjacency, incidence, and Laplacian for
  `3 > 1(0)1 < 6` triangular/sixfold coordination.
- [ ] **D2 — 3D graph:** construct and compare FCC and HCP twelve-neighbor
  realizations of `6 > 1(0)1 < 12`.
- [ ] **D3 — 4D recurrence graph:** define what the 24 states represent in
  `12 > 1(0)1 < 24`; do not call a static 3D object four-dimensional.
- [ ] **D4 — Spectral comparison:** measure eigenmodes, gaps, isotropy error,
  mixing, recurrence, and robustness across D1–D3.
- [ ] **D5 — `T_2to3` transform:** identify preserved invariants, added degrees
  of freedom, lost information, and inverse/projection error.
- [ ] **D6 — `T_3to4` transform:** repeat the same derivation for recurrence.
- [ ] **D7 — Count-versus-mechanism test:** show why 3/6/12/24 recur; reject
  count matching if no lawful transform exists.
- [ ] **D8 — Nine-cell folding:** compare 3x3, folded sheet,
  ring-plus-center, and graph-optimized vascular embeddings.

## E. Field equation, dispersion, and invariance

- [ ] **E1 — Exact damped roots:** finish A-114 without the small-`k` or
  small-damping assumption.
- [ ] **E2 — Regime map:** classify propagating, overdamped, unstable,
  recurrent, and persistent parameter regions.
- [ ] **E3 — Numerical dispersion:** measure phase/group velocity and
  anisotropy for each selected 2D and 3D stencil.
- [ ] **E4 — Lorentz conflict:** transform the damped Field equation and
  quantify preferred-frame observables instead of hiding them.
- [ ] **E5 — Emergent invariant limit:** calculate whether an approximately
  relativistic regime exists and state its error bounds.
- [ ] **E6 — Stable nonlinear modes:** find localized recurrent modes using
  continuation, Floquet multipliers, Lyapunov spectra, and perturbation tests.
- [ ] **E7 — Measurement windows:** prove normalization, overlap behavior,
  translation covariance, and resolution limits for Field observables.

## F. Micro structure and Mass Effect

- [ ] **F1 — Four-interaction state:** formalize knot/vortex, electrical
  shell, Mirror-Gate pressure/resistance, and Boundary-Tension Weave.
- [ ] **F2 — Work metric `W`:** derive the positive-semidefinite C-318 block
  metric with cross-couplings and declared units.
- [ ] **F3 — Translation response:** move one stable profile relative to
  Ground and calculate finite, anisotropy-aware carried-pattern response.
- [ ] **F4 — Four-interaction ablation:** remove every diagonal and
  off-diagonal block and report the change in recurrence and response.
- [ ] **F5 — Absolute scale:** derive rather than fit the conversion between
  dimensionless Field energy and measured energy/mass scales.
- [ ] **F6 — Shell spectrum repair:** compare fixed-radius eigenmodes, radial
  modes, nonlinear action, and boundary-work spectra.
- [ ] **F7 — Micro PPF:** model quark-vortex candidates, proton knot, and EM
  shell as nested PPF without claiming validation before comparison data.

## G. Magnetic and phase hardware

- [ ] **G1 — LLG reference cell:** simulate DC bias plus quadrature AC drive.
- [ ] **G2 — Ternary readout:** test whether DOWN/HOLD/UP are dynamically
  separable under damping, noise, and temperature.
- [ ] **G3 — Four-state phase memory:** test classical phase-memory stability;
  reserve `ququart` for demonstrated coherent four-level control.
- [ ] **G4 — Magnon transport:** calculate dispersion, injection mismatch,
  attenuation, broadening, reflection, and inter-symbol interference.
- [ ] **G5 — Readout:** compare MTJ and ISHE signal, energy, latency, and error.
- [ ] **G6 — Complete energy budget:** include bias, RF, injection, damping,
  readout, control, and cooling at equal throughput/error to controls.

## H. Orbital mechanics and three-body program

- [ ] **H1 — Newtonian control:** implement a validated barycentric N-body
  integrator with convergence and conservation tests.
- [ ] **H2 — Relativistic control:** add the established post-Newtonian or
  relativistic reference required by each target system.
- [ ] **H3 — One-Wave correction interface:** require
  `a_i=a_Gray,i+delta_a_OW,i`; acceleration is bookkeeping, not a declaration
  that a fundamental force exists.
- [ ] **H4 — Gray-limit recovery:** prove `delta_a_OW -> 0` recovers the
  Newtonian/relativistic control within numerical tolerance.
- [ ] **H5 — Two-body regression:** test circular, eccentric, inclined,
  escape, capture, and perturbed stable orbits before three bodies.
- [ ] **H6 — Mercury benchmark:** preserve the measured perihelion behavior
  and declared time/light-time conventions.
- [ ] **H7 — Relational three-body state:** retain both Jacobi vectors,
  hyperradius, hyperangle, shape orientation, phase, and internal PPF receipts.
- [ ] **H8 — Nested orbital PPF:** separate body-internal PPF, body Path in the
  system Field, and system PPF in its larger environment.
- [ ] **H9 — Common response law:** use one constrained One-Wave law across
  bodies; forbid unexplained per-planet correction coefficients.
- [ ] **H10 — Mechanism ablations:** separately test wake, boundary curvature,
  displacement, EM shell, core rotation, phase memory, and internal PPF.
- [ ] **H11 — Three-body test families:** run hierarchical triples, resonant
  triples, Lagrange configurations, chaotic scattering, capture, and ejection.
- [ ] **H12 — Identifiability:** use sensitivity matrices, Fisher information,
  synthetic recovery, and held-out ephemeris intervals.
- [ ] **H13 — Improvement test:** reject additions that merely redescribe the
  baseline or improve training intervals while degrading held-out predictions.

## I. Galactic scale

- [ ] **I1 — Units:** implement parsec/kiloparsec/light-year conversions with
  dimensional tests; integrate internally in one consistent unit system.
- [ ] **I2 — Gray galaxy baseline:** reproduce rotation from baryonic matter
  and explicitly declared standard comparison components.
- [ ] **I3 — Nested trail hypothesis:** define a measurable trail variable and
  predict arm density, width, lifetime, and pattern speed.
- [ ] **I4 — Arm-thinning test:** calculate whether a leading trail becoming
  thinner can generate another arm without violating continuity or observations.
- [ ] **I5 — Cluster environment:** distinguish local galaxy dynamics,
  Local-Group motion, cluster/supercluster flow, and Great-Attractor-scale data.
- [ ] **I6 — Wake-curvature model:** write a causal, unit-consistent evolution
  law and compare it against lensing, velocities, and morphology.
- [ ] **I7 — Milky Way–Andromeda test:** use uncertainty ensembles and compare
  baseline versus One-Wave correction rather than one cinematic trajectory.

## J. Neural, M4, and heterogeneous runtime

- [ ] **J1 — Six-route neural primitive:** test the logic as a recurrent cell
  rather than assuming every network uses it.
- [ ] **J2 — Hopfield necessity:** compare cue recovery and route stability
  against deterministic and random controls.
- [ ] **J3 — Boltzmann necessity:** compare exploration, energy, latency, and
  error against simpler stochastic controllers.
- [ ] **J4 — Gate 7:** compare minimum, product, copula, reliability-network,
  constrained-optimization, and dynamical phase-lock couplers.
- [ ] **J5 — CPU/GPU/NPU parity:** establish deterministic receipts,
  quantization tolerances, stale-result handling, and replay.
- [ ] **J6 — NPU M4 boundary:** measure whether fast-loop inference improves
  latency without allowing the NPU to commit authoritative state.

## K. Cross-domain falsification

- [ ] **K1 — Circle-pit phase diagram:** sweep coupling/noise and measure
  order, density, vorticity, and transition boundaries against crowd controls.
- [ ] **K2 — Music build/release:** compare the six-gate hypothesis against
  simpler onset, envelope, spectral, and structural models.
- [ ] **K3 — Human interaction grammar:** operationalize intention, reception,
  connection, and reaction without treating metaphor as physical identity.
- [ ] **K4 — Quasar comparison:** preserve native astrophysical equations and
  test only declared dimensionless mappings.
- [ ] **K5 — Physiology comparison:** preserve biological mechanism and test
  timing/threshold/hysteresis mappings without universalizing orgasms or other
  lifecycle examples into one literal equation.

## Recommended attack order

1. A: finite logic and commitment.
2. B: center-origin oscillator and thresholds.
3. C–D: recursive PPF and dimensional transforms.
4. E: Field equation, dispersion, and invariance.
5. F–G: micro mechanism and hardware carriers.
6. H: orbital and three-body validation.
7. I: galactic extension.
8. J: M4 runtime.
9. K: cross-domain falsification.

## Definition of done

This list is complete only when every checked task links to its code, data,
results, control comparison, failure report, and Brick decision. Unsupported
mechanisms remain Brown; contradictory results are Red; useful mathematics may
remain Yellow even when the proposed physical interpretation fails.
