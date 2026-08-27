import unittest

import numpy as np

from solar_system_control import NAMES, acceleration_receipt, attached_marker, energy, initial_state, step


class SolarSystemControlTests(unittest.TestCase):
    def test_all_eight_planets_moon_and_sun_exist(self):
        self.assertEqual(len(NAMES), 10)
        self.assertEqual(set(NAMES), {"Sun", "Mercury", "Venus", "Earth", "Moon", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"})

    def test_barycenter_and_momentum_start_at_origin(self):
        from solar_system_control import MASSES
        r, v = initial_state()
        self.assertTrue(np.allclose(np.sum(MASSES[:, None] * r, axis=0), 0.0, atol=1e-15))
        self.assertTrue(np.allclose(np.sum(MASSES[:, None] * v, axis=0), 0.0, atol=1e-15))

    def test_moon_remains_earth_bound_in_short_control_run(self):
        r, v = initial_state()
        earth, moon = NAMES.index("Earth"), NAMES.index("Moon")
        d0 = np.linalg.norm(r[moon] - r[earth])
        for day in range(30 * 24):
            r, v = step(r, v, 1 / 24, day / 24)
        d1 = np.linalg.norm(r[moon] - r[earth])
        self.assertLess(abs(d1 - d0) / d0, 0.03)

    def test_attached_marker_cannot_outpace_parent(self):
        p = np.array([2., 3., 4.])
        v = np.array([.1, -.2, .3])
        marker, marker_v = attached_marker(p, v, np.array([.01, 0., 0.]))
        self.assertTrue(np.array_equal(marker_v, v))
        self.assertTrue(np.allclose(marker - p, np.array([.01, 0., 0.])))

    def test_physics_channels_are_explicit(self):
        r, v = initial_state()
        receipt = acceleration_receipt(r, v)
        self.assertEqual(set(receipt), {"newtonian", "relativity_1pn", "one_wave_candidate"})
        self.assertTrue(np.all(receipt["one_wave_candidate"] == 0.0))
        self.assertGreater(np.linalg.norm(receipt["relativity_1pn"]), 0.0)

    def test_gray_control_energy_drift_is_small(self):
        r, v = initial_state()
        e0 = energy(r, v)
        for day in range(365):
            r, v = step(r, v, 1.0, day)
        self.assertLess(abs((energy(r, v) - e0) / e0), 2e-5)


if __name__ == "__main__":
    unittest.main()
