"""Music-domain adapter for the reusable Rabbit-Hopping route core.

Established music-coordinate facts used here:

* twelve pitch classes modulo 12;
* one ascending perfect-fifth step is +7 semitones modulo 12;
* reverse Circle-of-Fifths traversal is -7 semitones modulo 12;
* enharmonic spellings share the same pitch-class identity.

The adapter maps pitch classes to Rabbit-Hop source ranks 1..12 in chromatic
order C..B. It does not redefine the Rabbit-Hop arithmetic. Every note can use
the complete signed-K route families and both TOP-1/TOP+1 connectors.

One-Wave span conventions ``-5(0)+4`` (major) and ``-5(0)+3`` (minor) are
included explicitly as project conventions, separate from the established
pitch-class/Circle-of-Fifths rules above.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from One_Wave_Bench.brain.rabbit_hop_core import (
    MirrorPolarity,
    NumericRouteReceipt,
    RouteFamily,
    TraversalDirection,
    WrapperSide,
    numeric_coordinate,
    numeric_offset_ladder,
    numeric_wrapper_pair,
    recover_source_rank,
)


PITCH_CLASS_COUNT = 12
SHARP_NAMES = (
    "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"
)
FLAT_NAMES = (
    "C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"
)

# Accepted enharmonic names. Values are zero-based pitch classes.
NOTE_TO_PITCH_CLASS = {
    "C": 0,
    "B#": 0,
    "C#": 1,
    "DB": 1,
    "D": 2,
    "D#": 3,
    "EB": 3,
    "E": 4,
    "FB": 4,
    "E#": 5,
    "F": 5,
    "F#": 6,
    "GB": 6,
    "G": 7,
    "G#": 8,
    "AB": 8,
    "A": 9,
    "A#": 10,
    "BB": 10,
    "B": 11,
    "CB": 11,
}


class NoteSpelling(str, Enum):
    SHARPS = "sharps"
    FLATS = "flats"


class FifthDirection(str, Enum):
    FORWARD = "forward"
    REVERSE = "reverse"

    @property
    def semitone_step(self) -> int:
        return 7 if self is FifthDirection.FORWARD else -7


@dataclass(frozen=True, slots=True)
class MusicRouteReceipt:
    """A note identity plus its complete numeric Rabbit-Hop receipt."""

    note: str
    pitch_class: int
    source_rank: int
    numeric: NumericRouteReceipt

    @property
    def tuple(self) -> tuple[int, int, int]:
        return self.numeric.tuple

    @property
    def top_address(self) -> int:
        return self.numeric.top_address

    @property
    def wrapper_address(self) -> int:
        return self.numeric.wrapper_address

    @property
    def route_family(self) -> RouteFamily:
        return self.numeric.route_family

    @property
    def k(self) -> int:
        return self.numeric.k

    @property
    def wrapper(self) -> WrapperSide:
        return self.numeric.wrapper


@dataclass(frozen=True, slots=True)
class OneWaveSpan:
    """Project span convention around a center: left, center, right."""

    left: int
    center: int
    right: int

    @property
    def tuple(self) -> tuple[int, int, int]:
        return self.left, self.center, self.right


# Project conventions, not replacements for standard major/minor definitions.
ONE_WAVE_MAJOR_SPAN = OneWaveSpan(-5, 0, 4)
ONE_WAVE_MINOR_SPAN = OneWaveSpan(-5, 0, 3)


def _normalize_note(note: str) -> str:
    if not isinstance(note, str) or not note.strip():
        raise ValueError("note must be a non-empty note name")
    text = (
        note.strip()
        .replace("♯", "#")
        .replace("♭", "b")
    )
    if len(text) == 1:
        return text.upper()
    return text[0].upper() + text[1:].replace("b", "B").upper()


def pitch_class(note: str) -> int:
    """Return the zero-based pitch class for a note/enharmonic spelling."""

    normalized = _normalize_note(note)
    try:
        return NOTE_TO_PITCH_CLASS[normalized]
    except KeyError as exc:
        raise ValueError(f"unsupported note spelling: {note!r}") from exc


def note_name(
    value: int,
    *,
    spelling: NoteSpelling = NoteSpelling.SHARPS,
) -> str:
    """Return a canonical note spelling for any integer pitch-class value."""

    if not isinstance(value, int):
        raise TypeError("pitch-class value must be an integer")
    names = SHARP_NAMES if spelling is NoteSpelling.SHARPS else FLAT_NAMES
    return names[value % PITCH_CLASS_COUNT]


def chromatic_source_rank(note: str) -> int:
    """Map C..B chromatic pitch classes to Rabbit-Hop source ranks 1..12."""

    return pitch_class(note) + 1


def source_rank_note(
    source_rank: int,
    *,
    spelling: NoteSpelling = NoteSpelling.SHARPS,
) -> str:
    """Inverse of ``chromatic_source_rank`` for the declared 1..12 adapter."""

    if not isinstance(source_rank, int) or not 1 <= source_rank <= 12:
        raise ValueError("music source rank must be an integer from 1 through 12")
    return note_name(source_rank - 1, spelling=spelling)


def transpose(
    note: str,
    semitones: int,
    *,
    spelling: NoteSpelling = NoteSpelling.SHARPS,
) -> str:
    """Transpose a pitch class by an integer number of semitones."""

    if not isinstance(semitones, int):
        raise TypeError("semitones must be an integer")
    return note_name(pitch_class(note) + semitones, spelling=spelling)


def fifth_step(
    note: str,
    *,
    direction: FifthDirection = FifthDirection.FORWARD,
    spelling: NoteSpelling = NoteSpelling.SHARPS,
) -> str:
    """Move one step around the Circle of Fifths."""

    return transpose(note, direction.semitone_step, spelling=spelling)


def circle_of_fifths(
    start: str = "C",
    *,
    direction: FifthDirection = FifthDirection.FORWARD,
    spelling: NoteSpelling = NoteSpelling.SHARPS,
    include_return: bool = False,
) -> tuple[str, ...]:
    """Return one complete twelve-class Circle-of-Fifths traversal.

    The default result has twelve unique pitch classes. ``include_return``
    appends the starting pitch class as the thirteenth display position.
    """

    current = note_name(pitch_class(start), spelling=spelling)
    result = []
    for _ in range(PITCH_CLASS_COUNT):
        result.append(current)
        current = fifth_step(current, direction=direction, spelling=spelling)
    if include_return:
        result.append(result[0])
    return tuple(result)


def circle_index(
    note: str,
    *,
    start: str = "C",
    direction: FifthDirection = FifthDirection.FORWARD,
) -> int:
    """Return the 0..11 fifth-step index of a pitch class from ``start``."""

    target = pitch_class(note)
    current = pitch_class(start)
    for step in range(PITCH_CLASS_COUNT):
        if current == target:
            return step
        current = (current + direction.semitone_step) % PITCH_CLASS_COUNT
    raise AssertionError("all twelve pitch classes must occur in a fifth cycle")


def music_coordinate(
    note: str,
    *,
    spelling: NoteSpelling = NoteSpelling.SHARPS,
    polarity: MirrorPolarity = MirrorPolarity.POSITIVE,
    route_family: RouteFamily = RouteFamily.ORIGINAL,
    k: int = 0,
    wrapper: WrapperSide = WrapperSide.UPPER,
    traversal: TraversalDirection = TraversalDirection.FORWARD,
) -> MusicRouteReceipt:
    """Translate one note through any complete Rabbit-Hop route."""

    pc = pitch_class(note)
    source = pc + 1
    numeric = numeric_coordinate(
        source,
        polarity=polarity,
        route_family=route_family,
        k=k,
        wrapper=wrapper,
        traversal=traversal,
    )
    return MusicRouteReceipt(
        note=note_name(pc, spelling=spelling),
        pitch_class=pc,
        source_rank=source,
        numeric=numeric,
    )


def music_wrapper_pair(
    note: str,
    *,
    spelling: NoteSpelling = NoteSpelling.SHARPS,
    polarity: MirrorPolarity = MirrorPolarity.POSITIVE,
    route_family: RouteFamily = RouteFamily.ORIGINAL,
    k: int = 0,
    traversal: TraversalDirection = TraversalDirection.FORWARD,
) -> tuple[MusicRouteReceipt, MusicRouteReceipt]:
    """Return both mandatory TOP-1/TOP+1 receipts for one note/route."""

    pc = pitch_class(note)
    source = pc + 1
    numeric_pair = numeric_wrapper_pair(
        source,
        polarity=polarity,
        route_family=route_family,
        k=k,
        traversal=traversal,
    )
    canonical = note_name(pc, spelling=spelling)
    return tuple(
        MusicRouteReceipt(canonical, pc, source, numeric)
        for numeric in numeric_pair
    )


def music_offset_ladder(
    note: str,
    *,
    route_family: RouteFamily,
    min_k: int,
    max_k: int,
    spelling: NoteSpelling = NoteSpelling.SHARPS,
    polarity: MirrorPolarity = MirrorPolarity.POSITIVE,
    traversal: TraversalDirection = TraversalDirection.FORWARD,
) -> tuple[tuple[MusicRouteReceipt, MusicRouteReceipt], ...]:
    """Apply the full signed-K Rabbit-Hop ladder to one musical source."""

    pc = pitch_class(note)
    source = pc + 1
    numeric_ladder = numeric_offset_ladder(
        source,
        route_family=route_family,
        min_k=min_k,
        max_k=max_k,
        polarity=polarity,
        traversal=traversal,
    )
    canonical = note_name(pc, spelling=spelling)
    return tuple(
        tuple(MusicRouteReceipt(canonical, pc, source, numeric) for numeric in pair)
        for pair in numeric_ladder
    )


def recover_music_source(
    record: MusicRouteReceipt,
    *,
    spelling: NoteSpelling = NoteSpelling.SHARPS,
) -> str:
    """Use the full route receipt to rebuild the original pitch-class label."""

    source = recover_source_rank(record.numeric)
    return source_rank_note(source, spelling=spelling)


def fifths_rabbit_route(
    start: str = "C",
    *,
    direction: FifthDirection = FifthDirection.FORWARD,
    spelling: NoteSpelling = NoteSpelling.SHARPS,
    route_family: RouteFamily = RouteFamily.ORIGINAL,
    k: int = 0,
) -> tuple[tuple[MusicRouteReceipt, MusicRouteReceipt], ...]:
    """Compile a full Circle-of-Fifths traversal into Rabbit-Hop receipts."""

    return tuple(
        music_wrapper_pair(
            note,
            spelling=spelling,
            route_family=route_family,
            k=k,
        )
        for note in circle_of_fifths(
            start,
            direction=direction,
            spelling=spelling,
        )
    )


def flip_span(span: OneWaveSpan) -> OneWaveSpan:
    """One-Wave project FLIP: ``(-a,0,+b) -> (-b,0,+a)``."""

    if span.center != 0:
        raise ValueError("One-Wave span FLIP currently requires center zero")
    return OneWaveSpan(-span.right, 0, -span.left)


def span_notes(
    center_note: str,
    span: OneWaveSpan,
    *,
    spelling: NoteSpelling = NoteSpelling.SHARPS,
) -> tuple[str, str, str]:
    """Render a One-Wave span around a pitch-class center."""

    return (
        transpose(center_note, span.left, spelling=spelling),
        transpose(center_note, span.center, spelling=spelling),
        transpose(center_note, span.right, spelling=spelling),
    )
