import unittest

from One_Wave_Bench.engine.claim_loop import (
    FIELD,
    VOID,
    STEPS,
    ClaimDatabase,
    ClaimLoopError,
)


def run_steps(db, loop_id, prefix):
    for step in STEPS:
        db.record_step(loop_id, step, f"{prefix}: {step}")


class ClaimLoopTests(unittest.TestCase):
    def setUp(self):
        self.db = ClaimDatabase()
        self.claim = self.db.create_claim(
            "This configuration produces a persistent mode.", "tested boundary B0"
        )
        self.db.add_source(self.claim, "configuration spec", "sims/config_b0.json")
        self.loop = self.db.open_loop(self.claim, "Does the mode persist?", repo_commit="abc123")

    def field_pass(self):
        run_steps(self.db, self.loop, "field")
        self.db.add_evidence(self.loop, "persistence over t=0..100", "run-001")
        return self.db.handoff(self.loop, repo_commit="abc123")

    def test_only_two_machine_states(self):
        self.assertEqual(self.db.machine_record(self.loop).active_state, FIELD)
        self.field_pass()
        self.assertEqual(self.db.machine_record(self.loop).active_state, VOID)

    def test_machine_record_has_spec_fields(self):
        record = self.db.machine_record(self.loop).as_dict()
        self.assertEqual(
            set(record),
            {"active_state", "claim_id", "claim_version", "reference_version",
             "parent_loop_id", "current_step", "candidate", "evidence_ids",
             "contradiction_ids", "receipt_id"},
        )
        self.assertEqual(record["current_step"], 1)
        self.assertEqual(record["claim_version"], 1)

    def test_steps_are_progress_inside_state_and_ordered(self):
        with self.assertRaises(ClaimLoopError):
            self.db.record_step(self.loop, "move", "skip ahead")
        self.db.record_step(self.loop, "reference", "read claim v1")
        self.assertEqual(self.db.machine_record(self.loop).current_step, 2)
        self.assertEqual(self.db.machine_record(self.loop).active_state, FIELD)
        with self.assertRaises(ClaimLoopError):
            self.db.record_step(self.loop, "reference", "again")

    def test_field_holds_without_evidence(self):
        run_steps(self.db, self.loop, "field")
        result = self.db.handoff(self.loop)
        self.assertFalse(result.switched)
        self.assertEqual(result.to_state, FIELD)
        self.assertIn("no evidence recorded in this pass", result.blockers)
        self.assertEqual(self.db.machine_record(self.loop).active_state, FIELD)

    def test_field_holds_with_incomplete_receipt(self):
        self.db.record_step(self.loop, "reference", "read")
        self.db.add_evidence(self.loop, "x", "run-001")
        result = self.db.handoff(self.loop)
        self.assertFalse(result.switched)
        self.assertTrue(any(b.startswith("receipt incomplete") for b in result.blockers))

    def test_field_to_void_saves_receipt(self):
        result = self.field_pass()
        self.assertTrue(result.switched)
        receipt = self.db.receipt(result.receipt_id)
        self.assertEqual(receipt["state"], FIELD)
        self.assertEqual(receipt["repo_commit"], "abc123")
        self.assertEqual(set(receipt["body"]["steps"]), set(STEPS))
        record = self.db.machine_record(self.loop)
        self.assertEqual(record.current_step, 1)
        self.assertEqual(record.receipt_id, result.receipt_id)
        self.assertEqual(record.evidence_ids, [])

    def test_void_reads_field_receipt(self):
        result = self.field_pass()
        packet = self.db.reference_packet(self.loop)
        self.assertEqual(packet["incoming_receipt"]["receipt_id"], result.receipt_id)
        self.assertEqual(packet["claim"]["version"], 1)
        self.assertEqual(packet["evidence"][0]["kind"], "source")

    def test_void_needs_correction_or_counterproposal_and_next_question(self):
        self.field_pass()
        run_steps(self.db, self.loop, "void")
        self.db.add_evidence(self.loop, "boundary B1 run", "run-002")
        result = self.db.handoff(self.loop)
        self.assertFalse(result.switched)
        self.assertIn("no counterproposal or correction saved", result.blockers)
        self.assertIn("no next bounded question saved", result.blockers)
        self.db.propose_counter(self.loop, "persistence may be boundary-specific")
        self.db.set_next_question(self.loop, "Does the mode depend on the boundary?")
        self.assertTrue(self.db.handoff(self.loop).switched)

    def test_field_cannot_counterpropose(self):
        with self.assertRaises(ClaimLoopError):
            self.db.propose_counter(self.loop, "x")

    def test_explicit_hold_retains_state_until_released(self):
        run_steps(self.db, self.loop, "field")
        self.db.add_evidence(self.loop, "x", "run-001")
        self.db.hold(self.loop, "evidence: test still running")
        result = self.db.handoff(self.loop)
        self.assertFalse(result.switched)
        self.assertIn("evidence: test still running", result.blockers)
        self.assertEqual(self.db.machine_record(self.loop).active_state, FIELD)
        self.db.release(self.loop, "evidence: test still running")
        self.assertTrue(self.db.handoff(self.loop).switched)

    def test_changed_repo_commit_holds(self):
        run_steps(self.db, self.loop, "field")
        self.db.add_evidence(self.loop, "x", "run-001")
        result = self.db.handoff(self.loop, repo_commit="def456")
        self.assertFalse(result.switched)
        self.assertTrue(any("repository commit changed" in b for b in result.blockers))
        self.db.resync(self.loop, repo_commit="def456")
        self.assertEqual(self.db.machine_record(self.loop).current_step, 1)
        run_steps(self.db, self.loop, "field")
        self.assertTrue(self.db.handoff(self.loop, repo_commit="def456").switched)

    def test_stale_claim_version_holds(self):
        other = self.db.open_loop(self.claim, "parallel check")
        self.db.submit_correction(other, "Persistent only at B0.", "B0")
        run_steps(self.db, self.loop, "field")
        self.db.add_evidence(self.loop, "x", "run-001")
        result = self.db.handoff(self.loop)
        self.assertFalse(result.switched)
        self.assertTrue(any("newer version" in b for b in result.blockers))
        with self.assertRaises(ClaimLoopError):
            self.db.submit_correction(self.loop, "y", "z")
        self.db.resync(self.loop)
        self.assertEqual(self.db.machine_record(self.loop).claim_version, 2)

    def test_correction_creates_new_version_and_keeps_old(self):
        self.field_pass()
        version = self.db.submit_correction(
            self.loop, "Persistence is supported only for the tested boundary.", "B0 only"
        )
        self.assertEqual(version, 2)
        versions = self.db.claim_versions(self.claim)
        self.assertEqual([v["version"] for v in versions], [1, 2])
        self.assertEqual(versions[0]["text"], "This configuration produces a persistent mode.")
        self.assertEqual(versions[1]["created_by"], VOID)
        self.assertEqual(versions[1]["parent_version"], 1)
        self.assertEqual(versions[1]["status"], "proposed")

    def test_claim_status_is_separate_from_machine_state(self):
        self.db.set_status(self.loop, "supported")
        self.assertEqual(self.db.claim(self.claim)["status"], "supported")
        self.assertEqual(self.db.machine_record(self.loop).active_state, FIELD)
        with self.assertRaises(ClaimLoopError):
            self.db.set_status(self.loop, FIELD)

    def test_contradictions_tracked(self):
        x = self.db.add_contradiction(self.loop, "decay seen at larger boundary")
        self.assertEqual(self.db.machine_record(self.loop).contradiction_ids, [x])
        self.assertEqual(len(self.db.open_contradictions(self.claim)), 1)
        self.db.resolve_contradiction(self.loop, x)
        self.assertEqual(self.db.open_contradictions(self.claim), [])

    def test_child_loop_returns_evidence_upward(self):
        child = self.db.open_child(
            self.loop, "Compute decay rate at B1", "Decay rate at B1 is 0.02/t", "B1"
        )
        record = self.db.machine_record(child)
        self.assertEqual(record.parent_loop_id, self.loop)
        self.assertNotEqual(record.claim_id, self.claim)
        self.assertEqual(self.db.children(self.loop), [child])
        with self.assertRaises(ClaimLoopError):
            self.db.return_upward(child)
        run_steps(self.db, child, "child field")
        self.db.add_evidence(child, "fit result", "run-child-1")
        child_receipt = self.db.handoff(child).receipt_id
        evidence_id = self.db.return_upward(child)
        self.assertIn(evidence_id, self.db.machine_record(self.loop).evidence_ids)
        ev = self.db.evidence(evidence_id)
        self.assertEqual(ev["kind"], "child_receipt")
        self.assertEqual(ev["source"], child_receipt)
        # The child keeps its own receipts.
        self.assertEqual(len(self.db.receipts(child)), 1)
        self.assertEqual(self.db.receipts(self.loop), [])

    def test_persistent_mode_example(self):
        # FIELD: run a specified simulation.
        r1 = self.field_pass()
        self.assertTrue(r1.switched)

        # VOID: repeat with changed boundary; correct the claim.
        db, loop = self.db, self.loop
        db.record_step(loop, "reference", "claim v1, sources, Field receipt")
        db.record_step(loop, "choice", "does persistence survive a larger boundary?")
        db.record_step(loop, "move", "repeat with changed boundary conditions")
        db.record_step(loop, "views_up", "persistence fails at B1")
        db.record_step(loop, "actions_down", "none")
        db.record_step(loop, "state_scale", "persistence supported at B0 only")
        db.add_evidence(loop, "decay at B1", "run-002")
        db.submit_correction(loop, "Persistence is supported only for the tested boundary.", "B0")
        db.set_next_question(loop, "Does the mode depend on that boundary?")
        r2 = db.handoff(loop)
        self.assertTrue(r2.switched)
        self.assertEqual(db.receipt(r2.receipt_id)["claim_version"], 2)

        # FIELD: reads the corrected claim and both receipts.
        packet = db.reference_packet(loop)
        self.assertEqual(packet["machine"]["active_state"], FIELD)
        self.assertEqual(packet["claim"]["version"], 2)
        self.assertEqual(packet["incoming_receipt"]["receipt_id"], r2.receipt_id)
        self.assertEqual(
            packet["incoming_receipt"]["body"]["next_question"],
            "Does the mode depend on that boundary?",
        )
        self.assertEqual([r["receipt_id"] for r in db.receipts(loop)],
                         [r1.receipt_id, r2.receipt_id])

    def test_persists_across_reopen(self):
        import os
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "claims.db")
            db = ClaimDatabase(path)
            claim = db.create_claim("c", "s")
            loop = db.open_loop(claim, "q")
            db.record_step(loop, "reference", "r")
            db.conn.close()
            again = ClaimDatabase(path)
            self.assertEqual(again.machine_record(loop).current_step, 2)
            again.conn.close()


if __name__ == "__main__":
    unittest.main()
