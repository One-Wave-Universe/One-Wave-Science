"""Tests for the generic data contracts, in particular that a RulePacket
is a fixed instruction once built (see models.py's _freeze_mapping())."""

from __future__ import annotations

import unittest
from types import MappingProxyType

from Learner_App.parser.core import build_problem
from Learner_App.parser.models import RulePacket
from Learner_App.parser.adapters import MathBasicEquationsAdapter
from Learner_App.parser.adapters.math_basic_equations import DOMAIN, EQ_ADD_INVERSE


class RulePacketImmutabilityTests(unittest.TestCase):
    def test_constraints_is_a_read_only_mapping(self):
        packet = RulePacket(
            packet_id="p", seed=1, domain=DOMAIN, target_rules=[EQ_ADD_INVERSE],
            constraints={"variable_names": ["x"]},
        )
        self.assertIsInstance(packet.constraints, MappingProxyType)
        with self.assertRaises(TypeError):
            packet.constraints["variable_names"] = ["y"]

    def test_metadata_is_a_read_only_mapping(self):
        packet = RulePacket(
            packet_id="p", seed=1, domain=DOMAIN, target_rules=[EQ_ADD_INVERSE],
            metadata={"note": "hi"},
        )
        self.assertIsInstance(packet.metadata, MappingProxyType)
        with self.assertRaises(TypeError):
            packet.metadata["note"] = "bye"

    def test_mutating_original_constraints_dict_after_construction_has_no_effect(self):
        original = {"variable_names": ["x"]}
        packet = RulePacket(
            packet_id="p", seed=1, domain=DOMAIN, target_rules=[EQ_ADD_INVERSE],
            constraints=original,
        )
        original["variable_names"] = ["z"]
        original["new_key"] = "surprise"
        self.assertEqual(packet.constraints["variable_names"], ("x",))
        self.assertNotIn("new_key", packet.constraints)

    def test_list_constraint_values_are_frozen_to_tuples(self):
        packet = RulePacket(
            packet_id="p", seed=1, domain=DOMAIN, target_rules=[EQ_ADD_INVERSE],
            constraints={"variable_names": ["x", "y"]},
        )
        self.assertEqual(packet.constraints["variable_names"], ("x", "y"))

    def test_repeated_build_stays_deterministic_despite_external_mutation_attempt(self):
        original = {"variable_names": ["x"]}
        packet = RulePacket(
            packet_id="p", seed=99, domain=DOMAIN, target_rules=[EQ_ADD_INVERSE],
            constraints=original,
        )
        adapter = MathBasicEquationsAdapter()
        first = build_problem(packet, adapter=adapter)
        original["variable_names"] = ["q"]  # attempt to change the packet after the fact
        second = build_problem(packet, adapter=adapter)
        self.assertEqual(first.artifact_text, second.artifact_text)

    def test_nested_dict_constraint_value_is_frozen(self):
        nested = {"mode": "a"}
        packet = RulePacket(
            packet_id="p", seed=1, domain=DOMAIN, target_rules=[EQ_ADD_INVERSE],
            constraints={"domain_options": nested},
        )
        self.assertIsInstance(packet.constraints["domain_options"], MappingProxyType)
        with self.assertRaises(TypeError):
            packet.constraints["domain_options"]["mode"] = "b"

    def test_mutating_nested_dict_in_original_after_construction_has_no_effect(self):
        nested = {"mode": "a"}
        packet = RulePacket(
            packet_id="p", seed=1, domain=DOMAIN, target_rules=[EQ_ADD_INVERSE],
            constraints={"domain_options": nested},
        )
        nested["mode"] = "CHANGED"
        self.assertEqual(packet.constraints["domain_options"]["mode"], "a")

    def test_mutating_dict_nested_inside_list_after_construction_has_no_effect(self):
        item = {"x": 1}
        original_list = [item]
        packet = RulePacket(
            packet_id="p", seed=1, domain=DOMAIN, target_rules=[EQ_ADD_INVERSE],
            constraints={"items": original_list},
        )
        item["x"] = 999
        original_list.append({"x": 2})
        self.assertEqual(len(packet.constraints["items"]), 1)
        self.assertEqual(packet.constraints["items"][0]["x"], 1)
        with self.assertRaises(TypeError):
            packet.constraints["items"][0]["x"] = 42

    def test_nested_set_constraint_value_is_frozen(self):
        packet = RulePacket(
            packet_id="p", seed=1, domain=DOMAIN, target_rules=[EQ_ADD_INVERSE],
            constraints={"tags": {"a", "b"}},
        )
        self.assertIsInstance(packet.constraints["tags"], frozenset)
        self.assertEqual(packet.constraints["tags"], frozenset({"a", "b"}))

    def test_repeated_build_stays_deterministic_despite_nested_mutation_attempt(self):
        nested = {"seed_note": "original"}
        packet = RulePacket(
            packet_id="p", seed=7, domain=DOMAIN, target_rules=[EQ_ADD_INVERSE],
            constraints={"domain_options": nested},
        )
        adapter = MathBasicEquationsAdapter()
        first = build_problem(packet, adapter=adapter)
        nested["seed_note"] = "tampered"
        second = build_problem(packet, adapter=adapter)
        self.assertEqual(first.artifact_text, second.artifact_text)


if __name__ == "__main__":
    unittest.main()
