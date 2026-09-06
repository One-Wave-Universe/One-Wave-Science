import unittest

from mute_cycle import mute_cycle, stop_cycle
from nerve_three_winding import m4_may_drive


class MuteCycleTests(unittest.TestCase):
    def test_accept_up_moves_windings(self):
        r = mute_cycle("UP", True)
        self.assertEqual(r.admin, "UP")
        self.assertNotEqual((r.nerve.u, r.nerve.v, r.nerve.w), ("HOLD", "HOLD", "HOLD"))
        self.assertFalse(r.committed)

    def test_admin_reject_is_stop(self):
        r = stop_cycle("UP")
        self.assertEqual(r.admin, "STOP")
        self.assertEqual((r.nerve.u, r.nerve.v, r.nerve.w), ("HOLD", "HOLD", "HOLD"))
        self.assertTrue(r.committed)

    def test_m4_still_cannot_drive(self):
        self.assertFalse(m4_may_drive())

    def test_no_words(self):
        with self.assertRaises(ValueError):
            mute_cycle("follow", True)


if __name__ == "__main__":
    unittest.main()
