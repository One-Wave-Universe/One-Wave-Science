import math
import unittest

from commitment_map import (
    CommitmentParameters,
    CommitmentState,
    phase_lock,
    run_history,
    update_commitment,
)
from six_route_logic import BinaryChoice, LogicRoute, TernaryMove


YES_UP = LogicRoute(BinaryChoice.YES, TernaryMove.UP)
NO_UP = LogicRoute(BinaryChoice.NO, TernaryMove.UP)
YES_HOLD = LogicRoute(BinaryChoice.YES, TernaryMove.HOLD)


class CommitmentMapTests(unittest.TestCase):
    def test_phase_alignment_is_bounded(self):
        self.assertAlmostEqual(phase_lock(0.0), 1.0)
        self.assertAlmostEqual(phase_lock(math.pi), 0.0)

    def test_one_pulse_cannot_create_full_commitment(self):
        receipt = update_commitment(CommitmentState(), YES_UP, 1.0, 0.0)
        self.assertEqual(receipt.after.level, 0)
        self.assertLess(receipt.after.latent, CommitmentParameters().full_enter)

    def test_repeated_aligned_yes_builds_partial_then_full(self):
        receipts = run_history(CommitmentState(), [(YES_UP, 1.0, 0.0)] * 8)
        levels = [receipt.after.level for receipt in receipts]
        self.assertIn(2, levels)
        self.assertEqual(levels[-1], 3)

    def test_repeated_aligned_no_builds_negative_commitment(self):
        receipts = run_history(CommitmentState(), [(NO_UP, 1.0, 0.0)] * 8)
        self.assertEqual(receipts[-1].after.level, -3)

    def test_opposite_phase_blocks_new_drive(self):
        receipt = update_commitment(CommitmentState(), YES_UP, 1.0, math.pi)
        self.assertAlmostEqual(receipt.signed_drive, 0.0)
        self.assertAlmostEqual(receipt.after.latent, 0.0)

    def test_hold_retains_history_but_adds_no_drive(self):
        state = CommitmentState(latent=0.5, level=2)
        receipt = update_commitment(state, YES_HOLD, 1.0, 0.0)
        self.assertEqual(receipt.signed_drive, 0.0)
        self.assertAlmostEqual(receipt.after.latent, 0.46)
        self.assertEqual(receipt.after.level, 2)

    def test_partial_hysteresis_prevents_threshold_chatter(self):
        p = CommitmentParameters()
        retained = update_commitment(
            CommitmentState(latent=0.39, level=2), YES_HOLD, 0.0, 0.0, p
        )
        self.assertEqual(retained.after.level, 2)
        fresh = update_commitment(
            CommitmentState(latent=0.39, level=0), YES_HOLD, 0.0, 0.0, p
        )
        self.assertEqual(fresh.after.level, 0)

    def test_history_matters_at_same_latent_value(self):
        p = CommitmentParameters(retention=1.0)
        retained = update_commitment(
            CommitmentState(latent=0.35, level=2), YES_HOLD, 0.0, 0.0, p
        )
        uncommitted = update_commitment(
            CommitmentState(latent=0.35, level=0), YES_HOLD, 0.0, 0.0, p
        )
        self.assertEqual(retained.after.latent, uncommitted.after.latent)
        self.assertNotEqual(retained.after.level, uncommitted.after.level)

    def test_invalid_threshold_order_is_rejected(self):
        with self.assertRaises(ValueError):
            CommitmentParameters(partial_exit=0.5, partial_enter=0.4)


if __name__ == "__main__":
    unittest.main()

