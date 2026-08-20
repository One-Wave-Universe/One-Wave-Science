"""Plain-Python data model for a One-Wave Animator scene.

Kept free of any GUI framework dependency so it can be unit tested
without a display and so the file format is easy to reason about.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import List, Optional

SCENE_FORMAT_VERSION = 1

DEFAULT_CANVAS_WIDTH = 1280
DEFAULT_CANVAS_HEIGHT = 720


@dataclass
class BackgroundLayer:
    path: str  # absolute path to the source image on disk
    width: float
    height: float

    def to_dict(self, scene_dir: str) -> dict:
        return {
            "path": _to_portable_path(self.path, scene_dir),
            "width": self.width,
            "height": self.height,
        }

    @staticmethod
    def from_dict(data: dict, scene_dir: str) -> "BackgroundLayer":
        return BackgroundLayer(
            path=_from_portable_path(data["path"], scene_dir),
            width=float(data["width"]),
            height=float(data["height"]),
        )


@dataclass
class CharacterLayer:
    path: str  # absolute path to the source image on disk
    x: float
    y: float
    width: float
    height: float
    z: int

    def to_dict(self, scene_dir: str) -> dict:
        return {
            "path": _to_portable_path(self.path, scene_dir),
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "z": self.z,
        }

    @staticmethod
    def from_dict(data: dict, scene_dir: str) -> "CharacterLayer":
        return CharacterLayer(
            path=_from_portable_path(data["path"], scene_dir),
            x=float(data["x"]),
            y=float(data["y"]),
            width=float(data["width"]),
            height=float(data["height"]),
            z=int(data["z"]),
        )


@dataclass
class Scene:
    canvas_width: float = DEFAULT_CANVAS_WIDTH
    canvas_height: float = DEFAULT_CANVAS_HEIGHT
    background: Optional[BackgroundLayer] = None
    characters: List[CharacterLayer] = field(default_factory=list)

    def to_dict(self, scene_dir: str) -> dict:
        return {
            "format_version": SCENE_FORMAT_VERSION,
            "canvas": {"width": self.canvas_width, "height": self.canvas_height},
            "background": self.background.to_dict(scene_dir) if self.background else None,
            "characters": [c.to_dict(scene_dir) for c in self.characters],
        }

    @staticmethod
    def from_dict(data: dict, scene_dir: str) -> "Scene":
        canvas = data.get("canvas", {})
        background_data = data.get("background")
        return Scene(
            canvas_width=float(canvas.get("width", DEFAULT_CANVAS_WIDTH)),
            canvas_height=float(canvas.get("height", DEFAULT_CANVAS_HEIGHT)),
            background=BackgroundLayer.from_dict(background_data, scene_dir) if background_data else None,
            characters=[CharacterLayer.from_dict(c, scene_dir) for c in data.get("characters", [])],
        )

    def save(self, file_path: str) -> None:
        scene_dir = os.path.dirname(os.path.abspath(file_path))
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(scene_dir), f, indent=2)

    @staticmethod
    def load(file_path: str) -> "Scene":
        scene_dir = os.path.dirname(os.path.abspath(file_path))
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return Scene.from_dict(data, scene_dir)


def _to_portable_path(path: str, scene_dir: str) -> str:
    """Store image paths relative to the scene file when possible, so a
    scene folder stays portable if moved together with its assets."""
    abs_path = os.path.abspath(path)
    try:
        rel_path = os.path.relpath(abs_path, scene_dir)
    except ValueError:
        # Different drive on Windows: relpath is impossible, fall back to absolute.
        return abs_path
    if rel_path == os.pardir or rel_path.startswith(os.pardir + os.sep):
        return abs_path
    return rel_path.replace(os.sep, "/")


def _from_portable_path(stored_path: str, scene_dir: str) -> str:
    if os.path.isabs(stored_path):
        return stored_path
    return os.path.normpath(os.path.join(scene_dir, stored_path))
