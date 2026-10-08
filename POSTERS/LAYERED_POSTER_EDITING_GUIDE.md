# One-Wave Science posters — editable layer workflow

**Purpose:** Create and correct scientific posters without regenerating the entire image. This is the canonical operating guide for the five-poster Science communication series. Scientific content must still be checked against the canonical Science nodes and equations; the posters explain the One-Wave viewpoint rather than display repository metadata.

## Current Poster 2 prototype and verification

A first editable-layer starter was generated as `One_Wave_Poster_2_Editable_Layers.zip`. The archive was checked for integrity, its SVG parsed as valid XML, and it contains 71 individual SVG text elements. **This confirms structural editability, not that all diagrams, claims, or typography have been reviewed or that an editor installation was tested.**

Archive contents:
- `Poster_2_EDITABLE.svg` — **primary editable source**; contains separate vector/text elements.
- `Poster_2_PREVIEW.png` — flattened preview, **not** the editing source.
- `01_Background.png`, `02_Panel_Grid.png`, `03_Illustrations.png`, `04_Equations.png`, `05_Text.png` — transparent raster layer exports for compositing/reference.
- `README.txt` — starter notes.

The starter is a simplified rebuild, **not** a verified replacement for the original detailed Poster 2. Do not substitute it as the publication master until scientific and visual checks pass.

## Edit one item without disturbing the poster

1. Open the SVG in **Inkscape** (preferred) or another SVG-capable editor. Do **not** edit the preview PNG.
2. Save a working SVG revision; keep the prior version in Git history rather than maintaining competing permanent copies.
3. Select the target text or vector object. In Inkscape, use the Text tool for text and the Select/Node tools for shapes. If a selection is grouped, enter the group before editing; avoid ungrouping the entire poster.
4. Make the smallest correction. Example: replace an erroneous octave-halving caption `frequency ×2` with `frequency ÷2` while preserving its position.
5. Verify adjacent labels, equations, geometry, clipping, and line breaks. In particular check six planar directions/opposite pairs; twelve distinct 3D neighbors; and pure-fifth `3:2` versus equal-tempered `2^(7/12)`.
6. Save the SVG. Export a fresh PNG from the **saved SVG** at full page size, then visually compare before/after.
7. Confirm unrelated regions are unchanged. Record the correction and validation receipt in the relevant PR.

**No full-image regeneration for local text fixes.** Generate new diagram art separately on a transparent layer, then integrate only that component.

## Open / export on Ubuntu

Install an SVG editor using your system's authorized package workflow if not installed. For Ubuntu with working apt privileges, a typical command is:

```bash
sudo apt update && sudo apt install inkscape
```

The installation above is **an instruction, not a claim that it has been run**. Open the SVG:

```bash
inkscape Poster_2_EDITABLE.svg
```

Export an updated PNG:

```bash
inkscape Poster_2_EDITABLE.svg --export-filename=Poster_2_FINAL.png
```

For a quick structural check with Python:

```bash
python3 - <<'PY'
import xml.etree.ElementTree as ET
root = ET.parse('Poster_2_EDITABLE.svg').getroot()
print('SVG OK:', root.tag)
PY
```

## New poster construction — never start with a flattened master

1. Start from a versioned SVG or other genuinely layered master.
2. Keep background, borders/panels, illustrations, captions, equations, and footer separately editable. Text and equations must remain editable text/vector objects, not baked into an illustration PNG.
3. Keep each scientific diagram as an independent group/layer. When raster illustration is unavoidable, use a transparent PNG for that **diagram only**.
4. Lock dimensions, margins, palette, typography, and the five-poster visual identity before composing.
5. Reference `GENERAL_REFERENCE_RULES.md` and `AI_CANONICAL_START_HERE.md`; consult domain authorities for science. Do not invent node IDs or silently upgrade hypotheses to established results.
6. Communicate the One-Wave viewpoint plainly; use a short proposed/unverified qualifier for mechanisms not experimentally established.
7. Validate math and labels *before* raster export. Use a short correction checklist, not a fresh whole-poster prompt.
8. Use a task branch and PR, keep the authoritative master in the canonical Science repository, and store preview/export assets beside it if publication requires them. Avoid permanent duplicate checkouts or maintained local copies.

## Poster 2 content acceptance

The poster explains how the proposed continuous medium organizes through Ground/Zero, displacement, three rotations (Point/Path/Field), three differentials (local/path/field), three coupling classes (intersecting/mirrored/parallel), Field/Void, mirror polarity, sixfold planar and twelvefold 3D coordination, 0D–4D mathematical distinctions, proposed 3–6–12–24 nesting, octave scaling, circle of fifths, phase, closure, retained state, and micro–macro recursion.

- The **nine-relationship interaction** is the largest explanatory diagram.
- No internal forced clock/interval is implied by the drawing.
- `3 > 1(0)1 < 6`, `6 > 1(0)1 < 12`, and `12 > 1(0)1 < 24` are **proposed mappings**, not derived dimensional laws.
- Distinguish mathematical dimension, lattice neighbor count, and recurrence-state count.
- The role of four as a connector is open, not established.
- Distinguish geometric compression (many relations represented by a resolved whole) from physical compression (e.g. `χ = −∇·u`).
- Show octave doubling **and halving**, and distinguish a pure fifth `3:2` from equal temperament `2^(7/12)`.
- Show micro–macro recurrence as a proposed *relationship across scales*, not identical geometry or mechanism.
- Final QA: zoom to inspect small text; inspect geometry; compare unchanged regions; render/export; record actual results.

## Authority and location

This guide lives in the canonical **One-Wave Science** repo. Other repos (Builds, Bridge-Command), machines, and agents should link to it rather than maintain a competing guide. Do not confuse the downloadable starter ZIP with a committed canonical poster master: the poster files must be deliberately added and reviewed before being treated as repo assets.
