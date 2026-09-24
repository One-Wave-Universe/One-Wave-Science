#!/usr/bin/env python3

import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

import mudl


class HivePipeTests(unittest.TestCase):
    def test_action_registry_has_no_shell(self):
        for command in mudl.ACTIONS.values():
            self.assertIsInstance(command, list)
            self.assertNotIn("sh", command[0])
            self.assertNotIn("bash", command[0])

    def test_rejects_unknown_action(self):
        with tempfile.TemporaryDirectory() as directory:
            request = Path(directory) / "job.json"
            request.write_text(json.dumps({
                "version": 1, "id": "job", "action": "format_disk",
                "created_utc": "2026-09-12T17:00:00Z",
            }))
            with self.assertRaisesRegex(ValueError, "unknown or disabled"):
                mudl.validate_request(request)

    def test_rejects_extra_payload_keys(self):
        with tempfile.TemporaryDirectory() as directory:
            request = Path(directory) / "job.json"
            request.write_text(json.dumps({
                "version": 1, "id": "job", "action": "health",
                "created_utc": "2026-09-12T17:00:00Z",
                "command": "rm -rf /",
            }))
            with self.assertRaisesRegex(ValueError, "request keys"):
                mudl.validate_request(request)

    def test_executes_named_action_and_archives_request(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with mock.patch.multiple(
                mudl,
                QUEUE=root,
                PENDING=root / "pending",
                PROCESSING=root / "processing",
                RESULTS=root / "results",
                DONE=root / "done",
            ):
                mudl.ensure_dirs()
                request = mudl.PROCESSING / "job.json"
                request.write_text(json.dumps({
                    "version": 1, "id": "job", "action": "health",
                    "created_utc": "2026-09-12T17:00:00Z",
                }))
                output = mudl.execute(request)
                result = json.loads(output.read_text())
                self.assertEqual(result["exit_code"], 0)
                self.assertTrue((mudl.DONE / "job.json").exists())


if __name__ == "__main__":
    unittest.main()
