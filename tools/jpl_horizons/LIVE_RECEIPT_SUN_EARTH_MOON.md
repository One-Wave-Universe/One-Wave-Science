# LIVE RECEIPT — JPL HORIZONS SUN / EARTH / MOON VECTOR TARGET

Status: **SOURCE TARGET PASS / THREE-BODY GEOMETRY READY / ONE-WAVE GRAVITY EQUATION OPEN**

Date: 2026-09-14

## CORE-RULES-PRE

- NASA/JPL Horizons is the independent orbital target.
- Center, frame, time system, units, and API version remain attached.
- Derived pair geometry does not establish a gravity mechanism.
- One-Wave must initialize once, propagate forward, and be compared by numerical residuals.
- No trajectory coefficient may be fitted after seeing the target and then called derived.

## Live execution

Workflow:

```text
JPL Horizons Orbital Target Tests
```

Successful run ID:

```text
34909584003
```

Job ID:

```text
104193861179
```

Result:

```text
3 / 3 unit tests PASS
JPL_HORIZONS_TARGET_PASS
```

JPL API signature returned:

```text
source = NASA/JPL Horizons API
version = 1.2
```

## Query contract

Bodies:

```text
10  = Sun
399 = Earth
301 = Moon
```

Query:

```text
center = 500@0
reference system = ICRF
reference plane = FRAME
time type = TDB
units = km, km/s
vector table = 2
vector correction = NONE
start = 2026-09-01
stop = 2026-09-05
step = 1 day
```

Five common state-vector epochs were returned for each body.

## Source-integrity hashes

Raw JPL result text SHA-256:

```text
Sun   c0fa7ea053e4796d0cca0e0d6f9f395de6c7544dab348c8ab97d5ebc2edf6f70
Earth 1b09f9c6646749f4d696e6c501a58779e445a7dcb693e91a5eb8199189656bea
Moon  53e2ac460a6a25523e6cc8fa761e7b0fdf3d46b4b7c3006efe85f0e8b526198a
```

## First-epoch Earth state

At JD TDB 2461284.5 / 2026-09-01 00:00 TDB, relative to the selected center:

```text
x  = 139999643.3142931 km
y  = -52115631.06686907 km
z  = -22576451.30304516 km

vx = 10.58422296535738 km/s
vy = 25.2723180806048 km/s
vz = 10.95409213837444 km/s
```

These are source ephemeris values, not One-Wave outputs.

## Earth-Moon geometry across the five epochs

Distance decreased across this interval from:

```text
377789.2926862882 km
```

to:

```text
369491.9595892384 km
```

Live test range:

```text
369491.9595892384 .. 377789.2926862882 km
```

Relative-speed values progressed approximately:

```text
1.040773315226868 km/s
1.0461231079175455 km/s
1.0510396768181467 km/s
1.0556805023637792 km/s
1.0599753677457502 km/s
```

At the first epoch:

```text
radial relative speed = -0.03216128007882747 km/s
transverse speed      =  1.040276283374766 km/s
```

At the final epoch:

```text
radial relative speed = -0.014337619933783593 km/s
transverse speed      =  1.0598783953276776 km/s
```

## Earth-Sun geometry across the five epochs

Live test range:

```text
150848547.81109387 .. 150988622.40898448 km
```

Earth-Sun relative speed progressed approximately:

```text
29.500220557427074 .. 29.538992810615085 km/s
```

The radial component was negative over this interval, approximately:

```text
-0.3983 .. -0.4135 km/s
```

while transverse relative speed remained around:

```text
29.4975 .. 29.5361 km/s
```

## Why this matters for One-Wave

This is now a fixed numerical target for the gravity/orbital/three-body work.

The next One-Wave model must produce, from one declared initial state:

```text
Sun r(t), v(t)
Earth r(t), v(t)
Moon r(t), v(t)
```

Then compare:

```text
position residual = |r_OW - r_JPL|
velocity residual = |v_OW - v_JPL|
```

at later epochs without resetting the model from JPL between samples.

The correct next ladder is:

```text
1. conventional numerical control from same initial state
2. One-Wave governing equation with independently derived/fixed parameters
3. forward propagation
4. Earth-Moon / Earth-Sun / Sun-Moon residuals
5. extend duration beyond five days
6. add more bodies without changing the primitive definition
```

This directly attacks the user's stated three-body target instead of treating the three-body problem as a verbal puzzle.

## Kill conditions

The One-Wave gravity path remains FAIL/OPEN if it:

- repeatedly resets positions from JPL;
- fits a coefficient to the same five-day trajectory and calls it derived;
- changes its field/displacement definition when the third body enters;
- reports visual orbit similarity instead of km / km-s residuals;
- omits a standard-control integrator, leaving numerical error confused with physics.

## CORE-RULES-POST

- JPL source remained independent of One-Wave interpretation.
- Center/frame/time/units/API version were preserved.
- Pair distances and velocities are standard-derived geometry only.
- No One-Wave gravity parameter was fitted.
- Three-body forward-prediction target is now concrete.
- Math remains explicit in `MATH_BACKBONE/32_jpl_horizons_orbit_vectors_v1.md`.
- One-Wave gravity status remains YELLOW / OPEN until its governing equation is actually propagated against this target.
- Drift detected: no.
