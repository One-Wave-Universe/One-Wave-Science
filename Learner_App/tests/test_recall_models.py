from __future__ import annotations

import unittest

from Learner_App.recall.models import (
    DIRECTION_FORWARD,
    DIRECTION_REVERSE,
    MAX_RECALL_STEP,
    MIN_RECALL_STEP,
    MalformedRecallRecordError,
    RecallConfig,
    RecallRecord,
)


def _valid_record(**overrides) -> dict:
    defaults = dict(
        rule_id="EQ.ADD_INVERSE",
        times_seen=1,
        times_correct=1,
        times_missed=0,
        last_seen_cycle=1,
        current_recall_step=1,
        next_due_cycle=2,
        success_streak=1,
        error_streak=0,
        direction=DIRECTION_FORWARD,
        weight=0.0,
    )
    defaults.update(overrides)
    return defaults


class RecallRecordValidationTests(unittest.TestCase):
    def test_valid_record_constructs(self):
        RecallRecord(**_valid_record())

    def test_empty_rule_id_rejected(self):
        with self.assertRaises(MalformedRecallRecordError):
            RecallRecord(**_valid_record(rule_id=""))

    def test_step_below_min_rejected(self):
        with self.assertRaises(MalformedRecallRecordError):
            RecallRecord(**_valid_record(current_recall_step=MIN_RECALL_STEP - 1))

    def test_step_above_max_rejected(self):
        with self.assertRaises(MalformedRecallRecordError):
            RecallRecord(**_valid_record(current_recall_step=MAX_RECALL_STEP + 1))

    def test_step_at_bounds_accepted(self):
        RecallRecord(**_valid_record(current_recall_step=MIN_RECALL_STEP))
        RecallRecord(**_valid_record(current_recall_step=MAX_RECALL_STEP))

    def test_invalid_direction_rejected(self):
        with self.assertRaises(MalformedRecallRecordError):
            RecallRecord(**_valid_record(direction="sideways"))

    def test_negative_counts_rejected(self):
        for field in ("times_seen", "times_correct", "times_missed", "success_streak", "error_streak"):
            with self.assertRaises(MalformedRecallRecordError):
                RecallRecord(**_valid_record(**{field: -1}))

    def test_correct_plus_missed_exceeding_seen_rejected(self):
        with self.assertRaises(MalformedRecallRecordError):
            RecallRecord(**_valid_record(times_seen=1, times_correct=1, times_missed=1))

    def test_negative_cycle_values_rejected(self):
        with self.assertRaises(MalformedRecallRecordError):
            RecallRecord(**_valid_record(last_seen_cycle=-1))
        with self.assertRaises(MalformedRecallRecordError):
            RecallRecord(**_valid_record(next_due_cycle=-1))

    def test_reverse_direction_accepted(self):
        RecallRecord(**_valid_record(direction=DIRECTION_REVERSE))


class RecallConfigValidationTests(unittest.TestCase):
    def test_default_config_is_valid(self):
        RecallConfig()

    def test_wrong_number_of_gaps_rejected(self):
        with self.assertRaises(ValueError):
            RecallConfig(gaps_by_step=(1, 2, 3))

    def test_non_positive_gap_rejected(self):
        with self.assertRaises(ValueError):
            RecallConfig(gaps_by_step=(1, 1, 1, 1, 1, 0))
        with self.assertRaises(ValueError):
            RecallConfig(gaps_by_step=(1, 1, 1, 1, 1, -3))

    def test_non_positive_step_amounts_rejected(self):
        with self.assertRaises(ValueError):
            RecallConfig(step_advance_on_success=0)
        with self.assertRaises(ValueError):
            RecallConfig(step_retreat_on_miss=0)


if __name__ == "__main__":
    unittest.main()
