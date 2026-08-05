#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from one_wave_virtual_lens import (
    EventEncoder,
    LENS_SHAPE,
    PersistentVisualField,
    SyntheticVisualWorld,
    VirtualLens,
    VirtualLensBrain,
    VisualPatternCodec,
    run_demo,
)


class VirtualLensTests(unittest.TestCase):
    def test_lens_is_partial(self):
        world = SyntheticVisualWorld().render(0)
        lens = VirtualLens()
        view = lens.capture(world)
        self.assertEqual(view.shape, LENS_SHAPE)
        self.assertNotEqual(view.shape, world.shape)

    def test_event_encoder_reports_on_and_off(self):
        world = SyntheticVisualWorld()
        lens = VirtualLens()
        enc = EventEncoder(0.15)
        first = lens.capture(world.render(0))
        enc.initialize(first)
        events = enc.encode(lens.capture(world.render(1)), lens, 1)
        self.assertTrue(any(e.polarity > 0 for e in events))
        self.assertTrue(any(e.polarity < 0 for e in events))

    def test_persistent_field_keeps_static_wall(self):
        world = SyntheticVisualWorld()
        lens = VirtualLens()
        view = lens.capture(world.render(0))
        field = PersistentVisualField()
        field.initialize_from_view(view, lens)
        x0, y0, x1, y1 = world.wall
        before = float(field.field[y0:y1, x0:x1].mean())
        for _ in range(10):
            field.update([])
        after = float(field.field[y0:y1, x0:x1].mean())
        self.assertGreater(before, 0.1)
        self.assertAlmostEqual(before, after, places=6)

    def test_pattern_shape(self):
        brain = VirtualLensBrain()
        brain.step(0)
        self.assertEqual(brain.last_pattern.shape, (VisualPatternCodec.VECTOR_SIZE,))
        self.assertTrue(np.all(np.isin(brain.last_pattern, [-1, 1])))

    def test_demo_and_recall(self):
        with tempfile.TemporaryDirectory() as tmp:
            summary = run_demo(Path(tmp), ticks=90, make_gif=False)
        self.assertTrue(summary["loop_exists_all_ticks"])
        self.assertGreater(summary["total_events"], 0)
        self.assertGreaterEqual(summary["recall_correct"], 3)
        self.assertEqual(summary["recall_total"], 4)
        self.assertIsNotNone(summary["occlusion_prediction_mean_error_px"])
        self.assertLess(summary["occlusion_prediction_mean_error_px"], 16.0)
        self.assertTrue(all(t["energy_nonincreasing"] for t in summary["recall_trials"]))

    def test_original_hopfield_source_hash_is_preserved(self):
        package = Path(__file__).resolve().parent
        original = package / "hopfield_original" / "One_Wave_Hopfield_Brain_v2_1_Final.py"
        expected = package / "ORIGINAL_HOPFIELD_SHA256.txt"
        digest = hashlib.sha256(original.read_bytes()).hexdigest()
        self.assertEqual(digest, expected.read_text(encoding="utf-8").strip())


if __name__ == "__main__":
    unittest.main(verbosity=2)
