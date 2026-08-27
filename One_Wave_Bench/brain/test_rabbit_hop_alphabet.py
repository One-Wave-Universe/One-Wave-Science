import unittest

from One_Wave_Bench.brain.rabbit_hop_alphabet import (
    AlphabetOrientation,
    EvenAnchor,
    MirrorPolarity,
    OddSide,
    alphabet_rank,
    coordinate_family,
    shared_odd_bridge,
)


class RabbitHopAlphabetTests(unittest.TestCase):
    def test_a_complete_positive_family(self):
        self.assertEqual(
            tuple(record.tuple for record in coordinate_family("A")),
            ((1, 2, 1), (1, 2, 3), (1, 4, 3), (1, 4, 5)),
        )

    def test_b_complete_positive_family(self):
        self.assertEqual(
            tuple(record.tuple for record in coordinate_family("B")),
            ((2, 4, 3), (2, 4, 5), (2, 6, 5), (2, 6, 7)),
        )

    def test_z_complete_positive_family(self):
        self.assertEqual(
            tuple(record.tuple for record in coordinate_family("Z")),
            ((26, 52, 51), (26, 52, 53), (26, 54, 53), (26, 54, 55)),
        )

    def test_negative_is_exact_sign_mirror(self):
        positive = coordinate_family("A")
        negative = coordinate_family("A", polarity=MirrorPolarity.NEGATIVE)
        self.assertEqual(
            tuple(record.tuple for record in negative),
            tuple(tuple(-value for value in record.tuple) for record in positive),
        )

    def test_inverse_alphabet_makes_a_26_and_z_1(self):
        self.assertEqual(alphabet_rank("A", AlphabetOrientation.Z_TO_A), 26)
        self.assertEqual(alphabet_rank("Z", AlphabetOrientation.Z_TO_A), 1)

    def test_shared_odd_bridge_is_retained(self):
        self.assertEqual(shared_odd_bridge("A"), 3)
        self.assertEqual(shared_odd_bridge("B"), 5)

    def test_four_independent_route_labels_are_preserved(self):
        family = coordinate_family("M")
        labels = {(record.anchor, record.odd_side) for record in family}
        self.assertEqual(labels, {
            (EvenAnchor.CURRENT, OddSide.LOWER),
            (EvenAnchor.CURRENT, OddSide.UPPER),
            (EvenAnchor.NEXT, OddSide.LOWER),
            (EvenAnchor.NEXT, OddSide.UPPER),
        })


if __name__ == "__main__":
    unittest.main()
