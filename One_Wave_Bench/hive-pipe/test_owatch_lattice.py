#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
import unittest

import owatch_lattice as lattice


class OwatchLatticeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.runtime = self.root / ".runtime"
        lattice.RUNTIME_ROOT = self.runtime

        self.a = self.root / "A"
        self.b = self.root / "B"
        for p in (self.a, self.b):
            (p / ".owatch").mkdir(parents=True)

        (self.a / ".owatch" / "folder.json").write_text(
            json.dumps(
                {
                    "schema": "one-wave-watched-folder-v2",
                    "node_id": "node-a",
                    "role": "science",
                    "concept_tags": ["time", "transport"],
                    "authority_refs": ["A/theory.md"],
                    "edges": [
                        {
                            "type": "DEPENDS_ON",
                            "target": "node-b",
                            "weight": 1.0,
                            "note": "test dependency",
                        }
                    ],
                }
            )
        )
        (self.b / ".owatch" / "folder.json").write_text(
            json.dumps(
                {
                    "schema": "one-wave-watched-folder-v2",
                    "node_id": "node-b",
                    "role": "evidence",
                    "concept_tags": ["time", "measurement"],
                    "authority_refs": ["B/evidence.md"],
                    "edges": [],
                }
            )
        )
        (self.a / "theory.md").write_text(
            "# Theory\n\nFirst sentence. Second sentence!\n\n"
            "## Test\n\nA falsifiable paragraph lives here. Another sentence.\n"
        )
        (self.b / "evidence.md").write_text(
            "# Evidence\n\nMeasured values belong here.\n"
        )

    def tearDown(self):
        self.temp.cleanup()

    def test_discovers_stable_nodes_and_typed_edge(self):
        graph = lattice.graph_doc(self.root)
        self.assertEqual(set(graph["nodes"]), {"node-a", "node-b"})
        self.assertEqual(graph["edges"][0]["type"], "DEPENDS_ON")
        self.assertIn("navigation memory only", graph["truth_rule"])

    def test_layering_reaches_page_paragraph_sentence_word(self):
        doc = lattice.layer_document(self.a / "theory.md", self.root)
        self.assertGreaterEqual(len(doc["pages"]), 2)
        page = doc["pages"][0]
        para = page["paragraphs"][0]
        sent = para["sentences"][0]
        self.assertTrue(sent["sentence_id"].startswith("sentence-"))
        self.assertEqual(sent["words"][0]["text"], "Theory")

    def test_cache_is_compressed_runtime_state(self):
        nodes = lattice.discover_nodes(self.root)
        lattice.build_node_cache(self.root, nodes["node-a"])
        path = lattice.node_cache_path("node-a")
        self.assertTrue(path.is_file())
        self.assertEqual(path.suffix, ".gz")
        self.assertFalse(str(path).startswith(str(self.a)))

    def test_open_layer_returns_only_requested_sentence(self):
        result = lattice.open_layer(
            self.root,
            "node-a",
            file_path="A/theory.md",
            page=1,
            paragraph=1,
            sentence=1,
        )
        self.assertEqual(result["state"], "active")
        self.assertEqual(len(result["selection"]), 1)
        self.assertIn("Theory", result["selection"][0]["text"])

    def test_hysteresis_remembers_but_decays(self):
        first = lattice.update_hysteresis("node-a", "node-b", "DEPENDS_ON", "success")
        second = lattice.update_hysteresis("node-a", "node-b", "DEPENDS_ON", "success")
        self.assertGreater(second["score"], first["score"])
        before_failure = second["score"]
        failed = lattice.update_hysteresis("node-a", "node-b", "DEPENDS_ON", "failure")
        self.assertLess(failed["score"], before_failure)
        self.assertLessEqual(abs(failed["score"]), 1.0)

    def test_differential_router_exposes_components(self):
        lattice.update_hysteresis("node-a", "node-b", "DEPENDS_ON", "success")
        candidates = lattice.route_candidates(self.root, "node-a", "time measurement")
        self.assertEqual(candidates[0]["target"], "node-b")
        self.assertIn("positive", candidates[0])
        self.assertIn("negative", candidates[0])
        self.assertIn("path_hysteresis", candidates[0]["components"])
        self.assertIn("not evidence", candidates[0]["truth_warning"])

    def test_hold_penalizes_route(self):
        (self.b / ".owatch" / "HOLD.json").write_text('{"status":"HOLD"}\n')
        candidates = lattice.route_candidates(self.root, "node-a", "time measurement")
        self.assertEqual(candidates[0]["components"]["hold_penalty"], 1.0)

    def test_unknown_edge_type_fails_closed(self):
        policy = json.loads((self.a / ".owatch" / "folder.json").read_text())
        policy["edges"][0]["type"] = "MAGIC"
        (self.a / ".owatch" / "folder.json").write_text(json.dumps(policy))
        with self.assertRaises(ValueError):
            lattice.discover_nodes(self.root)


if __name__ == "__main__":
    unittest.main()
