from pathlib import Path

import pytest

from One_Wave_Bench.media.goblin_raccoon import flipbook_animator as animator


def test_timeline_holds_each_drawing_without_inbetweening(tmp_path: Path):
    a = tmp_path / "frame_01.png"
    b = tmp_path / "frame_02.png"
    a.touch()
    b.touch()
    cels = [animator.Cel(a, hold=2), animator.Cel(b, hold=3)]
    assert animator._timeline(cels, loop=True, ping_pong=False) == [a, a, b, b, b]


def test_ping_pong_reverses_existing_cels_only(tmp_path: Path):
    paths = [tmp_path / f"frame_{i:02d}.png" for i in range(1, 4)]
    for path in paths:
        path.touch()
    cels = [animator.Cel(path, hold=1) for path in paths]
    assert animator._timeline(cels, loop=True, ping_pong=True) == [paths[0], paths[1], paths[2], paths[1]]


def test_collect_cels_natural_sorts_numbered_art(tmp_path: Path):
    for name in ["turn_10.png", "turn_2.png", "turn_1.png"]:
        (tmp_path / name).touch()
    cels = animator._collect_cels({"cel_dir": str(tmp_path), "hold": 1}, Path("."))
    assert [cel.path.name for cel in cels] == ["turn_1.png", "turn_2.png", "turn_10.png"]


def test_collect_cels_fails_loudly_on_missing_art(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        animator._collect_cels({"cels": [{"path": str(tmp_path / "missing.png"), "hold": 2}]}, Path("."))
