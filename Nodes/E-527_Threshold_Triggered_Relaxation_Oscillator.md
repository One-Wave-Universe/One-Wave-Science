---
node_id: "E-527"
canonical_name: "Threshold-Triggered Relaxation Oscillator Model"
namespace: "NODE"
gate: "BRONZE"
lifecycle: "ACTIVE"
classification: "Application Node — Reduced Hybrid Dynamical Model"
claim_gate_detail: "None"
metadata_standard: "I-06"
---

# Node E-527: Threshold-Triggered Relaxation Oscillator Model

Bronze scope:
This node has one reproducible numerical validation with attached code,
parameters, data, figures, metadata, and analytic cross-checks. Bronze
applies only to the reduced model derived below. It does not prove a
specific biological event, a full Kuramoto lattice, consciousness, or
an Android hardware implementation.

Dependencies:
Upstream: E-524 Kuramoto Lattice Synchronization, E-526 Cellular Energy Balance and ATP Kinetics
Downstream: Android Body Book Chapter 1 regulation design; future full-lattice tests

Correction record:
The original candidate used

C(t) = R(t) U(t)

as though multiplying synchronization by available resource could by
itself create build-up, threshold, release, relaxation, and recovery.
That claim failed simulation.

The product C=RU is a readout. It is not an oscillator equation.

Three distinct cases were separated:

1. Constant supply:
   U approaches a fixed point, so C approaches a plateau. No cycle.

2. Finite substrate with no recharge:
   U rises and falls once, so C produces one transient pulse. A pulse
   is not a repeating relaxation oscillator.

3. Recharge plus state-dependent depletion plus hysteresis:
   the system repeatedly charges, triggers release, discharges, resets,
   and charges again. This is the minimal validated cycle in this node.

---

## Variables

R_* in (0,1] = settled synchronization order parameter supplied by the
                  E-524 layer after its transient

U(t) >= 0       = usable stored resource or activation reserve

h(t) in {0,1}   = release state
                  h=0: charging / inactive release
                  h=1: active release / depletion

P > 0           = recharge or production rate

lambda > 0      = ordinary loss rate

D > 0           = additional state-dependent depletion rate during release

C(t)             = coordinated available response

C_on             = upper trigger threshold

C_off            = lower reset threshold

with

0 < C_off < C_on.

The reduced model treats R_* as settled rather than simulating every
phase oscillator. E-524's full degree-6 lattice simulation remains a
separate unresolved task.

---

## Readout

C(t) = R_* U(t)

This means sufficient resource without coordination is insufficient,
and sufficient coordination without resource is insufficient.

The product is an observable or gate quantity. It does not generate a
cycle by itself.

---

## Hybrid Resource Equation

The resource obeys

dU/dt = P - lambda U - D h U.

When h=0:

dU/dt = P - lambda U.

The charging equilibrium is

U_charge = P/lambda.

When h=1:

dU/dt = P - (lambda + D)U.

The release equilibrium is

U_release = P/(lambda + D).

---

## Hysteretic Switching Rule

Release turns on when

h: 0 -> 1  if  C >= C_on.

Release turns off when

h: 1 -> 0  if  C <= C_off.

Because C=R_*U, the corresponding resource thresholds are

U_on = C_on/R_*,

U_off = C_off/R_*.

The separate on and off thresholds prevent rapid chatter at one
threshold and create a finite release interval.

---

## Exact Oscillation Conditions

A repeating relaxation cycle exists only if the inactive mode can
charge above the upper threshold and the active mode can discharge
below the lower threshold:

U_charge > U_on

and

U_release < U_off.

Equivalently,

P/lambda > C_on/R_*

and

P/(lambda + D) < C_off/R_*.

These inequalities define the admissible parameter window:

lambda C_on/R_* < P < (lambda + D) C_off/R_*.

A necessary condition for that window to exist is

D > lambda(C_on/C_off - 1).

The minimum settled synchronization required for triggering is

R_* > R_min = lambda C_on/P.

Thus synchronization controls whether the release threshold is
reachable, while depletion and hysteresis control whether the system
returns and repeats.

---

## Exact Period

During charging, the state moves from U_off to U_on. The charging time
is

T_charge = (1/lambda)
           ln[(U_charge - U_off)/(U_charge - U_on)].

During release, the state moves from U_on to U_off. The release time is

T_release = (1/(lambda + D))
            ln[(U_on - U_release)/(U_off - U_release)].

The predicted period is

T_period = T_charge + T_release.

This gives a direct numerical validation target rather than judging a
curve by resemblance.

---

## Reproducible Bronze Simulation

Canonical artifacts:

Nodes/E-527_Simulation/simulate_e527.py
Nodes/E-527_Simulation/simulation_metadata.json
Nodes/E-527_Simulation/case_1_constant_supply_plateau.csv
Nodes/E-527_Simulation/case_2_finite_substrate_single_pulse.csv
Nodes/E-527_Simulation/case_3_hybrid_relaxation_cycle.csv
Nodes/E-527_Simulation/case_3_switch_events.csv
Nodes/E-527_Simulation/parameter_sweep.csv
Nodes/E-527_Simulation/*.png

Validated parameter set:

R_* = 0.85
P = 0.08
lambda = 0.10
D = 0.60
C_on = 0.55
C_off = 0.25
U(0) = 0.30
dt = 0.001
t_end = 90

Analytic thresholds and equilibria:

U_on = 0.6470588235
U_off = 0.2941176471
U_charge = 0.8000000000
U_release = 0.1142857143

Both oscillation inequalities are satisfied.

Analytic period:

T_charge = 11.9625075823
T_release = 1.5515327706
T_period = 13.5140403529

Numerical result:

6 release events were produced.
Mean numerical period = 13.516
Analytic-vs-numerical period error = 0.0145 percent.

The validation script asserts:

- constant-supply C rises monotonically to a plateau,
- finite substrate produces exactly one pulse,
- the hybrid model produces at least five repeated cycles,
- the state remains bounded and nonnegative,
- numerical period agrees with the analytic period to better than
  0.5 percent.

All assertions passed.

---

## What Was Disproved

Disproved as a sufficient mechanism:

C(t)=R(t)U(t) alone produces a relaxation cycle.

Also corrected:

finite depletion alone produces a cycle.

Finite depletion without recharge produces one transient pulse, not a
repeating oscillator.

---

## What Was Validated

Validated once in the reduced model:

stable synchronization input
+
recharge
+
state-dependent depletion
+
hysteretic thresholds

can generate a repeatable relaxation oscillator whose numerical period
matches its analytic prediction.

---

## Limits

- R_* is a fixed settled synchronization input. The full E-524
  hexagonal Kuramoto lattice was not simulated here.
- The normalized parameters are test values, not measured biological
  constants.
- No named biological event has been claimed to follow this model.
- No Android hardware has been tested.
- The model does not derive P, lambda, D, C_on, or C_off from deeper
  One-Wave field variables.

---

## Next Work

1. Run E-524 on the actual finite degree-6 lattice and feed its measured
   R(t), rather than constant R_*, into this model.
2. Determine whether resource depletion changes coupling K, phase
   dispersion, or only available output.
3. Fit P, lambda, D, C_on, and C_off to one real target system before
   making any biological or engineering prediction.
4. Test noise sensitivity and threshold chatter.
5. Use the same model in a second independent application before any
   Silver promotion.

Final result:
The negative simulation was not a dead end. It identified the missing
state variable and switching structure. The corrected node now says
exactly what cycles, exactly why it cycles, and exactly what was not
proved.
