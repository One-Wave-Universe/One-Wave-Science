import math
import unittest

from body_rate_transport import compose_omega_body, compose_omega_ground, rot_x, rot_z


class BodyRateTransportTests(unittest.TestCase):
    def test_planar_rates_add(self):
        w = compose_omega_body((0, 0, 1), (0, 0, 2), rot_z(0.4))
        self.assertAlmostEqual(w[2], 3.0, places=12)

    def test_tilted_child_pulls_parent_z_into_xy(self):
        # child frame is rotated 90 deg about x relative to parent
        w = compose_omega_body((0, 0, 1), (0, 0, 0), rot_x(math.pi / 2))
        self.assertAlmostEqual(w[0], 0.0, places=12)
        self.assertAlmostEqual(w[1], -1.0, places=12)
        self.assertAlmostEqual(w[2], 0.0, places=12)

    def test_body_and_ground_charts_agree_on_speed(self):
        wp, wc = (0.2, 0.0, 0.5), (0.0, 0.3, 0.0)
        Rc = rot_x(0.7)
        Rp = rot_z(0.2)
        wb = compose_omega_body(wp, wc, Rc)
        wg = compose_omega_ground(wp, wc, Rp, Rc)
        nb = wb[0] ** 2 + wb[1] ** 2 + wb[2] ** 2
        ng = wg[0] ** 2 + wg[1] ** 2 + wg[2] ** 2
        self.assertAlmostEqual(nb, ng, places=10)


if __name__ == "__main__":
    unittest.main()
