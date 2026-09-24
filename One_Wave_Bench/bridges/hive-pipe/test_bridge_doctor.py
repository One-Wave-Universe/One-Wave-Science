#!/usr/bin/env python3
import unittest
from unittest import mock

import bridge_doctor


class BridgeDoctorTests(unittest.TestCase):
    def test_exit_codes_distinguish_failure_from_unverified(self):
        self.assertEqual(bridge_doctor.overall_exit([
            bridge_doctor.Check("x", bridge_doctor.PASS, "ok")
        ]), 0)
        self.assertEqual(bridge_doctor.overall_exit([
            bridge_doctor.Check("x", bridge_doctor.NOT_VERIFIED, "external")
        ]), 2)
        self.assertEqual(bridge_doctor.overall_exit([
            bridge_doctor.Check("x", bridge_doctor.FAIL, "broken")
        ]), 1)

    def test_ci_static_contracts_pass_in_repository(self):
        checks = bridge_doctor.static_checks()
        failures = [check for check in checks if check.status == bridge_doctor.FAIL]
        self.assertEqual(failures, [], failures)

    def test_inactive_required_service_is_failure(self):
        completed = mock.Mock(returncode=3, stdout="inactive\n", stderr="")
        with mock.patch.object(bridge_doctor, "run", return_value=completed):
            check = bridge_doctor.service_check("example.service", required=True)
        self.assertEqual(check.status, bridge_doctor.FAIL)
        self.assertIn("restart", check.action.lower())

    def test_inactive_optional_service_is_not_configured(self):
        completed = mock.Mock(returncode=4, stdout="unknown\n", stderr="")
        with mock.patch.object(bridge_doctor, "run", return_value=completed):
            check = bridge_doctor.service_check("optional.service", required=False)
        self.assertEqual(check.status, bridge_doctor.NOT_CONFIGURED)

    def test_pull_installer_prepares_both_routes_and_external_work_root(self):
        installer = (bridge_doctor.REPO_ROOT / "One_Wave_Bench/bridges/hive-pipe/install_chatgpt_terminal_pull.sh").read_text()
        self.assertIn("chatgpt-terminal-backup", installer)
        self.assertIn("EXTERNAL_WORK_ROOT", installer)
        self.assertIn("bridge_doctor.py\" --profile pull", installer)


if __name__ == "__main__":
    unittest.main()
