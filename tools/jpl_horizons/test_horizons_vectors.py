import unittest

from horizons_vectors import parse_vector_result, relative_geometry


class HorizonsVectorTests(unittest.TestCase):
    def test_parse_vec_table_2_csv(self):
        text = """header\n$$SOE\n2460920.500000000, A.D. 2026-Sep-01 00:00:00.0000, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0,\n$$EOE\nfooter\n"""
        rows = parse_vector_result(text)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["jd_tdb"], 2460920.5)
        self.assertEqual(rows[0]["x_km"], 1.0)
        self.assertEqual(rows[0]["vz_km_s"], 6.0)

    def test_relative_geometry(self):
        a = {
            "x_km": 0.0, "y_km": 0.0, "z_km": 0.0,
            "vx_km_s": 0.0, "vy_km_s": 0.0, "vz_km_s": 0.0,
        }
        b = {
            "x_km": 3.0, "y_km": 4.0, "z_km": 0.0,
            "vx_km_s": 0.6, "vy_km_s": 0.8, "vz_km_s": 0.0,
        }
        g = relative_geometry(a, b)
        self.assertAlmostEqual(g["distance_km"], 5.0)
        self.assertAlmostEqual(g["relative_speed_km_s"], 1.0)
        self.assertAlmostEqual(g["radial_speed_km_s"], 1.0)
        self.assertAlmostEqual(g["transverse_speed_km_s"], 0.0)

    def test_missing_markers_fail_closed(self):
        with self.assertRaises(ValueError):
            parse_vector_result("no ephemeris markers here")


if __name__ == "__main__":
    unittest.main()
