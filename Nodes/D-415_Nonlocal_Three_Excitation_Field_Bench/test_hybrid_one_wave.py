import unittest

import numpy as np

from hybrid_one_wave import hybrid_channels, hybrid_step, make_receipt
from solar_system_control import MASSES, initial_state


class HybridOneWaveTests(unittest.TestCase):
    def test_default_is_gray_plus_relativity(self):
        r, v = initial_state()
        channels = hybrid_channels(r, v, 0.0)
        self.assertTrue(np.all(channels["one_wave_explanation_raw"] == 0.0))
        self.assertTrue(np.all(channels["one_wave_explanation_closed"] == 0.0))

    def test_internal_candidate_cannot_invent_translation_or_rotation(self):
        r, v = initial_state()
        rng = np.random.default_rng(415)
        raw = rng.normal(size=r.shape) * 1e-12
        channels = hybrid_channels(r, v, 0.0, lambda *_: raw)
        closed = channels["one_wave_explanation_closed"]
        center = np.sum(MASSES[:, None] * r, axis=0) / MASSES.sum()
        translation = np.sum(MASSES[:, None] * closed, axis=0)
        torque = np.sum(np.cross(r - center, MASSES[:, None] * closed), axis=0)
        self.assertLess(np.linalg.norm(translation), 1e-25)
        self.assertLess(np.linalg.norm(torque), 1e-25)

    def test_receipt_exposes_every_channel(self):
        r, v = initial_state()
        receipt = make_receipt(r, v, 0.0)
        self.assertGreater(receipt.newtonian_norm, receipt.relativity_norm)
        self.assertEqual(receipt.one_wave_explanation_closed_norm, 0.0)
        self.assertEqual(receipt.relativity_explanation_mismatch, receipt.relativity_norm)

    def test_explanation_is_not_added_to_orbit(self):
        r, v = initial_state()
        huge = lambda *_: np.ones_like(r)
        r0, v0, _ = hybrid_step(r, v, 0.1, 0.0)
        r1, v1, _ = hybrid_step(r, v, 0.1, 0.0, huge)
        self.assertTrue(np.array_equal(r0, r1))
        self.assertTrue(np.array_equal(v0, v1))

    def test_nonfinite_candidate_is_rejected_before_step(self):
        r, v = initial_state()
        nonfinite = lambda *_: np.full_like(r, np.nan)
        with self.assertRaisesRegex(ValueError, "finite acceleration"):
            hybrid_step(r, v, 0.1, 0.0, nonfinite)

    def test_hybrid_step_is_finite(self):
        r, v = initial_state()
        r, v, receipt = hybrid_step(r, v, 0.25, 0.0)
        self.assertTrue(np.isfinite(r).all())
        self.assertTrue(np.isfinite(v).all())
        self.assertGreater(receipt.total_norm, 0.0)


if __name__ == "__main__":
    unittest.main()
