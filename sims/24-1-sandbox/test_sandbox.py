"""Registry structure/path controls; these deliberately do not run solvers."""
import copy
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import sandbox


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.root = self.repo / "sandbox"
        self.module = self.root / "modules" / "sample"
        self.module.mkdir(parents=True)
        (self.repo / "schema.json").write_text("{}")
        (self.repo / "engine").mkdir()
        (self.module / "adapter.py").write_text('raise RuntimeError("must not execute")')
        self.manifest = json.loads((sandbox.ROOT / "modules/01-lattice-primitive/manifest.json").read_text())
        self.manifest["state_schema"] = "../../../schema.json"
        self.manifest["adapter"] = {"existing": "../../../engine", "entry_point": "adapter.py"}
        self.write(self.manifest)

    def write(self, value, module=None):
        target = module or self.module
        target.mkdir(parents=True, exist_ok=True)
        (target / "manifest.json").write_text(json.dumps(value))

    def report(self):
        return sandbox.registry_report(self.root, self.repo)

    def test_valid_registry_never_executes_adapter(self):
        result = self.report()
        self.assertTrue(result["ok"])
        self.assertEqual(result["validation_scope"], "manifest-and-paths-only")
        self.assertEqual(result["module_execution"], "not-run")
        self.assertTrue(result["modules"][0]["entry_point_present"])

    def test_shape_errors_are_diagnostics(self):
        for value in (None, [], "text", 12, True):
            with self.subTest(value=value):
                self.write(value)
                self.assertFalse(self.report()["ok"])
                self.assertEqual(sandbox.validate(value), ["manifest:must-be-object"])

    def test_parse_and_encoding_errors_are_diagnostics(self):
        for data in (b'{invalid', b'\xff'):
            (self.module / "manifest.json").write_bytes(data)
            self.assertFalse(self.report()["ok"])

    def test_nested_wrong_types_fail_closed(self):
        for field in ("solver", "render", "fixtures", "validation", "adapter"):
            for value in (None, [], "text", 4, False):
                with self.subTest(field=field, value=value):
                    m = copy.deepcopy(self.manifest)
                    m[field] = value
                    self.write(m)
                    self.assertFalse(self.report()["ok"])

    def test_nested_field_and_list_shapes(self):
        for section, field in (("solver", "units"), ("solver", "equations"),
                               ("render", "views"), ("fixtures", "positive"),
                               ("validation", "convergence")):
            m = copy.deepcopy(self.manifest)
            m[section][field] = None
            self.write(m)
            self.assertFalse(self.report()["ok"])
        for field in ("dimensions", "controls", "data_sources"):
            for value in (None, "text", [None], [{}]):
                m = copy.deepcopy(self.manifest)
                m[field] = value
                self.write(m)
                self.assertFalse(self.report()["ok"])

    def test_required_strings_and_fields(self):
        for field in ("id", "name", "version", "claim_gate", "state_schema"):
            for value in (None, [], "", "  ", True):
                m = copy.deepcopy(self.manifest)
                m[field] = value
                self.write(m)
                self.assertFalse(self.report()["ok"])
        for field in ("schema", "slot", "dimensions", "solver", "render", "controls", "fixtures", "validation"):
            m = copy.deepcopy(self.manifest)
            del m[field]
            self.write(m)
            self.assertFalse(self.report()["ok"])

    def test_boolean_and_out_of_range_slots(self):
        for slot in (True, False, 0, 25, 1.0, "1", [], {}):
            self.manifest["slot"] = slot
            self.write(self.manifest)
            self.assertFalse(self.report()["ok"])

    def test_duplicate_ids_and_slots_mark_both_records(self):
        self.write(self.manifest, self.root / "modules/second")
        result = self.report()
        self.assertFalse(result["ok"])
        self.assertEqual(result["occupied_slots"], [])
        for item in result["modules"]:
            self.assertIn("duplicate-id", item["errors"])
            self.assertIn("duplicate-slot", item["errors"])

    def test_empty_and_missing_registry_fail(self):
        (self.module / "manifest.json").unlink()
        self.assertEqual(self.report()["errors"], ["registry:no-manifests"])
        self.assertFalse(sandbox.registry_report(self.repo / "absent", self.repo)["ok"])

    def test_missing_wrong_type_references(self):
        for field, value in (("state_schema", "missing.json"), ("state_schema", "."),
                             ("existing", "missing"), ("existing", "adapter.py"),
                             ("entry_point", "missing.py"), ("entry_point", ".")):
            m = copy.deepcopy(self.manifest)
            (m if field == "state_schema" else m["adapter"])[field] = value
            self.write(m)
            self.assertFalse(self.report()["ok"])

    def test_optional_entry_point_is_not_execution(self):
        del self.manifest["adapter"]["entry_point"]
        self.write(self.manifest)
        result = self.report()
        self.assertTrue(result["ok"])
        self.assertFalse(result["modules"][0]["entry_point_present"])
        self.assertEqual(result["modules"][0]["module_execution"], "not-run")

    def test_absolute_traversal_and_symlink_escapes(self):
        for value in (str(self.module / "adapter.py"), "../../../../outside.py", "bad\0path"):
            self.manifest["adapter"]["entry_point"] = value
            self.write(self.manifest)
            self.assertFalse(self.report()["ok"])
        with tempfile.TemporaryDirectory() as other:
            outside = Path(other) / "external.py"
            outside.write_text("pass")
            (self.module / "escape.py").symlink_to(outside)
            self.manifest["adapter"]["entry_point"] = "escape.py"
            self.write(self.manifest)
            self.assertFalse(self.report()["ok"])

    def test_input_cannot_override_diagnostics(self):
        self.manifest.update({"_path": "/untrusted", "_error": {"untrusted": True}})
        self.write(self.manifest)
        self.assertTrue(self.report()["ok"])
        self.assertEqual(self.report()["modules"][0]["path"], str(self.module / "manifest.json"))

    def test_cli_failure_is_json_and_exit_two(self):
        self.manifest["slot"] = True
        self.write(self.manifest)
        result = self.report()
        self.assertIsNone(result["modules"][0]["entry_point_present"])
        self.assertTrue((self.module / "adapter.py").is_file())
        with patch.object(sandbox, "registry_report", return_value=result), patch("sys.argv", ["sandbox.py", "--json"]):
            output = io.StringIO()
            with contextlib.redirect_stdout(output), self.assertRaises(SystemExit) as exited:
                sandbox.main()
            self.assertEqual(exited.exception.code, 2)
            self.assertFalse(json.loads(output.getvalue())["ok"])

    def test_read_failure_diagnostic(self):
        with patch.object(Path, "read_text", side_effect=PermissionError("denied")):
            self.assertFalse(self.report()["ok"])

    def test_current_repository_paths_and_status(self):
        result = sandbox.registry_report()
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["occupied_slots"], [1, 6])
        self.assertEqual([item["entry_point_present"] for item in result["modules"]], [True, False])
        self.assertTrue(all(item["module_execution"] == "not-run" for item in result["modules"]))


if __name__ == "__main__":
    unittest.main()
