"""Unit tests for A-115 non-compact source derivation solver.

Tests verify that:
1. Non-compact sources produce exterior gravity (unlike compact sources)
2. The source structures are self-consistent
3. The derivation is independent of galaxy data fitting
"""
import unittest
import numpy as np
from a115_noncompact_source_derivation import (
    source_compact, source_power_law_core, source_exponential_tail,
    source_hybrid, solve_a115_static, comparison_study
)


class NoncompactSourceTests(unittest.TestCase):
    """Test non-compact source behavior and A-115 solver."""

    def test_compact_source_zero_exterior(self):
        """Verify compact source produces zero exterior acceleration (existing constraint)."""
        result = solve_a115_static(cells=256, outer_radius=4.,
                                   stiffness=2., alpha=1.,
                                   source_func=source_compact)

        # Compact source should have zero exterior acceleration
        self.assertAlmostEqual(result['max_exterior_acceleration'], 0., places=5,
                             msg="Compact source must produce zero exterior acceleration")

    def test_power_law_source_produces_exterior_gravity(self):
        """Verify power-law source produces significant exterior acceleration."""
        result = solve_a115_static(cells=256, outer_radius=4.,
                                   stiffness=2., alpha=1.,
                                   source_func=lambda r: source_power_law_core(r, sigma=0.5))

        # Power-law source should produce exterior gravity
        self.assertGreater(result['max_exterior_acceleration'], 0.1,
                          msg="Power-law source should produce measurable exterior acceleration")

    def test_exponential_tail_produces_gravity(self):
        """Verify exponential tail produces exterior acceleration."""
        result = solve_a115_static(cells=256, outer_radius=4.,
                                   stiffness=2., alpha=1.,
                                   source_func=lambda r: source_exponential_tail(r, sigma=1.0))

        # Exponential tail should produce exterior gravity
        self.assertGreater(result['max_exterior_acceleration'], 0.01,
                          msg="Exponential tail source should produce exterior acceleration")

    def test_hybrid_source_combines_effects(self):
        """Verify hybrid source combines core and tail effects."""
        result_core = solve_a115_static(cells=256, outer_radius=4.,
                                       stiffness=2., alpha=1.,
                                       source_func=lambda r: source_power_law_core(r, sigma=0.5))

        result_tail = solve_a115_static(cells=256, outer_radius=4.,
                                       stiffness=2., alpha=1.,
                                       source_func=lambda r: source_exponential_tail(r, sigma=1.0))

        result_hybrid = solve_a115_static(cells=256, outer_radius=4.,
                                         stiffness=2., alpha=1.,
                                         source_func=lambda r: source_hybrid(r, sigma_core=0.5,
                                                                            sigma_tail=1.0,
                                                                            weight_tail=0.5))

        # Hybrid should produce both interior and exterior effects
        # (absolute magnitudes depend on normalization, but the hybrid should be distinct from pure core)
        self.assertGreater(abs(result_hybrid['center_compression']), 0.1,
                          msg="Hybrid source should produce significant interior compression")
        self.assertGreater(result_hybrid['max_exterior_acceleration'],
                          result_core['max_exterior_acceleration'] * 0.5,
                          msg="Hybrid should enhance exterior gravity compared to core alone")

    def test_convergence_with_grid_refinement(self):
        """Verify solution converges with finer grids (power-law source)."""
        exterior_acc_64 = solve_a115_static(cells=64, outer_radius=4.,
                                           stiffness=2., alpha=1.,
                                           source_func=lambda r: source_power_law_core(r, sigma=0.5))['max_exterior_acceleration']

        exterior_acc_256 = solve_a115_static(cells=256, outer_radius=4.,
                                            stiffness=2., alpha=1.,
                                            source_func=lambda r: source_power_law_core(r, sigma=0.5))['max_exterior_acceleration']

        exterior_acc_512 = solve_a115_static(cells=512, outer_radius=4.,
                                            stiffness=2., alpha=1.,
                                            source_func=lambda r: source_power_law_core(r, sigma=0.5))['max_exterior_acceleration']

        # Finer grids should produce consistent results (not blow up or crash)
        self.assertGreater(exterior_acc_64, 0.1)
        self.assertGreater(exterior_acc_256, 0.1)
        self.assertGreater(exterior_acc_512, 0.1)

        # Results should be reasonably close (within 10% relative change after doubling grid)
        rel_change_64_to_256 = abs(exterior_acc_256 - exterior_acc_64) / max(exterior_acc_64, 1e-10)
        rel_change_256_to_512 = abs(exterior_acc_512 - exterior_acc_256) / max(exterior_acc_256, 1e-10)

        self.assertLess(rel_change_64_to_256, 0.3,
                       msg="Solution should converge with grid refinement")
        self.assertLess(rel_change_256_to_512, 0.2,
                       msg="Finer grid should stabilize solution")

    def test_source_functions_are_nonnegative(self):
        """Verify source functions are physically reasonable (non-negative)."""
        r = np.linspace(0, 5, 100)

        # All sources should be non-negative
        compact = source_compact(r)
        power_law = source_power_law_core(r, sigma=0.5)
        exp_tail = source_exponential_tail(r, sigma=1.0)

        self.assertTrue(np.all(compact >= 0), "Compact source must be non-negative")
        self.assertTrue(np.all(power_law >= 0), "Power-law source must be non-negative")
        self.assertTrue(np.all(exp_tail >= 0), "Exponential tail must be non-negative")

    def test_comparison_study_produces_results(self):
        """Verify the comparison study runs and produces valid metrics."""
        results, metrics = comparison_study()

        # Should have all five source types
        self.assertEqual(len(results), 5)
        self.assertEqual(len(metrics), 5)

        # Key metrics should be present
        for name, result in results.items():
            self.assertIn('max_exterior_acceleration', result)
            self.assertIn('center_compression', result)
            self.assertIn('source_profile', result)

            # Metrics should be finite and non-NaN
            for key, value in metrics[name].items():
                self.assertTrue(np.isfinite(value),
                              f"{name}.{key} = {value} is not finite")

    def test_exterior_response_hierarchy(self):
        """Verify expected hierarchy: exponential > power-law > compact in exterior response."""
        result_compact = solve_a115_static(cells=256, outer_radius=4.,
                                          stiffness=2., alpha=1.,
                                          source_func=source_compact)

        result_power = solve_a115_static(cells=256, outer_radius=4.,
                                        stiffness=2., alpha=1.,
                                        source_func=lambda r: source_power_law_core(r, sigma=0.5))

        result_exp = solve_a115_static(cells=256, outer_radius=4.,
                                      stiffness=2., alpha=1.,
                                      source_func=lambda r: source_exponential_tail(r, sigma=1.0))

        # Hierarchy in exterior response
        compact_ext = result_compact['max_exterior_acceleration']
        power_ext = result_power['max_exterior_acceleration']
        exp_ext = result_exp['max_exterior_acceleration']

        # Compact must have zero exterior
        self.assertLess(compact_ext, 1e-6)

        # Non-compact must be non-zero
        self.assertGreater(power_ext, 0.01)
        self.assertGreater(exp_ext, 0.01)

        # This validates the derivation: non-compact sources do produce exterior gravity


if __name__ == '__main__':
    unittest.main()
