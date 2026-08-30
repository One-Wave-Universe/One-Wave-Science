import unittest

from One_Wave_Bench.simulators.field_void_recursive_sim import (
    RecursiveFieldVoidSimulator,
    Scale,
)


class RecursiveFieldVoidSimulatorTests(unittest.TestCase):
    def setUp(self):
        self.sim = RecursiveFieldVoidSimulator()

    def test_runs_exact_five_scale_ladder(self):
        receipts = self.sim.run("go forward")
        self.assertEqual(
            [r.scale for r in receipts],
            [Scale.MICRO, Scale.SMALL, Scale.MEDIUM, Scale.LARGE, Scale.MACRO],
        )

    def test_each_scale_keeps_field_void_and_m4_receipt(self):
        for receipt in self.sim.run("go forward"):
            self.assertTrue(receipt.field_proposal)
            self.assertTrue(receipt.m4_route)
            self.assertTrue(receipt.void_resolution)
            self.assertTrue(receipt.compressed_summary)

    def test_stop_is_void_admin_checker_override(self):
        receipts = self.sim.run("stop")
        for receipt in receipts:
            self.assertEqual(receipt.void_resolution, "DENY")
            self.assertEqual(receipt.action, "OVERRIDE_STOP")
            self.assertTrue(receipt.committed)

    def test_uncertain_input_defers_at_micro(self):
        receipt = self.sim.run("unknown signal")[0]
        self.assertEqual(receipt.void_resolution, "DEFER")
        self.assertEqual(receipt.action, "HOLD")
        self.assertFalse(receipt.committed)

    def test_next_scale_consumes_compressed_lower_receipt(self):
        receipts = self.sim.run("go forward")
        self.assertEqual(receipts[1].cue, receipts[0].compressed_summary)
        self.assertEqual(receipts[2].cue, receipts[1].compressed_summary)
        self.assertEqual(receipts[3].cue, receipts[2].compressed_summary)
        self.assertEqual(receipts[4].cue, receipts[3].compressed_summary)


if __name__ == "__main__":
    unittest.main()
