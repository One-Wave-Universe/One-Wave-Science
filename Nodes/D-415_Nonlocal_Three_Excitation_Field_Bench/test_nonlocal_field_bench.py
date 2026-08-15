import unittest

import numpy as np

from nonlocal_field_bench import (
    Config,
    advance,
    field_descriptors,
    harmonic_branches,
    make_global_kernel,
    minimum_image,
    relational_observables,
    triangular_laplacian,
    update_phase_locks,
)


class NonlocalFieldBenchTests(unittest.TestCase):
    def test_six_neighbor_laplacian_preserves_constant(self):
        field = np.full((12, 12), 2.0 + 3.0j)
        self.assertTrue(np.allclose(triangular_laplacian(field, 1.0), 0.0))

    def test_global_kernel_is_positive_and_normalized(self):
        kernel, _ = make_global_kernel(Config(n=12))
        self.assertGreater(float(kernel.min()), 0.0)
        self.assertAlmostEqual(float(kernel.sum()), 1.0, places=14)

    def test_field_update_is_translation_covariant(self):
        cfg = Config(n=16)
        _, kernel_fft = make_global_kernel(cfg)
        rng = np.random.default_rng(4)
        previous = rng.normal(size=(16, 16)) + 1j * rng.normal(size=(16, 16))
        current = rng.normal(size=(16, 16)) + 1j * rng.normal(size=(16, 16))
        expected = np.roll(advance(previous, current, cfg, kernel_fft), (3, -2), (0, 1))
        actual = advance(
            np.roll(previous, (3, -2), (0, 1)),
            np.roll(current, (3, -2), (0, 1)),
            cfg,
            kernel_fft,
        )
        self.assertTrue(np.allclose(actual, expected, atol=1e-12))

    def test_relational_outputs_ignore_common_translation(self):
        centers = np.array([[2.0, 3.0], [8.0, 4.0], [5.0, 10.0]])
        weights = np.array([2.0, 3.0, 4.0])
        shifted = (centers + np.array([5.0, 7.0])) % 16.0
        a = relational_observables(centers, weights, 16)
        b = relational_observables(shifted, weights, 16)
        for key in ("edge_12", "edge_23", "edge_31", "hyperradius"):
            self.assertAlmostEqual(a[key], b[key], places=12)

    def test_minimum_image(self):
        actual = minimum_image(np.array([15.0, -15.0]), 16)
        self.assertTrue(np.array_equal(actual, np.array([-1.0, 1.0])))

    def test_short_run_remains_finite(self):
        cfg = Config(n=16)
        _, kernel_fft = make_global_kernel(cfg)
        rng = np.random.default_rng(9)
        previous = 0.01 * (rng.normal(size=(16, 16)) + 1j * rng.normal(size=(16, 16)))
        current = previous.copy()
        for _ in range(50):
            following = advance(previous, current, cfg, kernel_fft)
            previous, current = current, following
        self.assertTrue(np.isfinite(current).all())

    def test_harmonic_graph_has_shared_nodes(self):
        self.assertEqual(harmonic_branches(0), (1, 3))
        self.assertEqual(harmonic_branches(1), (3, 5))

    def test_lock_hysteresis_builds_and_breaks(self):
        cfg = Config()
        lock = np.zeros(3)
        for _ in range(8):
            lock, _, _ = update_phase_locks(lock, np.zeros(3), np.zeros(3), cfg)
        self.assertTrue(np.all(lock > 0.5))
        lock, _, _ = update_phase_locks(
            lock,
            np.array([0.0, 1.0, 2.0]),
            np.array([0.0, 2.0, -2.0]),
            cfg,
        )
        self.assertTrue(np.all(lock < 1.0))

    def test_field_descriptors_are_finite(self):
        cfg = Config(n=16)
        q, r = np.indices((16, 16))
        current = np.exp(1j * 2.0 * np.pi * q / 16.0)
        descriptors = field_descriptors(current, current, cfg)
        for key in (
            "phase_coherence",
            "field_velocity_rms",
            "field_vorticity_rms",
            "stress_trace_mean",
        ):
            self.assertTrue(np.isfinite(descriptors[key]))


if __name__ == "__main__":
    unittest.main()
