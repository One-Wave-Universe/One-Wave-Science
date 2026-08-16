"""Render the D-415 spiral-arm formation scene directly to MP4.

This renderer is Python-first and has no browser dependency.  It visualizes
the YELLOW harmonic trail-lock hypothesis; it is not evidence that the
candidate galactic mechanism is physically validated.
"""

from __future__ import annotations

import argparse
import math
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


TAU = 2.0 * math.pi


@dataclass
class StarField:
    radius: np.ndarray
    angle: np.ndarray
    angular_rate: np.ndarray
    heat: np.ndarray


def wrap_phase(value: np.ndarray) -> np.ndarray:
    return np.arctan2(np.sin(value), np.cos(value))


def make_stars(count: int = 2400, seed: int = 415) -> StarField:
    rng = np.random.default_rng(seed)
    radius = 22.0 + 455.0 * np.sqrt(rng.random(count))
    angle = rng.random(count) * TAU
    angular_rate = 0.055 / (0.28 + radius / 460.0) + 0.006 * (
        rng.random(count) - 0.5
    )
    return StarField(radius, angle, angular_rate, rng.random(count))


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    names = (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    )
    try:
        return ImageFont.truetype(names, size=size)
    except OSError:
        return ImageFont.load_default()


def background(width: int, height: int) -> Image.Image:
    yy, xx = np.indices((height, width), dtype=np.float32)
    radial = np.sqrt(((xx - width * 0.43) / width) ** 2 + ((yy - height * 0.52) / height) ** 2)
    glow = np.exp(-radial * 5.2)
    rgb = np.empty((height, width, 3), dtype=np.uint8)
    rgb[..., 0] = np.clip(2 + 8 * glow, 0, 255)
    rgb[..., 1] = np.clip(7 + 25 * glow, 0, 255)
    rgb[..., 2] = np.clip(11 + 36 * glow, 0, 255)
    image = Image.fromarray(rgb, "RGB")
    draw = ImageDraw.Draw(image)
    rng = np.random.default_rng(416)
    for _ in range(max(120, width * height // 9000)):
        x = int(rng.integers(0, width))
        y = int(rng.integers(0, height))
        shade = int(rng.integers(70, 170))
        draw.point((x, y), fill=(shade, shade + 18, min(255, shade + 35)))
    return image


def draw_bar(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    width: int,
    value: float,
    color: tuple[int, int, int],
) -> None:
    value = max(0.0, min(1.0, value))
    draw.rounded_rectangle((x, y, x + width, y + 6), 3, fill=(16, 43, 56))
    draw.rounded_rectangle((x, y, x + int(width * value), y + 6), 3, fill=color)


def render_frame(
    base: Image.Image,
    stars: StarField,
    time_s: float,
    width: int,
    height: int,
) -> Image.Image:
    image = base.copy()
    draw = ImageDraw.Draw(image, "RGBA")
    scale = min(width / 1920.0, height / 1080.0)
    plot_right = int(width * 0.745)
    cx, cy = int(width * 0.383), int(height * 0.51)
    flatten = 0.62
    galactic_scale = min(width / 1920.0, height / 1080.0) * 1.58
    arm_count = 2 + int(time_s / 16.0) % 2
    pattern_spin = time_s * 0.026
    growth = min(1.0, time_s / 7.0)
    cycle = (time_s % 16.0) / 16.0

    # Directional parent-curvature traces.
    for ring in range(1, 6):
        radius = int((90 + ring * 86) * galactic_scale)
        draw.ellipse(
            (cx - radius, cy - int(flatten * radius), cx + radius, cy + int(flatten * radius)),
            outline=(69, 158, 198, max(18, 48 - ring * 5)),
            width=max(1, int(scale)),
        )

    phase = wrap_phase(
        arm_count * stars.angle
        + 4.7 * np.log(stars.radius / 36.0)
        - pattern_spin * arm_count
    )
    thin = 0.62 * (1.0 - stars.radius / 500.0) + 0.08
    coherence = np.exp(-(phase**2) / (2.0 * thin**2)) * growth
    next_phase = wrap_phase(
        (arm_count + 1) * stars.angle
        + 5.2 * np.log(stars.radius / 36.0)
        - pattern_spin * (arm_count + 1)
    )
    next_lock = np.exp(-(next_phase**2) / (2.0 * (thin + 0.05) ** 2)) * max(
        0.0, (cycle - 0.68) / 0.32
    )
    lock = np.maximum(coherence, next_lock)
    px = cx + stars.radius * galactic_scale * np.cos(stars.angle)
    py = cy + flatten * stars.radius * galactic_scale * np.sin(stars.angle)

    visible = (px > 30) & (px < plot_right - 15) & (py > 75) & (py < height - 40)
    for i in np.nonzero(visible)[0]:
        alpha = int(24 + 220 * lock[i])
        color = (255, 218, 150, alpha) if stars.heat[i] > 0.92 else (122, 207, 255, alpha)
        radius = 1 + int(lock[i] > 0.68)
        draw.ellipse(
            (int(px[i]) - radius, int(py[i]) - radius, int(px[i]) + radius, int(py[i]) + radius),
            fill=color,
        )

    # Central concentrated region, deliberately not the whole galactic curvature.
    for radius, alpha in ((58, 15), (38, 35), (22, 80)):
        rr = int(radius * scale * 1.5)
        draw.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), fill=(255, 194, 94, alpha))
    core = int(26 * scale * 1.5)
    draw.ellipse((cx - core, cy - core, cx + core, cy + core), fill=(225, 146, 52, 255))

    title_font = load_font(max(16, int(25 * scale)), bold=True)
    mono_font = load_font(max(10, int(12 * scale)))
    row_font = load_font(max(11, int(14 * scale)), bold=True)
    draw.text((int(55 * scale), int(48 * scale)), "GALAXY FORMING SPIRAL ARMS", font=title_font, fill=(232, 249, 255))
    draw.text(
        (int(55 * scale), int(82 * scale)),
        f"ONE FIELD · t {time_s:05.2f} · HARMONIC PATH m={arm_count}",
        font=mono_font,
        fill=(103, 133, 150),
    )

    panel_x = int(width * 0.765)
    panel_y = int(height * 0.11)
    panel_w = int(width * 0.205)
    panel_h = int(height * 0.80)
    draw.rounded_rectangle(
        (panel_x, panel_y, panel_x + panel_w, panel_y + panel_h),
        radius=max(8, int(18 * scale)),
        fill=(6, 19, 27, 220),
        outline=(25, 58, 73, 255),
        width=1,
    )
    draw.text((panel_x + 22, panel_y + 24), "ARM-FORMATION RECEIPT", font=mono_font, fill=(120, 150, 167))
    rows = (
        ("DIFFUSE STARS", "unlocked population", 1.0 - growth, (113, 143, 163)),
        ("HARMONIC PATH", f"m = {arm_count} phase trail", growth, (126, 223, 255)),
        ("TRAIL LENGTH", "outward recursive growth", cycle, (169, 156, 255)),
        ("ARM WIDTH", "thinning with length", max(0.08, 0.62 * (1.0 - cycle)), (255, 202, 115)),
        ("NEXT ARM", "release / recapture", max(0.0, (cycle - 0.68) / 0.32), (255, 127, 176)),
    )
    row_gap = int(panel_h * 0.145)
    for row_index, (name, detail, value, color) in enumerate(rows):
        yy = panel_y + int(panel_h * 0.115) + row_index * row_gap
        draw.text((panel_x + 22, yy), name, font=row_font, fill=color)
        draw.text((panel_x + 22, yy + int(26 * scale)), detail, font=mono_font, fill=(113, 141, 157))
        draw_bar(draw, panel_x + 22, yy + int(49 * scale), panel_w - 44, value, color)
    draw.text(
        (panel_x + 22, panel_y + panel_h - int(42 * scale)),
        "YELLOW · VISUALIZATION IS NOT VALIDATION",
        font=mono_font,
        fill=(77, 105, 121),
    )
    return image


def update_stars(stars: StarField, time_s: float, dt: float) -> None:
    arm_count = 2 + int(time_s / 16.0) % 2
    pattern_spin = time_s * 0.026
    growth = min(1.0, time_s / 7.0)
    phase = wrap_phase(
        arm_count * stars.angle
        + 4.7 * np.log(stars.radius / 36.0)
        - pattern_spin * arm_count
    )
    thin = 0.62 * (1.0 - stars.radius / 500.0) + 0.08
    lock = growth * np.exp(-(phase**2) / (2.0 * thin**2))
    stars.angle += dt * (stars.angular_rate - 0.032 * lock * phase / arm_count)


def render_video(output: Path, seconds: float, fps: int, width: int, height: int) -> None:
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        raise RuntimeError("ffmpeg is required to encode MP4 output")
    output.parent.mkdir(parents=True, exist_ok=True)
    command = [
        ffmpeg,
        "-y",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "rgb24",
        "-s",
        f"{width}x{height}",
        "-r",
        str(fps),
        "-i",
        "-",
        "-an",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        "18",
        "-pix_fmt",
        "yuv420p",
        str(output),
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    assert process.stdin is not None
    stars = make_stars()
    base = background(width, height)
    dt = 1.0 / fps
    for frame_index in range(round(seconds * fps)):
        time_s = frame_index * dt
        update_stars(stars, time_s, dt)
        frame = render_frame(base, stars, time_s, width, height)
        process.stdin.write(np.asarray(frame, dtype=np.uint8).tobytes())
    process.stdin.close()
    if process.wait() != 0:
        raise RuntimeError("ffmpeg failed to encode the video")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("galaxy_arm_formation.mp4"))
    parser.add_argument("--seconds", type=float, default=20.0)
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--height", type=int, default=1080)
    args = parser.parse_args()
    render_video(args.output, args.seconds, args.fps, args.width, args.height)
    print(args.output.resolve())


if __name__ == "__main__":
    main()
