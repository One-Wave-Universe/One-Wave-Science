#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

import logic_kernel as lk

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
CORPUS = HERE / "logic_kernel_corpus2.json"


def tree_hash(root: Path) -> str:
    h = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        h.update(path.relative_to(root).as_posix().encode("utf-8"))
        h.update(hashlib.sha256(path.read_bytes()).digest())
    return h.hexdigest()


class LogicKernelCorpus2Tests(unittest.TestCase):
    def setUp(self):
        self.corpus = json.loads(CORPUS.read_text(encoding="utf-8"))

    def test_repo_node_chain_files_exist(self):
        for rel in self.corpus["repo_node_chain"]:
            self.assertTrue((REPO / rel).is_file(), rel)

    def test_canon_referee_must_be_non_derived_canon(self):
        false_ref = lk.edge_from_dict({
            "edge_id":"bad-ref",
            "source":"span:a",
            "target":"span:c",
            "kind":"CONTRADICTS",
            "source_class":"derived",
            "derived":True,
            "reference":"runtime-derived",
            "intention":"should not referee",
            "consequence":"must HOLD"
        })
        parent1 = lk.edge_from_dict({
            "edge_id":"p1","source":"span:a","target":"span:b","kind":"SUPPORTS",
            "source_class":"canon","reference":"r1","intention":"i1","consequence":"c1"
        })
        parent2 = lk.edge_from_dict({
            "edge_id":"p2","source":"span:b","target":"span:c","kind":"SUPPORTS",
            "source_class":"canon","reference":"r2","intention":"i2","consequence":"c2"
        })
        d = lk.derive_pair(parent1, parent2)
        ledger = lk.DerivedLedger()
        ledger.add(d.proposal)
        receipt = lk.Receipt()
        memory = lk.RouteMemory()
        out = lk.invalidate_with_referee(false_ref, d.proposal.edge_id, ledger, memory, receipt)
        self.assertEqual(out["status"], lk.HOLD)
        self.assertEqual(receipt.wrong_derivations, 0)
        self.assertTrue(ledger.active(d.proposal.edge_id))

    def test_stable_ids_prevent_semantic_collision_prune(self):
        a = lk.edge_from_dict({
            "edge_id":"a1","source":"x","target":"y","kind":"SUPPORTS",
            "source_class":"canon","reference":"r1","intention":"i1","consequence":"c1"
        })
        b = lk.edge_from_dict({
            "edge_id":"b1","source":"y","target":"z","kind":"SUPPORTS",
            "source_class":"canon","reference":"r2","intention":"i2","consequence":"c2"
        })
        c = lk.edge_from_dict({
            "edge_id":"a2","source":"x","target":"y","kind":"SUPPORTS",
            "source_class":"canon","reference":"different","intention":"different","consequence":"different"
        })
        d = lk.edge_from_dict({
            "edge_id":"b2","source":"y","target":"z","kind":"SUPPORTS",
            "source_class":"canon","reference":"different2","intention":"different2","consequence":"different2"
        })
        one = lk.derive_pair(a,b).proposal
        two = lk.derive_pair(c,d).proposal
        self.assertNotEqual(one.edge_id, two.edge_id)

        ledger=lk.DerivedLedger()
        ledger.add(one); ledger.add(two)
        pruned,_ = ledger.prune(one.edge_id,"test")
        self.assertIn(one.edge_id, pruned)
        self.assertTrue(ledger.active(two.edge_id))

    def test_second_corpus_retracts_parent_and_grandchild(self):
        before = tree_hash(REPO / "Nodes")
        result = lk.run_lifecycle_corpus(self.corpus)
        after = tree_hash(REPO / "Nodes")

        self.assertTrue(result["passed"])
        self.assertGreater(result["receipt"]["wrong_derivations"], 0)
        self.assertGreater(result["receipt"]["pruned_derived"], 0)
        self.assertGreater(result["receipt"]["stale_children_pruned"], 0)
        self.assertEqual(result["receipt"]["hysteresis_boost_on_bad_path"], 0)
        self.assertEqual(result["poison_probe"]["before"], 0.47)
        self.assertEqual(result["poison_probe"]["after"], 0.47)
        self.assertEqual(before, after)
        self.assertFalse(result["authority"]["derived_is_canon"])
        self.assertFalse(result["authority"]["nodes_written"])

    def test_prune_is_idempotent(self):
        source1 = lk.edge_from_dict(self.corpus["seed_edges"]["cedar_supports_amber"])
        source2 = lk.edge_from_dict(self.corpus["seed_edges"]["amber_supports_violet"])
        derived = lk.derive_pair(source1, source2).proposal
        ledger = lk.DerivedLedger(); ledger.add(derived)
        first,_ = ledger.prune(derived.edge_id,"first")
        second,_ = ledger.prune(derived.edge_id,"second")
        self.assertEqual(len(first),1)
        self.assertEqual(second,[])


if __name__=="__main__":
    unittest.main()
