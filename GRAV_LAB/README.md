# GRAV LAB — Physics Lab

YELLOW test architecture. Open `PHYSICS_LAB.html` in a browser. No build.

Implements, without promoting hop arithmetic into a force:

- `dt = κ|ds|` and `R ≡ κ` (`GRAV/RESISTANCE_EQUALS_TIME.md`)
- `g ∝ −∇κ`, two-body Kepler check, restricted three-body Jacobi
- GEM `a ~ v × B_g` with `B_g` default 0
- Rabbit Hop lock tests (address receipts)
- CELL_V1 seven-flower geometry
- wear `Q` hysteresis and `ΔP ≈ B + 2γ/R` (`GRAV/DISPLACEMENT_PRESSURE_WEAR_HYSTERESIS.md`)

Integrator: velocity Verlet or leapfrog. No damping on the orbital step. Watch `E/E0` and `L/L0`.
