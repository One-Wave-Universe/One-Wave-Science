#!/usr/bin/env python3

import unittest

import terminal_parser


class TerminalParserTests(unittest.TestCase):
    def test_pwd_defaults_to_repo(self):
        result = terminal_parser.pwd()
        self.assertTrue(result["ok"])
        self.assertEqual(result["cwd"], str(terminal_parser.REPO_ROOT))

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

    def test_nonzero_exit_is_reported(self):
        result = terminal_parser.run(["false"])
        self.assertFalse(result["ok"])
        self.assertNotEqual(result["exit_code"], 0)

    def test_blocks_direct_privilege_and_raw_disk_commands(self):
        for argv in (["sudo", "id"], ["mkfs.ext4", "/dev/sdz"], ["reboot"]):
            with self.assertRaises(ValueError):
                terminal_parser.run(argv)

    def test_allows_shell_wrappers_used_by_ai_clients(self):
        result = terminal_parser.run(["bash", "-lc", "printf PERPLEXITY_SHELL_OK"])
        self.assertTrue(result["ok"])
        self.assertEqual(result["stdout"], "PERPLEXITY_SHELL_OK")
        self.assertEqual(result["exit_code"], 0)


if __name__ == "__main__":
    unittest.main()
