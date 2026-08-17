"""Render a layered Goblin Raccoon movement demo.

The background camera and transparent character sprite are evaluated as
independent animation tracks and composited only for the encoded output.
"""

from __future__ import annotations

import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
BACKGROUND = ROOT / "generated_images/exec-d31eeea1-f229-455f-b601-e32afc431c12.png"
FRAMES = HERE / "walk_cycle"
OUTPUT = HERE / "goblin_raccoon_moving_layers_demo.mp4"


def cover_crop(image: Image.Image, width: int, height: int, zoom: float, pan_x: float) -> Image.Image:
    scale = max(width / image.width, height / image.height) * zoom
    resized = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    max_x = max(0, resized.width - width)
    left = round(max_x * (0.5 + pan_x))
    top = max(0, round((resized.height - height) * 0.72))
    return resized.crop((left, top, left + width, top + height))


def render() -> Path:
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        raise RuntimeError("ffmpeg is required")

    width, height, fps, seconds = 1280, 720, 30, 12
    background = Image.open(BACKGROUND).convert("RGB")
    sprites = [Image.open(FRAMES / f"frame_{index:02d}.png").convert("RGBA") for index in range(6)]

    command = [
        ffmpeg, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{width}x{height}",
        "-r", str(fps), "-i", "-", "-f", "lavfi", "-i",
        f"anoisesrc=color=pink:amplitude=0.012:sample_rate=48000:duration={seconds}",
        "-filter_complex", "[1:a]lowpass=f=900,highpass=f=70,afade=t=in:d=1,afade=t=out:st=11:d=1[a]",
        "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(OUTPUT),
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    assert process.stdin is not None

    total = fps * seconds
    for frame_number in range(total):
        time_s = frame_number / fps

        # Background track: slow push and side drift, independent of GR.
        zoom = 1.03 + 0.045 * (time_s / seconds)
        pan = 0.12 * math.sin(time_s * 0.22)
        scene = cover_crop(background, width, height, zoom, pan).convert("RGBA")

        # Character track: a broad figure-eight route with perspective depth.
        route = time_s / seconds * math.tau
        x = width * 0.50 + width * 0.36 * math.sin(route)
        depth = 0.5 + 0.5 * math.sin(route * 2.0 - math.pi / 2.0)
        ground_y = 570 - 115 * depth
        sprite_height = round(350 + 105 * depth)
        sprite_index = int(time_s * 10) % len(sprites)
        sprite = sprites[sprite_index]
        sprite_width = round(sprite.width * sprite_height / sprite.height)
        sprite = sprite.resize((sprite_width, sprite_height), Image.Resampling.LANCZOS)

        # A separate shadow makes travel across the ground readable.
        shadow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        shadow = ImageDraw.Draw(shadow_layer)
        shadow_width = sprite_width * (0.52 + 0.18 * depth)
        shadow.ellipse(
            (x - shadow_width / 2, ground_y - 10, x + shadow_width / 2, ground_y + 18),
            fill=(0, 0, 0, 105),
        )
        shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(11))
        scene.alpha_composite(shadow_layer)

        bob = abs(math.sin(time_s * 10 * math.pi / 3)) * 8
        left = round(x - sprite_width / 2)
        top = round(ground_y - sprite_height - bob)
        scene.alpha_composite(sprite, (left, top))

        # Foreground fireflies sit above both tracks and reinforce parallax.
        fx = ImageDraw.Draw(scene, "RGBA")
        for index in range(18):
            px = (index * 179 + time_s * (13 + index % 4)) % width
            py = 85 + (index * 97) % 510 + math.sin(time_s * 1.3 + index) * 10
            radius = 1 + index % 3
            fx.ellipse((px - radius, py - radius, px + radius, py + radius), fill=(255, 214, 91, 80 + 30 * (index % 3)))

        process.stdin.write(scene.convert("RGB").tobytes())

    process.stdin.close()
    if process.wait() != 0:
        raise RuntimeError("ffmpeg encoding failed")
    return OUTPUT


if __name__ == "__main__":
    print(render())
