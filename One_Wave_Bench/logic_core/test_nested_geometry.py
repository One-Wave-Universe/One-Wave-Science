import unittest

from nested_geometry import hexagonal_bipyramid, receipt, tet_midpoint_split, triangle_midpoint_split


class NestedGeometryTests(unittest.TestCase):
    def test_bipyramid_euler(self):
        bi = hexagonal_bipyramid()
        self.assertEqual(bi["V"], 8)
        self.assertEqual(bi["E"], 18)
        self.assertEqual(bi["F"], 12)
        self.assertEqual(bi["euler"], 2)
        self.assertEqual(bi["pyramids"], 6)

    def test_triangle_splits_to_four(self):
        self.assertEqual(triangle_midpoint_split()["child_triangles"], 4)

    def test_tet_has_octa_and_hex_belt(self):
        t = tet_midpoint_split()
        self.assertEqual(t["corner_tets"], 4)
        self.assertEqual(t["central_octahedra"], 1)
        self.assertEqual(t["octa_equatorial_hex_edges"], 6)

    def test_six_is_not_auto_routes(self):
        rec = receipt()
        self.assertTrue(rec["six_is_not_six_routes"])
        self.assertEqual(rec["brick"], "Yellow")


if __name__ == "__main__":
    unittest.main()
