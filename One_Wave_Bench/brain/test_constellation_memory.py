import unittest

from One_Wave_Bench.brain.constellation_memory import (
    ConstellationMemory,
    MemoryNode,
    ValidationDecision,
    demo_constellation,
)
from One_Wave_Bench.brain.rabbit_hop_alphabet import MirrorPolarity


class ConstellationMemoryTests(unittest.TestCase):
    def test_rabbit_hop_rebuild_beats_matched_flat_baseline(self):
        memory = demo_constellation()

        # "flower" alone ties the two overlapping memories in a flat lookup.
        self.assertIsNone(memory.baseline_recall({"flower"}))

        rebuilt = memory.rebuild(
            {"flower"}, route_handle="A", context="garden"
        )
        self.assertEqual(rebuilt.memory.memory_id, "sniff_flower")
        self.assertEqual(rebuilt.receipt.baseline_memory, None)
        self.assertEqual(rebuilt.receipt.validation, ValidationDecision.ACCEPT)
        self.assertEqual(rebuilt.receipt.associative_completion,
                         ("garden", "scent", "sniff"))

    def test_route_records_a_real_2n_plus_or_minus_1_connector(self):
        receipt = demo_constellation().rebuild(
            {"flower"}, route_handle="A", context="garden"
        ).receipt
        self.assertEqual(len(receipt.route), 1)
        step = receipt.route[0]
        self.assertEqual(step.connector, 3)
        self.assertEqual(step.source.tuple, (1, 2, 3))
        self.assertEqual(step.target.tuple, (2, 4, 3))

    def test_route_is_exactly_invertible_from_its_receipt(self):
        receipt = demo_constellation().rebuild(
            {"flower"}, route_handle="A", context="garden"
        ).receipt
        inverse = receipt.inverted_route()
        self.assertEqual(inverse[0].source, receipt.route[0].target)
        self.assertEqual(inverse[0].target, receipt.route[0].source)
        self.assertEqual(inverse[0].connector, receipt.route[0].connector)

    def test_mirror_polarity_is_preserved_in_route_receipt(self):
        receipt = demo_constellation().rebuild(
            {"flower"},
            route_handle="A",
            context="garden",
            polarity=MirrorPolarity.NEGATIVE,
        ).receipt
        self.assertEqual(receipt.route[0].source.tuple, (-1, -2, -3))
        self.assertEqual(receipt.route[0].target.tuple, (-2, -4, -3))
        self.assertEqual(receipt.inverted_route()[0].connector, -3)

    def test_boltzmann_fill_is_seeded_bounded_and_marked_uncertain(self):
        memory = ConstellationMemory((
            MemoryNode("left", "A", frozenset({"shared", "left"})),
            MemoryNode("handle", "B", frozenset({"handle"})),
            MemoryNode("right", "C", frozenset({"shared", "right"})),
        ))
        first = memory.rebuild({"shared"}, route_handle="B", seed=7)
        second = memory.rebuild({"shared"}, route_handle="B", seed=7)
        self.assertEqual(first, second)
        self.assertTrue(first.receipt.boltzmann_probabilities)
        self.assertTrue(first.receipt.probabilistic_fill)
        self.assertEqual(
            first.receipt.uncertain_features,
            first.receipt.probabilistic_fill,
        )
        self.assertAlmostEqual(
            sum(probability for _, probability in first.receipt.boltzmann_probabilities),
            1.0,
        )

    def test_similar_memories_remain_separate(self):
        memory = demo_constellation()
        rebuilt = memory.rebuild(
            {"flower"}, route_handle="A", context="garden"
        )
        self.assertEqual(rebuilt.memory.features,
                         frozenset({"flower", "garden", "sniff", "scent"}))
        self.assertNotIn("approach", rebuilt.memory.features)

    def test_context_validation_can_hold_or_reject_without_rewriting_memory(self):
        memory = demo_constellation()
        before = memory.nodes
        held = memory.rebuild({"flower"}, route_handle="A")
        rejected = memory.rebuild(
            {"flower"}, route_handle="A", context="street"
        )
        self.assertEqual(held.receipt.validation, ValidationDecision.HOLD)
        self.assertEqual(rejected.receipt.validation, ValidationDecision.REJECT)
        self.assertEqual(memory.nodes, before)


if __name__ == "__main__":
    unittest.main()
