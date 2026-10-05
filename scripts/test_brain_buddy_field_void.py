"""Deterministic tests for the Field/Void science lane."""
from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import brain_buddy_council as bb  # noqa: E402


class FieldVoidTests(unittest.TestCase):
    def test_void_counter_proposal_status(self):
        text = "Exact correction: replace ambiguous sentence.\nVOID_STATUS: COUNTER_PROPOSE"
        self.assertEqual(bb.field_void_status(text, "void"), "COUNTER_PROPOSE")

    def test_void_accept_status(self):
        self.assertEqual(bb.field_void_status("VOID_STATUS: ACCEPT", "void"), "ACCEPT")

    def test_missing_status_holds(self):
        self.assertEqual(bb.field_void_status("no status line", "void"), "HOLD")

    def test_context_packet_includes_yaml_metadata_and_one_node(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "Nodes").mkdir()
            (root / "Root_Axioms").mkdir()
            (root / "Nodes" / "E-533_test.md").write_text(
                '---\nnode_id: "E-533"\ngate: "YELLOW"\nlifecycle: "ACTIVE"\nmetadata_standard: "I-06"\n---\n\n# Time dilation transport\nfinite transport ceiling',
                encoding="utf-8",
            )
            (root / "Nodes" / "A-100_other.md").write_text(
                '---\nnode_id: "A-100"\ngate: "GREEN"\nlifecycle: "ACTIVE"\nmetadata_standard: "I-06"\n---\n\n# unrelated',
                encoding="utf-8",
            )
            packet = bb.science_context_packet(root, "time dilation transport E-533")
            self.assertIn('node_id: "E-533"', packet)
            self.assertIn('gate: "YELLOW"', packet)
            self.assertIn('lifecycle: "ACTIVE"', packet)
            self.assertNotIn('node_id: "A-100"', packet)

    def test_void_prompt_allows_exact_counter_correction(self):
        prompt = bb.void_prompt("q", "CTX", "FIELD PROPOSAL", "")
        self.assertIn("VOID_STATUS: COUNTER_PROPOSE", prompt)
        self.assertIn("exact correction", prompt.lower())
        self.assertIn("repo path", prompt.lower())


if __name__ == "__main__":
    unittest.main()