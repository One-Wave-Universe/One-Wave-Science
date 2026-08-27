"""HTTP API for Voice Forge: the surface a Custom GPT Action (or any other
external caller) plugs into to find or create voice profiles from
recordings/video, and to blend two of them into a new voice.

Run with:
    uvicorn api.main:app --host 0.0.0.0 --port 8000

Set VOICE_FORGE_API_KEY to require an `X-API-Key` header on every request
(recommended for anything reachable from the internet). See
Tools/Voice-Forge/README.md "ChatGPT integration" for deployment and
Custom GPT Action setup.
"""
from __future__ import annotations

import os
import shutil
import tempfile
from typing import Optional

from fastapi import Depends, FastAPI, File, Form, Header, HTTPException, Request, UploadFile
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from engine import io_utils, pipeline, video_utils
from engine.recipe import Recipe, SourceEntry

from .library import VoiceLibrary

API_KEY = os.environ.get("VOICE_FORGE_API_KEY")
LIBRARY_ROOT = os.environ.get(
    "VOICE_FORGE_LIBRARY", os.path.join(os.path.dirname(__file__), "..", "library")
)

library = VoiceLibrary(LIBRARY_ROOT)

app = FastAPI(
    title="One-Wave Voice Forge API",
    description=(
        "Create reusable voice profiles from an uploaded recording or video, "
        "find saved voice profiles again, and blend two of them into a new "
        "voice you can render and play back."
    ),
    version="1.0.0",
)


def require_api_key(x_api_key: Optional[str] = Header(None)) -> bool:
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return True


class VoiceProfile(BaseModel):
    id: str
    name: str
    description: str = ""
    tags: list[str] = []
    sample_rate: int
    duration_sec: float
    created_at: str
    parent_ids: list[str] = []


class CombineRequest(BaseModel):
    voice_id_a: str = Field(..., description="Library id of the first voice")
    voice_id_b: str = Field(..., description="Library id of the second voice")
    amount_a: float = Field(0.5, ge=0, le=1, description="Blend weight for voice A (0-1)")
    amount_b: float = Field(0.5, ge=0, le=1, description="Blend weight for voice B (0-1)")
    pitch_semitones: float = Field(0.0, ge=-12, le=12, description="Pitch shift in semitones")
    formant_ratio: float = Field(1.0, ge=0.7, le=1.5, description="Formant/vocal-tract-size shift, independent of pitch")
    body_db: float = Field(0.0, ge=-12, le=12, description="Chest resonance boost/cut in dB")
    brightness_db: float = Field(0.0, ge=-12, le=12, description="Presence/brightness boost/cut in dB")
    breathiness: float = Field(0.0, ge=0, le=1, description="Added breath amount, 0-1")
    rasp: float = Field(0.0, ge=0, le=1, description="Added rasp/grit amount, 0-1")
    nasality_db: float = Field(0.0, ge=-12, le=12, description="Nasality boost/cut in dB")
    articulation: float = Field(0.0, ge=0, le=1, description="Consonant/transient clarity, 0-1")
    dry_wet: float = Field(1.0, ge=0, le=1, description="0 = original references, 1 = fully processed blend")
    output_gain_db: float = Field(0.0, ge=-24, le=12, description="Final output gain in dB")
    save_as_name: Optional[str] = Field(
        None, description="If set, save the combined result as a new reusable voice profile with this name"
    )
    save_as_description: str = ""
    save_as_tags: list[str] = []


class CombineResponse(BaseModel):
    audio_url: str = Field(..., description="URL to the rendered WAV of the combined voice")
    saved_voice: Optional[VoiceProfile] = Field(None, description="The new voice profile, if save_as_name was set")


@app.get("/", include_in_schema=False)
def root():
    return {"service": "One-Wave Voice Forge API", "docs": "/docs", "openapi": "/openapi.json"}


@app.post(
    "/voices",
    response_model=VoiceProfile,
    operation_id="createVoiceProfile",
    summary="Create a voice profile from an uploaded recording or video",
    description=(
        "Upload an audio or video file containing one person's/character's voice. "
        "The audio track is extracted and normalized, then saved as a reusable "
        "voice profile that can be found later or combined with another voice."
    ),
    dependencies=[Depends(require_api_key)],
)
async def create_voice(
    file: UploadFile = File(..., description="Audio or video file containing the reference voice"),
    name: str = Form(..., description="Human-readable name for this voice, e.g. 'Grandpa 1998 tape'"),
    description: str = Form("", description="Optional free-text description"),
    tags: str = Form("", description="Optional comma-separated tags, e.g. 'male,warm,narrator'"),
):
    suffix = os.path.splitext(file.filename or "upload")[1] or ".bin"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        wav_path = video_utils.extract_audio(tmp_path)
    except video_utils.AudioExtractionError as exc:
        raise HTTPException(status_code=400, detail=f"Could not read audio from upload: {exc}")
    finally:
        os.unlink(tmp_path)

    try:
        y, sr = io_utils.load_audio(wav_path)
        if len(y) < sr * 0.2:
            raise HTTPException(status_code=400, detail="Extracted audio is too short to use as a voice profile")
        duration = len(y) / sr
        tag_list = [t.strip() for t in tags.split(",") if t.strip()]
        meta = library.create(wav_path, sr, duration, name, description, tag_list)
    finally:
        os.unlink(wav_path)

    return meta


@app.get(
    "/voices",
    response_model=list[VoiceProfile],
    operation_id="findVoiceProfiles",
    summary="Find saved voice profiles by name, description, or tag",
    dependencies=[Depends(require_api_key)],
)
def find_voices(query: Optional[str] = None):
    return library.list(query)


@app.get(
    "/voices/{voice_id}",
    response_model=VoiceProfile,
    operation_id="getVoiceProfile",
    summary="Get one saved voice profile by id",
    dependencies=[Depends(require_api_key)],
)
def get_voice(voice_id: str):
    meta = library.get(voice_id)
    if not meta:
        raise HTTPException(status_code=404, detail="Voice profile not found")
    return meta


@app.delete(
    "/voices/{voice_id}",
    operation_id="deleteVoiceProfile",
    summary="Delete a saved voice profile",
    dependencies=[Depends(require_api_key)],
)
def delete_voice(voice_id: str):
    if not library.delete(voice_id):
        raise HTTPException(status_code=404, detail="Voice profile not found")
    return {"deleted": voice_id}


@app.post(
    "/voices/combine",
    response_model=CombineResponse,
    operation_id="combineVoiceProfiles",
    summary="Blend two saved voice profiles into a new voice and render it to a playable WAV",
    description=(
        "Combines two previously created voice profiles by trait (pitch, formant, "
        "body, brightness, breathiness, etc.), renders the result to a WAV file, "
        "and returns a URL to it. Optionally saves the combined voice as a new "
        "profile so it can be found and reused later."
    ),
    dependencies=[Depends(require_api_key)],
)
def combine_voices(req: CombineRequest, request: Request):
    meta_a = library.get(req.voice_id_a)
    meta_b = library.get(req.voice_id_b)
    if not meta_a or not meta_b:
        raise HTTPException(status_code=404, detail="One or both voice profiles were not found")

    recipe = Recipe(
        name=req.save_as_name or f"{meta_a['name']} + {meta_b['name']}",
        sample_rate=max(meta_a["sample_rate"], meta_b["sample_rate"]),
        sources=[
            SourceEntry(id="A", path=library.source_path(req.voice_id_a), amount=req.amount_a),
            SourceEntry(id="B", path=library.source_path(req.voice_id_b), amount=req.amount_b),
        ],
        timing_source_id="A",
    )
    t = recipe.traits
    t.pitch_semitones = req.pitch_semitones
    t.formant_ratio = req.formant_ratio
    t.body_db = req.body_db
    t.brightness_db = req.brightness_db
    t.breathiness = req.breathiness
    t.rasp = req.rasp
    t.nasality_db = req.nasality_db
    t.articulation = req.articulation
    t.dry_wet = req.dry_wet
    t.output_gain_db = req.output_gain_db

    try:
        result = pipeline.render_recipe(recipe, base_dir=None, render_stems=False)
    except Exception as exc:  # noqa: BLE001 - surface any DSP error to the caller
        raise HTTPException(status_code=500, detail=f"Render failed: {exc}")

    token, render_path = library.save_render(result.audio, result.sr)
    audio_url = f"{str(request.base_url).rstrip('/')}/files/{token}.wav"

    saved_voice = None
    if req.save_as_name:
        mono = result.audio.mean(axis=1)
        saved_voice = library.create(
            render_path,
            result.sr,
            len(mono) / result.sr,
            req.save_as_name,
            req.save_as_description,
            req.save_as_tags,
            parent_ids=[req.voice_id_a, req.voice_id_b],
        )

    return CombineResponse(audio_url=audio_url, saved_voice=saved_voice)


app.mount("/files", StaticFiles(directory=os.path.join(LIBRARY_ROOT, "renders")), name="files")
