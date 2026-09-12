import unittest

import numpy as np

from solar_system_control import (
    HAS_GLOBAL_INTRINSIC_DIPOLE, NAMES, SPIN_PERIOD_DAYS, acceleration_receipt,
    attached_marker, energy, external_parent_tidal_acceleration, initial_state,
    orbital_period_days, spin_orbit_ratio, step,
)


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
        self.assertEqual(
            set(receipt),
            {"newtonian", "relativity_1pn", "one_wave_candidate", "external_parent_wake"},
        )
        self.assertTrue(np.all(receipt["one_wave_candidate"] == 0.0))
        self.assertTrue(np.all(receipt["external_parent_wake"] == 0.0))
        self.assertGreater(np.linalg.norm(receipt["relativity_1pn"]), 0.0)

    def test_gray_control_energy_drift_is_small(self):
        r, v = initial_state()
        e0 = energy(r, v)
        for day in range(365):
            r, v = step(r, v, 1.0, day)
        self.assertLess(abs((energy(r, v) - e0) / e0), 2e-5)

    def test_mercury_spin_orbit_ratio_is_the_real_three_two_resonance(self):
        # Standard gravitational/tidal control fact (UPDATED_38/39): Mercury
        # is NOT tidally locked 1:1. It completes 3 rotations per 2 orbits.
        # This must not be relabeled as an electromagnetic lock.
        self.assertAlmostEqual(spin_orbit_ratio("Mercury"), 1.5, places=3)

    def test_moon_spin_period_matches_its_orbital_period(self):
        # The Moon genuinely is tidally locked to Earth (1:1), by ordinary
        # gravitational tidal torque -- not by any magnetic mechanism.
        self.assertAlmostEqual(spin_orbit_ratio("Moon"), 1.0, places=6)

    def test_venus_and_mars_have_no_global_intrinsic_dipole(self):
        # Explicit Updated 39/40 control: these two must not receive a
        # global EM-shell term, ruling out "bound by a parent magnetic
        # field" as the explanation for their rotation state.
        self.assertFalse(HAS_GLOBAL_INTRINSIC_DIPOLE["Venus"])
        self.assertFalse(HAS_GLOBAL_INTRINSIC_DIPOLE["Mars"])
        self.assertFalse(HAS_GLOBAL_INTRINSIC_DIPOLE["Moon"])
        self.assertTrue(HAS_GLOBAL_INTRINSIC_DIPOLE["Mercury"])
        self.assertTrue(HAS_GLOBAL_INTRINSIC_DIPOLE["Earth"])
        for giant in ("Jupiter", "Saturn", "Uranus", "Neptune"):
            self.assertTrue(HAS_GLOBAL_INTRINSIC_DIPOLE[giant])

    def test_orbital_period_recovers_known_values(self):
        # Kepler's third law from the same JPL elements/mu already used for
        # position -- an independent Gray control check, not a new claim.
        self.assertAlmostEqual(orbital_period_days("Earth"), 365.25, delta=0.5)
        self.assertAlmostEqual(orbital_period_days("Mercury"), 87.969, delta=0.1)

    def test_external_parent_wake_defaults_to_zero(self):
        r = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
        self.assertTrue(np.all(external_parent_tidal_acceleration(r) == 0.0))

    def test_external_parent_wake_uses_declared_tensor_and_center(self):
        r = np.array([[3.0, 0.0, 0.0]])
        tensor = np.diag([2.0, -1.0, -1.0])
        center = np.array([1.0, 0.0, 0.0])
        result = external_parent_tidal_acceleration(r, tensor, center)
        self.assertTrue(np.allclose(result, np.array([[4.0, 0.0, 0.0]])))

    def test_all_bodies_have_spin_and_dipole_data(self):
        for name in NAMES:
            self.assertIn(name, SPIN_PERIOD_DAYS)
            self.assertIn(name, HAS_GLOBAL_INTRINSIC_DIPOLE)


if __name__ == "__main__":
    unittest.main()
