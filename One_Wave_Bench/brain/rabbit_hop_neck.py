"""Six-string / 24-fret music-neck adapter for Rabbit Hopping.

This module provides a concrete standard-guitar labeling layer over the same
12 pitch classes and Rabbit-Hop core. It is an adapter, not a claim that the
physical guitar neck defines the underlying Rabbit-Hop arithmetic.

String numbers follow standard guitar convention: 6 is the lowest-pitched E
string and 1 is the highest-pitched E string. Frets are zero-based; fret 0 is
the open string. The default map includes frets 0..24 inclusive.
"""

from __future__ import annotations

from dataclasses import dataclass

from One_Wave_Bench.brain.rabbit_hop_core import (
    MirrorPolarity,
    RouteFamily,
    TraversalDirection,
)
from One_Wave_Bench.brain.rabbit_hop_music import (
    MusicRouteReceipt,
    NoteSpelling,
    music_wrapper_pair,
    note_name,
    pitch_class,
)


STANDARD_GUITAR_TUNING = (
    (6, "E"),
    (5, "A"),
    (4, "D"),
    (3, "G"),
    (2, "B"),
    (1, "E"),
)
DEFAULT_MAX_FRET = 24


@dataclass(frozen=True, slots=True)
class NeckPosition:
    string_number: int
    fret: int
    open_note: str
    note: str
    pitch_class: int


def _tuning_map(
    tuning: tuple[tuple[int, str], ...] = STANDARD_GUITAR_TUNING,
) -> dict[int, str]:
    result = dict(tuning)
    if set(result) != {1, 2, 3, 4, 5, 6}:
        raise ValueError("tuning must define guitar strings 1 through 6 exactly once")
    # Validate all note labels up front.
    for note in result.values():
        pitch_class(note)
    return result


def fret_note(
    open_note: str,
    fret: int,
    *,
    spelling: NoteSpelling = NoteSpelling.SHARPS,
) -> str:
    """Return the pitch-class label at one fret above an open-string note."""

    if not isinstance(fret, int) or fret < 0:
        raise ValueError("fret must be an integer >= 0")
    return note_name(pitch_class(open_note) + fret, spelling=spelling)


def neck_position(
    string_number: int,
    fret: int,
    *,
    tuning: tuple[tuple[int, str], ...] = STANDARD_GUITAR_TUNING,
    spelling: NoteSpelling = NoteSpelling.SHARPS,
) -> NeckPosition:
    """Resolve one string/fret location to its pitch-class identity."""

    tuning_map = _tuning_map(tuning)
    if string_number not in tuning_map:
        raise ValueError("string_number must be 1 through 6")
    if not isinstance(fret, int) or fret < 0:
        raise ValueError("fret must be an integer >= 0")
    open_note = note_name(pitch_class(tuning_map[string_number]), spelling=spelling)
    note = fret_note(open_note, fret, spelling=spelling)
    return NeckPosition(
        string_number=string_number,
        fret=fret,
        open_note=open_note,
        note=note,
        pitch_class=pitch_class(note),
    )


def neck_map(
    *,
    max_fret: int = DEFAULT_MAX_FRET,
    tuning: tuple[tuple[int, str], ...] = STANDARD_GUITAR_TUNING,
    spelling: NoteSpelling = NoteSpelling.SHARPS,
) -> tuple[NeckPosition, ...]:
    """Return all six strings from open position through ``max_fret``."""

    if not isinstance(max_fret, int) or max_fret < 0:
        raise ValueError("max_fret must be an integer >= 0")
    tuning_map = _tuning_map(tuning)
    return tuple(
        neck_position(
            string_number,
            fret,
            tuning=tuple(tuning_map.items()),
            spelling=spelling,
        )
        for string_number in (6, 5, 4, 3, 2, 1)
        for fret in range(max_fret + 1)
    )


def neck_rabbit_pair(
    string_number: int,
    fret: int,
    *,
    tuning: tuple[tuple[int, str], ...] = STANDARD_GUITAR_TUNING,
    spelling: NoteSpelling = NoteSpelling.SHARPS,
    polarity: MirrorPolarity = MirrorPolarity.POSITIVE,
    route_family: RouteFamily = RouteFamily.ORIGINAL,
    k: int = 0,
    traversal: TraversalDirection = TraversalDirection.FORWARD,
) -> tuple[MusicRouteReceipt, MusicRouteReceipt]:
    """Compile one neck location through any complete Rabbit-Hop route."""

    position = neck_position(
        string_number,
        fret,
        tuning=tuning,
        spelling=spelling,
    )
    return music_wrapper_pair(
        position.note,
        spelling=spelling,
        polarity=polarity,
        route_family=route_family,
        k=k,
        traversal=traversal,
    )
