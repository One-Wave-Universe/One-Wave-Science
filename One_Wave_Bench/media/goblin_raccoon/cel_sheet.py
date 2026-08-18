"""Utilities for turning traditional cel sheets into discrete flipbook frames."""
from __future__ import annotations

import argparse
import base64
import io
import re
from pathlib import Path
from typing import Iterable

from PIL import Image

_DATA_URI = re.compile(r'href=["\']data:image/(?P<kind>png|jpeg|jpg|webp);base64,(?P<data>[^"\']+)', re.IGNORECASE)


def _open_sheet(path: str | Path) -> Image.Image:
    path = Path(path)
    if path.suffix.lower() != ".svg":
        return Image.open(path).convert("RGBA")

    text = path.read_text(encoding="utf-8")
    match = _DATA_URI.search(text)
    if not match:
        raise ValueError("SVG sheet does not contain an embedded PNG/JPEG/WebP image")
    payload = base64.b64decode(match.group("data"))
    return Image.open(io.BytesIO(payload)).convert("RGBA")


def slice_sheet(
    sheet: str | Path,
    output_dir: str | Path,
    *,
    columns: int = 4,
    rows: int = 3,
    count: int | None = None,
    prefix: str = "frame",
) -> list[Path]:
    """Slice a regular cel sheet left-to-right, top-to-bottom.

    The source is never modified. SVG wrappers with embedded raster artwork are
    decoded directly, which matches the existing Goblin Raccoon 12-cel sheets.
    """
    if columns < 1 or rows < 1:
        raise ValueError("columns and rows must be positive")
    maximum = columns * rows
    frame_count = maximum if count is None else int(count)
    if not 1 <= frame_count <= maximum:
        raise ValueError(f"count must be between 1 and {maximum}")

    image = _open_sheet(sheet)
    if image.width % columns or image.height % rows:
        raise ValueError(
            f"sheet size {image.width}x{image.height} is not evenly divisible by {columns}x{rows}"
        )

    cell_w = image.width // columns
    cell_h = image.height // rows
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    for index in range(frame_count):
        row, col = divmod(index, columns)
        frame = image.crop((col * cell_w, row * cell_h, (col + 1) * cell_w, (row + 1) * cell_h))
        target = output_dir / f"{prefix}_{index + 1:02d}.png"
        frame.save(target, "PNG")
        written.append(target)
    return written


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Slice a cel sheet into numbered PNG flipbook frames.")
    parser.add_argument("sheet")
    parser.add_argument("output_dir")
    parser.add_argument("--columns", type=int, default=4)
    parser.add_argument("--rows", type=int, default=3)
    parser.add_argument("--count", type=int)
    parser.add_argument("--prefix", default="frame")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = _parser().parse_args(list(argv) if argv is not None else None)
    for path in slice_sheet(
        args.sheet,
        args.output_dir,
        columns=args.columns,
        rows=args.rows,
        count=args.count,
        prefix=args.prefix,
    ):
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
