#!/usr/bin/env python3
"""Local copy of the HEX-SPLIT fifths walk.

This repo runs alone. If HEX-SPLIT/clock.json exists beside you later,
prefer that file. Until then these twelve slots are the contract.
"""
from __future__ import annotations

from pathlib import Path
import json

SLOTS = [
    {"step": 0, "gray": "C",  "pyramid": 1, "polarity": "express",  "tag": "P1-E", "midi": 60},
    {"step": 1, "gray": "G",  "pyramid": 2, "polarity": "compress", "tag": "P2-C", "midi": 67},
    {"step": 2, "gray": "D",  "pyramid": 3, "polarity": "express",  "tag": "P3-E", "midi": 62},
    {"step": 3, "gray": "A",  "pyramid": 4, "polarity": "compress", "tag": "P4-C", "midi": 69},
    {"step": 4, "gray": "E",  "pyramid": 5, "polarity": "express",  "tag": "P5-E", "midi": 64},
    {"step": 5, "gray": "B",  "pyramid": 6, "polarity": "compress", "tag": "P6-C", "midi": 71},
    {"step": 6, "gray": "F#", "pyramid": 1, "polarity": "compress", "tag": "P1-C", "midi": 66},
    {"step": 7, "gray": "C#", "pyramid": 2, "polarity": "express",  "tag": "P2-E", "midi": 61},
    {"step": 8, "gray": "G#", "pyramid": 3, "polarity": "compress", "tag": "P3-C", "midi": 68},
    {"step": 9, "gray": "D#", "pyramid": 4, "polarity": "express",  "tag": "P4-E", "midi": 63},
    {"step": 10,"gray": "A#", "pyramid": 5, "polarity": "compress", "tag": "P5-C", "midi": 70},
    {"step": 11,"gray": "F",  "pyramid": 6, "polarity": "express",  "tag": "P6-E", "midi": 65},
]


def load_slots() -> list[dict]:
    for candidate in (
        Path(__file__).parent / "clock.json",
        Path(__file__).resolve().parents[1] / "HEX-SPLIT" / "clock.json",
    ):
        if candidate.exists():
            data = json.loads(candidate.read_text())
            return data.get("slots", SLOTS)
    return SLOTS


def slot_at(t: int) -> dict:
    slots = load_slots()
    return slots[t % len(slots)]
