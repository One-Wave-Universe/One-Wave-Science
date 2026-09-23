#!/usr/bin/env python3

import unittest
from unittest import mock

import android_reference_parser as arp


BASE = {
    "cwd": "/home/test/One-Wave-Science",
    "repo_root": "/home/test/One-Wave-Science",
    "branch": "test-branch",
    "head": "abc123",
    "status": "## test-branch",
    "git_repo": True,
}


class AndroidReferenceParserTests(unittest.TestCase):
    def setUp(self):
        arp.clear_reference_tokens()

    def test_reference_issues_one_shot_token(self):
        with mock.patch.object(arp, "_snapshot", return_value=dict(BASE)):
            issued = arp.reference(BASE["cwd"])
        self.assertTrue(issued["ok"])
        self.assertTrue(issued["one_shot"])
        self.assertEqual(issued["cycle"]["void_test"]["decision"], "ALLOW")
        self.assertTrue(issued["reference_token"])

    def test_android_action_requires_reference(self):
        result = arp.run("", ["printf", "NO"])
        self.assertFalse(result["ok"])
        self.assertEqual(result["decision"], "HOLD")
        self.assertEqual(result["code"], "REFERENCE_REQUIRED")

    def test_reference_is_consumed_after_one_action(self):
        with mock.patch.object(arp, "_snapshot", return_value=dict(BASE)):
            issued = arp.reference(BASE["cwd"])
            with mock.patch.object(arp.terminal_parser, "run", return_value={"ok": True, "stdout": "OK"}):
                first = arp.run(issued["reference_token"], ["printf", "OK"], cwd=BASE["cwd"])
                second = arp.run(issued["reference_token"], ["printf", "AGAIN"], cwd=BASE["cwd"])

        self.assertTrue(first["ok"])
        self.assertEqual(first["decision"], "CONFIRM")
        self.assertFalse(second["ok"])
        self.assertEqual(second["decision"], "HOLD")
        self.assertEqual(second["code"], "REFERENCE_UNKNOWN_OR_REUSED")

    def test_pre_action_drift_holds_without_execution(self):
        issued_snapshot = dict(BASE)
        drifted = dict(BASE, head="different-head")
        with mock.patch.object(arp, "_snapshot", side_effect=[issued_snapshot, drifted]):
            issued = arp.reference(BASE["cwd"])
            with mock.patch.object(arp.terminal_parser, "run") as run:
                result = arp.run(issued["reference_token"], ["printf", "NO"], cwd=BASE["cwd"])

        run.assert_not_called()
        self.assertFalse(result["ok"])
        self.assertEqual(result["decision"], "HOLD")
        self.assertEqual(result["code"], "REFERENCE_DRIFT")

    def test_cycle_is_field_reference_void_test_field_act_void_confirm(self):
        with mock.patch.object(arp, "_snapshot", return_value=dict(BASE)):
            issued = arp.reference(BASE["cwd"])
            with mock.patch.object(arp.terminal_parser, "run", return_value={"ok": True, "stdout": "OK"}):
                result = arp.run(issued["reference_token"], ["printf", "OK"], cwd=BASE["cwd"])

        self.assertEqual(
            list(result["cycle"]),
            ["field_reference", "void_test", "field_act", "void_confirm"],
        )
        self.assertEqual(result["cycle"]["void_confirm"]["decision"], "CONFIRM")
        self.assertTrue(result["cycle"]["void_confirm"]["next_action_requires_new_reference"])


if __name__ == "__main__":
    unittest.main()
