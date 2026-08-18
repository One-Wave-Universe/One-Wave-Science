"""Stable human/AI-facing interface for Goblin Raccoon animation tools."""

from .cel_sheet import slice_sheet
from .film_reel import (
    AudioTrack,
    Exposure,
    FilmProject,
    PerspectiveGrid,
    lay_art_sequence,
    make_project_spec,
)
from .film_reel_renderer import make_video
from .flipbook_animator import make_video as make_legacy_flipbook_video

__all__ = [
    "AudioTrack",
    "Exposure",
    "FilmProject",
    "PerspectiveGrid",
    "lay_art_sequence",
    "make_project_spec",
    "make_video",
    "make_legacy_flipbook_video",
    "slice_sheet",
]
