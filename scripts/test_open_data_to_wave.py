#!/usr/bin/env python3
import json
import math
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from open_data_to_wave import transform

MAPPING = {
    "state_identity": "record",
    "coupling_rule": "adjacent samples",
    "timing_relationship": "source time/index",
    "propagation_behavior": "ordered sequence",
}
PROVENANCE = {"source": "test", "record_id": "r1"}


class OpenDataToWaveTests(unittest.TestCase):
    def series(self, samples, time_unit=None):
        return transform({"mode": "measurement_series", "provenance": PROVENANCE,
                          "mapping": MAPPING, "samples": samples, "time_unit": time_unit})

    def test_cadence_is_not_signal_frequency(self):
        # A known 10 Hz example is sampled at 100 Hz; the adapter estimates neither.
        samples = [{"t": i / 100, "value": math.sin(2 * math.pi * 10 * i / 100)}
                   for i in range(20)]
        output = self.series(samples, "s")
        self.assertEqual(output["schema"], "one-wave-wave-data-v2")
        self.assertAlmostEqual(output["timing"]["sample_rate_Hz"], 100)
        self.assertIsNone(output["states"][0]["inverse_sample_interval_Hz"])
        for state in output["states"]:
            self.assertIsNone(state["f"])
            self.assertFalse(state["frequency_known"])
        self.assertAlmostEqual(output["states"][1]["inverse_sample_interval_Hz"], 100)
        self.assertEqual(output["provenance"], PROVENANCE)
        self.assertEqual(output["states"][1]["m"]["raw"], samples[1])

    def test_constant_values_do_not_claim_measured_zero_hz(self):
        output = self.series([{"t": 0, "value": 2}, {"t": 1, "value": 2}], "s")
        self.assertEqual([s["A"] for s in output["states"]], [0.0, 0.0])
        self.assertIsNone(output["states"][1]["f"])
        self.assertFalse(output["states"][1]["frequency_known"])

    def test_declared_units_convert_cadence_only(self):
        for unit, delta in [("s", .01), ("ms", 10), ("us", 10000), ("ns", 10000000)]:
            with self.subTest(unit=unit):
                output = self.series([{"t": 0, "value": 1}, {"t": delta, "value": 2}], unit)
                self.assertAlmostEqual(output["timing"]["sample_rate_Hz"], 100)
                self.assertEqual(output["states"][1]["t"], delta)
                self.assertEqual(output["timing"]["time_unit"], unit)

    def test_unknown_time_units_do_not_create_hertz(self):
        for unit in [None, "index", "energy_eV", "unknown"]:
            with self.subTest(unit=unit):
                output = self.series([{"t": 0, "value": 1}, {"t": 1, "value": 2}], unit)
                self.assertIsNone(output["timing"]["sample_rate_Hz"])
                self.assertIsNone(output["states"][1]["inverse_sample_interval_Hz"])
                self.assertEqual(output["timing"]["cadence_reason"], "time_unit_unknown_or_unsupported")

    def test_missing_and_mixed_timestamps_do_not_create_cadence(self):
        for samples, expected in [([{"value": 1}, {"value": 2}], "index"),
                                  ([{"t": 100, "value": 1}, {"value": 2}], "mixed_source_and_index")]:
            with self.subTest(expected=expected):
                output = self.series(samples, "s")
                self.assertEqual(output["timing"]["time_coordinates"], expected)
                self.assertIsNone(output["timing"]["sample_rate_Hz"])
                self.assertTrue(all(s["sample_interval_s"] is None for s in output["states"]))

    def test_mixed_timestamp_order_is_unassessed_not_cadence(self):
        for samples in [[{"t": 2, "value": 1}, {"t": 2, "value": 2}, {"value": 3}],
                        [{"t": 2, "value": 1}, {"value": 2}, {"t": 1, "value": 3}]]:
            with self.subTest(samples=samples):
                output = self.series(samples, "s")
                self.assertEqual(output["timing"]["time_coordinates"], "mixed_source_and_index")
                self.assertIsNone(output["timing"]["uniform_sampling"])
                self.assertIsNone(output["timing"]["sample_rate_Hz"])
                self.assertTrue(all(s["inverse_sample_interval_Hz"] is None for s in output["states"]))

    def test_single_timestamp_has_no_cadence(self):
        output = self.series([{"t": 0, "value": 1}], "s")
        self.assertIsNone(output["timing"]["uniform_sampling"])
        self.assertIsNone(output["timing"]["sample_rate_Hz"])
        self.assertEqual(output["timing"]["cadence_reason"], "fewer_than_two_samples")

    def test_nonuniform_intervals_are_not_a_global_sample_rate(self):
        output = self.series([{"t": t, "value": i} for i, t in enumerate([0, 1, 3])], "s")
        self.assertFalse(output["timing"]["uniform_sampling"])
        self.assertIsNone(output["timing"]["sample_rate_Hz"])
        self.assertEqual([s["inverse_sample_interval_Hz"] for s in output["states"]], [None, 1, .5])

    def test_invalid_time_intervals_rejected(self):
        for t in [0, -1, float("nan"), float("inf"), True]:
            with self.subTest(t=t):
                with self.assertRaises(ValueError):
                    self.series([{"t": 0, "value": 1}, {"t": t, "value": 2}], "s")

    def test_nonfinite_values_and_positions_rejected(self):
        for key in ["value", "x"]:
            for value in [float("nan"), float("inf"), -float("inf"), True]:
                with self.subTest(key=key, value=value):
                    with self.assertRaises(ValueError):
                        self.series([{"t": 0, "value": 1, key: value}], "s")

    def test_metadata_has_no_frequency_or_cadence(self):
        output = transform({"mode": "metadata_sequence", "provenance": PROVENANCE,
                            "mapping": MAPPING, "metadata": {"bytes": 200, "count": 4}})
        self.assertEqual(output["timing"]["time_coordinates"], "metadata_index")
        self.assertIsNone(output["timing"]["sample_rate_Hz"])
        for state in output["states"]:
            self.assertIsNone(state["f"])
            self.assertFalse(state["frequency_known"])
            self.assertIsNone(state["inverse_sample_interval_Hz"])
        self.assertEqual([s["m"]["raw_value"] for s in output["states"]], [200, 4])

    def test_cli_outputs_strict_json_with_null_frequency(self):
        with tempfile.TemporaryDirectory() as directory:
            src, dest = Path(directory) / "input.json", Path(directory) / "output.json"
            src.write_text(json.dumps({"mode": "measurement_series", "provenance": PROVENANCE,
                                      "mapping": MAPPING, "time_unit": "s",
                                      "samples": [{"t": 0, "value": 1}, {"t": 1, "value": 2}]}))
            result = subprocess.run([sys.executable, str(Path(__file__).with_name("open_data_to_wave.py")),
                                     str(src), "-o", str(dest)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            def invalid_constant(value):
                raise AssertionError("nonstandard JSON constant " + value)
            output = json.loads(dest.read_text(), parse_constant=invalid_constant)
            self.assertIsNone(output["states"][1]["f"])
            self.assertEqual(output["timing"]["sample_rate_Hz"], 1.0)

    def test_measurement_series_preserves_raw_values(self):
        output = transform(
            {
                "mode": "measurement_series",
                "provenance": PROVENANCE,
                "mapping": MAPPING,
                "samples": [{"t": 0, "value": 10}, {"t": 2, "value": 20}],
            }
        )
        self.assertEqual(output["representation_kind"], "source_measurement_wave")
        self.assertTrue(output["source_physical_wave_or_series"])
        self.assertEqual(output["states"][1]["m"]["raw_value"], 20.0)

    def test_metadata_is_explicitly_derived(self):
        output = transform(
            {
                "mode": "metadata_sequence",
                "provenance": PROVENANCE,
                "mapping": MAPPING,
                "metadata": {"energy": 125.1, "width": 4.0, "label": "x"},
            }
        )
        self.assertEqual(output["representation_kind"], "derived_metadata_wave")
        self.assertFalse(output["source_physical_wave_or_series"])
        self.assertIn("not a claim", output["warning"])

    def test_requires_four_mapping_fields(self):
        with self.assertRaises(ValueError):
            transform(
                {
                    "mode": "metadata_sequence",
                    "provenance": PROVENANCE,
                    "mapping": {},
                    "metadata": {"x": 1},
                }
            )


if __name__ == "__main__":
    unittest.main()
