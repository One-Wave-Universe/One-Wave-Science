import unittest

from triad_brain import cycle, stop


class TriadBrainTests(unittest.TestCase):
    def test_cpu_native_not_jetson(self):
        s = cycle("FIELD", "HOLD", "PHASE")
        self.assertEqual(s.device, "CPU_REFERENCE")
        self.assertFalse(s.committed)

    def test_only_void_resolving_commits(self):
        self.assertFalse(cycle("FIELD", "UP", "DIRECTION", verb="Resolving").committed)
        self.assertTrue(stop().committed)
        self.assertEqual(stop().ac, "HOLD")

    def test_rejects_fourth_ac_move(self):
        with self.assertRaises(ValueError):
            cycle("FIELD", "SIDEWAYS", "PHASE")


if __name__ == "__main__":
    unittest.main()
