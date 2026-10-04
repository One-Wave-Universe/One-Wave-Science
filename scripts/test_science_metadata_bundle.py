import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from science_metadata_bundle import endpoints, snapshot, summary, verify_bundle


class MetadataTests(unittest.TestCase):
    def test_exact_bytes_pagination_and_round_trip(self):
        documents = {"https://gwosc.org/start": b'{ "next": "https://gwosc.org/end", "results": [{"detector":"H1"}] }',
                     "https://gwosc.org/end": b'{"next":null,"results":[{"detector":"L1"}]}'}
        def fetch(url, hosts, timeout):
            raw = documents[url]
            return raw, json.loads(raw), {"final_url": url, "http_status": 200}
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            result = snapshot("gwosc", "https://gwosc.org/start", p, {"gwosc.org"}, fetcher=fetch)
            self.assertEqual(result["status"], "complete")
            self.assertEqual(len(result["pages"]), 2)
            for page in result["pages"]:
                self.assertEqual((p / page["raw_body_file"]).read_bytes(), documents[page["requested_url"]])
            receipt = {"requests": [result], "all_complete": True}
            (p / "receipt.json").write_text(json.dumps(receipt))
            self.assertTrue(verify_bundle(p))
            (p / result["pages"][0]["raw_body_file"]).write_bytes(b'{}')
            with self.assertRaises(ValueError): verify_bundle(p)

    def test_page_cap_never_claims_complete(self):
        def fetch(url, hosts, timeout):
            raw = b'{"results": [], "next": "https://gwosc.org/next"}'
            return raw, json.loads(raw), {}
        with tempfile.TemporaryDirectory() as d:
            r = snapshot("gwosc", "https://gwosc.org/start", Path(d), {"gwosc.org"}, max_pages=1, fetcher=fetch)
            self.assertEqual(r["status"], "incomplete")

    def test_missing_units_remain_unknown(self):
        r = summary("cern-open-data", {"id": "5501", "metadata": {"title": "Example"}})
        self.assertIsNone(r["units"])
        self.assertIsNone(r["license"])
        with self.assertRaises(ValueError): summary("cern-open-data", {"metadata": {}})
        with self.assertRaises(ValueError): summary("gwosc", {"unrecognized": True})

    def test_provider_count_mismatch_is_incomplete(self):
        def fetch(*args):
            raw = b'{"results": [], "results_count": 5, "next": null}'
            return raw, json.loads(raw), {}
        with tempfile.TemporaryDirectory() as d:
            r = snapshot("gwosc", "https://gwosc.org/start", Path(d), {"gwosc.org"}, fetcher=fetch)
            self.assertEqual(r["status"], "incomplete")
            self.assertEqual(r["reason"], "provider count mismatch")

    def test_endpoint_failure_preserves_failure(self):
        def fetch(*args): raise TimeoutError("provider timeout")
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(TimeoutError):
                snapshot("gwosc", "https://gwosc.org/start", Path(d), {"gwosc.org"}, fetcher=fetch)

    def test_ids_do_not_inject_query_parameters(self):
        with self.assertRaises(ValueError): endpoints("5501?x=y", "GW150914")
        with self.assertRaises(ValueError): endpoints("5501", "GW150914/other")


if __name__ == "__main__": unittest.main()
