#!/usr/bin/env python3
import sys
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
