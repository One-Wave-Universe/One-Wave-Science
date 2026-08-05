#!/usr/bin/env python3
"""Unit tests for One-Wave Boltzmann Administrator v1.0."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import numpy as np

from one_wave_boltzmann_administrator import (
    ACTION_NAMES,
    BrainMode,
    BoltzmannAdministrator,
    BridgePacket,
    JointRBM,
    SignedBridgeCodec,
    SurvivalScenarioFactory,
    evaluate_accuracy,
    scenarios_to_matrix,
)


class AdministratorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.codec = SignedBridgeCodec()
        factory = SurvivalScenarioFactory(seed=77)
        scenarios = factory.make(1800)
        train, cls.test = scenarios[:1500], scenarios[1500:]
        cls.model = JointRBM(cls.codec.visible_bits, n_hidden=48, seed=77)
        cls.model.fit(
            scenarios_to_matrix(train, cls.codec),
            epochs=45,
            batch_size=75,
            learning_rate=0.04,
            momentum=0.5,
        )
        cls.admin = BoltzmannAdministrator(cls.model, cls.codec, seed=77)

    def test_codec_roundtrip(self) -> None:
        new = (-5.5, -3.0, 0.0, 2.5, 5.5)
        old = tuple(-x for x in new)
        bits = self.codec.encode_state(new, old)
        new_decoded, old_decoded = self.codec.decode_state(bits)
        self.assertEqual(new, new_decoded)
        self.assertEqual(old, old_decoded)

    def test_packet_rejects_bad_width(self) -> None:
        with self.assertRaises(ValueError):
            BridgePacket(new_up=(1, 2, 3), old_down=(0, 0, 0, 0, 0), tick=0).validate()  # type: ignore[arg-type]

    def test_six_gate_order_and_broadcast(self) -> None:
        scenario = self.test[0]
        result = self.admin.run_cycle(
            BridgePacket(
                new_up=scenario.new_up,
                old_down=scenario.old_down,
                tick=1,
                mode=BrainMode.WAKING,
                loop_id="unit",
            )
        )
        self.assertEqual([e.gate for e in result.gate_events], [1, 2, 3, 4, 5, 6])
        self.assertIn("4 tells 5", result.gate_events[3].message)
        self.assertIn("5 tells 6", result.gate_events[4].message)
        self.assertEqual(result.broadcast["rule"], "6 tells everybody")
        self.assertTrue(result.loop_exists)

    def test_dream_modes_hold_external_output(self) -> None:
        scenario = self.test[1]
        for mode in (BrainMode.DAYDREAM, BrainMode.DREAM_SLEEP):
            result = self.admin.run_cycle(
                BridgePacket(
                    new_up=scenario.new_up,
                    old_down=scenario.old_down,
                    tick=2,
                    mode=mode,
                    external_output_requested=True,
                )
            )
            self.assertFalse(result.external_release_recommended)

    def test_warm_temperature_has_more_entropy(self) -> None:
        scenario = self.test[2]
        cold, _ = self.admin.action_distribution(scenario.new_up, scenario.old_down, 0.45)
        warm, _ = self.admin.action_distribution(scenario.new_up, scenario.old_down, 1.45)
        cold_h = -np.sum(cold * np.log(cold + 1e-12))
        warm_h = -np.sum(warm * np.log(warm + 1e-12))
        self.assertGreater(warm_h, cold_h)

    def test_model_persistence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "weights.npz"
            self.model.save(path)
            loaded = JointRBM.load(path, seed=77)
            self.assertTrue(np.allclose(self.model.W, loaded.W))
            self.assertTrue(np.allclose(self.model.vbias, loaded.vbias))
            self.assertTrue(np.allclose(self.model.hbias, loaded.hbias))

    def test_accuracy_above_chance(self) -> None:
        result = evaluate_accuracy(self.admin, self.test)
        self.assertGreater(result["accuracy"], 0.70)
        self.assertGreater(result["accuracy"], 1.0 / len(ACTION_NAMES))

    def test_constant_reference_loop(self) -> None:
        reference = (0.0,) * 5
        for tick in range(300):
            scenario = self.test[tick % len(self.test)]
            result = self.admin.run_cycle(
                BridgePacket(
                    new_up=scenario.new_up,
                    old_down=reference,
                    tick=tick,
                    flip_phase=tick % 2,
                )
            )
            reference = result.next_old_reference
            self.assertTrue(result.loop_exists)
            self.assertTrue(all(-5.5 <= x <= 5.5 for x in reference))


if __name__ == "__main__":
    unittest.main(verbosity=2)
