# Displacement pressure and wear hysteresis

Status: YELLOW / candidate architecture.
Sources: `docs/updates/UPDATED_41_PLANETARY_SCALE_DISPLACEMENT_MODEL.md`, `GRAV/QCD_BAG_PRESSURE.md`, `GRAV/GLUONIC_SURFACE_TENSION.md`, `GRAV/FIELD_TAP_SLIP_125.md`, CELL_V1 remanence rule.

Date: 2026-09-18

## Displacement

A body is a persistent displacement structure. Orbit, well, tide, EM shell, stress, and stability are readouts of the current state, not bolt-on forces.

Bound layer:

```
L2D = {C, T, γ, Q, Ω}
```

compression, tension, shear/damping, integrity `Q`, circulation.

## Displacement pressure

Bag + skin, same diagram at every octave:

```
p = p_inside - B
ΔP ≈ B + 2γ / R
```

`B` is vacuum / bag squeeze = κ of that scale. `γ` is surface tension. Neighboring fields add `ΔS = S_local − S_ref`. No memory relay. Current state only.

Energy enters → cannot propagate → tension on the rim → rotation picks an axis → skin slips → fountain. Dump is not mass deletion.

## Wear

Wear is state change of the bound layer, not cosmetic scuffing.

```
P_shear ~ γ (ΔΩ)²
Q_{n+1} = HYSTERESIS(Q_n, u_{n+1})
```

`u` includes shear, path cost `R|ds|`, and `ΔP`. Old remanence plus new event yields new remanence. Drive removed, leftover stays.

As `Q` falls, `γ` softens. Near a crossover the skin can change sign. `ΔP` climbs against a weaker rim.

## Hysteresis cycle

1. Virgin `Q ≈ 1`.
2. Load: `Q` falls on the upper branch.
3. Hold / STAY: remanence remains.
4. Unload: partial recover. Missing height is the wear.
5. Slip if `Q` or `ΔP` crosses the coercive wall. Fountain. Partial `Q` rebound to a *new* remanence.
6. Next cycle starts there. Same input, different switch.

Loading and unloading that coincide are flex, not wear. Fat loop area is dumped order.

Equal `Q` from two different `u(t)` paths are not the same receipt.

## Lab meters

`GRAV_LAB/PHYSICS_LAB.html`: wear `Q`, `ΔP` skin, slip count. Slip sheds leftover speed; mass is not deleted.
