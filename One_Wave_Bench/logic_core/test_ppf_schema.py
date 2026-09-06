import unittest

from ppf_schema import (
    FieldState,
    PPFState,
    leaf_point,
    nest,
    quantity,
    segment_path,
    zero_field,
)


class PPFSchemaTests(unittest.TestCase):
    def test_units_and_frames_are_declared(self):
        p = leaf_point(1.0, 0.0, 0.2)
        self.assertEqual(p.position.unit, "m")
        self.assertEqual(p.orientation.unit, "rad")
        self.assertEqual(p.position.frame, "ground")
        self.assertEqual(p.orientation.frame, "local")

    def test_bad_unit_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "unit"):
            quantity((1.0,), "furlong", "ground", "nope")

    def test_child_scale_must_be_parent_minus_one(self):
        child = PPFState(
            scale=0,
            point=leaf_point(0.0, 0.0),
            path=segment_path(0.0, 0.0, 1.0, 0.0),
            field=zero_field(),
        )
        with self.assertRaisesRegex(ValueError, "child scale"):
            PPFState(
                scale=2,
                point=leaf_point(0.5, 0.0),
                path=segment_path(0.0, 0.0, 1.0, 0.0),
                field=zero_field(),
                children=[child],
            )

    def test_nest_depth_and_leaves(self):
        leaves = [
            PPFState(
                scale=0,
                point=leaf_point(float(i), 0.0),
                path=segment_path(float(i), 0.0, float(i) + 1.0, 0.0),
                field=zero_field(),
            )
            for i in range(3)
        ]
        parent = nest(1, leaf_point(1.0, 0.0, scale_label="small"), leaves)
        self.assertEqual(parent.depth(), 2)
        self.assertEqual(parent.leaf_count(), 3)
        self.assertEqual(sum(1 for _ in parent.walk()), 4)

    def test_field_is_not_a_path(self):
        field = zero_field("V")
        path = segment_path(0.0, 0.0, 1.0, 0.0)
        self.assertIsInstance(field, FieldState)
        self.assertNotEqual(field.amplitude.unit, path.length.unit)


if __name__ == "__main__":
    unittest.main()
