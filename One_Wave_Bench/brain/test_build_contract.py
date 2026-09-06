import unittest

from build_contract import KERNEL, NERVE_TO_BRAIN, THRESHOLD_BANDS, VERBS, extra_axes_allowed


class BuildContractTests(unittest.TestCase):
    def test_counts(self):
        self.assertEqual(KERNEL["choices"], 2)
        self.assertEqual(KERNEL["moves"], 3)
        self.assertEqual(KERNEL["gates"], 6)
        self.assertEqual(len(VERBS), 5)
        self.assertEqual(NERVE_TO_BRAIN, (3, 1))
        self.assertFalse(extra_axes_allowed())

    def test_last_band_still_fifteen(self):
        self.assertEqual(THRESHOLD_BANDS[-1], (15, 0))


if __name__ == "__main__":
    unittest.main()
