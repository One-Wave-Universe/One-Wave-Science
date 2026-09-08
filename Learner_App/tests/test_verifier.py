from __future__ import annotations

import unittest

from Learner_App.parser.models import RulePacket
from Learner_App.parser.verifier import (
    build_verification,
    check_forbidden_rules_absent,
    check_requested_rules_present,
)


def _packet(**kwargs) -> RulePacket:
    defaults = dict(packet_id="v", seed=1, domain="test/x", target_rules=["A"])
    defaults.update(kwargs)
    return RulePacket(**defaults)


class VerifierTests(unittest.TestCase):
    def test_requested_rules_present_true_when_all_present(self):
        packet = _packet(target_rules=["A", "B"])
        self.assertTrue(check_requested_rules_present(["A", "B", "C"], packet))

    def test_requested_rules_present_false_when_missing(self):
        packet = _packet(target_rules=["A", "B"])
        self.assertFalse(check_requested_rules_present(["A"], packet))

    def test_forbidden_rules_absent_true_when_none_present(self):
        packet = _packet(forbidden_rules=["Z"])
        self.assertTrue(check_forbidden_rules_absent(["A"], packet))

    def test_forbidden_rules_absent_false_when_present(self):
        packet = _packet(forbidden_rules=["Z"])
        self.assertFalse(check_forbidden_rules_absent(["A", "Z"], packet))

    def test_build_verification_passes_on_clean_input(self):
        packet = _packet(target_rules=["A"], forbidden_rules=["Z"])
        result = build_verification(
            rules_used=["A"], packet=packet, well_formed=True, adapter_valid=True, errors=[]
        )
        self.assertTrue(result.passed)
        self.assertEqual(result.errors, ())

    def test_build_verification_fails_and_reports_missing_rule(self):
        packet = _packet(target_rules=["A"])
        result = build_verification(
            rules_used=[], packet=packet, well_formed=True, adapter_valid=True, errors=[]
        )
        self.assertFalse(result.passed)
        self.assertTrue(any("A" in e for e in result.errors))

    def test_build_verification_fails_when_not_well_formed_even_if_rules_match(self):
        packet = _packet(target_rules=["A"])
        result = build_verification(
            rules_used=["A"],
            packet=packet,
            well_formed=False,
            adapter_valid=False,
            errors=["reparse failed"],
        )
        self.assertFalse(result.passed)


if __name__ == "__main__":
    unittest.main()
