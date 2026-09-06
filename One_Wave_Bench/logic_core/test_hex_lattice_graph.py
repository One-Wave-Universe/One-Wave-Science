import math
import unittest

from hex_lattice_graph import (
    AXIS_PAIRS,
    NEIGHBOR_OFFSETS,
    coordination,
    directed_routes,
    disk_sites,
    edge_list,
    incidence_matrix,
    laplacian,
    laplacian_spectrum,
    seven_cell,
    site_xy,
    axis_pairs,
)


class HexLatticeGraphTests(unittest.TestCase):
    def test_six_directed_neighbors(self):
        self.assertEqual(len(NEIGHBOR_OFFSETS), 6)
        self.assertEqual(len(directed_routes()), 6)
        self.assertEqual(len(AXIS_PAIRS), 3)
        self.assertEqual(len(axis_pairs()), 3)

    def test_seven_cell_is_center_plus_ring(self):
        cells = seven_cell()
        self.assertEqual(len(cells), 7)
        self.assertIn((0, 0), cells)
        self.assertEqual(coordination(cells, (0, 0)), 6)
        for site in cells:
            if site != (0, 0):
                self.assertEqual(coordination(cells, site), 3)

    def test_neighbor_distances_equal(self):
        origin = site_xy((0, 0))
        distances = []
        for off in NEIGHBOR_OFFSETS:
            x, y = site_xy(off)
            distances.append(math.hypot(x - origin[0], y - origin[1]))
        for d in distances:
            self.assertAlmostEqual(d, 1.0, places=12)

    def test_laplacian_kernel_is_constants(self):
        sites = seven_cell()
        L = laplacian(sites)
        row_sums = [sum(row) for row in L]
        self.assertTrue(all(s == 0 for s in row_sums))
        spec = laplacian_spectrum(sites)
        self.assertAlmostEqual(spec[0], 0.0, places=8)
        self.assertGreater(spec[1], 0.0)

    def test_incidence_counts_edges(self):
        sites = seven_cell()
        edges = edge_list(sites)
        inc = incidence_matrix(sites)
        self.assertEqual(len(edges), 12)
        self.assertEqual(len(inc), 7)
        self.assertEqual(len(inc[0]), 12)

    def test_disk_radius_one_is_seven_cell(self):
        self.assertEqual(set(disk_sites(1)), set(seven_cell()))

    def test_interior_coordination_on_larger_disk(self):
        sites = disk_sites(2)
        self.assertEqual(coordination(sites, (0, 0)), 6)


if __name__ == "__main__":
    unittest.main()
