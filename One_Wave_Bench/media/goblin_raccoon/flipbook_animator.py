"""Provider-neutral flipbook/cel animation renderer for Goblin Raccoon Studio.

The renderer intentionally treats artwork as traditional animation cels: each
source drawing is a discrete frame and can be held for one or more ticks.  It
does not invent in-between poses.  Background, character cels, and audio remain
independent tracks until final compositing.
"""
from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from PIL import Image


@dataclass(frozen=True)
class Cel:
    path: Path
    hold: int = 1


def _load_spec(project_spec: Mapping[str, Any] | str | Path) -> dict[str, Any]:
    if isinstance(project_spec, Mapping):
        return dict(project_spec)
    path = Path(project_spec)
    return json.loads(path.read_text(encoding="utf-8"))


def _resolve(base: Path, value: str | Path | None) -> Path | None:
    if value in (None, ""):
        return None
    path = Path(value)
    return path if path.is_absolute() else base / path


def _natural_key(path: Path) -> tuple[Any, ...]:
    import re
    return tuple(int(part) if part.isdigit() else part.lower() for part in re.split(r"(\d+)", path.name))


def _collect_cels(spec: Mapping[str, Any], base: Path) -> list[Cel]:
    raw = spec.get("cels")
    default_hold = max(1, int(spec.get("hold", 2)))
    cels: list[Cel] = []

    if raw:
        for item in raw:
            if isinstance(item, str):
                path = _resolve(base, item)
                assert path is not None
                cels.append(Cel(path=path, hold=default_hold))
            else:
                path = _resolve(base, item["path"])
                assert path is not None
                cels.append(Cel(path=path, hold=max(1, int(item.get("hold", default_hold)))))
    else:
        folder = _resolve(base, spec.get("cel_dir"))
        if folder is None:
            raise ValueError("project_spec needs either 'cels' or 'cel_dir'")
        patterns = spec.get("patterns", ["*.png", "*.webp", "*.jpg", "*.jpeg"])
        found: list[Path] = []
        for pattern in patterns:
            found.extend(folder.glob(pattern))
        for path in sorted(set(found), key=_natural_key):
            cels.append(Cel(path=path, hold=default_hold))

    if not cels:
        raise ValueError("no animation cels were found")
    missing = [str(cel.path) for cel in cels if not cel.path.exists()]
    if missing:
        raise FileNotFoundError("missing cel(s): " + ", ".join(missing))
    return cels


def _timeline(cels: Sequence[Cel], loop: bool, ping_pong: bool) -> list[Path]:
    expanded: list[Path] = []
    for cel in cels:
        expanded.extend([cel.path] * cel.hold)
    if ping_pong and len(expanded) > 2:
        expanded += expanded[-2:0:-1]
    if not loop:
        return expanded
    return expanded


def _cover(image: Image.Image, width: int, height: int, zoom: float = 1.0, pan_x: float = 0.0, pan_y: float = 0.0) -> Image.Image:
    scale = max(width / image.width, height / image.height) * zoom
    resized = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    left = round((resized.width - width) / 2 + pan_x)
    top = round((resized.height - height) / 2 + pan_y)
    left = max(0, min(left, max(0, resized.width - width)))
    top = max(0, min(top, max(0, resized.height - height)))
    return resized.crop((left, top, left + width, top + height))


def _fit_cel(cel: Image.Image, target_height: int) -> Image.Image:
    scale = target_height / cel.height
    return cel.resize((max(1, round(cel.width * scale)), target_height), Image.Resampling.LANCZOS)


def _frame_position(spec: Mapping[str, Any], width: int, height: int, t: float) -> tuple[float, float, float]:
    pos = spec.get("position", {})
    x = float(pos.get("x", 0.5)) * width
    y = float(pos.get("y", 0.82)) * height
    scale = float(spec.get("character_scale", 0.58))

    route = spec.get("route", "still")
    strength = float(spec.get("route_strength", 1.0))
    if route == "walk-right":
        x += ((t % 1.0) - 0.5) * width * 0.6 * strength
    elif route == "walk-left":
        x -= ((t % 1.0) - 0.5) * width * 0.6 * strength
    elif route == "figure-eight":
        phase = t * math.tau
        x += math.sin(phase) * width * 0.27 * strength
        y += math.sin(phase * 2.0) * height * 0.08 * strength
    return x, y, scale


def make_video(project_spec: Mapping[str, Any] | str | Path) -> Path:
    """Render an MP4 from discrete flipbook/cel artwork.

    ``project_spec`` may be a dict or a path to JSON.  The public function is
    intentionally AI/provider-neutral so any agent can call the same renderer.
    """
    spec = _load_spec(project_spec)
    base = Path(spec.get("base_dir", ".")).resolve()
    width = int(spec.get("width", 1280))
    height = int(spec.get("height", 720))
    fps = max(1, int(spec.get("fps", 12)))
    seconds = max(0.1, float(spec.get("seconds", 6)))
    output = _resolve(base, spec.get("output", "goblin-raccoon-flipbook.mp4"))
    assert output is not None
    output.parent.mkdir(parents=True, exist_ok=True)

    ffmpeg = shutil.which(str(spec.get("ffmpeg", "ffmpeg")))
    if ffmpeg is None:
        raise RuntimeError("ffmpeg is required to encode MP4 output")

    cels = _collect_cels(spec, base)
    frames = _timeline(cels, bool(spec.get("loop", True)), bool(spec.get("ping_pong", False)))
    background_path = _resolve(base, spec.get("background"))
    audio_path = _resolve(base, spec.get("audio"))

    background = Image.open(background_path).convert("RGB") if background_path else Image.new("RGB", (width, height), spec.get("background_color", "#101510"))
    loaded = {path: Image.open(path).convert("RGBA") for path in set(frames)}

    command = [
        ffmpeg, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
        "-s", f"{width}x{height}", "-r", str(fps), "-i", "-",
    ]
    if audio_path:
        command += ["-i", str(audio_path), "-shortest"]
    command += ["-c:v", "libx264", "-preset", "medium", "-crf", str(spec.get("crf", 18)), "-pix_fmt", "yuv420p"]
    if audio_path:
        command += ["-c:a", "aac", "-b:a", str(spec.get("audio_bitrate", "192k"))]
    command += ["-movflags", "+faststart", str(output)]

    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    assert process.stdin is not None
    total_frames = max(1, round(seconds * fps))
    loop = bool(spec.get("loop", True))
    camera = spec.get("camera", {})

    try:
        for index in range(total_frames):
            progress = index / max(1, total_frames - 1)
            zoom = float(camera.get("zoom", 1.0)) + float(camera.get("zoom_delta", 0.0)) * progress
            pan_x = float(camera.get("pan_x", 0.0)) * progress
            pan_y = float(camera.get("pan_y", 0.0)) * progress
            scene = _cover(background, width, height, zoom=zoom, pan_x=pan_x, pan_y=pan_y).convert("RGBA")

            timeline_index = index % len(frames) if loop else min(index, len(frames) - 1)
            cel = loaded[frames[timeline_index]]
            x, y, char_scale = _frame_position(spec, width, height, progress)
            sprite = _fit_cel(cel, max(1, round(height * char_scale)))
            left = round(x - sprite.width / 2)
            top = round(y - sprite.height)
            scene.alpha_composite(sprite, (left, top))
            process.stdin.write(scene.convert("RGB").tobytes())
    finally:
        process.stdin.close()

    if process.wait() != 0:
        raise RuntimeError("ffmpeg encoding failed")
    return output


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render old-school cel/flipbook animation from a JSON project spec.")
    parser.add_argument("project_spec", help="Path to the JSON project specification")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = _parser().parse_args(list(argv) if argv is not None else None)
    print(make_video(args.project_spec))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
