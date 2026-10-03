"""Deterministic tests for the Field/Void pair. No network, no keys.

python3 -m unittest software-zer0/field_void_pair/test_field_void_pair.py
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import threading
import unittest
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from pair_loop import FieldVoidPair, grounding_score, parse_void  # noqa: E402
from providers import Provider, ProviderError, available  # noqa: E402
from repo_lens import CANON_FILES, RepoLens  # noqa: E402
import server  # noqa: E402

LENS = RepoLens.build()


class Scripted(Provider):
    """Replays fixed replies; records what it was shown."""

    def __init__(self, replies, name="offline"):
        super().__init__(name=name, model="scripted")
        self.replies = list(replies)
        self.seen = []

    def complete(self, system, user):
        self.seen.append((system, user))
        r = self.replies.pop(0) if len(self.replies) > 1 else self.replies[0]
        if isinstance(r, Exception):
            raise r
        return r


GOOD_FIELD = "Step: reuse `simulations/zer0_first_cycle.py` per `AGENTS.md`.\nCITES: `AGENTS.md`"
ALLOW = "VERDICT: ALLOW\nREFERENCE: 0.9\nGOAL: 0.8\nNOTE: grounded"


def pair(field_replies, void_replies, turns=8):
    return FieldVoidPair(goal="test goal", field_ai=Scripted(field_replies),
                         void_ai=Scripted(void_replies), lens=LENS, max_turns=turns)


class LensTests(unittest.TestCase):
    def test_lens_covers_whole_repo_and_canon(self):
        self.assertGreater(len(LENS.files), 100)
        txt = LENS.render("field void zer0")
        for rel in CANON_FILES:
            self.assertIn("### " + rel, txt)
        self.assertIn(f"{len(LENS.files)} tracked files", txt)

    def test_citation_check_is_against_real_files(self):
        good, bad = LENS.cited_paths("see `AGENTS.md`, `nope/missing.py` and Ghost.md")
        self.assertEqual(good, ["AGENTS.md"])
        self.assertIn("nope/missing.py", bad)
        self.assertIn("Ghost.md", bad)

    def test_fvpair_repo_env_points_lens_at_repo(self):
        from repo_lens import find_repo_root
        os.environ["FVPAIR_REPO"] = str(LENS.root)
        try:
            self.assertEqual(find_repo_root(Path("/")), LENS.root.resolve())
        finally:
            del os.environ["FVPAIR_REPO"]
        with self.assertRaises(FileNotFoundError):
            find_repo_root(Path("/"))

    def test_grounding_score(self):
        self.assertEqual(grounding_score([], []), -1.0)
        self.assertEqual(grounding_score(["a"], []), 1.0)
        self.assertEqual(grounding_score(["a"], ["b"]), 0.0)


class VoidParseTests(unittest.TestCase):
    def test_parse_full(self):
        v = parse_void("VERDICT: correct\nREFERENCE: -0.3\nGOAL: 2\nNOTE: fix it")
        self.assertEqual((v["verdict"], v["reference"], v["goal"], v["note"]),
                         ("CORRECT", -0.3, 1.0, "fix it"))

    def test_malformed_reads_as_hold_not_pass(self):
        v = parse_void("Looks great to me!")
        self.assertEqual(v["verdict"], "HOLD")
        self.assertEqual((v["reference"], v["goal"]), (0.0, 0.0))
        self.assertFalse(v["parsed"])


class LoopTests(unittest.TestCase):
    def test_uses_zer0_harness_not_a_copy(self):
        p = pair([GOOD_FIELD], [ALLOW])
        self.assertEqual(Path(p.zer0.__file__).resolve(),
                         (LENS.root / "simulations" / "zer0_first_cycle.py").resolve())

    def test_both_sides_share_the_same_lens(self):
        p = pair([GOOD_FIELD], [ALLOW], turns=1)
        p.step()
        f_sys, v_sys = p.field_ai.seen[0][0], p.void_ai.seen[0][0]
        lens_part = f_sys[f_sys.index("=== ONE-WAVE REPO LENS"):]
        self.assertTrue(v_sys.endswith(lens_part))
        self.assertIn("FIELD PROPOSAL", p.void_ai.seen[0][1])

    def test_confirm_moves_reference_and_bar_rises(self):
        p = pair([GOOD_FIELD], [ALLOW], turns=3)
        r1 = p.step()
        self.assertEqual(r1["zer0"]["resolved"], "+")
        self.assertGreater(p.ref, 0.0)
        self.assertEqual(p.confirmed, GOOD_FIELD)
        refs = [r1["zer0"]["ref_out"]] + [p.step()["zer0"]["ref_out"] for _ in range(2)]
        self.assertTrue(all(-1.0 <= r <= 1.0 for r in refs))
        self.assertEqual(p.stop, "HARD_STOP")

    def test_ungrounded_denials_hit_three_strikes(self):
        bad_field = "Trust me, it works. CITES: `made/up.py`"
        deny = "VERDICT: OVERRIDE\nREFERENCE: -0.9\nGOAL: -0.5\nNOTE: no such file"
        p = pair([bad_field], [deny], turns=10)
        p.run()
        self.assertEqual(p.stop, "THREE_STRIKES")
        self.assertEqual(p.turn, 3)
        self.assertEqual(p.confirmed, "")
        self.assertTrue(all(r["zer0"]["resolved"] == "-" for r in p.history))
        self.assertIn("no such file", p.field_ai.seen[1][1])  # override fed back

    def test_disagreement_holds_and_settles(self):
        # X grounded (+), Y denied (-), Z neutral (0): split vote -> HOLD
        split = "VERDICT: OVERRIDE\nREFERENCE: -0.9\nGOAL: 0.0\nNOTE: split"
        p = pair([GOOD_FIELD], [split], turns=10)
        p.run()
        self.assertEqual(p.stop, "SETTLED")
        self.assertEqual(p.ref, 0.0)
        self.assertTrue(all(r["zer0"]["resolved"] == "0" for r in p.history))

    def test_escalate_stops(self):
        p = pair([GOOD_FIELD], ["VERDICT: ESCALATE\nREFERENCE: 0\nGOAL: 0\nNOTE: help"])
        p.run()
        self.assertEqual(p.stop, "ESCALATE")
        self.assertEqual(p.turn, 1)

    def test_provider_error_is_reported_not_hidden(self):
        p = pair([ProviderError("boom")], [ALLOW])
        p.run()
        self.assertEqual(p.stop, "PROVIDER_ERROR")
        self.assertIn("boom", p.history[-1]["error"])

    def test_offline_pair_runs_and_writes_ledger(self):
        p = FieldVoidPair(goal="offline run", field_ai=Provider("offline", "x"),
                          void_ai=Provider("offline", "x"), lens=LENS, max_turns=4)
        p.run()
        self.assertIn(p.stop, ("SETTLED", "HARD_STOP"))
        with tempfile.TemporaryDirectory() as d:
            out = p.write_ledger(Path(d) / "run.jsonl")
            rows = [json.loads(line) for line in out.read_text().splitlines()]
        self.assertEqual(rows[-1]["label"], "SOFTWARE_ONLY")
        self.assertEqual(len(rows), p.turn + 1)


class BundleTests(unittest.TestCase):
    """No checkout on disk: the lens and Zer0 come from the compressed snapshot."""

    @classmethod
    def setUpClass(cls):
        from repo_lens import write_bundle
        cls.tmp = tempfile.TemporaryDirectory()
        cls.path = write_bundle(LENS.root, Path(cls.tmp.name) / "lens_bundle.tar.xz")
        cls.lens = RepoLens.build(cls.path)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_bundle_is_small_and_matches_checkout(self):
        self.assertLess(self.path.stat().st_size, 15_000_000)
        self.assertTrue(self.lens.bundle)
        self.assertEqual(self.lens.files, LENS.files)
        self.assertEqual(self.lens.render("field void zer0"), LENS.render("field void zer0"))
        self.assertTrue(self.lens.snapshot()["root"].startswith("bundle:"))

    def test_loop_runs_from_bundle_with_real_zer0_source(self):
        p = FieldVoidPair(goal="bundle run", field_ai=Scripted([GOOD_FIELD]),
                          void_ai=Scripted([ALLOW]), lens=self.lens, max_turns=2)
        self.assertIn("repo/simulations/zer0_first_cycle.py", p.zer0.__file__)
        p.run()
        self.assertEqual(p.stop, "HARD_STOP")
        self.assertGreater(p.ref, 0.0)

    def test_find_source_falls_back_to_bundle(self):
        from repo_lens import find_source
        os.environ["FVPAIR_BUNDLE"] = str(self.path)
        try:
            # Searching from / finds no checkout, so the bundle is used.
            import repo_lens
            orig = repo_lens.find_repo_root
            repo_lens.find_repo_root = lambda start=None: orig(Path("/"))
            try:
                self.assertEqual(find_source(), self.path.resolve())
            finally:
                repo_lens.find_repo_root = orig
        finally:
            del os.environ["FVPAIR_BUNDLE"]


class KeyHygieneTests(unittest.TestCase):
    def test_keys_never_leave_the_process(self):
        os.environ["DEEPSEEK_API_KEY"] = "sk-secret-test-value"
        try:
            blob = json.dumps(available())
            self.assertNotIn("sk-secret-test-value", blob)
            self.assertIn('"ready": true', blob)
        finally:
            del os.environ["DEEPSEEK_API_KEY"]


class ServerTests(unittest.TestCase):
    def test_app_start_step_ledger(self):
        httpd = server.serve("127.0.0.1", 0, LENS)
        th = threading.Thread(target=httpd.serve_forever, daemon=True)
        th.start()
        base = f"http://127.0.0.1:{httpd.server_address[1]}"

        def call(path, body=None):
            data = json.dumps(body).encode() if body is not None else None
            req = urllib.request.Request(base + path, data=data,
                                         headers={"content-type": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as r:
                raw = r.read().decode()
                return json.loads(raw) if "json" in r.headers["content-type"] and "ndjson" not in r.headers["content-type"] else raw

        try:
            self.assertIn("Field", call("/"))
            self.assertTrue(any(p["name"] == "offline" for p in call("/api/providers")["providers"]))
            s = call("/api/start", {"goal": "app test", "max_turns": 3,
                                    "field": {"provider": "offline"}, "void": {"provider": "offline"}})
            summary = s["summary"]
            while not summary["stop"]:
                out = call("/api/step", {"id": s["id"]})
                summary = out["summary"]
                self.assertIn("zer0", out["record"])
            ledger = call(f"/api/ledger?id={s['id']}")
            self.assertIn("SOFTWARE_ONLY", ledger)
            with self.assertRaises(urllib.error.HTTPError):
                call("/api/start", {"goal": ""})
        finally:
            httpd.shutdown()
            httpd.server_close()


if __name__ == "__main__":
    unittest.main()
