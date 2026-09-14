import gzip
import math
import unittest

from gwosc_strain_wave import (
    analyze_segment,
    extract_centered_segment,
    parse_gzipped_ascii_strain,
    select_strain_file,
)


class GWOSCWaveTests(unittest.TestCase):
    def test_sine_peak_lands_on_known_bin(self):
        fs = 1024.0
        n = 2048
        f0 = 64.0
        signal = [1e-21 * math.sin(2.0 * math.pi * f0 * i / fs) for i in range(n)]
        receipt = analyze_segment(signal, fs, 20.0, 200.0, top_bins=5)
        self.assertAlmostEqual(receipt.df_Hz, 0.5)
        self.assertEqual(receipt.n_samples, n)
        self.assertAlmostEqual(receipt.strongest_bins[0]["frequency_Hz"], f0)
        self.assertGreater(receipt.strongest_bins[0]["psd_strain2_per_Hz"], 0.0)
        self.assertGreater(receipt.band_power_strain2, 0.0)

    def test_ascii_parser_ignores_headers_and_preserves_values(self):
        text = "# strain\n% metadata\n1.0e-21\n-2.5e-22\n0\n"
        payload = gzip.compress(text.encode("utf-8"))
        self.assertEqual(parse_gzipped_ascii_strain(payload), [1.0e-21, -2.5e-22, 0.0])

    def test_centered_segment_uses_event_gps(self):
        fs = 8.0
        samples = list(range(64))
        segment, meta = extract_centered_segment(
            samples,
            sample_rate_Hz=fs,
            file_gps_start=1000.0,
            center_gps=1004.0,
            window_seconds=2.0,
        )
        self.assertEqual(len(segment), 16)
        self.assertEqual(meta["center_index"], 32)
        self.assertEqual(segment[0], 24)
        self.assertEqual(segment[-1], 39)

    def test_file_selector_does_not_mix_detectors_or_rates(self):
        rows = [
            {"detector": "H1", "sample_rate_kHz": 16, "duration": 32, "file_format": "TXT", "download_url": "a"},
            {"detector": "H1", "sample_rate_kHz": 4, "duration": 32, "file_format": "TXT", "download_url": "b"},
            {"detector": "L1", "sample_rate_kHz": 4, "duration": 32, "file_format": "TXT", "download_url": "c"},
        ]
        selected = select_strain_file(rows, "H1", 4, 32, "TXT")
        self.assertEqual(selected["download_url"], "b")

    def test_non_power_of_two_analysis_is_rejected(self):
        with self.assertRaises(ValueError):
            analyze_segment([0.0] * 1000, 1000.0, 20.0, 400.0, top_bins=3)


if __name__ == "__main__":
    unittest.main()
