import unittest

from layered_loop_map import layer_may_commit, receipt


class LayeredLoopTests(unittest.TestCase):
    def test_only_up_commits(self):
        self.assertFalse(layer_may_commit("low"))
        self.assertFalse(layer_may_commit("mid"))
        self.assertTrue(layer_may_commit("up"))

    def test_six_routes_untouched(self):
        self.assertEqual(receipt()["kernel_routes"], 6)
        self.assertFalse(receipt()["language_required"])


if __name__ == "__main__":
    unittest.main()
