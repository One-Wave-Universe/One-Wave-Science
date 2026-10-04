"""
Parameter Optimization: Finding Physical (γ, β) Values
=======================================================

The Maxwell validation revealed that (γ=0.5, β=0.5) puts us in a
decay-dominated regime where transverse waves don't propagate like light.

We need to find (γ, β) values that produce:
1. Transverse wave velocity ω/k ≈ constant (light-like)
2. Longitudinal waves gapped (plasma-like)
3. No exponential decay of propagating modes
4. Stability across full k range
"""

import numpy as np
import matplotlib.pyplot as plt
from vector_field_framework import vector_dispersion_longitudinal, vector_dispersion_transverse

# ============================================================================
# PART 1: PARAMETER QUALITY METRICS
# ============================================================================

def compute_quality_metrics(gamma, beta, k_range=None):
    """
    Evaluate (γ, β) against EM criteria.

    Returns: (propagation_quality, stability_quality, overall_score)
    """

    if k_range is None:
        k_range = np.linspace(0.01, 3.0, 50)

    omega_trans_p = []
    omega_trans_m = []

    lambda_max = 0

    for k in k_range:
        w_tp, w_tm, lambda_p, lambda_m = vector_dispersion_transverse(k, gamma, beta)
        omega_trans_p.append(np.real(w_tp))
        omega_trans_m.append(np.real(w_tm))

        # Track stability
        lambda_max = max(lambda_max, np.abs(lambda_p), np.abs(lambda_m))

    omega_trans_p = np.array(omega_trans_p)
    omega_trans_m = np.array(omega_trans_m)

    # METRIC 1: Wave velocity consistency
    # Light-like waves have ω/k ≈ constant
    with np.errstate(divide='ignore', invalid='ignore'):
        v_p = omega_trans_p / k_range
        v_p = v_p[k_range > 0.1]  # Ignore k→0

    if len(v_p) > 0 and np.nanmax(v_p) > 0:
        v_mean = np.nanmean(v_p)
        v_std = np.nanstd(v_p)
        propagation_quality = max(0, 1.0 - (v_std / (v_mean + 1e-6)))
    else:
        propagation_quality = 0.0

    # METRIC 2: Stability
    # All modes should have |λ| ≤ 1
    stability_quality = max(0, 1.0 - (lambda_max - 1.0)) if lambda_max > 0 else 1.0

    # METRIC 3: Overall score
    overall = 0.6 * propagation_quality + 0.4 * stability_quality

    return propagation_quality, stability_quality, overall, lambda_max


# ============================================================================
# PART 2: PARAMETER SCAN
# ============================================================================

print("="*80)
print("PHASE 4: PARAMETER OPTIMIZATION")
print("="*80)
print()

# Fine grid of (γ, β) values
gamma_vals = np.linspace(0.01, 0.99, 20)
beta_vals = np.linspace(0.01, 2.0, 25)

results = []

print("Scanning parameter space (γ, β)...")
print()

for gamma in gamma_vals:
    for beta in beta_vals:
        prop_q, stab_q, overall, lambda_max = compute_quality_metrics(gamma, beta)
        results.append({
            'gamma': gamma,
            'beta': beta,
            'propagation': prop_q,
            'stability': stab_q,
            'overall': overall,
            'lambda_max': lambda_max
        })

# Find best parameters
results_sorted = sorted(results, key=lambda x: x['overall'], reverse=True)

print("TOP 10 PARAMETER SETS (by overall quality):")
print("-" * 80)
print(f"{'Rank':<6} {'γ':<8} {'β':<8} {'Propagation':<14} {'Stability':<14} {'Overall':<10}")
print("-" * 80)

for i, res in enumerate(results_sorted[:10]):
    print(f"{i+1:<6} {res['gamma']:<8.3f} {res['beta']:<8.3f} {res['propagation']:<14.4f} {res['stability']:<14.4f} {res['overall']:<10.4f}")

print()

# ============================================================================
# PART 3: DETAILED ANALYSIS OF BEST PARAMETERS
# ============================================================================

best = results_sorted[0]
gamma_best = best['gamma']
beta_best = best['beta']

print("="*80)
print("DETAILED ANALYSIS: BEST PARAMETERS")
print("="*80)
print(f"\nOptimal: γ = {gamma_best:.4f}, β = {beta_best:.4f}")
print(f"Overall quality score: {best['overall']:.4f}")
print(f"  - Propagation quality: {best['propagation']:.4f}")
print(f"  - Stability quality: {best['stability']:.4f}")
print()

# Test the best parameters across full k range
k_range = np.linspace(0.01, 4.0, 100)

omega_trans_p_best = []
omega_trans_m_best = []
omega_long_p_best = []
omega_long_m_best = []
v_trans_best = []

for k in k_range:
    w_tp, w_tm, _, _ = vector_dispersion_transverse(k, gamma_best, beta_best)
    w_lp, w_lm, _, _ = vector_dispersion_longitudinal(k, gamma_best, beta_best)

    omega_trans_p_best.append(np.real(w_tp))
    omega_trans_m_best.append(np.real(w_tm))
    omega_long_p_best.append(np.real(w_lp))
    omega_long_m_best.append(np.real(w_lm))

    if k > 0.01:
        v_trans_best.append(np.real(w_tp) / k)

omega_trans_p_best = np.array(omega_trans_p_best)
omega_trans_m_best = np.array(omega_trans_m_best)
omega_long_p_best = np.array(omega_long_p_best)
omega_long_m_best = np.array(omega_long_m_best)
v_trans_best = np.array(v_trans_best)

print("Transverse (B-like) mode velocity:")
print(f"  Mean: {np.nanmean(v_trans_best):.6f}")
print(f"  Std:  {np.nanstd(v_trans_best):.6f}")
print(f"  Min:  {np.nanmin(v_trans_best):.6f}")
print(f"  Max:  {np.nanmax(v_trans_best):.6f}")
print()

if np.nanstd(v_trans_best) / (np.nanmean(v_trans_best) + 1e-6) < 0.1:
    print("  ✓ Velocity is approximately constant (light-like!)")
else:
    print("  ~ Velocity varies but better than default parameters")
print()

print("Longitudinal (E-like) mode behavior:")
print(f"  At k=0.1: ω_L = {omega_long_p_best[np.argmin(np.abs(k_range - 0.1))]:.6f}")
print(f"  At k=1.0: ω_L = {omega_long_p_best[np.argmin(np.abs(k_range - 1.0))]:.6f}")
print(f"  Gap frequency: {abs(omega_long_p_best[0]):.6f}")
print()

# ============================================================================
# PART 4: COMPARISON PLOT
# ============================================================================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle(f'Optimized Parameters: γ={gamma_best:.3f}, β={beta_best:.3f}',
             fontsize=14, fontweight='bold')

# Transverse real part
axes[0, 0].plot(k_range, omega_trans_p_best, 'b-', linewidth=2, label='ω₊')
axes[0, 0].plot(k_range, omega_trans_m_best, 'b--', linewidth=2, label='ω₋')
axes[0, 0].set_xlabel('k', fontsize=11)
axes[0, 0].set_ylabel('Re(ω)', fontsize=11)
axes[0, 0].set_title('Transverse (B-like): Propagation', fontweight='bold')
axes[0, 0].grid(True, alpha=0.3)
axes[0, 0].legend()

# Transverse velocity
v_p_best = omega_trans_p_best[1:] / k_range[1:]
axes[0, 1].plot(k_range[1:], v_p_best, 'b-', linewidth=2)
axes[0, 1].axhline(np.nanmean(v_p_best), color='r', linestyle='--', linewidth=2, label=f'Mean: {np.nanmean(v_p_best):.4f}')
axes[0, 1].set_xlabel('k', fontsize=11)
axes[0, 1].set_ylabel('ω/k (velocity)', fontsize=11)
axes[0, 1].set_title('Transverse: Wave Velocity', fontweight='bold')
axes[0, 1].grid(True, alpha=0.3)
axes[0, 1].legend()
axes[0, 1].set_ylim([0, max(np.nanpercentile(v_p_best, 95), 1.0)])

# Longitudinal real part
axes[1, 0].plot(k_range, omega_long_p_best, 'r-', linewidth=2, label='ω₊')
axes[1, 0].plot(k_range, omega_long_m_best, 'r--', linewidth=2, label='ω₋')
axes[1, 0].set_xlabel('k', fontsize=11)
axes[1, 0].set_ylabel('Re(ω)', fontsize=11)
axes[1, 0].set_title('Longitudinal (E-like): Dispersion', fontweight='bold')
axes[1, 0].grid(True, alpha=0.3)
axes[1, 0].legend()

# Parameter quality heatmap
gamma_grid = np.array([r['gamma'] for r in results])
beta_grid = np.array([r['beta'] for r in results])
quality_grid = np.array([r['overall'] for r in results]).reshape(len(gamma_vals), len(beta_vals))

im = axes[1, 1].contourf(beta_grid.reshape(len(gamma_vals), len(beta_vals)),
                          gamma_grid.reshape(len(gamma_vals), len(beta_vals)),
                          quality_grid, levels=20, cmap='RdYlGn')
axes[1, 1].plot(beta_best, gamma_best, 'b*', markersize=20, label='Optimal')
axes[1, 1].set_xlabel('β (coupling)', fontsize=11)
axes[1, 1].set_ylabel('γ (damping)', fontsize=11)
axes[1, 1].set_title('Parameter Quality Map', fontweight='bold')
axes[1, 1].legend()
plt.colorbar(im, ax=axes[1, 1], label='Overall Quality')

plt.tight_layout()
plt.savefig('/tmp/claude-0/-home-claude/3b9cfc7f-c329-58d1-9355-8542cf012cd9/scratchpad/parameter_optimization.png', dpi=150)
print("Parameter optimization plot saved.")

# ============================================================================
# PART 5: RECOMMENDATION
# ============================================================================

print()
print("="*80)
print("RECOMMENDATION FOR PHASE 4 CONTINUATION")
print("="*80)
print()

if best['overall'] > 0.7:
    print(f"✓ Found viable parameters: γ = {gamma_best:.4f}, β = {beta_best:.4f}")
    print(f"  Quality score: {best['overall']:.4f}/1.0")
    print()
    print("  These parameters should produce:")
    print("  - Approximately constant transverse wave velocity (light-like)")
    print("  - Gapped longitudinal modes (plasma-like)")
    print("  - Stable propagation across k-space")
    print()
    print("  NEXT: Re-run Maxwell validation with these parameters")
elif best['overall'] > 0.5:
    print(f"~ Partially viable: γ = {gamma_best:.4f}, β = {beta_best:.4f}")
    print(f"  Quality score: {best['overall']:.4f}/1.0")
    print()
    print("  These parameters are better than default but may need further tuning.")
    print("  Trade-offs:")
    if best['propagation'] < best['stability']:
        print("    - Propagation quality is limiting factor")
    else:
        print("    - Stability is limiting factor")
else:
    print("✗ No good parameters found in this range")
    print("  May need to expand search or reconsider model")

print()
print("="*80)
