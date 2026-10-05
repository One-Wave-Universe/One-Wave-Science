# Native 3D field lab

From the repository root, with Python 3, NumPy and SciPy installed:

```sh
python One_Wave_Simulator/native_3d/server.py
```

Open **http://127.0.0.1:8765/**. The service binds only to this computer's loopback interface. No account, API key, upload or network service is used. Stop it with Ctrl+C. The static master simulator links here because the numerical lab needs its Python process; opening the HTML alone cannot run the solver.

## Running experiment

- Start/reset builds the selected experiment. Edited settings are pending until reset.
- Run/Pause and Step evolve the original Python numerical state at its declared fixed timestep.
- Bulk uses `solvers/bulk_excitation.py`: native 3D FCC12 periodic complex field, four coupled response coordinates, Gaussian norm input and an optional x phase gradient. Linear control removes focusing and saturation and starts from the same Gaussian. This is a chosen constitutive hypothesis, not established quantum particle physics.
- The ±(1,1,0) controls impose an exact periodic FCC lattice translation on the field array. Norm and model energy stay invariant; a fixed-origin detector changes. They are not force-driven displacement or deformation of the physical lattice sites.
- Cavity uses `solvers/joint_boundary_response.py`: a finite 13-site FCC graph, four-role second-order recurrence and exact discrete energy. Its real amplitudes have sign, not the bulk's complex phase. The displayed carried-profile tensor is the existing cycle-averaged diagnostic for the selected W-normalized eigenmode, independently checked by ±velocity energy finite differences. It is not instantaneous bulk inertia, a free particle, or a physical mass in kg. Within degenerate eigenspaces the chosen eigenvector is basis-dependent.
- Orbit, pan, zoom, role selection and camera reset change only the projection. Dot size is local intensity; all-four hue is coherent summed phase (undefined at a zero sum). Axis positions are model coordinates, never pixels used as physical distances.
- Export records actual real/imaginary arrays (plus the previous real cavity state needed for its second-order energy), positions, controls, time, measured quantities, last 256 energy samples and startup source SHA-256 values. A source-drift warning blocks further mutation until restart. An export is a state receipt, not a full replay history.

## Dimensional and physical boundary

Native geometry is three spatial dimensions, FCC stacking and twelve directed bulk nearest neighbors. The finite cavity omits exterior bonds. The screen is a perspective projection; its time trace does not establish D-410's 24-position recurrence. Norm, energy, length, time and response are dimensionless model quantities. No experimental mass target or conversion constant is inserted.

The later physical stages in the master simulator stay locked. In particular, localization survives some four-role ablations, physical displacement/velocity and geometric weave are not derived, and the hypothetical bulk closure is distinct from the canonical memory recurrence. See [bulk derivation](../../solvers/BULK_EXCITATION_DERIVATION.md), [joint response](../../solvers/JOINT_RESPONSE_DERIVATION.md), [C-318](../../Nodes/C-318_Mass_Mechanism_Candidate_Resolution.md) and [G-759](../../Nodes/G-759_Mass_Effect_Four_Actions.md).

The next bounded physics experiment is an explicit smooth periodic potential drive with matched zero/+force/−force runs, norm-centroid displacement, exact source-work ledger, pinning checks and timestep/domain/spacing controls. A narrow acceleration fit alone cannot establish Mass Effect: the four-interaction work metric must be derived and recurrence maintained.

## Verification

```sh
python One_Wave_Simulator/native_3d/test_lab.py
python solvers/test_bulk_excitation.py
python solvers/test_joint_boundary_response.py
# In another terminal with the server running; Playwright + Chromium required:
node One_Wave_Simulator/native_3d/test_ui.cjs
```

The dedicated CI repeats numerical tests and browser interaction, retaining screenshots and the exported state. The endpoint exposes only fixed reset/step/displace operations, capped grids, steps and bodies, strict loopback Host and same-origin mutation guards. It does not serve repository paths, execute commands or enable CORS. It is a single shared experiment per process; do not run competing browser tabs as independent sessions.
