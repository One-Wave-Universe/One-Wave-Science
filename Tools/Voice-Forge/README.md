# One-Wave Voice Forge

## Purpose
A standalone character-voice design program. It is separate from the animator. The animator only receives finished dialogue clips plus timing metadata.

## Core rule
Do not begin from a canned TTS/machine voice and hide it with effects. Voice Forge must work from recorded/reference human voices the user has permission to use, or from original generated base voices designed for the project.

Do not clone or impersonate an identifiable real person's voice without authorization. A celebrity/reference can be used as a descriptive target or inspiration, but the saved result should be an original character voice unless rights/permission are available.

## Character voice pipeline
1. Import 1-4 reference takes.
2. Analyze each reference separately.
3. Separate controllable traits instead of baking them together:
   - pitch contour
   - formant / apparent vocal-tract size
   - resonance / body
   - brightness
   - breath / air
   - rasp / grit
   - nasality
   - articulation sharpness
   - speaking rate
   - timing / pause profile
   - dynamics
   - vibrato / instability
4. Blend references by trait, not just waveform volume.
5. Allow continuous A/B blend controls per trait.
6. Apply character finishing:
   - high/low cut
   - body EQ
   - presence
   - de-esser
   - compressor
   - saturation / drive
   - optional doubler
   - optional delay
   - plate/spring/room reverb slots
7. Save a reusable character recipe.
8. Render a clean dialogue file plus metadata for the animator.

## Required controls
- Reference A amount
- Reference B amount
- Optional Reference C/D amount
- Pitch shift
- Formant shift independent of pitch
- Body / chest resonance
- Brightness / presence
- Breathiness
- Rasp / grit
- Nasality
- Articulation
- Timing stretch without pitch change
- Micro-pitch instability
- Layer/doubler amount
- Stereo width
- Dry/wet
- Output gain

## Voice-combiner behavior
The combiner is non-destructive. Each reference stays intact. A character recipe stores trait weights and processing settings. Rendering can always be repeated from the originals.

The program must support:
- solo/mute each source
- A/B instant comparison
- randomize within safe ranges
- save named presets
- lock selected traits while changing others
- undo/redo
- render WAV
- render stem layers
- export a compact recipe JSON alongside the WAV

## Animator handoff
Voice Forge exports:
- dialogue.wav
- dialogue.recipe.json
- optional stems/

The animator imports the finished clip and places it on the reel timeline. The animator must not own voice synthesis internals.

## First implementation target
Desktop/local-first program for Ubuntu/Jetson-compatible environments where possible. Heavy neural inference may run on GPU; basic editing, analysis, mixing, and rendering must work locally without cloud tokens.

## Hard stop for Phase 1
Phase 1 is complete only when two authorized human reference recordings can be loaded, blended with independent pitch/formant/body/brightness controls, previewed A/B, saved as a recipe, and rendered to WAV without using a canned TTS voice as the source.

## Implementation status (Phase 1)

Phase 1 is implemented as a local Python/PySide6 desktop app plus a
headless engine package usable from a script or another program.

```
Voice-Forge/
  engine/         DSP core: no Qt dependency, fully unit-testable.
    io_utils.py     load/save WAV, mono conversion, resampling
    analysis.py     LPC spectral-envelope + pitch estimation
    dsp.py          pitch/formant tools, EQ, dynamics, breath/rasp,
                     de-esser, delay, reverb, doubler, stereo width
    blend.py        trait-based cross-synthesis blend of 2-4 references
    recipe.py       the reusable JSON "character recipe" schema
    pipeline.py     load -> blend -> pitch/formant -> character ->
                     finishing -> render, plus stem/handoff export
  app/            PySide6 GUI (main_window, sliders, undo/redo, preview)
  api/            FastAPI HTTP surface: find/create voice profiles from
                  a recording or video, combine two into a new voice --
                  what a ChatGPT Custom GPT Action plugs into
  tools/          make_sample_voices.py: synthesizes two original demo
                  reference voices so the tool can be tried without any
                  real recordings
  tests/          pytest suite for the engine, the API, and a headless
                  GUI smoke test
```

### How the blend works

Each reference is decomposed (via per-frame LPC) into an excitation
("residual") and a spectral envelope (formants). References are time-
aligned to one chosen "timing source," their envelopes are combined with
a weighted log-magnitude average, and their excitations are combined
with a weighted sum -- so a blend mixes vocal-tract character and
excitation character independently, per the "blend by trait, not just
waveform volume" rule above. Pitch shift acts on the excitation only;
formant shift warps the envelope's frequency axis only -- so the two
controls are independent of each other. A recipe never stores rendered
audio, only trait weights and references to the original files, so
re-rendering the same recipe from the same originals is exact.

### Setup

```
cd Tools/Voice-Forge
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

PySide6's Qt platform plugins need a few system libraries that aren't
always preinstalled on a minimal Linux desktop/server image:
`libegl1 libgl1 libxkbcommon0` (windowing) and `libpulse0` (audio
playback for the in-app preview). On Debian/Ubuntu/Jetson:
`sudo apt-get install libegl1 libgl1 libxkbcommon0 libpulse0`. Rendering
to WAV works without these; only the on-screen window and audio preview
need them.

### Run the GUI

```
python tools/make_sample_voices.py   # optional: generate two demo reference voices
python main.py
```

Load two (or up to four) reference WAV files into Ref A/B/C/D, adjust
the blend amount per reference and the trait/finishing sliders, use
"Preview current" or the A/B "Snapshot"/"Play" buttons to audition, then
"Render..." to write the Animator handoff bundle to a folder you choose.

### Use the engine headlessly (from a script or another program)

```python
from engine.recipe import Recipe
from engine import pipeline

recipe = Recipe.default_two_source("voice_a.wav", "voice_b.wav", name="My Blended Voice")
recipe.traits.pitch_semitones = -2.0
recipe.traits.formant_ratio = 1.1

result = pipeline.render_recipe(recipe, render_stems=True)
pipeline.export(result, "out/", recipe)  # writes dialogue.wav, dialogue.recipe.json, stems/
```

The rendered `dialogue.wav` is a plain stereo float WAV -- it can be
dropped into any other program or app (a DAW, a game engine, a TTS
front-end that accepts a reference voice, the One-Wave Animator, etc.)
just like any other audio file. `dialogue.recipe.json` is the reusable,
non-destructive recipe: reopen it in Voice Forge to keep tuning the same
blend from the original references.

### Tests

```
pip install pytest
pytest tests/
```

The GUI smoke test uses `pytest.importorskip("PySide6")` and Qt's
`offscreen` platform plugin, matching the One-Wave Animator's test
pattern, so the engine tests still run even where the GUI's system
libraries aren't installed.

### ChatGPT integration (HTTP API)

`api/` exposes the engine over HTTP so an external caller -- a Custom GPT
Action, or anything else that can make HTTPS calls -- can find or create
voice profiles from a recording or video, and combine two of them into a
new voice it can play back. It's a thin wrapper: every request just
builds a `Recipe` and calls `pipeline.render_recipe`, same as the GUI.

Voice profiles are stored under `library/` (one directory per voice,
holding its reference audio) with a JSON index; combined renders are
served back over HTTP so a caller gets a URL, not a binary blob.

#### Setup

```
cd Tools/Voice-Forge
pip install -r requirements.txt -r requirements-api.txt
```

Uploads go through `ffmpeg` first (so any audio *or video* container --
mp4, mov, m4a, mp3, whatever a phone or export tool produces -- works,
not just WAV): `sudo apt-get install ffmpeg`.

#### Run it

```
export VOICE_FORGE_API_KEY=choose-a-long-random-value   # omit only for local-only testing
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

This must be reachable over **HTTPS** at a stable public URL for a
Custom GPT Action to call it -- for a quick test, tunnel it (e.g. `ngrok
http 8000`); for anything real, deploy it behind a proper reverse proxy
(Fly.io, Render, your own VPS with Caddy/nginx, etc.). This repo doesn't
include that hosting step -- it's wherever you already deploy things.

#### Wire it into a Custom GPT

In the GPT builder: **Configure -> Actions -> Create new action**, then
**Import from URL** with `https://your-host/openapi.json` (FastAPI
generates this automatically). Set Authentication to **API Key**, header
name `X-API-Key`, value matching `VOICE_FORGE_API_KEY`. That's it --
ChatGPT reads the three operations below from the schema itself.

#### Endpoints

| Method | Path | operationId | Does |
|---|---|---|---|
| POST | `/voices` | `createVoiceProfile` | Upload a recording or video; extracts and saves the voice |
| GET | `/voices?query=...` | `findVoiceProfiles` | Search saved voices by name/description/tag |
| GET | `/voices/{id}` | `getVoiceProfile` | Fetch one voice profile |
| DELETE | `/voices/{id}` | `deleteVoiceProfile` | Remove a saved voice profile |
| POST | `/voices/combine` | `combineVoiceProfiles` | Blend two voices, render a WAV, optionally save the result as a new voice |

`combine` accepts the same trait controls as the GUI (pitch, formant,
body, brightness, breathiness, rasp, nasality, articulation, dry/wet,
output gain) and returns `audio_url` pointing at the rendered file, plus
`saved_voice` if `save_as_name` was given -- so "combine this voice and
that voice" can also become a new findable voice in one call, matching
the original ask: find this voice and this voice, combine them, and
hear it.

```bash
curl -X POST https://your-host/voices \
  -H "X-API-Key: $VOICE_FORGE_API_KEY" \
  -F "file=@grandpa.mp4" -F "name=Grandpa" -F "tags=warm,narrator"

curl https://your-host/voices?query=grandpa -H "X-API-Key: $VOICE_FORGE_API_KEY"

curl -X POST https://your-host/voices/combine \
  -H "X-API-Key: $VOICE_FORGE_API_KEY" -H "Content-Type: application/json" \
  -d '{"voice_id_a":"<id_a>","voice_id_b":"<id_b>","amount_a":0.6,"amount_b":0.4,"save_as_name":"Blended Narrator"}'
```

### One-click install (Ubuntu desktop app)

To get an actual installable desktop app instead of running from
source -- a Desktop icon plus an Applications-menu entry, no
`python`/`pip` needed afterwards -- run one script:

```
Tools/Voice-Forge/install.sh
```

That's it. It builds a standalone binary the first time (takes a
minute or two), installs it to `~/.local/share/voiceforge/`, and drops
a "One-Wave Voice Forge" icon on your Desktop and in your Applications
menu -- no sudo, no system-wide changes. Running it again later just
reinstalls instantly (it only rebuilds if there's no build yet, or if
you pass `--rebuild`). To remove everything it installed:

```
Tools/Voice-Forge/uninstall.sh
```

If the Desktop icon shows a warning instead of launching the first
time you double-click it (a GNOME/Nautilus quirk for new desktop
files), right-click it and choose "Allow Launching" -- the installer
already tries to mark it trusted automatically via `gio`, but not every
desktop environment honors that.

Under the hood, `install.sh` is `packaging/build_ubuntu.sh` (builds
`dist/VoiceForge/` with PyInstaller, bundling the Python/Qt runtime)
followed by `packaging/install_ubuntu.sh` (copies it into your account
and writes the two `.desktop` launchers); run those directly if you
want the build and install steps separately.

This is source-built packaging, not a signed/notarized release: the
built binary still needs the same runtime system libraries as running
from source (see Setup above) -- normal on a standard Ubuntu desktop,
not guaranteed on a minimal server image. `build_ubuntu.sh` checks for
them and tells you the `apt-get install` command if any are missing.
