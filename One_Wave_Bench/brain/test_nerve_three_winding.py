import unittest

from nerve_three_winding import from_admin, m4_may_drive, rest


class ThreeWindingNerveTests(unittest.TestCase):
    def test_rest_is_hold(self):
        n = rest()
        self.assertEqual((n.u, n.v, n.w), ("HOLD", "HOLD", "HOLD"))

    def test_m4_cannot_drive(self):
        self.assertFalse(m4_may_drive())

    def test_admin_up_is_three_phase(self):
        n = from_admin("UP")
        self.assertEqual(n.source, "ADMIN")
        self.assertEqual(len({n.u, n.v, n.w}), 3)


if __name__ == "__main__":
    unittest.main()
