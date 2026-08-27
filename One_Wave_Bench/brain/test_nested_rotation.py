import unittest

from One_Wave_Bench.brain.nested_rotation import (
    Carrier,
    NestedRotationReceipt,
    RotationLevel,
    Season,
    THRESHOLD_BANDS,
    threshold_bands_for,
)


class NestedRotationTests(unittest.TestCase):
    def test_declared_threshold_bands_are_exact(self):
        self.assertEqual(
            tuple((band.high, band.low) for band in THRESHOLD_BANDS),
            ((100, 90), (85, 75), (70, 60), (55, 45),
             (40, 30), (25, 15), (15, 0)),
        )

    def test_fifteen_is_a_shared_transition_boundary(self):
        self.assertEqual(threshold_bands_for(15), (6, 7))

    def test_gaps_are_not_silently_filled(self):
        self.assertEqual(threshold_bands_for(87), ())

    def test_four_seasons_form_a_closed_cycle(self):
        season = Season.SPRING
        observed = []
        for _ in range(4):
            observed.append(season)
            season = season.next
        self.assertEqual(
            observed,
            [Season.SPRING, Season.SUMMER, Season.FALL, Season.WINTER],
        )
        self.assertIs(season, Season.SPRING)

    def test_every_carrier_receipt_has_point_path_field_rotation(self):
        receipt = NestedRotationReceipt(
            Carrier.QUANTUM_MAGNETIC, 0.0, 1.0, 2.0, 95, Season.SPRING
        )
        self.assertEqual(set(receipt.phases), set(RotationLevel))

    def test_nested_carriers_run_quantum_to_proton_knot(self):
        quantum = NestedRotationReceipt(
            Carrier.QUANTUM_MAGNETIC, 0.0, 0.1, 0.2, 95, Season.SPRING
        )
        electric = NestedRotationReceipt(
            Carrier.ELECTRIC, 0.3, 0.4, 0.5, 80, Season.SUMMER, (quantum,)
        )
        quark = NestedRotationReceipt(
            Carrier.QUARK_VORTEX, 0.6, 0.7, 0.8, 65, Season.FALL, (electric,)
        )
        proton = NestedRotationReceipt(
            Carrier.PROTON_KNOT, 0.9, 1.0, 1.1, 50, Season.WINTER, (quark,)
        )
        self.assertIs(proton.contained[0].contained[0].contained[0], quantum)

    def test_larger_carrier_cannot_be_nested_inside_smaller(self):
        proton = NestedRotationReceipt(
            Carrier.PROTON_KNOT, 0.0, 0.1, 0.2, 95, Season.SPRING
        )
        with self.assertRaises(ValueError):
            NestedRotationReceipt(
                Carrier.QUANTUM_MAGNETIC, 0.0, 0.1, 0.2, 95,
                Season.SPRING, (proton,),
            )


if __name__ == "__main__":
    unittest.main()
