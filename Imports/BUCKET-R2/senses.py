#!/usr/bin/env python3
"""Stub senses. Replace bodies, keep signatures."""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


@dataclass
class Frame:
    t: int
    mean: float
    motion: float


class Eye:
    def __init__(self) -> None:
        self.prev = 0.5

    def grab(self, t: int) -> Frame:
        # stub: slow sine gray-world + a little jitter
        mean = 0.5 + 0.15 * math.sin(t / 3.0)
        motion = abs(mean - self.prev)
        self.prev = mean
        return Frame(t=t, mean=mean, motion=motion)


class Ear:
    def hear(self, drum_hit: bool, guitar_onset: bool) -> dict:
        return {
            "self_drum": drum_hit,
            "guitar": guitar_onset,
            "room": float(drum_hit) + 0.7 * float(guitar_onset),
        }


class Drum:
    def hit(self, vel: float) -> bool:
        return vel > 0.15


class Mouth:
    def say(self, word: str) -> str:
        return word.lower().strip() or "…"
