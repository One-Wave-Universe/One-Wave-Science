#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import unittest

import logic_kernel as lk


def e(source, target, kind, reference="r", intention="i", consequence="c"):
    return lk.Edge(source, target, kind, reference, intention, consequence)


class LogicKernelTests(unittest.TestCase):
    def test_supports_transitivity(self):
        d=lk.evaluate([e("A","B","SUPPORTS"),e("B","C","SUPPORTS")])
        self.assertEqual(d.status, lk.DERIVED)
        self.assertEqual((d.proposal.source,d.proposal.target,d.proposal.kind),("A","C","SUPPORTS"))
        self.assertTrue(d.proposal.derived)

    def test_contradiction_propagation(self):
        d=lk.evaluate([e("A","B","CONTRADICTS"),e("C","A","SUPPORTS")])
        self.assertEqual(d.status, lk.DERIVED)
        self.assertEqual((d.proposal.source,d.proposal.target,d.proposal.kind),("C","B","CONTRADICTS"))

    def test_missing_metadata_holds(self):
        d=lk.evaluate([e("A","B","SUPPORTS",reference="")])
        self.assertEqual(d.status, lk.HOLD)

    def test_self_contradiction_holds(self):
        d=lk.evaluate([e("A","A","CONTRADICTS")])
        self.assertEqual(d.status, lk.HOLD)
        self.assertIn("terminate", d.reason)

    def test_two_node_contradiction_cycle_holds(self):
        d=lk.evaluate([e("A","B","CONTRADICTS"),e("B","A","CONTRADICTS")])
        self.assertEqual(d.status, lk.HOLD)
        self.assertEqual(len(d.bad_path_keys),2)

    def test_hold_decays_and_never_boosts(self):
        memory=lk.RouteMemory({"CONTRADICTS:A->B":0.7,"CONTRADICTS:B->A":0.7})
        receipt=lk.Receipt()
        d=lk.evaluate([e("A","B","CONTRADICTS"),e("B","A","CONTRADICTS")])
        lk.apply_memory(d,memory,receipt)
        self.assertLess(memory.score("CONTRADICTS:A->B"),0.7)
        self.assertLess(memory.score("CONTRADICTS:B->A"),0.7)
        self.assertEqual(receipt.hysteresis_boost_on_bad_path,0)

    def test_unresolved_does_not_change_unrelated_memory(self):
        memory=lk.RouteMemory({"SUPPORTS:X->Y":0.42})
        receipt=lk.Receipt()
        d=lk.evaluate([e("X","Y","SUPPORTS")])
        lk.apply_memory(d,memory,receipt)
        self.assertEqual(d.status, lk.UNRESOLVED)
        self.assertEqual(memory.score("SUPPORTS:X->Y"),0.42)

    def test_corpus_passes(self):
        corpus=json.loads(json.dumps({"schema":"owatch-logic-kernel-corpus-v1","poison_probe_key":"SUPPORTS:X->Y","initial_route_memory":{"CONTRADICTS:A->B":0.6,"CONTRADICTS:B->A":0.6,"SUPPORTS:A->B":0.1,"SUPPORTS:B->C":0.1,"SUPPORTS:C->A":0.1,"SUPPORTS:X->Y":0.42},"cases":[{"name":"supports_transitivity","edges":[{"source":"A","target":"B","kind":"SUPPORTS","reference":"ref-A-B","intention":"test transitivity","consequence":"derived proposal only"},{"source":"B","target":"C","kind":"SUPPORTS","reference":"ref-B-C","intention":"test transitivity","consequence":"derived proposal only"}],"expect_status":"DERIVED","expect_proposal":{"source":"A","target":"C","kind":"SUPPORTS"}},{"name":"contradiction_propagation","edges":[{"source":"A","target":"B","kind":"CONTRADICTS","reference":"ref-A-B","intention":"test propagation","consequence":"derived proposal only"},{"source":"C","target":"A","kind":"SUPPORTS","reference":"ref-C-A","intention":"test propagation","consequence":"derived proposal only"}],"expect_status":"DERIVED","expect_proposal":{"source":"C","target":"B","kind":"CONTRADICTS"}},{"name":"missing_metadata_holds","edges":[{"source":"M","target":"N","kind":"SUPPORTS","reference":"","intention":"test hold","consequence":"no proposal"}],"expect_status":"HOLD"},{"name":"self_contradiction_holds","edges":[{"source":"Q","target":"Q","kind":"CONTRADICTS","reference":"ref-Q-Q","intention":"test self loop","consequence":"terminate"}],"expect_status":"HOLD"},{"name":"planted_two_node_contradiction_loop","edges":[{"source":"A","target":"B","kind":"CONTRADICTS","reference":"ref-A-B","intention":"plant bad loop","consequence":"terminate"},{"source":"B","target":"A","kind":"CONTRADICTS","reference":"ref-B-A","intention":"plant bad loop","consequence":"terminate"}],"expect_status":"HOLD"},{"name":"unrelated_query_remains_unresolved_not_poisoned","edges":[{"source":"X","target":"Y","kind":"SUPPORTS","reference":"ref-X-Y","intention":"unrelated probe","consequence":"no derivation"}],"expect_status":"UNRESOLVED"}]}))
        result=lk.run_corpus(corpus)
        self.assertTrue(result["passed"])
        self.assertEqual(result["receipt"]["wrong_derivations"],0)
        self.assertEqual(result["receipt"]["hysteresis_boost_on_bad_path"],0)
        self.assertTrue(result["checks"]["unrelated_route_not_poisoned"])
        self.assertTrue(result["checks"]["at_least_one_terminated_loop"])

if __name__=="__main__":
    unittest.main()
