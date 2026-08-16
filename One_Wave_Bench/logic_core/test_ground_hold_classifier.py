import unittest

from ground_hold_classifier import (
    HoldThresholds,
    PresenceSample,
    classify_presence,
)
from mirror_operator import PhaseState
from six_route_logic import BinaryChoice, TernaryMove


class GroundHoldClassifierTests(unittest.TestCase):
    def test_logical_ground_has_no_binary_route(self):
        receipt = classify_presence(PresenceSample(PhaseState(0.0, 0.0), None, 0.0, 0.0, 0.0))
        self.assertTrue(receipt.logical_ground)
        self.assertIsNone(receipt.route)
        self.assertFalse(receipt.coherent_hold)

    def test_yes_hold_and_no_hold_remain_distinct(self):
        base = dict(oscillator=PhaseState(0.2, 0.0), stored_energy=0.2,
                    phase_lock=0.98, topology_retention=0.99)
        yes = classify_presence(PresenceSample(choice=BinaryChoice.YES, **base))
        no = classify_presence(PresenceSample(choice=BinaryChoice.NO, **base))
        self.assertTrue(yes.coherent_hold and no.coherent_hold)
        self.assertNotEqual(yes.route, no.route)
        self.assertEqual(yes.binary_relation, "YES")
        self.assertEqual(no.binary_relation, "NO")

    def test_center_crossing_is_not_hold(self):
        receipt = classify_presence(
            PresenceSample(PhaseState(0.0, 1.0), BinaryChoice.YES, 0.2, 0.98, 0.99)
        )
        self.assertTrue(receipt.at_center)
        self.assertTrue(receipt.center_crossing)
        self.assertIs(receipt.movement, TernaryMove.UP)
        self.assertFalse(receipt.coherent_hold)

    def test_turning_point_hold_can_be_away_from_center(self):
        receipt = classify_presence(
            PresenceSample(PhaseState(1.0, 0.0), BinaryChoice.YES, 0.2, 0.98, 0.99)
        )
        self.assertTrue(receipt.turning_point_hold)
        self.assertFalse(receipt.at_center)
        self.assertTrue(receipt.coherent_hold)

    def test_zero_speed_without_retention_is_not_coherent_hold(self):
        receipt = classify_presence(
            PresenceSample(PhaseState(0.5, 0.0), BinaryChoice.YES, 0.0, 0.98, 0.99)
        )
        self.assertIs(receipt.movement, TernaryMove.HOLD)
        self.assertFalse(receipt.energy_retained)
        self.assertFalse(receipt.coherent_hold)

    def test_phase_unlocked_zero_speed_is_not_coherent_hold(self):
        receipt = classify_presence(
            PresenceSample(PhaseState(0.5, 0.0), BinaryChoice.YES, 0.2, 0.2, 0.99)
        )
        self.assertFalse(receipt.phase_locked)
        self.assertFalse(receipt.coherent_hold)

    def test_topology_loss_breaks_coherent_hold(self):
        receipt = classify_presence(
            PresenceSample(PhaseState(0.5, 0.0), BinaryChoice.YES, 0.2, 0.98, 0.2)
        )
        self.assertFalse(receipt.topology_retained)
        self.assertFalse(receipt.coherent_hold)

    def test_uncommitted_activity_is_not_logical_ground(self):
        receipt = classify_presence(
            PresenceSample(PhaseState(0.1, 0.0), None, 0.1, 0.0, 0.0)
        )
        self.assertFalse(receipt.logical_ground)
        self.assertIsNone(receipt.route)

    def test_invalid_thresholds_are_rejected(self):
        with self.assertRaises(ValueError):
            HoldThresholds(phase_lock_min=1.1)


if __name__ == "__main__":
    unittest.main()

