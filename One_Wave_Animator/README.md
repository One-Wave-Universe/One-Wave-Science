# One-Wave Animator

A simple Windows desktop cartoon-making program.

## Step 1 — Scene Editor

This first milestone is a working scene editor:

- Import **one background** image (PNG/JPG) — the canvas resizes to match it.
- Import any number of **transparent PNG characters** on top of it.
- **Drag** characters around the canvas.
- **Resize** a selected character from its bottom-right handle, aspect ratio locked.
- Reorder characters front-to-back from the **Layers** panel (or `Ctrl+]` / `Ctrl+[`).
- **Delete** a selected character (`Delete` key, or the Layers panel button).
- **Save** a scene to a `.owascene` (JSON) file and **reopen** it exactly as saved.
- **Export an animation clip**: each character layer becomes one frame (bottom
  layer = frame 1, in the order shown in the Layers panel), composited over
  the fixed background, and written out as an animated GIF (`Animation` menu,
  `Ctrl+E`). Import several pose images of the same character at the same
  spot, order them in the Layers panel, and export — no drawing/tweening yet,
  this cycles between whole poses.

No drawing or tweening tools yet — that comes in a later step.

## Requirements

- Python 3.9+
- [PySide6](https://pypi.org/project/PySide6/) (Qt for Python)
- [Pillow](https://pypi.org/project/Pillow/) (GIF animation export)

```bash
pip install -r requirements.txt
```

## Running

```bash
python main.py
```

Sample assets to try it with live in `assets/sample/` (`sample_background.png`,
`sample_character.png`). Regenerate them any time with:

```bash
python tools/make_sample_assets.py
```

## Running the tests

```bash
pip install pytest
pytest tests/
```

`tests/test_scene_model.py` covers the JSON scene format (pure Python, no
display needed). `tests/test_gui_smoke.py` and `tests/test_multi_character_workflow.py`
exercise the import → drag → resize → reorder → delete → save → reopen
workflow against real Qt objects, headlessly, via the `offscreen` Qt platform
plugin. `tests/test_gif_export.py` covers the QImage-frames-to-GIF encoding
in isolation; `tests/test_animation_export.py` covers the full Animation-menu
export path end to end, verifying real frame order and pixel content.

## Project layout

```
main.py                  Entry point
app/
  scene_model.py         Plain-Python Scene/BackgroundLayer/CharacterLayer + JSON I/O
  graphics_items.py      QGraphicsItem subclasses: BackgroundItem, CharacterItem
  canvas_view.py          SceneCanvas(QGraphicsView): the editable scene
  layers_panel.py        Layers dock widget (reorder / delete)
  main_window.py          Menus, dirty-state tracking, open/save dialogs, animation export
  gif_export.py          QImage-list -> animated GIF encoding (Pillow)
tools/make_sample_assets.py  Generates the placeholder sample images
assets/sample/            Sample background + character PNGs
tests/                    Unit + headless GUI smoke tests
```

## Scene file format

A `.owascene` file is JSON. Image paths are stored relative to the scene
file when they live alongside it (so a scene folder stays portable if
moved together with its images), and as absolute paths otherwise:

```json
{
  "format_version": 1,
  "canvas": { "width": 800, "height": 450 },
  "background": { "path": "assets/sample_background.png", "width": 800, "height": 450 },
  "characters": [
    { "path": "assets/sample_character.png", "x": 120, "y": 80, "width": 200, "height": 320, "z": 1 }
  ]
}
```

## Packaging a Windows .exe

This app runs on Windows as-is once dependencies are installed. To produce
a standalone `.exe` (run this step **on Windows**, from this folder):

```bash
pip install pyinstaller
pyinstaller --noconsole --onefile --name "One-Wave Animator" main.py
```

The executable is written to `dist/One-Wave Animator.exe`.
