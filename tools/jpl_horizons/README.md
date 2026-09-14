# NASA/JPL Horizons -> Orbital / Three-Body Target Pipeline

Status: **YELLOW tooling / empirical state-vector target / One-Wave gravity not yet applied**

## CORE-RULES-PRE

Read first:

- `CORE_RULES_LOCK.md`
- `MATH_BACKBONE/00_MATH_BACKBONE_LOCK.md`
- `MATH_BACKBONE/32_jpl_horizons_orbit_vectors_v1.md`

This pipeline is for making orbital mechanics a hard numerical target. It must not fit One-Wave parameters to the same target and then call that a derivation.

## Source

NASA/JPL Horizons API:

```text
https://ssd-api.jpl.nasa.gov/doc/horizons.html
```

Horizons vector tables provide Cartesian position and velocity states for dynamical studies.

## First three-body target

```text
Sun   = body 10
Earth = body 399
Moon  = body 301
center = 500@0
frame = ICRF / FRAME
units = km and km/s
time = TDB
correction = NONE (geometric state)
```

Run:

```bash
python3 tools/jpl_horizons/horizons_vectors.py \
  --bodies 10,399,301 \
  --center '500@0' \
  --start 2026-09-01 \
  --stop 2026-09-05 \
  --step '1 d' \
  --output /tmp/sun-earth-moon.json
```

## Output

For each body and epoch the source layer keeps:

```text
JD TDB
calendar TDB
x y z [km]
vx vy vz [km/s]
center
reference system
reference plane
API signature/version
query URL
raw Horizons result SHA-256
```

The standard-derived layer adds pairwise:

```text
dx dy dz
dvx dvy dvz
distance
relative speed
radial speed
transverse speed
```

No One-Wave force/displacement equation is applied in v1.

## How another AI should use it

Do not start by fitting an orbit picture.

A proper One-Wave gravity test needs:

```text
INITIAL EPOCH:
INITIAL STATE SOURCE:
ONE-WAVE GOVERNING EQUATION:
DERIVED/FIXED PARAMETERS:
NUMERICAL INTEGRATOR:
TIME STEP:
PREDICTION INTERVAL:
JPL COMPARISON EPOCHS:
POSITION RESIDUAL:
VELOCITY RESIDUAL:
STANDARD-CONTROL RESIDUAL:
PASS / FAIL / OPEN:
```

Most importantly: initialize once, propagate forward, and compare later. Do not reset the model from JPL at every sample.

## Three-body progression

Use this order:

```text
1. Earth-Moon pair geometry
2. Sun-Earth pair geometry
3. Sun-Moon pair geometry
4. all three from one common initial epoch
5. conventional Newtonian/relativistic numerical control
6. One-Wave forward prediction
7. residual comparison over progressively longer intervals
```

If One-Wave requires a definition change when the third body is introduced, that is drift and must be exposed.

## Tests

```bash
PYTHONPATH=tools/jpl_horizons \
python3 -m unittest -v tools/jpl_horizons/test_horizons_vectors.py
```

The live workflow also queries JPL for the real Sun/Earth/Moon state target.

## CORE-RULES-POST

- JPL source remains the target, not evidence for One-Wave.
- Center/frame/time/units remain explicit.
- No reverse fitting is allowed.
- Three-body work must be forward predictive.
- Residuals must be numerical, not visual resemblance.
- Standard-control integration is required before blaming residuals on physics.
- Drift detected: state YES or NO.
