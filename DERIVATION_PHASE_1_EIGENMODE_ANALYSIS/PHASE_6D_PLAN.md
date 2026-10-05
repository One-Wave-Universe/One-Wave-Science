# Phase 6D: Continuum Limit Validation

**Date:** 2026-10-05  
**Status:** Planning phase  
**Objective:** Verify that Faraday error → 0 as domain size increases and time discretization decreases

---

## Purpose

Phase 6C achieved 68.8% error reduction (2.36 → 0.74) by implementing proper Helmholtz decomposition via Poisson solving. However, the remaining error is still significant (~0.74).

Phase 6D will test the hypothesis that this remaining error comes from:
1. **Finite domain effects** - 7-cell cluster is too small
2. **Time discretization** - O(dt²) error in finite differences
3. **Operator discretization** - O(a²) error in gradient/curl operators

Expected: Error should scale as O(1/L²) + O(dt²) + O(a²) and approach zero in continuum limit.

---

## Experimental Design

### Test Matrix

```
Domain Size:     radius 2, 3, 5, 7 hexagon
Time Step:       dt = 0.1, 0.05, 0.02, 0.01
Lattice Spacing: a = 1.0 (standard)
Total Steps:     20 (constant simulation length = 2.0 time units)
```

This creates 4×4 = 16 independent test cases, each showing how error behaves.

### Measurements

For each case:
- **Faraday error:** max(|∇×E + ∂B/∂t|) over all sites and timesteps
- **Domain size:** N_sites in the hexagonal cluster
- **Temporal resolution:** Number of steps N_steps = 2.0/dt

Plot:
1. **Faraday error vs domain radius** (at dt=0.1)
2. **Faraday error vs dt** (at radius=5)
3. **Error scaling law**: Check if error ~ 1/N_sites + dt²

### Success Criteria

- Error monotonically decreases as domain size increases
- Error monotonically decreases as dt decreases
- Error approaches zero (< 0.05) for radius=7 and dt=0.01
- Scaling follows predicted O(N⁻¹) + O(dt²) pattern

---

## Implementation Tasks

### 1. Domain Generation
```python
def hexagon_cluster(radius: int) -> List[Site]:
    """Generate hexagonal cluster of given radius.
    
    radius=1: 7 sites (center + 6 neighbors)
    radius=2: 19 sites
    radius=3: 37 sites
    radius=5: 91 sites
    radius=7: 169 sites
    """
```

Utility: Will use existing `hex_lattice_graph` utilities, extend to larger domains.

### 2. Parametric Evolution
```python
def maxwell_evolution_v6_parametric(
    psi_0, psi_1, sites,
    total_time=2.0,
    dt=0.1,
    # ... other params
) -> (error_faraday, error_scaling_info)
```

Refactor Phase 6C solver to accept arbitrary domain size and dt.

### 3. Benchmark Suite
```python
def phase6d_benchmark_suite():
    """Run 16-case matrix, record all errors and scaling data."""
    results = {}
    for radius in [2, 3, 5, 7]:
        for dt in [0.1, 0.05, 0.02, 0.01]:
            results[(radius, dt)] = maxwell_evolution_v6_parametric(...)
    return results
```

Output: Structured results file (JSON) with all measurements.

### 4. Analysis and Plotting
```python
def analyze_phase6d_results(results):
    """Extract scaling laws and generate plots."""
    # Plot 1: Error vs radius
    # Plot 2: Error vs dt
    # Plot 3: Scaling law verification
    # Plot 4: 3D surface of error(radius, dt)
```

Output: Matplotlib figures showing convergence behavior.

### 5. Report Generation
Comprehensive report (Markdown):
- Executive summary of scaling results
- Hypothesis confirmation or refutation
- Error decomposition (domain vs time vs operator)
- Continuum limit extrapolation
- Recommendations for Phase 6E

---

## Expected Outcomes

### Success Case
Error follows predicted scaling:
```
error(radius, dt) ≈ C₁/radius² + C₂·dt²
```

With C₁, C₂ ~O(1), confirming:
- Domain effects scale as O(N⁻¹)
- Time discretization scales as O(dt²)
- Both approach zero in refinement limit

### Partial Success Case
Error decreases with refinement but doesn't match simple scaling law.
- Indicates additional error sources (e.g., boundary effects, Poisson solver accuracy)
- Requires investigation of error mechanisms

### Failure Case
Error plateaus or increases with refinement.
- Suggests fundamental issue with Phase 6C implementation
- Would require debugging extraction method or Poisson solver

---

## Files to Create/Modify

### New Files
- `discrete_domain_generator.py` - Utilities for arbitrary-size hexagon clusters
- `phase6d_parametric_solver.py` - Refactored Maxwell solver for scaling studies
- `phase6d_benchmark.py` - 16-case test matrix execution
- `phase6d_analysis.py` - Error analysis and plotting
- `PHASE_6D_RESULTS.md` - Benchmark results and report
- `phase6d_plots/` - Directory for generated figures

### Modified Files
- `discrete_maxwell_solver_v6_poisson.py` - Extract reusable components

---

## Timeline Estimate

1. **Domain generation** (1 hr) - Create hexagon_cluster utilities
2. **Parametric solver** (2 hrs) - Refactor V6 for arbitrary domains/dt
3. **Benchmark execution** (4 hrs) - Run 16 cases (some may take time for large domains)
4. **Analysis** (2 hrs) - Process results, generate plots
5. **Report** (1 hr) - Write up findings

**Total: ~10 hours**

---

## Risk Mitigation

### Risk: Large domains slow down Poisson solver
**Mitigation:** Profile Poisson solver performance early. If slow, optimize FFT implementation or use iterative solver for larger domains.

### Risk: Floating-point errors accumulate in long simulations
**Mitigation:** Use higher precision (complex128) if needed. Monitor for NaN/Inf blowups.

### Risk: Results don't show expected scaling
**Mitigation:** Fallback to detailed error source analysis. May require investigating lattice dispersion, boundary conditions, or numerical method accuracy.

---

## Next Phase (6E)

Based on Phase 6D results:

- **If error → 0:** Declare Maxwell validation complete. Move to gravity field validation (Phase 7).
- **If error plateaus:** Investigate and implement alternative extraction methods or improved Poisson solver.
- **If error is systematic:** Analyze error sources and develop targeted refinements.

---

## Connection to Larger Goals

Phase 6 Maxwell validation is one component of comprehensive One-Wave framework validation:

```
Phase 1-4:  Wave equation structure ✓
Phase 5:    Modified rule for transverse modes ✓
Phase 6:    Maxwell equation validation (6A-6D)
  6A: Asymmetric approach [2x error]
  6B: Symmetric Laplacian [2x improvement → 2.36]
  6C: Poisson-based extraction [68.8% improvement → 0.74]
  6D: Continuum limit validation [target: error → 0]
Phase 7:    Gravity field validation
Phase 8:    Complete Standard Model
```

Phase 6D completion unlocks Phase 7 work.
