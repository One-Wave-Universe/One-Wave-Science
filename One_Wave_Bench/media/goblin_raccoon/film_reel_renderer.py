"""Render Goblin Raccoon film-reel projects without procedural character motion.

The renderer consumes the same explicit project state edited by the browser UI
or an AI agent.  Every output frame resolves to a background plate plus a cel
exposure anchored at its feet.  Music, ambience, dialogue, and SFX are mixed as
independent ffmpeg inputs with independent gain and start offsets.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any, Iterable, Mapping

from PIL import Image

from .film_reel import FilmProject, project_from_dict


def _load_spec(project_spec: Mapping[str, Any] | str | Path) -> tuple[dict[str, Any], Path]:
    if isinstance(project_spec, Mapping):
        data = dict(project_spec)
        return data, Path(data.get("base_dir", ".")).resolve()
    path = Path(project_spec).resolve()
    data = json.loads(path.read_text(encoding="utf-8"))
    return data, Path(data.get("base_dir", path.parent)).resolve()


def _resolve(base: Path, value: str | Path | None) -> Path | None:
    if value in (None, ""):
        return None
    path = Path(value)
    return path if path.is_absolute() else base / path


def _load_project(data: Mapping[str, Any]) -> FilmProject:
    # FilmProject's stable subset deliberately ignores renderer-only keys such
    # as assets/output/base_character_height.
    return project_from_dict(data)


def _background(project: FilmProject, base: Path) -> Image.Image:
    path = _resolve(base, project.background)
    if path is None:
        return Image.new("RGB", (project.background_width, project.background_height), "#101510")
    image = Image.open(path).convert("RGB")
    # Background defines the world.  No cover-crop or camera box is introduced.
    if image.size != (project.background_width, project.background_height):
        image = image.resize(
            (project.background_width, project.background_height),
            Image.Resampling.LANCZOS,
        )
    return image


def _load_assets(data: Mapping[str, Any], base: Path) -> dict[str, Image.Image]:
    raw = data.get("assets", {})
    if isinstance(raw, list):
        raw = {str(item["id"]): item["path"] for item in raw}
    assets: dict[str, Image.Image] = {}
    for asset_id, value in dict(raw).items():
        path_value = value.get("path") if isinstance(value, Mapping) else value
        path = _resolve(base, path_value)
        if path is None or not path.exists():
            raise FileNotFoundError(f"missing art asset {asset_id!r}: {path}")
        assets[str(asset_id)] = Image.open(path).convert("RGBA")
    return assets


def _fit_actor(
    image: Image.Image,
    *,
    scene_height: int,
    base_character_height: float,
    depth_scale: float,
) -> Image.Image:
    target_height = max(1, round(scene_height * base_character_height * depth_scale))
    scale = target_height / max(1, image.height)
    return image.resize(
        (max(1, round(image.width * scale)), target_height),
        Image.Resampling.LANCZOS,
    )


def _render_frame(
    project: FilmProject,
    background: Image.Image,
    assets: Mapping[str, Image.Image],
    frame: int,
    base_character_height: float,
) -> Image.Image:
    scene = background.copy().convert("RGBA")
    resolved = project.resolve_frame(frame)
    if resolved.asset_id is None:
        return scene.convert("RGB")
    source = assets.get(resolved.asset_id)
    if source is None:
        raise KeyError(f"timeline references unknown asset {resolved.asset_id!r}")
    assert resolved.scale is not None
    sprite = _fit_actor(
        source,
        scene_height=project.background_height,
        base_character_height=base_character_height,
        depth_scale=resolved.scale,
    )
    if resolved.rotation_deg:
        sprite = sprite.rotate(-resolved.rotation_deg, expand=True, resample=Image.Resampling.BICUBIC)
    assert resolved.x is not None and resolved.ground_y is not None
    # x is center; y is *feet/ground contact*.  Never center the sprite on y.
    left = round(resolved.x * project.background_width - sprite.width / 2)
    top = round(resolved.ground_y * project.background_height - sprite.height)
    scene.alpha_composite(sprite, (left, top))
    return scene.convert("RGB")


def _audio_filter(project: FilmProject, existing: list[tuple[int, float, int]]) -> tuple[str | None, str | None]:
    """Build volume/delay/amix filter for ffmpeg audio input indexes."""
    if not existing:
        return None, None
    pieces: list[str] = []
    labels: list[str] = []
    for ordinal, (input_index, gain, start_ms) in enumerate(existing):
        label = f"a{ordinal}"
        pieces.append(
            f"[{input_index}:a]adelay={max(0, start_ms)}|{max(0, start_ms)},"
            f"volume={max(0.0, gain):.6f}[{label}]"
        )
        labels.append(f"[{label}]")
    if len(labels) == 1:
        pieces.append(f"{labels[0]}anull[aout]")
    else:
        pieces.append(
            "".join(labels)
            + f"amix=inputs={len(labels)}:duration=longest:normalize=0[aout]"
        )
    return ";".join(pieces), "[aout]"


def make_video(project_spec: Mapping[str, Any] | str | Path) -> Path:
    """Render an MP4 from a film-reel project dict or JSON file."""
    data, base = _load_spec(project_spec)
    project = _load_project(data)
    assets = _load_assets(data, base)
    background = _background(project, base)
    base_character_height = float(data.get("base_character_height", 0.58))
    output = _resolve(base, data.get("output", "goblin-raccoon-film-reel.mp4"))
    assert output is not None
    output.parent.mkdir(parents=True, exist_ok=True)

    ffmpeg = shutil.which(str(data.get("ffmpeg", "ffmpeg")))
    if ffmpeg is None:
        raise RuntimeError("ffmpeg is required to encode film-reel MP4 output")

    command = [
        ffmpeg,
        "-y",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-s",
        f"{project.background_width}x{project.background_height}",
        "-r",
        str(project.fps),
        "-i",
        "-",
    ]

    audio_inputs: list[tuple[int, float, int]] = []
    next_input = 1
    for track in project.audio:
        path = _resolve(base, track.path)
        if path is None or not path.exists():
            raise FileNotFoundError(f"missing {track.kind} audio: {path}")
        command += ["-i", str(path)]
        audio_inputs.append((next_input, float(track.gain), int(track.start_ms)))
        next_input += 1

    filter_complex, audio_map = _audio_filter(project, audio_inputs)
    if filter_complex:
        command += ["-filter_complex", filter_complex]

    command += [
        "-map",
        "0:v:0",
        "-c:v",
        "libx264",
        "-preset",
        str(data.get("preset", "medium")),
        "-crf",
        str(data.get("crf", 18)),
        "-pix_fmt",
        "yuv420p",
    ]
    if audio_map:
        command += ["-map", audio_map, "-c:a", "aac", "-b:a", str(data.get("audio_bitrate", "192k"))]
    command += ["-t", f"{project.duration_ms / 1000.0:.6f}", "-movflags", "+faststart", str(output)]

    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    assert process.stdin is not None
    try:
        for frame in range(project.frame_count):
            rendered = _render_frame(
                project,
                background,
                assets,
                frame,
                base_character_height,
            )
            process.stdin.write(rendered.tobytes())
    finally:
        process.stdin.close()

    if process.wait() != 0:
        raise RuntimeError("ffmpeg film-reel encoding failed")
    return output


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render explicit Goblin Raccoon film-reel project JSON.")
    parser.add_argument("project_spec")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = _parser().parse_args(list(argv) if argv is not None else None)
    print(make_video(args.project_spec))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
