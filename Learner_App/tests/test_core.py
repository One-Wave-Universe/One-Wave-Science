"""Reusability acceptance tests for the generic core (issue #40, items 1-10).

Run with:
    python3 -m unittest discover -s Learner_App/tests -t . -p "test_*.py" -v
(from the repository root).
"""

from __future__ import annotations

import dataclasses
import inspect
import unittest
from pathlib import Path

from Learner_App.parser import adapter as adapter_module
from Learner_App.parser import core as core_module
from Learner_App.parser import verifier as verifier_module
from Learner_App.parser.core import (
    PacketRejectedError,
    ProblemVerificationError,
    build_problem,
)
from Learner_App.parser.adapter import (
    UnknownAdapterError,
    get_adapter,
    register_adapter,
    unregister_adapter,
)
from Learner_App.parser.adapters import MathBasicEquationsAdapter
from Learner_App.parser.adapters.math_basic_equations import DOMAIN as MATH_DOMAIN
from Learner_App.parser.adapters.math_basic_equations import (
    EQ_ADD_INVERSE,
    EQ_MUL_INVERSE,
)
from Learner_App.parser.models import RulePacket
from Learner_App.tests.fixtures.trivial_echo_adapter import (
    DOMAIN as ECHO_DOMAIN,
    TrivialEchoAdapter,
)

CORE_SOURCE_FILES = [
    Path(inspect.getfile(core_module)),
    Path(inspect.getfile(adapter_module)),
    Path(inspect.getfile(verifier_module)),
]


class CorePurityTests(unittest.TestCase):
    """Items 1-3: the core has no algebra baked into it."""

    def test_core_has_no_hardcoded_eq_rule_ids(self):
        for path in CORE_SOURCE_FILES:
            text = path.read_text()
            self.assertNotIn("EQ.", text, f"{path} references an algebra rule id")

    def test_core_has_no_algebra_specific_ast_assumptions(self):
        forbidden_terms = [
            "coefficient",
            "variable_name",
            "equation",
            "divisor",
            "lhs",
            "rhs",
        ]
        for path in CORE_SOURCE_FILES:
            text = path.read_text().lower()
            for term in forbidden_terms:
                self.assertNotIn(
                    term, text, f"{path} contains algebra-specific term {term!r}"
                )

    def test_math_only_constraints_isolated_to_math_adapter(self):
        math_adapter_path = Path(
            inspect.getfile(MathBasicEquationsAdapter)
        )
        for path in CORE_SOURCE_FILES:
            if path == math_adapter_path:
                continue
            text = path.read_text()
            self.assertNotIn("coefficient_range", text)
            self.assertNotIn("variable_names", text)


class RegistryTests(unittest.TestCase):
    """Items 4-5: adapters register without touching core, and unknown
    adapters fail loudly."""

    def setUp(self):
        unregister_adapter(MATH_DOMAIN)

    def tearDown(self):
        unregister_adapter(MATH_DOMAIN)

    def test_adapter_registers_without_editing_core(self):
        register_adapter(MATH_DOMAIN, MathBasicEquationsAdapter())
        self.assertIs(type(get_adapter(MATH_DOMAIN)), MathBasicEquationsAdapter)

    def test_unregistered_domain_fails_loudly(self):
        packet = RulePacket(
            packet_id="p1", seed=1, domain="nonexistent/domain", target_rules=["ANYTHING"]
        )
        with self.assertRaises(UnknownAdapterError):
            build_problem(packet)


class AdapterDomainMatchTests(unittest.TestCase):
    """The explicit `adapter=` override must not be usable to build a
    packet under an adapter for a different domain -- domain selection is
    the router's call, encoded in packet.domain."""

    def test_mismatched_explicit_adapter_is_rejected(self):
        packet = RulePacket(
            packet_id="p6", seed=1, domain=MATH_DOMAIN, target_rules=[EQ_ADD_INVERSE]
        )
        with self.assertRaises(PacketRejectedError):
            build_problem(packet, adapter=TrivialEchoAdapter())

    def test_matching_explicit_adapter_is_accepted(self):
        packet = RulePacket(
            packet_id="p7", seed=1, domain=ECHO_DOMAIN, target_rules=["ECHO.PRESENT"]
        )
        result = build_problem(packet, adapter=TrivialEchoAdapter())
        self.assertEqual(result.domain, ECHO_DOMAIN)


class DeterminismTests(unittest.TestCase):
    """Item 7: same packet + seed is byte-for-byte deterministic."""

    def test_same_packet_and_seed_is_deterministic(self):
        packet = RulePacket(
            packet_id="det-1",
            seed=42,
            domain=MATH_DOMAIN,
            target_rules=[EQ_ADD_INVERSE, EQ_MUL_INVERSE],
        )
        adapter = MathBasicEquationsAdapter()
        first = build_problem(packet, adapter=adapter)
        second = build_problem(packet, adapter=adapter)
        self.assertEqual(first.artifact_text, second.artifact_text)
        self.assertEqual(first.structure, second.structure)
        self.assertEqual(first.rules_used, second.rules_used)

    def test_different_seed_can_vary_text(self):
        adapter = MathBasicEquationsAdapter()
        packet_a = RulePacket(
            packet_id="det-2", seed=1, domain=MATH_DOMAIN, target_rules=[EQ_ADD_INVERSE]
        )
        packet_b = dataclasses.replace(packet_a, seed=2)
        result_a = build_problem(packet_a, adapter=adapter)
        result_b = build_problem(packet_b, adapter=adapter)
        # Not guaranteed to differ for every possible seed pair, but true
        # for this pair with the current RNG usage -- documents the intent.
        self.assertNotEqual(result_a.artifact_text, result_b.artifact_text)


class ContradictionRejectionTests(unittest.TestCase):
    """Item 8: contradictory packets are rejected before generation."""

    def test_same_rule_in_target_and_forbidden_is_rejected_generically(self):
        packet = RulePacket(
            packet_id="p2",
            seed=1,
            domain=MATH_DOMAIN,
            target_rules=[EQ_ADD_INVERSE],
            forbidden_rules=[EQ_ADD_INVERSE],
        )
        with self.assertRaises(PacketRejectedError):
            build_problem(packet, adapter=MathBasicEquationsAdapter())

    def test_rejection_happens_before_generation(self):
        calls = []

        class SpyAdapter(MathBasicEquationsAdapter):
            def generate_candidate(self, packet, rng):
                calls.append(1)
                return super().generate_candidate(packet, rng)

        packet = RulePacket(
            packet_id="p3",
            seed=1,
            domain=MATH_DOMAIN,
            target_rules=[EQ_ADD_INVERSE],
            forbidden_rules=[EQ_ADD_INVERSE],
        )
        with self.assertRaises(PacketRejectedError):
            build_problem(packet, adapter=SpyAdapter())
        self.assertEqual(calls, [])


class IndependentReparseTests(unittest.TestCase):
    """Item 9: the returned structure comes from an independent reparse of
    the external artifact text, not the generator's internal object."""

    def test_returned_structure_matches_fresh_reparse_of_artifact_text(self):
        adapter = MathBasicEquationsAdapter()
        packet = RulePacket(
            packet_id="p4", seed=7, domain=MATH_DOMAIN, target_rules=[EQ_ADD_INVERSE]
        )
        result = build_problem(packet, adapter=adapter)
        fresh_structure = adapter.parse_artifact(result.artifact_text)
        self.assertEqual(result.structure, fresh_structure)
        self.assertTrue(result.verification.passed)


class NoAnswerFieldTests(unittest.TestCase):
    """Item 10: nothing in the generic public output carries an answer."""

    def test_generated_problem_has_no_answer_field(self):
        forbidden_field_names = {"answer", "solution", "value", "result"}
        field_names = {f.name for f in dataclasses.fields(core_module.GeneratedProblem)}
        self.assertFalse(field_names & forbidden_field_names)

    def test_generated_problem_metadata_carries_no_answer_key(self):
        adapter = MathBasicEquationsAdapter()
        packet = RulePacket(
            packet_id="p5",
            seed=3,
            domain=MATH_DOMAIN,
            target_rules=[EQ_ADD_INVERSE, EQ_MUL_INVERSE],
        )
        result = build_problem(packet, adapter=adapter)
        forbidden_keys = {"answer", "solution", "solved_value", "x_value"}
        self.assertFalse(set(result.metadata) & forbidden_keys)


if __name__ == "__main__":
    unittest.main()
