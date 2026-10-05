"""Refresh-controller fault injection uses disposable repositories only."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

P = Path(__file__).with_name("refresh.py")
spec = importlib.util.spec_from_file_location("refresh_under_test", P)
refresh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(refresh)


class RefreshTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.root = self.base / "repo"
        self.root.mkdir()
        self.output = self.base / "bundle"
        self.dep = {"schema": "one-wave-module-refresh-dependencies/v1", "shared": ["authority.md", refresh.DEPENDENCIES],
                    "modules": {"lattice-primitive": ["lattice/**"], "spectral-lattice-phase": ["spectral/**"]}}
        for path, content in (("authority.md", "rules"), ("lattice/kernel.js", "lattice"), ("spectral/engine.py", "spectral"),
                              (refresh.DEPENDENCIES, json.dumps(self.dep))):
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
        self.git("init", "-q")
        self.commit()
        self.head = self.git("rev-parse", "HEAD")

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.root), *args], text=True, stderr=subprocess.DEVNULL).strip()

    def commit(self):
        self.git("add", ".")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-qm", "fixture")

    def simple_commands(self, extra=None):
        result = {name: [(name, [sys.executable, "-c", "print('verified test fixture')"], None)]
                  for name in ("registry", *refresh.MODULES)}
        if extra:
            result.update(extra)
        return result

    def run_refresh(self, commands=None, **kwargs):
        with patch.object(refresh, "commands", return_value=commands or self.simple_commands()):
            return refresh.refresh(self.root, self.head, self.output, **kwargs)

    def test_clean_reference_runs_and_finalizes_without_source_changes(self):
        result = self.run_refresh()
        self.assertEqual(result["status"], "COMPLETED")
        self.assertEqual(result["reference_before"], result["reference_after"])
        self.assertEqual(self.git("status", "--porcelain"), "")
        self.assertTrue((self.output / "summary.json").is_file())
        self.assertFalse((self.output / "summary.json.tmp").exists())
        self.assertFalse(json.loads((self.output / "RUNNING.json").read_text())["eligible_as_current"])

    def test_governing_node_selects_only_correct_module_and_authority_both(self):
        actual = refresh.load_dependencies(refresh.ROOT)
        cases = {
            "Nodes/G-767_Measured_Spectrum_Lattice_Phase_Map.md": ["spectral-lattice-phase"],
            "Nodes/G-764_Combined_State_Lattice_Simulator_Foundation.md": ["lattice-primitive"],
            "AGENTS.md": list(refresh.MODULES),
            "Governance_I_Series/I-06_Canonical_Node_Metadata_and_Alias_Resolution.md": list(refresh.MODULES),
            "sims/24-1-sandbox/refresh.py": list(refresh.MODULES),
            ".github/workflows/lattice-kernel-tests.yml": list(refresh.MODULES),
            "PHASE_5_STATUS.md": [],
        }
        for path, expected in cases.items():
            self.assertEqual(refresh.affected_modules(actual, [path]), expected, path)

    def test_changed_base_runs_only_affected_module(self):
        old = self.head
        (self.root / "spectral/engine.py").write_text("new source")
        self.commit()
        self.head = self.git("rev-parse", "HEAD")
        result = self.run_refresh(base=old)
        self.assertEqual(result["affected_modules"], ["spectral-lattice-phase"])
        self.assertEqual([c["group"] for c in result["commands"]], ["registry", "spectral-lattice-phase"])
        self.assertEqual(result["modules"]["lattice-primitive"]["status"], "NOT_RUN_UNAFFECTED")

    def test_unrelated_change_does_not_inherit_green(self):
        old = self.head
        (self.root / "unrelated.md").write_text("unrelated")
        self.commit()
        self.head = self.git("rev-parse", "HEAD")
        result = self.run_refresh(base=old)
        self.assertEqual(result["status"], "NO_AFFECTED_MODULES")
        self.assertFalse(result["eligible_as_current"])
        self.assertEqual(result["commands"], [])

    def test_dirty_checkout_is_preserved_and_not_executed(self):
        (self.root / "lattice/kernel.js").write_text("user changes")
        result = self.run_refresh()
        self.assertEqual(result["status"], "HOLD")
        self.assertEqual(result["commands"], [])
        self.assertEqual((self.root / "lattice/kernel.js").read_text(), "user changes")

    def test_wrong_head_and_unknown_base_hold(self):
        self.head = "0" * 40
        self.assertEqual(self.run_refresh()["status"], "HOLD")
        self.output = self.base / "another"
        self.head = self.git("rev-parse", "HEAD")
        self.assertEqual(self.run_refresh(base="0"*40)["status"], "HOLD")

    def test_added_deleted_dependency_membership_changes_fingerprint(self):
        before, _ = refresh.reference(self.root)
        (self.root / "lattice/added.js").write_text("added")
        after, _ = refresh.reference(self.root)
        self.assertNotEqual(before["groups"], after["groups"])
        (self.root / "lattice/kernel.js").unlink()
        deleted, _ = refresh.reference(self.root)
        self.assertNotEqual(after["groups"], deleted["groups"])

    def test_missing_dependency_holds(self):
        (self.root / "authority.md").unlink()
        result = self.run_refresh()
        self.assertEqual(result["status"], "HOLD")
        self.assertFalse(result["eligible_as_current"])

    def test_actual_command_source_drift_invalidates_entire_bundle(self):
        drift = [sys.executable, "-c", "from pathlib import Path; Path('lattice/kernel.js').write_text('drift')"]
        commands = self.simple_commands({"registry": [("drift", drift, None)]})
        result = self.run_refresh(commands)
        self.assertEqual(result["status"], "HOLD")
        self.assertFalse(result["eligible_as_current"])
        self.assertEqual(len(result["commands"]), 1)
        self.assertTrue(all(v["status"] != "COMPLETED" for v in result["modules"].values()))
        self.assertEqual((self.root / "lattice/kernel.js").read_text(), "drift")

    def test_failed_command_is_retained_and_not_retried(self):
        commands = self.simple_commands({"registry": [("fail", [sys.executable, "-c", "print('negative evidence'); raise SystemExit(3)"], None)]})
        result = self.run_refresh(commands)
        self.assertEqual(result["status"], "HOLD")
        self.assertEqual(len(result["commands"]), 1)
        self.assertIn("negative evidence", (self.output / "fail.stdout.txt").read_text())

    def test_real_timeout_and_output_cap(self):
        timeout = refresh.execute([sys.executable, "-c", "import time; time.sleep(5)"], self.root, timeout=0.1)
        self.assertEqual(timeout["reason"], "timeout")
        self.assertLess(timeout["elapsed_s"], 2)
        capped = refresh.execute([sys.executable, "-c", "print('x'*1000000)"], self.root, max_output=512)
        self.assertEqual(capped["reason"], "output-limit")
        self.assertLessEqual(len(capped["stdout"].encode()) + len(capped["stderr"].encode()), 512)

    def test_timeout_becomes_hold_not_completed(self):
        commands = self.simple_commands({"registry": [("timeout", [sys.executable, "-c", "import time; time.sleep(5)"], None)]})
        with patch.object(refresh, "COMMAND_TIMEOUT", 0.1):
            result = self.run_refresh(commands)
        self.assertEqual(result["status"], "HOLD")
        self.assertEqual(result["commands"][0]["reason"], "timeout")

    def test_malformed_registry_receipt_stops_pipeline(self):
        commands = self.simple_commands({"registry": [("registry", [sys.executable, "-c", "print('{}')"], "registry.json")]})
        result = self.run_refresh(commands)
        self.assertEqual(result["status"], "HOLD")
        self.assertEqual(len(result["commands"]), 1)
        self.assertFalse((self.output / "registry.json").exists())

    def test_stale_source_receipt_rejected(self):
        module = "spectral-lattice-phase"
        raw = subprocess.check_output([sys.executable, str(refresh.ROOT / "sims/24-1-sandbox/modules/06-spectral-lattice-phase/adapter.py")], text=True)
        receipt = json.loads(raw)
        hashes = receipt["final"]["provenance"]["source_sha256"]
        paths = set(hashes)
        before = {"groups": {"shared": {}, module: hashes}}
        refresh.check_receipt(raw, module, before)
        for key in ("configuration", "initial", "final", "measurements", "geometry"):
            incomplete = copy.deepcopy(receipt)
            del incomplete[key]
            with self.assertRaises(refresh.Hold):
                refresh.check_receipt(json.dumps(incomplete), module, before)
        receipt = copy.deepcopy(receipt)
        receipt["final"]["provenance"]["source_sha256"][next(iter(paths))] = "b"*64
        with self.assertRaises(refresh.Hold):
            refresh.check_receipt(json.dumps(receipt), module, before)
        for raw in ("null", "[]", "{", "NaN", '{"value":1e999}'):
            with self.assertRaises(refresh.Hold):
                refresh.check_receipt(raw, module, before)

    def test_actual_lattice_receipt_and_state_mismatch(self):
        raw = subprocess.check_output(["node", str(refresh.ROOT / "sims/24-1-sandbox/modules/01-lattice-primitive/adapter.js")], text=True)
        receipt = json.loads(raw)
        module = "lattice-primitive"
        before = {"groups": {"shared": {}, module: receipt["provenance"]["source_sha256"]}}
        refresh.check_receipt(raw, module, before)
        receipt["geometry"]["points"][0]["displacement"] = 123456
        with self.assertRaises(refresh.Hold):
            refresh.check_receipt(json.dumps(receipt), module, before)

    def test_partial_registry_and_snapshot_source_identity_refused(self):
        raw = subprocess.check_output([sys.executable, str(refresh.ROOT / "sims/24-1-sandbox/sandbox.py"), "--json"], text=True)
        good = json.loads(raw)
        refresh.check_receipt(raw, "registry", {})
        for key in ("modules", "occupied_slots", "errors", "validation_scope"):
            value = copy.deepcopy(good)
            del value[key]
            with self.assertRaises(refresh.Hold):
                refresh.check_receipt(json.dumps(value), "registry", {})
        raw = subprocess.check_output([sys.executable, str(refresh.ROOT / "sims/24-1-sandbox/modules/06-spectral-lattice-phase/adapter.py")], text=True)
        value = json.loads(raw)
        module = "spectral-lattice-phase"
        before = {"groups": {"shared": {}, module: value["final"]["provenance"]["source_sha256"]}}
        value["initial"]["provenance"]["source_sha256"] = {}
        with self.assertRaises(refresh.Hold):
            refresh.check_receipt(json.dumps(value), module, before)

    def test_lattice_history_must_be_finite_typed_and_consistent(self):
        raw = subprocess.check_output(["node", str(refresh.ROOT / "sims/24-1-sandbox/modules/01-lattice-primitive/adapter.js")], text=True)
        good = json.loads(raw)
        module = "lattice-primitive"
        before = {"groups": {"shared": {}, module: good["provenance"]["source_sha256"]}}
        changes = [lambda r: r.update(samples=[None] * len(r["samples"])),
                   lambda r: r["samples"][1].update(time=False),
                   lambda r: r["samples"][1].update(time=-1),
                   lambda r: r["samples"][1]["measurements"].update(energy="unknown"),
                   lambda r: r["samples"][-1]["measurements"].update(energy=999),
                   lambda r: r.update(solver=[None] * len(r["solver"])),
                   lambda r: r["initial"]["provenance"].update(source="wrong")]
        for change in changes:
            value = copy.deepcopy(good)
            change(value)
            with self.assertRaises(refresh.Hold):
                refresh.check_receipt(json.dumps(value), module, before)

    def test_occupied_unsafe_and_symlink_outputs_refused(self):
        self.output.mkdir()
        with self.assertRaises(refresh.Hold):
            self.run_refresh()
        for output in (self.root / "output", self.root / ".git/output"):
            with self.assertRaises(refresh.Hold):
                refresh.create_bundle(self.root, output)
        link = self.base / "link"
        link.symlink_to(self.output)
        with self.assertRaises(refresh.Hold):
            refresh.create_bundle(self.root, link)

    def test_dependency_map_cannot_supply_commands_or_escape(self):
        for alteration in ({"command": "bad"}, {"shared": ["../escape"]}, {"modules": {}}):
            value = {**self.dep, **alteration}
            (self.root / refresh.DEPENDENCIES).write_text(json.dumps(value))
            with self.assertRaises(refresh.Hold):
                refresh.load_dependencies(self.root)

    def test_workflow_cancels_superseded_runs_and_preserves_evidence(self):
        workflow = (refresh.ROOT / ".github/workflows/lattice-kernel-tests.yml").read_text()
        for expected in ("cancel-in-progress: true", "github.event.pull_request.number || github.ref", "persist-credentials: false",
                         "contents: read", "if: always()", "actions/upload-artifact@v4", "REFRESH_HEAD", "'Nodes/**'", "'AGENTS.md'"):
            self.assertIn(expected, workflow)
        job_env = workflow.split("    env:", 1)[1].split("    steps:", 1)[0]
        self.assertNotIn("runner.", job_env)
        self.assertIn('--output "$RUNNER_TEMP/$REFRESH_BUNDLE"', workflow)
        self.assertIn("path: ${{ runner.temp }}/${{ env.REFRESH_BUNDLE }}", workflow)
        self.assertNotIn("git pull", workflow)
        self.assertNotIn("contents: write", workflow)


if __name__ == "__main__":
    unittest.main()
