# MATH BACKBONE 32 — JPL HORIZONS ORBIT VECTOR TARGET v1

Status: **YELLOW / EMPIRICAL ORBIT TARGET PIPELINE / ONE-WAVE GRAVITY EQUATION OPEN**

## CORE-RULES-PRE

Relevant core rules: 1, 2, 3, 5, 6, 7, 10, 13, 14, 15, 16, 17, 18.

Authoritative target: NASA/JPL Horizons Cartesian vector ephemerides.

This node does not derive gravity. It defines how orbital state-vector data become a fixed target that any One-Wave gravity/displacement/orbital rule must reproduce.

## 1. Source state

For body \(i\), Horizons supplies a state vector relative to a declared center and frame:

\[
\mathbf r_i(t)=(x_i,y_i,z_i)
\]

and

\[
\mathbf v_i(t)=(v_{x,i},v_{y,i},v_{z,i}).
\]

For this pipeline the requested output units are km and km/s, with a declared ICRF/frame convention.

Never drop the center/frame metadata. Coordinates without the reference origin are incomplete.

## 2. Relative vectors

For bodies \(i\) and \(j\), define

\[
\Delta \mathbf r_{ij}=\mathbf r_j-\mathbf r_i
\]

and

\[
\Delta \mathbf v_{ij}=\mathbf v_j-\mathbf v_i.
\]

Relative distance is

\[
\boxed{R_{ij}=|\Delta \mathbf r_{ij}|}
\]

and relative speed is

\[
\boxed{V_{ij}=|\Delta \mathbf v_{ij}|}.
\]

These are standard derived quantities from the source ephemeris.

## 3. Radial and transverse motion

When \(R_{ij}>0\), radial relative speed is

\[
\boxed{V_{r,ij}=\frac{\Delta \mathbf r_{ij}\cdot\Delta \mathbf v_{ij}}{R_{ij}}}.
\]

Then transverse speed magnitude is

\[
\boxed{V_{t,ij}=\sqrt{\max(V_{ij}^2-V_{r,ij}^2,0)}}.
\]

These descriptors are useful for comparing orbit geometry without assuming the mechanism causing it.

## 4. Empirical acceleration estimate

For uniformly spaced samples with step \(\Delta t\), a centered finite-difference acceleration target may be estimated from source velocities:

\[
\boxed{\mathbf a_i(t_n)\approx\frac{\mathbf v_i(t_{n+1})-\mathbf v_i(t_{n-1})}{2\Delta t}}.
\]

Or from positions:

\[
\boxed{\mathbf a_i(t_n)\approx\frac{\mathbf r_i(t_{n+1})-2\mathbf r_i(t_n)+\mathbf r_i(t_{n-1})}{\Delta t^2}}.
\]

Finite-difference resolution error must be studied before using this as a precision gravity test.

## 5. Three-body target

For Sun, Earth, and Moon, the empirical target at each common epoch is the joint state

\[
\mathcal S(t)=\{\mathbf r_S,\mathbf v_S,\mathbf r_E,\mathbf v_E,\mathbf r_M,\mathbf v_M\}.
\]

Derived pair geometry includes

\[
R_{SE},\quad R_{SM},\quad R_{EM},
\]

plus corresponding relative velocities.

A One-Wave three-body model is not validated by reproducing one distance at one time. It must propagate a declared initial state forward and remain inside declared residual bounds over a time interval.

## 6. Model residuals

Given One-Wave predicted state \(\mathbf r_i^{OW}(t)\), define position residual

\[
\boxed{\epsilon_{r,i}(t)=|\mathbf r_i^{OW}(t)-\mathbf r_i^{JPL}(t)|}
\]

and velocity residual

\[
\boxed{\epsilon_{v,i}(t)=|\mathbf v_i^{OW}(t)-\mathbf v_i^{JPL}(t)|}.
\]

The model must declare:

- initial-state source;
- free parameters;
- integration method;
- step size;
- frame/center;
- residual tolerance;
- comparison duration.

Do not reinitialize from JPL at every step and then claim long-term prediction.

## 7. Standard-reference lane

The JPL ephemeris is the measurement/model target used for comparison.

A later control implementation should also propagate the same initial state with a conventional gravitational integrator under the same numerical conditions. That separates One-Wave model error from numerical integration error.

## 8. One-Wave claims this can pressure-test

- gravity as displacement/wake;
- nested influence Moon -> Earth -> Sun -> galaxy;
- path/field rotation rules;
- claimed three-body simplification;
- scale recursion in orbital dynamics;
- any no-force ontology that claims the same observed trajectories.

Changing ontology does not remove the requirement to reproduce the ephemeris.

## 9. Kill conditions

FAIL or remain OPEN if:

1. a parameter is fitted directly to the same trajectory and then called derived;
2. coordinate center/frame is omitted or changed mid-test;
3. the model is repeatedly reset to JPL states instead of predicting forward;
4. only a hand-picked time interval is shown after failures elsewhere;
5. Earth-Moon works but Sun/Earth/Moon requires changing the primitive definition;
6. a visual orbit resemblance substitutes for quantitative residuals;
7. standard control integration is omitted when numerical error could explain the difference.

## 10. Status

PASS:

- JPL Horizons can supply authoritative state-vector targets;
- pair distances/relative velocities are deterministic standard-derived quantities;
- the source can be stored with API version and query settings.

OPEN / YELLOW:

- One-Wave gravitational field equation;
- One-Wave forward integrator;
- derived constants/parameters;
- residual tolerances justified from data/model uncertainty;
- three-body performance against JPL over meaningful intervals.

## CORE-RULES-POST

- JPL target remains independent of One-Wave interpretation.
- Source center/frame/time/units are mandatory.
- No reverse fit is permitted.
- Three-body success requires forward prediction, not repeated source resets.
- Math is explicit and preserved.
- One-Wave gravity remains YELLOW until its own equation produces the target.
- Drift detected: no.
