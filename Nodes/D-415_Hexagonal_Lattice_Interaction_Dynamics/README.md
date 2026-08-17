# D-415 Hexagonal Lattice Interaction Dynamics — Runner

**Status:** YELLOW reduced runner  
**Identity lock:** A-115 / C-323 — one compression field; gravity = local response; dark-matter behavior = extended wake of the same field; no second substance; no force-carriers.

## What this is

Discrete bond **restoring responses** on the D-408 triangular lattice:

- bulk compression response \(K\chi\)
- shear response \(\mu\)
- gradient-of-compression response \(\alpha\)
- oriented residual response \(\beta C\) on bound sites only (E-532)
- curvature penalty \(\gamma\)

Update is velocity-Verlet on site displacements. Energy, bound count, and outer-annulus wake \(\chi\) are logged every sample stride.

## Required first runs (D-415 / D-412)

| Case | Intent |
|------|--------|
| `zero_input_hold` | No spontaneous bound flags, no drift |
| `single_bound_core` | Bound flag appears and holds; far compression = gravity view |
| `single_core_oriented` | Oriented residual present |
| `two_cores_opposite_C` | Opposite orientation labels; wake cancellation test |
| `free_packet_null` | Free packet never acquires persistent bound flag |

## Run

```bash
cd Nodes/D-415_Hexagonal_Lattice_Interaction_Dynamics
python simulate_d415.py --out results
```

Outputs: per-case CSV, `d415_summary.json` with checks and receipts.

## What is still open

- Absolute scale (C-318 identifiability)
- Dual-harmonic H-label tracking on free sector (E-531)
- Coefficient calibration
- Explicit finite-wake kernel length \(\sigma\)
- Moving/rotating core wake profile derivation for galactic comparison (Book 5 Ch1)
- D-409 3-D upgrade

## Language

Bond objects are **restoring responses**, not forces.  
Dark-matter behavior is the extended compression of the same field, not a particle.
