from __future__ import annotations

import unittest

from Learner_App.recall.models import (
    DIRECTION_FORWARD,
    DIRECTION_REVERSE,
    MAX_RECALL_STEP,
    MIN_RECALL_STEP,
    MalformedRecallRecordError,
    RecallConfig,
)
from Learner_App.recall.models import InvalidInverseMappingError
from Learner_App.recall.worker import (
    due_rules,
    get_inverse_rule_id,
    is_due,
    learn_rule,
    overdue_amount,
    ready_for_reverse,
    record_miss,
    record_success,
    require_inverse_rule_id,
    restore,
    schedule_reverse,
    snapshot,
)

CONFIG = RecallConfig(gaps_by_step=(1, 3, 7, 14, 30, 60))
INVERSES = {"EQ.ADD_INVERSE": "EQ.SUB_INVERSE", "EQ.SUB_INVERSE": "EQ.ADD_INVERSE"}


class LearnRuleTests(unittest.TestCase):
    def test_starts_at_first_step_forward(self):
        record = learn_rule("EQ.ADD_INVERSE", cycle=5, config=CONFIG)
        self.assertEqual(record.current_recall_step, MIN_RECALL_STEP)
        self.assertEqual(record.direction, DIRECTION_FORWARD)
        self.assertEqual(record.times_seen, 1)
        self.assertEqual(record.times_correct, 1)
        self.assertEqual(record.next_due_cycle, 5 + CONFIG.gaps_by_step[0])


class ScheduleReverseTests(unittest.TestCase):
    def test_starts_at_first_step_reverse_with_zero_attempts(self):
        record = schedule_reverse("EQ.SUB_INVERSE", cycle=9, config=CONFIG)
        self.assertEqual(record.current_recall_step, MIN_RECALL_STEP)
        self.assertEqual(record.direction, DIRECTION_REVERSE)
        self.assertEqual(record.times_seen, 0)
        self.assertEqual(record.next_due_cycle, 9 + CONFIG.gaps_by_step[0])


class RecordSuccessMissTests(unittest.TestCase):
    def test_success_advances_step_and_pushes_due_date_out(self):
        record = learn_rule("R", cycle=1, config=CONFIG)
        updated = record_success(record, cycle=2, config=CONFIG)
        self.assertEqual(updated.current_recall_step, 2)
        self.assertEqual(updated.next_due_cycle, 2 + CONFIG.gaps_by_step[1])
        self.assertEqual(updated.success_streak, 2)
        self.assertEqual(updated.error_streak, 0)
        self.assertEqual(updated.times_seen, 2)
        self.assertEqual(updated.times_correct, 2)

    def test_miss_retreats_step_and_pulls_due_date_in(self):
        record = learn_rule("R", cycle=1, config=CONFIG)
        record = record_success(record, cycle=2, config=CONFIG)  # step 2
        record = record_success(record, cycle=5, config=CONFIG)  # step 3
        updated = record_miss(record, cycle=12, config=CONFIG)
        self.assertEqual(updated.current_recall_step, 2)
        self.assertEqual(updated.next_due_cycle, 12 + CONFIG.gaps_by_step[1])
        self.assertEqual(updated.error_streak, 1)
        self.assertEqual(updated.success_streak, 0)
        self.assertEqual(updated.times_missed, 1)

    def test_step_never_exceeds_max_bound(self):
        record = learn_rule("R", cycle=0, config=CONFIG)
        cycle = 0
        for _ in range(20):
            cycle += 100
            record = record_success(record, cycle=cycle, config=CONFIG)
        self.assertEqual(record.current_recall_step, MAX_RECALL_STEP)

    def test_step_never_drops_below_min_bound(self):
        record = learn_rule("R", cycle=0, config=CONFIG)
        cycle = 0
        for _ in range(20):
            cycle += 100
            record = record_miss(record, cycle=cycle, config=CONFIG)
        self.assertEqual(record.current_recall_step, MIN_RECALL_STEP)

    def test_updates_never_produce_a_malformed_record(self):
        # record_success/record_miss build via dataclasses.replace(); if
        # they ever produced an inconsistent record, RecallRecord's own
        # __post_init__ would raise here.
        record = learn_rule("R", cycle=0, config=CONFIG)
        for cycle in range(1, 50):
            record = record_success(record, cycle=cycle, config=CONFIG) if cycle % 3 else record_miss(
                record, cycle=cycle, config=CONFIG
            )
        self.assertIsNotNone(record)


class DueQueryTests(unittest.TestCase):
    def test_is_due_and_overdue_amount(self):
        record = learn_rule("R", cycle=0, config=CONFIG)  # next_due = 1
        self.assertFalse(is_due(record, cycle=0))
        self.assertTrue(is_due(record, cycle=1))
        self.assertEqual(overdue_amount(record, cycle=1), 0)
        self.assertEqual(overdue_amount(record, cycle=5), 4)
        self.assertEqual(overdue_amount(record, cycle=0), 0)  # never negative

    def test_due_rules_orders_most_overdue_first(self):
        a = learn_rule("A", cycle=0, config=CONFIG)  # due at 1
        b = learn_rule("B", cycle=0, config=CONFIG)
        b = record_success(b, cycle=1, config=CONFIG)  # due at 1+3=4
        records = {"A": a, "B": b}
        due = due_rules(records, cycle=10)
        self.assertEqual([r.rule_id for r in due], ["A", "B"])  # A more overdue

    def test_due_rules_ties_break_on_error_streak_then_rule_id(self):
        a = learn_rule("A", cycle=0, config=CONFIG)
        a = record_miss(a, cycle=0, config=CONFIG)  # step stays 1, error_streak=1
        b = learn_rule("B", cycle=0, config=CONFIG)  # error_streak=0
        records = {"B": b, "A": a}
        due = due_rules(records, cycle=5)
        self.assertEqual([r.rule_id for r in due], ["A", "B"])  # A has higher error_streak

    def test_due_rules_excludes_not_yet_due(self):
        a = learn_rule("A", cycle=0, config=CONFIG)
        due = due_rules({"A": a}, cycle=0)
        self.assertEqual(due, ())

    def test_due_rules_deterministic_ordering_independent_of_dict_order(self):
        a = learn_rule("A", cycle=0, config=CONFIG)
        b = learn_rule("B", cycle=0, config=CONFIG)
        c = learn_rule("C", cycle=0, config=CONFIG)
        order1 = due_rules({"A": a, "B": b, "C": c}, cycle=5)
        order2 = due_rules({"C": c, "A": a, "B": b}, cycle=5)
        self.assertEqual(order1, order2)


class InverseTests(unittest.TestCase):
    def test_get_inverse_rule_id_returns_mapped_value(self):
        self.assertEqual(get_inverse_rule_id("EQ.ADD_INVERSE", inverses=INVERSES), "EQ.SUB_INVERSE")

    def test_get_inverse_rule_id_returns_none_when_unmapped(self):
        self.assertIsNone(get_inverse_rule_id("EQ.IDENTITY", inverses=INVERSES))

    def test_ready_for_reverse_none_below_max_step(self):
        record = learn_rule("EQ.ADD_INVERSE", cycle=0, config=CONFIG)
        self.assertIsNone(ready_for_reverse(record, inverses=INVERSES))

    def test_ready_for_reverse_at_max_step_with_inverse(self):
        record = learn_rule("EQ.ADD_INVERSE", cycle=0, config=CONFIG)
        cycle = 0
        for _ in range(10):
            cycle += 100
            record = record_success(record, cycle=cycle, config=CONFIG)
        self.assertEqual(record.current_recall_step, MAX_RECALL_STEP)
        self.assertEqual(ready_for_reverse(record, inverses=INVERSES), "EQ.SUB_INVERSE")

    def test_rule_without_inverse_never_gets_fake_reverse_mapping(self):
        record = learn_rule("EQ.IDENTITY", cycle=0, config=CONFIG)
        cycle = 0
        for _ in range(10):
            cycle += 100
            record = record_success(record, cycle=cycle, config=CONFIG)
        self.assertEqual(record.current_recall_step, MAX_RECALL_STEP)
        self.assertIsNone(ready_for_reverse(record, inverses=INVERSES))

    def test_require_inverse_rule_id_returns_mapped_value(self):
        self.assertEqual(
            require_inverse_rule_id("EQ.ADD_INVERSE", inverses=INVERSES), "EQ.SUB_INVERSE"
        )

    def test_require_inverse_rule_id_raises_cleanly_when_impossible(self):
        with self.assertRaises(InvalidInverseMappingError):
            require_inverse_rule_id("EQ.IDENTITY", inverses=INVERSES)

    def test_reverse_direction_record_is_never_itself_reverse_eligible(self):
        record = schedule_reverse("EQ.SUB_INVERSE", cycle=0, config=CONFIG)
        cycle = 0
        for _ in range(10):
            cycle += 100
            record = record_success(record, cycle=cycle, config=CONFIG)
        self.assertEqual(record.direction, DIRECTION_REVERSE)
        self.assertIsNone(ready_for_reverse(record, inverses=INVERSES))


class SnapshotRestoreTests(unittest.TestCase):
    def test_round_trip_preserves_records(self):
        a = learn_rule("A", cycle=0, config=CONFIG)
        b = schedule_reverse("B", cycle=1, config=CONFIG)
        records = {"A": a, "B": b}
        restored = restore(snapshot(records))
        self.assertEqual(records, restored)

    def test_snapshot_is_json_serializable(self):
        import json

        a = learn_rule("A", cycle=0, config=CONFIG)
        json.dumps(snapshot({"A": a}))

    def test_snapshot_order_is_deterministic(self):
        a = learn_rule("A", cycle=0, config=CONFIG)
        b = learn_rule("B", cycle=0, config=CONFIG)
        self.assertEqual(snapshot({"B": b, "A": a}), snapshot({"A": a, "B": b}))

    def test_restore_of_malformed_data_raises_cleanly(self):
        with self.assertRaises(MalformedRecallRecordError):
            restore([{"rule_id": "A", "current_recall_step": 99}])

    def test_restore_of_data_missing_fields_raises_cleanly(self):
        with self.assertRaises(MalformedRecallRecordError):
            restore([{"rule_id": "A"}])

    def test_restored_state_produces_identical_future_due_decisions(self):
        a = learn_rule("A", cycle=0, config=CONFIG)
        b = learn_rule("B", cycle=0, config=CONFIG)
        b = record_success(b, cycle=1, config=CONFIG)
        original = {"A": a, "B": b}
        restored = restore(snapshot(original))
        self.assertEqual(due_rules(original, cycle=20), due_rules(restored, cycle=20))


if __name__ == "__main__":
    unittest.main()
