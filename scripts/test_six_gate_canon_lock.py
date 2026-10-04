"""Current physical authority must not regress to old six-device wording."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import six_gate_canon_lock as canon


class CanonTests(unittest.TestCase):
    def fixture(self, root):
        ai = root / "AI_CANONICAL_START_HERE.md"
        master = root / "00_MASTER_INDEX.md"
        ai.write_text("\n".join(canon.AI_REQUIRED))
        master.write_text("\n".join(canon.MASTER_REQUIRED))
        files = []
        for name, required in canon.CURRENT_PHYSICAL_REQUIRED.items():
            p = root / name; p.write_text("\n".join(required)); files.append(p)
        return ai, master, tuple(files)

    def test_current_physical_contract_passes(self):
        with tempfile.TemporaryDirectory() as d:
            ai, master, files = self.fixture(Path(d))
            with patch.multiple(canon, ROOT=Path(d), AI_START=ai, MASTER=master, CANON_FILES=files):
                self.assertEqual(canon.check(), [])

    def test_old_six_physical_gate_reading_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            ai, master, files = self.fixture(Path(d))
            ai.write_text(ai.read_text() + "\n" + canon.AI_FORBIDDEN[0])
            with patch.multiple(canon, ROOT=Path(d), AI_START=ai, MASTER=master, CANON_FILES=files):
                self.assertTrue(any("superseded" in e for e in canon.check()))

    def test_missing_logical_physical_separation_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            ai, master, files = self.fixture(Path(d))
            files[0].write_text(files[0].read_text().replace("logical/receipt sequence only", ""))
            with patch.multiple(canon, ROOT=Path(d), AI_START=ai, MASTER=master, CANON_FILES=files):
                self.assertTrue(any("logical/receipt" in e for e in canon.check()))

    def test_gate_seven_guard_required(self):
        with tempfile.TemporaryDirectory() as d:
            ai, master, files = self.fixture(Path(d))
            ai.write_text(ai.read_text().replace("no internal Gate 7", ""))
            with patch.multiple(canon, ROOT=Path(d), AI_START=ai, MASTER=master, CANON_FILES=files):
                self.assertTrue(any("Gate 7" in e for e in canon.check()))


if __name__ == "__main__": unittest.main()
