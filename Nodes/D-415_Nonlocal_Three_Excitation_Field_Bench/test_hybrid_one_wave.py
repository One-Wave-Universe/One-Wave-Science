import unittest

import numpy as np

from hybrid_one_wave import hybrid_channels, hybrid_step, make_receipt
from solar_system_control import MASSES, initial_state


class HybridOneWaveTests(unittest.TestCase):
    def test_default_is_gray_plus_relativity(self):
        r, v = initial_state()
        channels = hybrid_channels(r, v, 0.0)
        self.assertTrue(np.all(channels["one_wave_raw"] == 0.0))
        self.assertTrue(np.all(channels["one_wave_closed"] == 0.0))

    def test_internal_candidate_cannot_invent_force_or_torque(self):
        r, v = initial_state()
        rng = np.random.default_rng(415)
        raw = rng.normal(size=r.shape) * 1e-12
        channels = hybrid_channels(r, v, 0.0, lambda *_: raw)
        closed = channels["one_wave_closed"]
        center = np.sum(MASSES[:, None] * r, axis=0) / MASSES.sum()
        force = np.sum(MASSES[:, None] * closed, axis=0)
        torque = np.sum(np.cross(r - center, MASSES[:, None] * closed), axis=0)
        self.assertLess(np.linalg.norm(force), 1e-25)
        self.assertLess(np.linalg.norm(torque), 1e-25)

    def test_receipt_exposes_every_channel(self):
        r, v = initial_state()
        receipt = make_receipt(r, v, 0.0)
        self.assertGreater(receipt.newtonian_norm, receipt.relativity_norm)
        self.assertEqual(receipt.one_wave_closed_norm, 0.0)

    def test_hybrid_step_is_finite(self):
        r, v = initial_state()
        r, v, receipt = hybrid_step(r, v, 0.25, 0.0)
        self.assertTrue(np.isfinite(r).all())
        self.assertTrue(np.isfinite(v).all())
        self.assertGreater(receipt.total_norm, 0.0)


if __name__ == "__main__":
    unittest.main()
