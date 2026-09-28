# Modular Physics Engine

Status: YELLOW bench architecture. Not Gold. Not a derived proton.

Every node is a **visual module** that plugs into one shared field.
Pipelines from D-414 feed **drives**, they do not rewrite the source experiments.

```text
LIGO/Virgo strain envelopes  →  Z_M  Mirror-Gate drive
CERN/CODATA anchors          →  Z_K  knot phase / mass ladder drive
125 GeV Higgs measurement    →  Z_M  boundary scale anchor (C-322)
Reactor Keepin + binding     →  Z_T  weave / confinement drive
EEG records                  →  Z_E  electrical shell drive
```

D-414 law, restated:

- LIGO remains gravitational-wave data.
- CERN/CODATA remains measured particle constants.
- EEG remains cortical voltage.
- Reactor data remains neutron kinetics.
- They are folded onto B-221 (BEGIN MOVE HOLD BUILD BREAK LOOP), doubled, mirrored through the oscillation center, and used as `driveVal(u)` on the four channels of one bounded field.

Camera and scale never change the update rule (D-412).

## Bus

```text
Field {
  psi, prev, neighbors, chi_wake,
  drive_ZM, drive_ZE, drive_ZK, drive_ZT
}

Module.tick(Field)   # a node writes only what its brick allows
```

Unlock order still follows the Brick System. A-114 cannot run if A-109 is off.
A-115 applies nested wake curvature; pipelines only modulate it.

## Module map (first rack)

| Module | Brick | Writes |
|---|---|---|
| A-101 Ground | Yellow | sites exist |
| A-102 Displacement | Yellow | psi live |
| A-109 Memory | Yellow | (1-γ) inertia |
| A-114 Dispersion | Yellow | neighbor β update |
| A-115 Compression | Green/Yellow split | χ and g0 from wakes + local |
| E-532 Bound wake | Yellow | bound flag, Yukawa kernel |
| D-414 Four-channel | Yellow | pipeline sampling into Z_* |
| D-413 Ground lab | Yellow | orbital restore on same Field |

Add a node = add a Module subclass. Do not fork a second engine.

## Honesty

This architecture expands D-414 and D-413. It does not promote them.
Synthetic 48-point folds stand in when `waves_bundle.json` is offline.
When the official bundle is present, adapters must read
`Nodes/D-414_Four_Interaction_Shell_Simulation/data/waves_bundle.json`
and use `fold.bidirectional_envelope` exactly.

Parent: D-412, D-413, D-414, A-115, C-322, B-221, I-02 / THE_BRICK_SYSTEM.
