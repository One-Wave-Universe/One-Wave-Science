# One-Wave Equation Solver — verification-first plan

Status: PROPOSED, UNVERIFIED. Branch-only development; no changes to existing science claims.

## Mission
Build a general-purpose mathematical solver for canonical One-Wave equations and established comparison models. The engine must be able to reject hypotheses, not tailor numerical behavior to confirm them.

## Reference gates
Before implementation read GENERAL_REFERENCE_RULES.md, AI_CANONICAL_START_HERE.md, AI_FOREMAN_WORK_REGISTER.md, 00_MASTER_INDEX.md, and V1_VERIFICATION_MATRIX.md. Locate and inspect authoritative A-115 displacement, W2 gravity, cosmology, and scalar/differential/vector/tensor/stratum/harmonic chapters and nodes. Never replace canonical equations with inferred ones. Record exact source paths, equation IDs, assumptions and status.

## Core components
1. Equation registry: source file, line, claim status, units, variables, assumptions, domain and boundary conditions.
2. Symbolic checks: SymPy derivatives, divergence, curl, tensor contractions, dimensional checks, limiting cases.
3. Numerical methods: NumPy/SciPy ODE, boundary-value, nonlinear root, eigenvalue and PDE baseline methods; independently validated manufactured solutions.
4. Comparators: conventional elasticity, Newtonian gravity and appropriate established models, with the same initial/boundary data and uncertainty.
5. Diagnostics: residuals, mesh/time-step convergence (numerical time stepping is not a physical clock assumption), conservation, stability, sensitivity, identifiability and falsification thresholds.
6. Evidence: immutable inputs, versions, solver settings, raw outputs, plots, failure reports, reproducible tests and node references.

## First target: A-115
Candidate definition chi = -div(u) is a mathematical identity/definition, not evidence for gravity. Verify its precise repository meaning and dimensions. Find the actual governing equation or energy/action. Derive predictions from documented assumptions only. Cross-check W2 derivation and flag unsupported jumps. Use measured or published independent datasets, never hand-picked fitting targets.

## Milestones
M0: Inventory canonical math and competing equations; output a gap matrix.
M1: SymPy unit/identity checks and known analytic benchmark suite.
M2: Implement one documented displacement-field boundary-value case, validate residual and convergence.
M3: Derive one pre-registered falsifiable prediction and compare against a standard model and independent data.
M4: Publish reproduction packet and update V1_VERIFICATION_MATRIX and relevant Nodes only after review.

## Acceptance tests
- Analytic benchmark recovered within specified tolerance.
- Refining resolution reduces error as expected.
- Changing assumptions produces visible diagnostic changes.
- Failed/inconclusive runs retained, not discarded.
- No claimed physical validation from internal mathematical consistency alone.

## Scope
Science repository owns the equations and evidence; Builds and 3D circuit builder may consume results via references only. Do not tailor the solver to CELL_V1 or change breadboard artifacts.
