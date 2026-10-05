import math
import unittest

from point_rotation import PointAttitude, compose, det3, inertia_axis_stability, point_L_dot, receipt_planar_spin, rot_z, step_L


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


    def test_open_gradient_keeps_L(self):
        L = (0.2, 0.0, 1.5)
        d_open = point_L_dot(L, True, 3.0, gravity=(9.0, 0.0, 0.0))
        d_open_other = point_L_dot(L, True, 3.0, gravity=(0.0, 4.0, 0.0))
        self.assertEqual(d_open, (0.0, 0.0, 0.0))
        self.assertEqual(d_open, d_open_other)
        self.assertEqual(step_L(L, 0.1, True, 3.0, gravity=(1.0, 2.0, 3.0)), L)

    def test_closed_gradient_resists_and_ignores_gravity(self):
        L = (0.0, 0.0, 2.0)
        d1 = point_L_dot(L, False, 4.0, gravity=(0.0, 0.0, 0.0))
        d2 = point_L_dot(L, False, 4.0, gravity=(8.0, -3.0, 1.0))
        self.assertEqual(d1, d2)
        self.assertEqual(d1, (0.0, 0.0, -8.0))
        nxt = step_L(L, 0.1, False, 4.0, gravity=(5.0, 5.0, 5.0))
        self.assertAlmostEqual(nxt[2], 1.2, places=12)
        self.assertLess(abs(nxt[2]), abs(L[2]))

    def test_middle_inertia_axis_fights(self):
        labels = inertia_axis_stability((1.0, 3.0, 2.0))
        self.assertEqual(labels[0], "stable")
        self.assertEqual(labels[2], "fights")
        self.assertEqual(labels[1], "stable")

if __name__ == "__main__":
    unittest.main()
