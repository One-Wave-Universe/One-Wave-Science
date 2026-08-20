"""Step 01 verification for the minimal Field engine shell."""

from __future__ import annotations

import importlib.util
import pathlib
import sys
import unittest


HERE = pathlib.Path(__file__).resolve().parent
ENGINE_PATH = HERE / "field_engine.py"


def load_engine(path: pathlib.Path):
    """Load the shell module from an explicit path.

    Step 01 uses an explicit path so a missing shell component is observable
    and cannot be hidden by an unrelated installed module.
    """
    if not path.is_file():
        raise FileNotFoundError(f"required Field shell component missing: {path}")

    module_name = "field_engine_step01"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load Field shell component: {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(module_name, None)
        raise
    return module


class FieldShellTests(unittest.TestCase):
    def test_shell_reports_ready(self) -> None:
        engine = load_engine(ENGINE_PATH)
        state = engine.start_field_shell()

        self.assertEqual(state.role, "field")
        self.assertEqual(state.step, 1)
        self.assertTrue(state.ready)
        self.assertEqual(state.status, "FIELD_SHELL_READY")
        self.assertEqual(engine.main(), 0)

    def test_missing_shell_component_is_detected(self) -> None:
        missing = HERE / "__deliberately_missing_field_engine__.py"
        with self.assertRaisesRegex(FileNotFoundError, "required Field shell component missing"):
            load_engine(missing)


if __name__ == "__main__":
    unittest.main()
