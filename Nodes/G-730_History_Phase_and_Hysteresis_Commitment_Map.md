# G-730 — History, Phase, and Hysteresis Commitment Map

**Status:** YELLOW control mathematics / semantics comparison open  
**Dependencies:** B-216, B-222, G-727–G-729

## Purpose

The five commitment states are derived readouts, not five primitive choices:

```text
-3 = full disagree
-2 = partial disagree
 0 = unity/reference/uncommitted readout
+2 = partial agree
+3 = full agree
```

They arise from a continuous latent coordinate `q`, route history,
differential magnitude, phase alignment, retention, and hysteresis.

## Candidate update

For binary sign `b in {-1,+1}`, ternary movement `m in {-1,0,+1}`,
bounded differential magnitude `d`, and phase error `Delta_phi`, define

`L(Delta_phi)=[1+cos(Delta_phi)]/2`

and the current choice-oriented candidate

`q_(n+1)=clip(r*q_n+g*b*m*d*L,-q_max,+q_max)`.

Here `r` is retention and `g` is gain. HOLD adds no new drive but can retain
prior commitment. Opposite phase supplies zero coherent drive in this first
candidate.

This equation deliberately exposes one unresolved semantic assumption:
`b*m` treats movement as oriented through the selected binary relation. It must
be compared with an absolute-axis movement model and an energy-gradient model.

## Hysteretic readout

Separate entry and exit thresholds form a five-state Schmitt readout:

- neutral enters partial only at `|q| >= theta_partial_enter`;
- partial persists until `|q| < theta_partial_exit`;
- partial enters full at `|q| >= theta_full_enter`;
- full persists until `|q| < theta_full_exit`;
- thresholds obey
  `partial_exit < partial_enter < full_exit < full_enter`.

This produces path dependence: equal current `q` can yield different readouts
when the prior committed states differ. That is retained history, not an
arbitrary lookup.

## Current verified properties

- output is restricted to `{-3,-2,0,+2,+3}`;
- one maximum default pulse remains below full commitment;
- repeated aligned YES receipts reach `+2` and then `+3`;
- repeated aligned NO receipts reach `-2` and then `-3`;
- opposite-phase input adds no coherent drive;
- HOLD adds no drive while retention carries prior state;
- entry/exit separation prevents immediate threshold chatter;
- invalid threshold ordering is rejected.

## Not yet a physical law

Parameter values are demonstration defaults, not universal constants. A5,
A6, and B1–B5 must determine state meaning, noise response, dwell times,
threshold calibration, and whether the candidate semantics match the
continuous oscillator and measured systems.

## Executable authority

- `One_Wave_Bench/logic_core/commitment_map.py`
- `One_Wave_Bench/logic_core/test_commitment_map.py`

The combined logic suite contains twenty-nine passing tests.
