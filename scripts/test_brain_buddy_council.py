"""Deterministic tests for Brain Buddy lead mode (Rule 50 core).

These tests replace the provider call in-process only. They prove the
orchestration logic; they do not prove a live Gemini/DeepSeek return path.
Run: python3 -m unittest scripts/test_brain_buddy_council.py
"""
from __future__ import annotations

from pathlib import Path
import re
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import brain_buddy_council as bb  # noqa: E402

RID = re.compile(r"^RETURN_ID: (\S+)$", re.MULTILINE)


def ok(prompt: str, text: str, echo: bool = True) -> dict:
    tag = f"\nRETURN_ID: {RID.findall(prompt)[-1]}" if echo else ""
    return {"ok": True, "exit_code": 0, "elapsed_s": 0.1, "answer": text + tag, "stderr": "", "timed_out": False}


def fail(stderr: str, exit_code: int = 1, timed_out: bool = False) -> dict:
    return {"ok": False, "exit_code": exit_code, "elapsed_s": 0.1, "answer": "", "stderr": stderr, "timed_out": timed_out}


class Script:
    """Scripted provider: seat -> list of callables(prompt) -> result."""

    def __init__(self, **plan):
        self.plan = {k: list(v) for k, v in plan.items()}
        self.calls: list[tuple[str, str]] = []

    def __call__(self, seat: str, prompt: str) -> dict:
        self.calls.append((seat, prompt))
        return self.plan[seat].pop(0)(prompt)


def run(script: Script, lead: str = "gemini", **kw) -> dict:
    return bb.run_lead(
        "What does node X claim?",
        lead,
        script,
        request_id="bb-test",
        baseline="deadbeef",
        transport_timeout=240,
        **kw,
    )


class LeadModeTests(unittest.TestCase):
    def test_challenge_then_refinement_then_no_objection(self):
        s = Script(
            gemini=[
                lambda p: ok(p, "Answer v1"),
                lambda p: ok(p, "Answer v2, corrected per DeepSeek"),
            ],
            deepseek=[
                lambda p: ok(p, "OBJECTION: misreads Nodes/X.md\nVERDICT: OBJECTION"),
                lambda p: ok(p, "Resolved.\nVERDICT: NO MATERIAL OBJECTION"),
            ],
        )
        r = run(s)
        self.assertEqual(r["outcome"], "NO_ACTIVE_OBJECTION")
        self.assertEqual(r["final_answer"], "Answer v2, corrected per DeepSeek")
        self.assertEqual(r["refinements"], 1)
        self.assertEqual(r["loops"], 2)
        self.assertEqual([c[0] for c in s.calls], ["gemini", "deepseek", "gemini", "deepseek"])
        self.assertTrue(all(t["return_verified"] for t in r["turns"]))
        self.assertEqual(r["seats"]["gemini"]["role"], "lead")
        # The refinement prompt carries the reviewer's objection back to the lead.
        self.assertIn("misreads Nodes/X.md", s.calls[2][1])
        # Every prompt carries the request and baseline identity.
        self.assertTrue(all("REQUEST_ID: bb-test" in p and "BASELINE: deadbeef" in p for _, p in s.calls))

    def test_any_seat_can_lead(self):
        s = Script(
            deepseek=[lambda p: ok(p, "DeepSeek leads")],
            gemini=[lambda p: ok(p, "VERDICT: NO MATERIAL OBJECTION")],
        )
        r = run(s, lead="deepseek")
        self.assertEqual(r["lead"], "deepseek")
        self.assertEqual(r["seats"]["gemini"]["role"], "reviewer")
        self.assertEqual(r["outcome"], "NO_ACTIVE_OBJECTION")
        self.assertIn("You are Deepseek, the lead seat", s.calls[0][1])

    def test_no_fixed_round_count(self):
        n = 6
        gem = [lambda p: ok(p, "v0")] + [lambda p, i=i: ok(p, f"v{i}") for i in range(1, n + 1)]
        ds = [lambda p, i=i: ok(p, f"OBJECTION: point {i}\nVERDICT: OBJECTION") for i in range(n)]
        ds.append(lambda p: ok(p, "VERDICT: NO MATERIAL OBJECTION"))
        r = run(Script(gemini=gem, deepseek=ds))
        self.assertEqual(r["outcome"], "NO_ACTIVE_OBJECTION")
        self.assertEqual(r["refinements"], n)

    def test_unclear_verdict_is_not_agreement(self):
        s = Script(
            gemini=[lambda p: ok(p, "v1"), lambda p: ok(p, "v2")],
            deepseek=[lambda p: ok(p, "Looks fine I guess"), lambda p: ok(p, "VERDICT: NO MATERIAL OBJECTION")],
        )
        r = run(s)
        self.assertEqual(r["refinements"], 1)
        self.assertEqual(r["outcome"], "NO_ACTIVE_OBJECTION")

    def test_repeated_objection_stalls_and_stays_visible(self):
        obj = "OBJECTION: still wrong about Nodes/X.md\nVERDICT: OBJECTION"
        s = Script(
            gemini=[lambda p: ok(p, "v1"), lambda p: ok(p, "v2")],
            deepseek=[lambda p: ok(p, obj), lambda p: ok(p, obj)],
        )
        r = run(s)
        self.assertEqual(r["outcome"], "STALLED_UNRESOLVED")
        self.assertIn("deepseek", r["open_objections"])

    def test_timeout_marks_out_to_lunch_not_completion(self):
        s = Script(
            gemini=[lambda p: ok(p, "v1")],
            deepseek=[lambda p: fail("Timed out", 124, timed_out=True)],
        )
        r = run(s)
        self.assertEqual(r["seats"]["deepseek"]["state"], bb.OUT_TO_LUNCH)
        self.assertEqual(r["outcome"], "NO_REVIEWERS_AVAILABLE")
        self.assertNotEqual(r["outcome"], "NO_ACTIVE_OBJECTION")

    def test_lead_unavailable(self):
        r = run(Script(gemini=[lambda p: fail("HTTP 429 from relay: quota")]))
        self.assertEqual(r["outcome"], "LEAD_UNAVAILABLE")
        self.assertEqual(r["seats"]["gemini"]["state"], bb.OUT_TO_LUNCH)
        self.assertEqual(r["final_answer"], "")

    def test_missing_return_id_is_invalid_return(self):
        s = Script(
            gemini=[lambda p: ok(p, "v1")],
            deepseek=[lambda p: ok(p, "VERDICT: NO MATERIAL OBJECTION", echo=False)],
        )
        r = run(s)
        self.assertEqual(r["seats"]["deepseek"]["state"], bb.INVALID_RETURN)
        self.assertEqual(r["outcome"], "NO_REVIEWERS_AVAILABLE")
        self.assertNotIn("text", r["turns"][-1])

    def test_stale_return_id_is_invalid_return(self):
        s = Script(
            gemini=[lambda p: ok(p, "v1")],
            deepseek=[lambda p: ok(p, "VERDICT: NO MATERIAL OBJECTION\nRETURN_ID: bb-test-01-gemini-000000", echo=False)],
        )
        r = run(s)
        self.assertEqual(r["seats"]["deepseek"]["state"], bb.INVALID_RETURN)

    def test_operator_limit_is_unresolved_not_agreement(self):
        s = Script(
            gemini=[lambda p: ok(p, "v1")],
            deepseek=[lambda p: ok(p, "OBJECTION: x\nVERDICT: OBJECTION")],
        )
        r = run(s, max_loops=1)
        self.assertEqual(r["outcome"], "OPERATOR_LIMIT_UNRESOLVED")
        self.assertIn("deepseek", r["open_objections"])

    def test_user_stop(self):
        s = Script(
            gemini=[lambda p: ok(p, "v1")],
            deepseek=[lambda p: ok(p, "OBJECTION: x\nVERDICT: OBJECTION")],
        )
        r = run(s, user_turn=lambda n: "/stop")
        self.assertEqual(r["outcome"], "USER_STOPPED")

    def test_unknown_lead_rejected(self):
        with self.assertRaises(bb.CouncilError):
            run(Script(), lead="chatgpt")


class ClassifyFailureTests(unittest.TestCase):
    def state(self, stderr: str) -> str:
        return bb.classify_failure(fail(stderr), 240)[0]

    def test_states(self):
        self.assertEqual(self.state("RuntimeError: HTTP 403 from http://x: client not allowed"), bb.AUTH_FAILURE)
        self.assertEqual(self.state("urllib.error.HTTPError: HTTP Error 401: Unauthorized"), bb.AUTH_FAILURE)
        self.assertEqual(self.state("RuntimeError: HTTP 429 from http://x: rate limit"), bb.OUT_TO_LUNCH)
        self.assertEqual(self.state("RuntimeError: Unable to reach http://x: [Errno 111] Connection refused"), bb.OFFLINE)
        self.assertEqual(self.state("urllib.error.URLError: <urlopen error [Errno 113] No route to host>"), bb.OFFLINE)
        self.assertEqual(self.state("RuntimeError: Gemini relay response missing choices"), bb.INVALID_RETURN)
        self.assertEqual(self.state("RuntimeError: Hive Pipe token not found. Run create_client_token.sh"), bb.AUTH_FAILURE)
        self.assertEqual(self.state("something else broke"), bb.OUT_TO_LUNCH)

    def test_timeout(self):
        state, reason = bb.classify_failure(fail("", 124, timed_out=True), 240)
        self.assertEqual(state, bb.OUT_TO_LUNCH)
        self.assertIn("no transport response within 240s", reason)


if __name__ == "__main__":
    unittest.main()
