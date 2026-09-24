#!/usr/bin/env python3

import shutil
import tempfile
from pathlib import Path
import unittest
from unittest import mock

import terminal_parser


class TerminalParserTests(unittest.TestCase):
    def test_pwd_defaults_to_repo(self):
        result = terminal_parser.pwd()
        self.assertTrue(result["ok"])
        self.assertEqual(result["cwd"], str(terminal_parser.REPO_ROOT))

    def test_explicit_external_root_is_allowed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            with mock.patch.object(terminal_parser, "ALLOWED_ROOTS", (terminal_parser.HOME, root)):
                result = terminal_parser.pwd(str(root))
        self.assertTrue(result["ok"])
        self.assertEqual(result["cwd"], str(root))

    def test_directory_outside_authorized_roots_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            with mock.patch.object(terminal_parser, "ALLOWED_ROOTS", (terminal_parser.HOME,)):
                with self.assertRaisesRegex(ValueError, "authorized Jetson work root"):
                    terminal_parser.pwd(str(root))

    def test_which_finds_python(self):
        result = terminal_parser.which("python3")
        self.assertTrue(result["ok"])
        self.assertTrue(result["path"])

    def test_run_returns_stdout_and_exit_code(self):
        result = terminal_parser.run(["printf", "TERMINAL_PARSER_OK"])
        self.assertTrue(result["ok"])
        self.assertEqual(result["stdout"], "TERMINAL_PARSER_OK")
        self.assertEqual(result["stderr"], "")
        self.assertEqual(result["exit_code"], 0)
        self.assertIn("duration_ms", result)

    def test_run_receipt_contains_actual_reference_on_both_sides(self):
        result = terminal_parser.run(["printf", "REFERENCE_OK"])
        self.assertTrue(result["ok"])
        self.assertEqual(result["reference_before"]["head"], result["reference_after"]["head"])
        self.assertEqual(result["reference_before"]["root"], str(terminal_parser.REPO_ROOT))
        self.assertFalse(result["reference_changed"])
        self.assertEqual(result["reference_card"]["goblin"], "reference")
        self.assertEqual(result["response_card"]["goblin"], "checker")
        self.assertEqual(result["reference_card"]["action_sha256"], result["response_card"]["action_sha256"])
        self.assertIn("+00:00", result["response_card"]["stamped_at"])

    def test_missing_project_reference_blocks_command_before_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            with mock.patch.dict(terminal_parser.os.environ, {"ONE_WAVE_PROJECT_ROOT": directory}):
                with self.assertRaisesRegex(ValueError, "AGENTS.md missing"):
                    terminal_parser.run(["printf", "MUST_NOT_RUN"])

    def test_nonzero_exit_is_reported(self):
        result = terminal_parser.run(["false"])
        self.assertFalse(result["ok"])
        self.assertNotEqual(result["exit_code"], 0)

    def test_blocks_direct_privilege_and_raw_disk_commands(self):
        for argv in (["sudo", "id"], ["mkfs.ext4", "/dev/sdz"], ["reboot"]):
            with self.assertRaises(ValueError):
                terminal_parser.run(argv)

    def test_python_run_executes_temporary_source(self):
        result = terminal_parser.python_run("import sys\nprint(int(sys.argv[1]) + 1)", args=["41"])
        self.assertTrue(result["ok"])
        self.assertEqual(result["stdout"].strip(), "42")
        self.assertEqual(result["language"], "python")
        self.assertTrue(result["temporary_source"])

    @unittest.skipUnless(shutil.which("g++"), "g++ required")
    def test_cpp_compile_run_builds_and_executes(self):
        result = terminal_parser.cpp_compile_run(
            '#include <iostream>\nint main(){std::cout << 42 << "\\n";}',
            standard="c++20",
        )
        self.assertTrue(result["ok"])
        self.assertEqual(result["stdout"].strip(), "42")
        self.assertEqual(result["language"], "c++")
        self.assertEqual(result["phase"], "run")

    def test_direct_code_bridge_rejects_oversized_source(self):
        with self.assertRaisesRegex(ValueError, "code exceeds"):
            terminal_parser.python_run("x" * (terminal_parser.MAX_SOURCE + 1))

    def test_allows_shell_wrappers_used_by_ai_clients(self):
        result = terminal_parser.run(["bash", "-lc", "printf PERPLEXITY_SHELL_OK"])
        self.assertTrue(result["ok"])
        self.assertEqual(result["stdout"], "PERPLEXITY_SHELL_OK")
        self.assertEqual(result["exit_code"], 0)


if __name__ == "__main__":
    unittest.main()