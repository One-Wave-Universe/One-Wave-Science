import unittest

import numpy as np

from planetary_displacement_state import (
    Bound2DState, FieldState, PathState, PlanetaryDisplacementState, PointState,
    RecursivePPF, RotationState, distinguishable_active_range, em_shell_modifier,
    local_reference_slope, make_receipt,
)


def earth_state() -> PlanetaryDisplacementState:
    z = np.zeros(3)
    rotations = RotationState(np.array([0., 0., 1.1]), np.array([0., 0., .9]),
                              np.array([0., 0., 1.0]), np.array([0., 0., 1.]),
                              np.array([0., 0., .8]), np.array([0., 0., .7]))
    return PlanetaryDisplacementState(
        "Earth", Bound2DState(1., 1., 1., .1, 1., 0., 1.),
        PointState(1., 0., rotations, z, z),
        PathState(np.array([1., 0., 0.]), np.array([0., 1., 0.]), 0., 0., 1.),
        FieldState(2., .1, 3., rotations.field, 0., 1., .25),
        RecursivePPF(*range(1, 10)),
    )


class PlanetaryDisplacementStateTests(unittest.TestCase):
    def test_local_minus_reference_slope(self):
        local, delta = local_reference_slope(np.array([2., 3.]), np.array([.5, .25]), .4)
        self.assertAlmostEqual(local, 1.75)
        self.assertAlmostEqual(delta, 1.35)

    def test_active_range_is_derived_from_distinguishability(self):
        radius = np.arange(5.)
        slope = np.array([5., 2., .8, .21, .05])
        reference = np.zeros(5)
        self.assertEqual(distinguishable_active_range(radius, slope, reference, .2), 3.)

    def test_path_rotation_uses_relational_state(self):
        self.assertTrue(np.allclose(earth_state().path.rotation, np.array([0., 0., 1.])))

    def test_receipt_contains_nine_component_ppf_and_rotations(self):
        receipt = make_receipt(earth_state(), np.array([2., 1., .5]),
                               np.array([1., .3, 0.]), np.ones(10) * .1)
        self.assertEqual(receipt.overlap_count, 2)
        self.assertGreater(receipt.ppf_norm, 0.)
        self.assertAlmostEqual(receipt.core_mantle_differential, .1)
        self.assertAlmostEqual(receipt.matter_em_differential, .2)

    def test_no_global_dipole_control_can_disable_em_modifier(self):
        self.assertEqual(em_shell_modifier(4., 0., 99.), 4.)


if __name__ == "__main__":
    unittest.main()
