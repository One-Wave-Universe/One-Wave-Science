import unittest

from scale_ladder import LADDER, is_brain, m4_commits


class ScaleLadderTests(unittest.TestCase):
    def test_order(self):
        self.assertEqual(LADDER[0], "cell")
        self.assertEqual(LADDER[-1], "two_rubiks")

    def test_only_two_rubiks_is_brain(self):
        self.assertFalse(is_brain("rubik"))
        self.assertTrue(is_brain("two_rubiks"))
        self.assertFalse(m4_commits())


if __name__ == "__main__":
    unittest.main()
