#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import unittest

import logic_kernel as lk

HERE = Path(__file__).resolve().parent
CORPUS = HERE / "logic_kernel_corpus.json"


def e(source, target, kind, reference="r", intention="i", consequence="c", edge_id=None):
    return lk.edge_from_dict({
        "edge_id": edge_id or f"test-{kind}-{source}-{target}",
        "source": source,
        "target": target,
        "kind": kind,
        "source_class": "canon",
        "reference": reference,
        "intention": intention,
        "consequence": consequence,
    })


class LogicKernelTests(unittest.TestCase):
    def test_supports_transitivity(self):
        d=lk.evaluate([e("A","B","SUPPORTS","r1",edge_id="s1"),e("B","C","SUPPORTS","r2",edge_id="s2")])
        self.assertEqual(d.status, lk.DERIVED)
        self.assertEqual((d.proposal.source,d.proposal.target,d.proposal.kind),("A","C","SUPPORTS"))
        self.assertTrue(d.proposal.derived)
        self.assertEqual(set(d.proposal.parent_ids),{"s1","s2"})

    def test_contradiction_propagation(self):
        d=lk.evaluate([e("A","B","CONTRADICTS","r1",edge_id="c1"),e("C","A","SUPPORTS","r2",edge_id="s1")])
        self.assertEqual(d.status, lk.DERIVED)
        self.assertEqual((d.proposal.source,d.proposal.target,d.proposal.kind),("C","B","CONTRADICTS"))

    def test_missing_metadata_holds(self):
        d=lk.evaluate([e("A","B","SUPPORTS",reference="",edge_id="m1")])
        self.assertEqual(d.status, lk.HOLD)
        self.assertIn("m1", d.bad_path_ids)

    def test_self_contradiction_holds(self):
        d=lk.evaluate([e("A","A","CONTRADICTS",edge_id="self1")])
        self.assertEqual(d.status, lk.HOLD)
        self.assertIn("terminate", d.reason)

    def test_two_node_contradiction_cycle_holds(self):
        d=lk.evaluate([
            e("A","B","CONTRADICTS",edge_id="l1"),
            e("B","A","CONTRADICTS",edge_id="l2")
        ])
        self.assertEqual(d.status, lk.HOLD)
        self.assertEqual(set(d.bad_path_ids),{"l1","l2"})

    def test_hold_decays_and_never_boosts(self):
        a=e("A","B","CONTRADICTS",edge_id="l1")
        b=e("B","A","CONTRADICTS",edge_id="l2")
        memory=lk.RouteMemory({"l1":0.7,"l2":0.7})
        receipt=lk.Receipt()
        d=lk.evaluate([a,b])
        lk.apply_memory(d,memory,receipt)
        self.assertLess(memory.score("l1"),0.7)
        self.assertLess(memory.score("l2"),0.7)
        self.assertEqual(receipt.hysteresis_boost_on_bad_path,0)

    def test_unresolved_does_not_change_unrelated_memory(self):
        edge=e("X","Y","SUPPORTS",edge_id="control")
        memory=lk.RouteMemory({"control":0.42})
        receipt=lk.Receipt()
        d=lk.evaluate([edge])
        lk.apply_memory(d,memory,receipt)
        self.assertEqual(d.status, lk.UNRESOLVED)
        self.assertEqual(memory.score("control"),0.42)

    def test_corpus_passes(self):
        corpus=json.loads(CORPUS.read_text(encoding="utf-8"))
        result=lk.run_corpus(corpus)
        self.assertTrue(result["passed"])
        self.assertEqual(result["receipt"]["wrong_derivations"],0)
        self.assertEqual(result["receipt"]["hysteresis_boost_on_bad_path"],0)
        self.assertTrue(result["checks"]["unrelated_route_not_poisoned"])
        self.assertTrue(result["checks"]["at_least_one_terminated_loop"])


if __name__=="__main__":
    unittest.main()
