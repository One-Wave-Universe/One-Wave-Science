from pathlib import Path
p=Path('Virtual_Breadboard/SPICE_PARITY.md')
s=p.read_text()
old='16. Sparse matrix representation and factorization for large breadboards.'
new="16. **Sparse matrix representation and factorization for large breadboards** — IMPLEMENTED in the generic MNA core. Matrix assembly now stores only stamped nonzero coefficients while preserving the existing `A[row][col]` stamp semantics, so proven device stamps do not need a parallel sparse-only implementation. The preserved dense Gauss-Jordan solver remains selectable as `linearSolver: 'dense'`; `linearSolver: 'sparse'` uses sparse row maps with partial-pivot forward elimination/back-substitution, and `auto` selects sparse for matrices of 64 unknowns or more. Solver metadata reports matrix size, nonzero count/density, factor nonzeros, peak fill, and the active linear solver. Permanent qualification compares a 200x200 sparse system against the dense reference and verifies a real 100-section resistor ladder gives identical node voltages while auto-selecting sparse storage."
if old not in s: raise SystemExit('roadmap anchor missing')
p.write_text(s.replace(old,new,1))
