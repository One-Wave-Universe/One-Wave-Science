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

    def test_micro_is_complete_cell_field_void_loop(self):
        micro = self.sim.run("go forward")[0]
        self.assertEqual(micro.scale, Scale.MICRO)
        self.assertEqual(micro.binary_choice, "YES")
        self.assertEqual(micro.field_move, "EXPRESS")
        self.assertEqual(micro.void_check, "CONFIRM")
        self.assertEqual(micro.output, "EXPRESS")
        self.assertEqual(micro.reference_before, "CENTER")
        self.assertEqual(micro.reference_after, "YES:EXPRESS")
        self.assertTrue(micro.compressed_summary)

    def test_micro_unknown_defers_and_preserves_reference(self):
        micro = self.sim.run("unknown signal")[0]
        self.assertEqual(micro.void_check, "DEFER")
        self.assertEqual(micro.output, "HOLD")
        self.assertEqual(micro.reference_after, micro.reference_before)

    def test_micro_stop_is_void_deny_and_preserves_reference(self):
        micro = self.sim.run("stop")[0]
        self.assertEqual(micro.binary_choice, "NO")
        self.assertEqual(micro.void_check, "DENY")
        self.assertEqual(micro.output, "STOP")
        self.assertEqual(micro.reference_after, micro.reference_before)

    def test_small_consumes_micro_compressed_receipt(self):
        receipts = self.sim.run("go forward")
        self.assertEqual(receipts[1].cue, receipts[0].compressed_summary)

    def test_higher_scales_preserve_field_m4_void_chain(self):
        for receipt in self.sim.run("go forward")[1:]:
            self.assertTrue(receipt.field_proposal)
            self.assertTrue(receipt.m4_route)
            self.assertTrue(receipt.void_resolution)
            self.assertTrue(receipt.compressed_summary)

    def test_deny_propagates_upward_as_override(self):
        receipts = self.sim.run("stop")
        for receipt in receipts[1:]:
            self.assertEqual(receipt.void_resolution, "DENY")
            self.assertEqual(receipt.action, "OVERRIDE_STOP")
            self.assertTrue(receipt.committed)

    def test_each_higher_scale_consumes_prior_compressed_receipt(self):
        receipts = self.sim.run("go forward")
        self.assertEqual(receipts[2].cue, receipts[1].compressed_summary)
        self.assertEqual(receipts[3].cue, receipts[2].compressed_summary)
        self.assertEqual(receipts[4].cue, receipts[3].compressed_summary)


if __name__ == "__main__":
    unittest.main()
