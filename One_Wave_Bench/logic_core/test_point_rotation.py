import math
import unittest

from point_rotation import PointAttitude, compose, det3, receipt_planar_spin, rot_z


class PointRotationTests(unittest.TestCase):
    def test_rotation_has_unit_det(self):
        rec = receipt_planar_spin(math.pi / 3, 2.0)
        self.assertAlmostEqual(rec["detR"], 1.0, places=12)
        self.assertEqual(rec["L_body"], (0.0, 0.0, 2.0))
        self.assertFalse(rec["path_circulation_stolen"])

    def test_compose_multiplies_frames(self):
        p = PointAttitude(R=rot_z(0.3), omega_body=(0, 0, 1))
        c = PointAttitude(R=rot_z(0.2), omega_body=(0, 0, 4))
        g = compose(p, c)
        self.assertAlmostEqual(det3(g.R), 1.0, places=12)
        self.assertAlmostEqual(g.R[0][0], math.cos(0.5), places=12)
        self.assertEqual(g.omega_body[2], 4.0)

    def test_ground_L_rotates_with_frame(self):
        att = PointAttitude(R=rot_z(math.pi / 2), omega_body=(1.0, 0.0, 0.0))
        Lg = att.L_ground()
        self.assertAlmostEqual(Lg[0], 0.0, places=12)
        self.assertAlmostEqual(Lg[1], 1.0, places=12)


if __name__ == "__main__":
    unittest.main()
