"""Proves the core/adapter boundary is real: a second, non-equation adapter
round-trips through the exact same build_problem() pipeline used by the
math adapter, with no changes to parser/core.py, parser/adapter.py, or
parser/verifier.py (see test_core.py's CorePurityTests for the source-scan
side of that claim).
"""

from __future__ import annotations

import unittest

from Learner_App.parser.adapter import (
    ProblemAdapter,
    UnknownAdapterError,
    get_adapter,
    register_adapter,
    unregister_adapter,
)
from Learner_App.parser.adapters import MathBasicEquationsAdapter
from Learner_App.parser.core import build_problem
from Learner_App.parser.models import RulePacket
from Learner_App.tests.fixtures.trivial_echo_adapter import (
    DOMAIN as ECHO_DOMAIN,
    ECHO_ABSENT_OK,
    ECHO_PRESENT,
    TrivialEchoAdapter,
)


class ProtocolComplianceTests(unittest.TestCase):
    def test_math_adapter_satisfies_protocol(self):
        self.assertIsInstance(MathBasicEquationsAdapter(), ProblemAdapter)

    def test_trivial_echo_adapter_satisfies_protocol(self):
        self.assertIsInstance(TrivialEchoAdapter(), ProblemAdapter)


class SecondAdapterReusabilityTests(unittest.TestCase):
    """Item 6: a minimal test adapter round-trips a non-equation artifact
    through the same core contract."""

    def setUp(self):
        unregister_adapter(ECHO_DOMAIN)
        register_adapter(ECHO_DOMAIN, TrivialEchoAdapter())

    def tearDown(self):
        unregister_adapter(ECHO_DOMAIN)

    def test_registered_via_registry_and_resolved_by_domain(self):
        packet = RulePacket(
            packet_id="echo-1", seed=1, domain=ECHO_DOMAIN, target_rules=[ECHO_PRESENT]
        )
        result = build_problem(packet)
        self.assertEqual(result.domain, ECHO_DOMAIN)
        self.assertIn(ECHO_PRESENT, result.rules_used)
        self.assertTrue(result.verification.passed)

    def test_explicit_adapter_still_works_without_registry(self):
        packet = RulePacket(
            packet_id="echo-2", seed=5, domain=ECHO_DOMAIN, target_rules=[ECHO_ABSENT_OK]
        )
        result = build_problem(packet, adapter=TrivialEchoAdapter())
        self.assertEqual(result.rules_used, (ECHO_ABSENT_OK,))

    def test_deterministic_like_the_math_adapter(self):
        packet = RulePacket(
            packet_id="echo-3", seed=99, domain=ECHO_DOMAIN, target_rules=[ECHO_PRESENT]
        )
        adapter = TrivialEchoAdapter()
        first = build_problem(packet, adapter=adapter)
        second = build_problem(packet, adapter=adapter)
        self.assertEqual(first.artifact_text, second.artifact_text)

    def test_unregistering_leaves_domain_unknown(self):
        unregister_adapter(ECHO_DOMAIN)
        packet = RulePacket(
            packet_id="echo-4", seed=1, domain=ECHO_DOMAIN, target_rules=[ECHO_PRESENT]
        )
        with self.assertRaises(UnknownAdapterError):
            build_problem(packet)
        # restore for tearDown symmetry
        register_adapter(ECHO_DOMAIN, TrivialEchoAdapter())


if __name__ == "__main__":
    unittest.main()
