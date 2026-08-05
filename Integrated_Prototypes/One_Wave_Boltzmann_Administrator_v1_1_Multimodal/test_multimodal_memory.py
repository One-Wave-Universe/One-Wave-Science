#!/usr/bin/env python3
from __future__ import annotations

import unittest

from multimodal_memory import (
    AllocationProfile,
    EqualReserveHopfieldMemory,
    MemoryModality,
    example_traces,
)


class MultimodalMemoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.traces = example_traces()
        self.memory = EqualReserveHopfieldMemory(block_width=24, seed=91)
        self.memory.store_many(self.traces)

    def test_equal_reserved_capacity(self) -> None:
        profile = AllocationProfile()
        self.assertEqual(sum(profile.reserved_percent.values()), 100.0)
        self.assertTrue(all(value == 20.0 for value in profile.reserved_percent.values()))

    def test_dialogue_heavy_profile_preserves_visual_access(self) -> None:
        profile = AllocationProfile.dialogue_sound_pressure_profile()
        attention = profile.effective_attention(mode="waking")
        self.assertGreater(attention[MemoryModality.DIALOGUE], attention[MemoryModality.IMAGE])
        self.assertGreaterEqual(attention[MemoryModality.IMAGE], profile.minimum_live_percent)
        self.assertAlmostEqual(sum(attention.values()), 100.0, places=6)

    def test_recall_without_visual_cue(self) -> None:
        target = self.traces[0]
        result = self.memory.recall(
            expected_memory=target.memory_id,
            cue=target,
            available=(
                MemoryModality.DIALOGUE,
                MemoryModality.SOUND,
                MemoryModality.BODY_PRESSURE,
                MemoryModality.MOVEMENT_GAZE,
            ),
            profile=AllocationProfile.dialogue_sound_pressure_profile(),
        )
        self.assertTrue(result.correct_attractor)
        self.assertIn("image", result.missing_modalities)
        self.assertTrue(result.converged)

    def test_recall_from_body_and_dialogue_only(self) -> None:
        target = self.traces[1]
        result = self.memory.recall(
            expected_memory=target.memory_id,
            cue=target,
            available=(MemoryModality.DIALOGUE, MemoryModality.BODY_PRESSURE),
            profile=AllocationProfile.dialogue_sound_pressure_profile(),
            mode="daydream",
        )
        self.assertTrue(result.correct_attractor)


if __name__ == "__main__":
    unittest.main(verbosity=2)
