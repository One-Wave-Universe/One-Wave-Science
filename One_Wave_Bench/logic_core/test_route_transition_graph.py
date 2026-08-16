import unittest

from route_transition_graph import TransitionLaw, analyze, build_edges


class RouteTransitionGraphTests(unittest.TestCase):
    def test_product_graph_is_two_by_three_cartesian_product(self):
        receipt = analyze(TransitionLaw.PRODUCT)
        self.assertEqual(receipt.node_count, 6)
        self.assertEqual(receipt.edge_count, 7)
        self.assertEqual(receipt.degree_sequence, (2, 2, 2, 2, 3, 3))
        self.assertTrue(receipt.connected)
        self.assertEqual(receipt.diameter, 3)

    def test_center_gated_flip_is_connected_and_sparser(self):
        receipt = analyze(TransitionLaw.CENTER_GATED_FLIP)
        self.assertEqual(receipt.edge_count, 5)
        self.assertTrue(receipt.connected)
        self.assertEqual(receipt.diameter, 3)
        self.assertEqual(receipt.degree_sequence, (1, 1, 1, 1, 3, 3))

    def test_movement_only_separates_yes_and_no(self):
        receipt = analyze(TransitionLaw.MOVEMENT_ONLY)
        self.assertEqual(receipt.edge_count, 4)
        self.assertFalse(receipt.connected)
        self.assertIsNone(receipt.diameter)

    def test_all_candidate_edges_are_reversible(self):
        for law in TransitionLaw:
            self.assertTrue(analyze(law).reversible)

    def test_no_candidate_has_absorbing_route(self):
        for law in TransitionLaw:
            self.assertEqual(analyze(law).absorbing_nodes, ())

    def test_center_gated_edges_are_subset_of_product(self):
        self.assertLess(build_edges(TransitionLaw.CENTER_GATED_FLIP),
                        build_edges(TransitionLaw.PRODUCT))


if __name__ == "__main__":
    unittest.main()
