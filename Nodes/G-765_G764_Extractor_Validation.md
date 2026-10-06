---
id: G-765
title: G-764 Validated Against G-739's Six-Gate Extractor on a Real Integrated Trajectory
status: yellow
tier: executable-math
claim_boundary: numerical validation of G-764's derived thresholds/criteria against one
  concrete simulated trajectory of the exact test-bench equation; not a scan over
  parameter space, not a physical-carrier claim
---

# Node G-765: G-764 Validated Against G-739's Six-Gate Extractor

## Purpose

G-764 derived a closed-form commitment map `K` and a set of thresholds
(`x*`, `x_pm`, `h_c`, a capture criterion, a ringdown frequency) from
UPDATED_43's biased double-well test bench, and named as its own
"Recommended Next Step":

> Run G-739's extractor against numerically integrated trajectories of this
> exact equation across a grid of `(h,u(t))` route assignments and confirm
> the gate sequence ... lines up with the crossing/capture events derived
> here. That is a Yellow-to-Bronze promotion test this node sets up but does
> not perform.

This node performs that test on one concrete trajectory, using the real
`extract_six_gates` code in `One_Wave_Bench/dynamics/six_gate_extractor.py`
(the same extractor G-739 defines) and RK4-integrating G-764's exact
equation. The script is `One_Wave_Bench/dynamics/g765_validate_g764.py`;
its output is committed verbatim as `g765_validation_receipt.json`. This is
a report of what that run actually produced, including a real bug it
uncovered and a real correction to G-764 Section 8 — not a hand-picked
success story.

## 1. Method

A smooth (tanh-ramped, not a literal step-function) bias program
`h(t)` drives the equation `ẍ+γẋ+ax³-bx-h(t)=0` through the full
`Begin -> Build -> Hold -> Build -> Break -> Loop` cycle named in
UPDATED_43: hold at `h=+0.3` (`|h|<h_c`, favors the `+` well without
forbidding the `-` well) long enough to fall into and settle in the `+`
well, then reverse to `h=-1.2` (`|h|>h_c`, forces a single well) to drive
a genuine forced escape into the `-` well, then relax to `h=-0.3` to hold
there. Parameters: `a=b=1`, `γ=1.0` (chosen only for a clean, non-wildly-
ringing settle; not derived by G-764).

Two quantities the extractor needs but G-764 does not derive — coherence
`c∈[0,1]` and heat `h_i≥0` — are supplied here as an explicit, flagged
modeling choice, not a G-764 result: `heat = γv²` (the exact damping-
dissipation term from the equation of motion) and `coherence =
clip(P_drive,0,∞)/(clip(P_drive,0,∞)+heat)` where `P_drive=v·h(t)` is the
power injected by the bias field. **This matters because UPDATED_43's own
required-output list — center residence, crossing direction, partial/full
excursion, hysteresis, return, phase — does not include a Coherent-vs-
Unstable-Build distinction.** That distinction is G-739 extractor
machinery, not something G-764 claims to derive; the `coherence_min=0.5`,
`heat_max=0.35` thresholds below are a declared, un-derived, non-tuned
choice, and the Coherent/Unstable Build labels below should be read with
that caveat.

Every other threshold fed to the extractor is one of G-764's own
derived constants: `center_band=x*`, and the position-based full-
commitment split uses `x_pm`. `begin_energy_max` and `hold_energy_min`
are set at 10% and 50% of the zero-bias well depth `b²/4a`. `speed_tol`,
`energy_rate_tol`, and `break_rate_min` are declared, non-derived
tolerances in the caller units G-739 requires.

## 2. A real bug this run found: `boundary` is not `x_pm`

The first pass reused `x_pm` (G-764's own "full commitment" position) as
the extractor's `boundary` parameter — the hard runaway/structural-limit
that triggers `Break` on an outward-moving excursion past it. This was
wrong, and the run showed it immediately: at `h=0.3` the `+` well's actual
rest point is not `x_pm=1.0`, it is the root of `ax³-bx-h=0`, which is
`x≈1.13`. The extractor correctly read the system as sitting quietly,
essentially motionless, past `x_pm`, and — because `boundary=x_pm` — flagged
that stable, correctly-committed rest as a boundary-excursion `Break`.

**`x_pm` and `boundary` are two different concepts that only coincide at
`h=0`.** `x_pm` is where a biased well's occupant is fully committed and
meant to rest; `boundary` is meant to be a limit past which the system has
broken something, not a place it is supposed to end up. Fixed here by
setting `boundary=2.0`, safely beyond every biased rest point this
program's bias magnitudes reach. Any future use of this extractor on
biased-double-well dynamics needs its own `boundary`, derived from the
bias range actually in play, not borrowed from the zero-bias fixed point.

## 3. Result: the qualitative gate order

Collapsing consecutive repeats and dropping `Unclassified` samples, the
run produced:

```
Begin -> Coherent Build -> Unstable Build -> Hold -> Unstable Build -> Hold
-> Hold -> Break -> Coherent Build -> Unstable Build -> Loop
-> Unstable Build -> Hold -> Unstable Build -> Hold -> Hold
```

This reproduces UPDATED_43's named order — Begin, a Build phase, Hold,
another Build/Break episode, Loop, then Hold again — honestly, but not
cleanly: raw per-sample labels alternate between Build/Hold/Unclassified
near threshold boundaries (1321 of 8001 samples are `Unclassified`, and
`Coherent`/`Unstable` Build alternate within what is physically one
continuous phase). That alternation is a real property of thresholding a
continuous trajectory sample-by-sample near its boundaries, not noise to
paper over. `Loop` fires exactly once, at `t=16.9`, matching the trajectory's
own independently-computed zero-crossing time (`t=16.9`) to the simulation's
time resolution — this part is an exact match, not an approximation.

## 4. Result: the capture criterion needs a fixed-`h` caveat

G-764 Section 7 defines capture as `E(t)<V(x*;h)`. At `t=10`, mid-Hold in
the `+` well under constant `h=0.3`, this reads `True` (captured) — correct.
At `t=16.5`, after `h` has reversed past `h_c`, the same criterion (now
evaluated with the *current* `h`) reads `False`: the trajectory that was
captured is no longer captured, with no new energy added to it. This is not
an error in Section 7 — energy conservation was never violated, since the
external field did work when `h` changed — but Section 7's text does not
warn that its captured/escaped read is only valid while `h` is held fixed,
and needs re-evaluation at the new `h` whenever the bias itself moves. That
caveat should be added to G-764 Section 7.

## 5. Result: Section 8's ringdown formula needs a bias-dependent generalization

The measured ringdown frequency in the final (`-`) well, from `v`
zero-crossings after `t=30` (residual amplitude ~`6×10⁻⁴`, safely in the
linear regime — this is not an anharmonic-amplitude effect), is
`ω≈1.5967`. G-764 Section 8's formula `ω_well=√(2b)=1.4142` (derived at
the unbiased well `x_pm`) does not match. The actual `-` well under
`h=-0.3` sits at `x≈-1.1254` (confirmed to be the exact root of
`ax³-bx-h=0`), where the curvature is `V''=3ax²-b≈2.7997`, not `2b=2`.
Using this curvature with the standard damped-oscillator correction,

\[
\omega_{\rm ring}=\sqrt{V''(x_{\rm well}(h))-(\gamma/2)^2}
=\sqrt{2.7997-0.25}=1.5969,
\]

matches the measured `1.5967` to four significant figures. **G-764 Section
8's `ω_well=√(2b)` holds only at `h=0`; the general, bias-dependent, damping-
corrected formula is `ω_ring=√(V''(x_well(h))-(γ/2)²)`**, which reduces to
`√(2b)` exactly when `h→0` (since `x_well(0)=x_pm` and `V''(x_pm)=2b`,
matching G-764 Section 8's own computation) and to `0` at `γ=2√(V'')`
(critical damping, no ringdown) as expected.

## Cross-check summary

| G-764 claim | Checked how | Outcome |
|---|---|---|
| Ground (`x=0`) is an unstable saddle | perturbation `x(0)=0.02`, `h(0)=0.3` immediately grows away from 0 | confirmed (qualitative, expected) |
| `x*=x_pm/√3` splits partial/full | used directly as `center_band`; extractor's Begin/Hold split behaved consistently at this value | consistent, no contradiction found |
| `h_c` splits bistable/forced | `|h|=0.3<h_c` (Hold phases) vs `|h|=1.2>h_c` (escape phase) both behaved as the bistable/forced distinction predicts | confirmed |
| `K(x(T))` five-state position map | checkpoint table (script output) | agrees with the physical phase at every checked point |
| Capture criterion `E(t)<V(x*;h)` | checked at fixed-`h` Hold and after a bias reversal | correct at fixed `h`; needs the fixed-`h` caveat above |
| `ω_well=√(2b)` ringdown | measured via zero-crossings after settling | wrong at `h≠0` as stated; exactly right once generalized (Sec. 5 above) |
| `Begin->Build->Hold->Build->Break->Loop` order | full extractor run | reproduced qualitatively; Loop time exact; Build sub-labels not part of G-764's claim (see Sec. 1) |

## What this is not

- Not a parameter scan — one bias program, one damping value, one set of
  declared thresholds. Different `γ`, `h` magnitudes, or ramp speeds could
  behave differently; this node does not claim they will not.
- Not a validation of the Coherent-vs-Unstable-Build distinction as
  physics — that split needs coherence/heat definitions this node supplies
  only as a flagged, non-derived modeling choice, because UPDATED_43 never
  asked G-764 to derive one.
- Not a claim that `a,b,γ,h_0` have physical values.
- Does not touch the self lifecycle (G-742) or Field/Void ternaries (G-740),
  per UPDATED_44, same boundary G-764 already stated.

## Failure Conditions

This node fails if the reported numbers (crossing time, ringdown frequency,
capture-criterion values) cannot be reproduced by re-running
`g765_validate_g764.py` unchanged; if the `boundary`-vs-`x_pm` distinction
in Section 2 is shown to be wrong rather than a genuine conceptual conflation;
or if the generalized ringdown formula in Section 5 fails to reduce to
`√(2b)` at `h=0` under direct substitution (it is checked here only
numerically at one biased point, not proven in closed form for general `h`).

## Recommended Next Step

Prove the generalized ringdown formula in closed form as a function of `h`
(the well position `x_well(h)` is already an exact root of a depressed
cubic, so `V''(x_well(h))=3a\,x_well(h)^2-b` is available in closed form via
the standard cubic root formulas); add the Section 7 fixed-`h` caveat and
this Section 8 generalization directly into G-764; then extend this
validation to a small grid of `(h_0,\gamma)` values rather than the single
program used here, as G-764's own recommended step originally asked for.
