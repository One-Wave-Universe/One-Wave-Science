"""Scientific-software controls for the unchanged static G-767 statistic."""
import copy
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

P = Path(__file__).with_name("adapter.py")
spec = importlib.util.spec_from_file_location("spectral_adapter_under_test", P)
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)


class SpectralAdapterTests(unittest.TestCase):
    def config(self, scales=None, **changes):
        config = adapter._default()
        config["trials"] = 24
        if scales is not None:
            config["records"] = [{"scale": x} for x in scales]
        config.update(changes)
        return config

    def test_exact_engine_equivalence_including_null(self):
        c = self.config([1.25, 2.3, 3.75, 9.4], seed=15)
        receipt = adapter.run(c)
        xs = [(r["scale"], r.get("width")) for r in c["records"]]
        real, mean, p = adapter.ENGINE.null_test(xs, c["x0"], c["trials"], c["seed"])
        a = receipt["final"]["state"]["analysis"]
        self.assertEqual(a["phase"], adapter.ENGINE.phases(xs, c["x0"]))
        self.assertEqual((a["coherence"], a["null_mean_coherence"], a["empirical_upper_tail_p"]), (real, mean, p))
        self.assertEqual(receipt["null_model"]["inference"], "diagnostic-only")

    def test_exact_octave_positive(self):
        a = adapter.step(adapter.initialize(self.config()))["analysis"]
        self.assertEqual(a["phase"], [0.0] * 5)
        self.assertEqual(a["octave"], list(range(5)))
        self.assertEqual(a["coherence"], 1.0)

    def test_quarter_offsets_zero_resultant(self):
        a = adapter.step(adapter.initialize(self.config([2**(n/4) for n in range(4)])))["analysis"]
        self.assertLess(a["coherence"], 1e-12)
        self.assertEqual(a["empirical_upper_tail_p"], 1.0)

    def test_degenerate_range_has_no_false_significance(self):
        a = adapter.step(adapter.initialize(self.config([2, 2, 2])))["analysis"]
        self.assertEqual(a["coherence"], 1.0)
        self.assertEqual(a["null_mean_coherence"], 1.0)
        self.assertEqual(a["empirical_upper_tail_p"], 1.0)

    def test_scale_and_reference_rescaling_preserves_phase_coherence(self):
        first = adapter.step(adapter.initialize(self.config([1.25, 3.5, 8])))
        second = adapter.step(adapter.initialize(self.config([10, 28, 64], x0=8)))
        for key in ("log2_ratio", "octave", "phase", "coherence"):
            self.assertEqual(first["analysis"][key], second["analysis"][key])
        # Floating-point null sampling is deliberately not replaced to enforce invariance.

    def test_labels_width_uncertainty_are_retained_metadata_only(self):
        c = self.config()
        baseline = adapter.run(c)
        for i, row in enumerate(c["records"]):
            row.update(label="source label " + str(i), width=0.1, uncertainty=0.2, unit="dimensionless")
        receipt = adapter.run(c)
        self.assertEqual(receipt["measurements"], baseline["measurements"])
        self.assertEqual(receipt["final"]["state"]["configuration"]["records"], c["records"])
        self.assertNotEqual(receipt["final"]["provenance"]["normalized_input_sha256"], baseline["final"]["provenance"]["normalized_input_sha256"])

    def test_seeded_receipts_reproduce(self):
        c = self.config([1.3, 2.2, 5.1, 8.7])
        self.assertEqual(adapter.run(c), adapter.run(copy.deepcopy(c)))
        self.assertNotEqual(adapter.run(c)["measurements"]["null_mean_coherence"], adapter.run({**c, "seed": 999})["measurements"]["null_mean_coherence"])

    def test_snapshot_roundtrip_and_continuation(self):
        initial = adapter.initialize(self.config())
        initial_copy = copy.deepcopy(initial)
        restored = adapter.restore(json.loads(json.dumps(adapter.serialize(initial))))
        self.assertEqual(adapter.step(initial), adapter.step(restored))
        self.assertEqual(initial, initial_copy)
        final = adapter.step(restored)
        self.assertEqual(adapter.restore(adapter.serialize(final)), final)
        restored["configuration"]["records"][0]["scale"] = 7
        self.assertEqual(initial, initial_copy)

    def test_restore_rejects_tampered_data_measurements_and_sources(self):
        snapshot = adapter.serialize(adapter.step(adapter.initialize(self.config())))
        mutations = [lambda s: s["state"]["analysis"].update(coherence=0.25),
                     lambda s: s["measurements"][0].update(value=999),
                     lambda s: s["provenance"]["source_sha256"].update({adapter.ENGINE_PATH: "0"*64}),
                     lambda s: s["state"]["configuration"].update(trials=10000000),
                     lambda s: s["provenance"].update(python_version="unknown")]
        for mutate in mutations:
            s = copy.deepcopy(snapshot)
            mutate(s)
            with self.assertRaises(ValueError):
                adapter.restore(s)

    def test_failed_step_preserves_state(self):
        initial = adapter.initialize(self.config())
        old = copy.deepcopy(initial)
        for kwargs in ({"dt": 0}, {"dt": 0.1}, {"inputs": {}}, {"inputs": []}):
            with self.assertRaises(ValueError):
                adapter.step(initial, **kwargs)
            self.assertEqual(initial, old)
        with self.assertRaises(ValueError):
            adapter.step(adapter.step(initial))

    def test_geometry_is_same_state_nonspatial_and_owned(self):
        state = adapter.step(adapter.initialize(self.config([1, 2**0.25, 2**0.5, 2**0.75])))
        g = adapter.geometry(state)
        self.assertFalse(g["physical_spatial_geometry"])
        points = g["points"]
        resultant = math.hypot(sum(p["unit_circle"][0] for p in points), sum(p["unit_circle"][1] for p in points))/len(points)
        self.assertAlmostEqual(resultant, adapter.measure(state)["coherence"], places=14)
        for i, point in enumerate(points):
            self.assertEqual(point["scatter"], [state["analysis"]["log2_ratio"][i], state["analysis"]["phase"][i]])
        g["points"][0]["scatter"][0] = 999
        self.assertNotEqual(adapter.geometry(state)["points"][0]["scatter"][0], 999)
        with self.assertRaises(ValueError):
            adapter.geometry(adapter.initialize(self.config()))

    def test_units_and_unknown_fields_refused(self):
        for changes in ({"reference_unit": "Hz"}, {"scale_unit": ""}, {"x0": True},
                        {"reference_policy": "optimized-on-evaluation"}, {"sample_rate": 4096}, {"frequency": 100}):
            with self.assertRaises(ValueError):
                adapter.initialize(self.config(**changes))
        c = self.config()
        c["records"][0]["unit"] = "GeV"
        with self.assertRaises(ValueError):
            adapter.initialize(c)
        # Caller may explicitly declare frequency scales, but this is not sampled time-series data.
        r = adapter.run(self.config(scale_unit="Hz", reference_unit="Hz"))
        self.assertIsNone(r["execution"]["sample_rate"])
        self.assertIsNone(r["execution"]["frequency"])

    def test_invalid_scales_and_reference_domain(self):
        for value in (0, -1, True, "1", None, math.inf, math.nan, 10**400):
            with self.subTest(value=str(value)[:20]), self.assertRaises(ValueError):
                adapter.initialize(self.config([value, 2, 3]))
        for c in (self.config([1e-300, 2e-300, 3e-300], x0=1e300),
                  self.config([1e300, 2e300, 3e300], x0=1e-300),
                  self.config([sys.float_info.max]*3)):
            with self.assertRaises(ValueError):
                adapter.initialize(c)

    def test_budget_and_integer_validation(self):
        for changes in ({"trials": 0}, {"trials": True}, {"trials": 2.5}, {"trials": 10001},
                        {"seed": True}, {"seed": -1}, {"seed": 2**32}, {"records": []},
                        {"records": [{"scale": 1}]*10001}, {"records": [{"scale": 1}]*100, "trials": 3000}):
            with self.assertRaises(ValueError):
                adapter.initialize(self.config(**changes))

    def test_metadata_validation_and_input_ownership(self):
        for key, value in (("width", -1), ("width", math.inf), ("uncertainty", True), ("label", {})):
            c = self.config()
            c["records"][0][key] = value
            with self.assertRaises(ValueError):
                adapter.initialize(c)
        c = self.config()
        state = adapter.initialize(c)
        c["records"][0]["scale"] = 100
        self.assertEqual(state["configuration"]["records"][0]["scale"], 1)

    def test_source_hashes_and_source_drift(self):
        for path, sha in adapter.references().items():
            self.assertEqual(sha, hashlib.sha256((adapter.ROOT / path).read_bytes()).hexdigest())
        with patch.object(adapter, "references", return_value={}):
            with self.assertRaisesRegex(ValueError, "Source changed"):
                adapter.run(self.config())
        with patch.object(adapter, "_IMPORT_ERROR", ValueError("unavailable")):
            with self.assertRaisesRegex(ValueError, "source loading failed"):
                adapter.initialize(self.config())

    def test_malformed_source_manifest_is_bounded_error(self):
        manifests = [[], None, {**adapter.manifest(), "adapter": None}]
        for key in ("state_schema", "entry_point"):
            m = adapter.manifest()
            del (m if key == "state_schema" else m["adapter"])[key]
            manifests.append(m)
        for value in (None, [], ""):
            m = adapter.manifest()
            m["state_schema"] = value
            manifests.append(m)
        for m in manifests:
            with self.subTest(manifest=m), patch.object(adapter, "manifest", return_value=m):
                with self.assertRaises(ValueError):
                    adapter.run(self.config())

    def test_receipt_replay_validation_and_forgery_refusal(self):
        r = adapter.run(self.config())
        self.assertEqual(adapter.validate(r)["scope"], "deterministic-software-replay-only")
        r["measurements"]["coherence"] = 0.123
        with self.assertRaises(ValueError):
            adapter.validate(r)

    def test_default_cli_is_explicit_synthetic_and_finite(self):
        result = subprocess.run([sys.executable, str(P)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        receipt = json.loads(result.stdout)
        self.assertEqual(receipt["configuration"]["source"]["kind"], "synthetic")
        self.assertEqual(receipt["scientific_status"], "exploratory-only")
        self.assertFalse(receipt["final"]["provenance"]["source_declaration_verified"])
        self.assertIsNone(receipt["execution"]["physical_time"])
        self.assertEqual(receipt["measurements"]["coherence"], 1.0)

    def test_invalid_cli_has_nonzero_json_receipt(self):
        with tempfile.TemporaryDirectory() as directory:
            request = Path(directory) / "request.json"
            for text in ('{"bad":1}', '{', '[1,2,3]', 'null'):
                request.write_text(text)
                result = subprocess.run([sys.executable, str(P), str(request)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 2, (text, result.stdout))
                self.assertEqual(json.loads(result.stdout)["status"], "invalid")


if __name__ == "__main__":
    unittest.main()
