"""Persistent voice-profile library used by the HTTP API.

Every saved voice is a directory under the library root:

    library/<id>/source.wav   -- the reference audio (extracted/normalized)
    library/index.json        -- {id: metadata} for every saved voice
    library/renders/<token>.wav -- rendered combine/render outputs, served
                                    back over HTTP so a caller (ChatGPT
                                    included) gets a URL, not a blob

This intentionally does not touch engine.recipe.Recipe -- a library entry
is a reusable *source*, not a tuned blend. Combining voices builds a
Recipe on the fly from two library entries' source.wav files.
"""
from __future__ import annotations

import datetime
import json
import os
import shutil
import uuid


class VoiceLibrary:
    def __init__(self, root: str):
        self.root = os.path.abspath(root)
        self.index_path = os.path.join(self.root, "index.json")
        os.makedirs(self.root, exist_ok=True)
        os.makedirs(os.path.join(self.root, "renders"), exist_ok=True)
        if not os.path.exists(self.index_path):
            self._write_index({})

    def _read_index(self) -> dict:
        with open(self.index_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_index(self, data: dict) -> None:
        with open(self.index_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def create(self, source_wav_path: str, sample_rate: int, duration_sec: float,
               name: str, description: str = "", tags: list | None = None,
               parent_ids: list | None = None) -> dict:
        voice_id = uuid.uuid4().hex[:12]
        voice_dir = os.path.join(self.root, voice_id)
        os.makedirs(voice_dir, exist_ok=True)
        dest_wav = os.path.join(voice_dir, "source.wav")
        shutil.copy(source_wav_path, dest_wav)

        meta = {
            "id": voice_id,
            "name": name,
            "description": description,
            "tags": tags or [],
            "sample_rate": sample_rate,
            "duration_sec": round(duration_sec, 3),
            "created_at": datetime.datetime.utcnow().isoformat() + "Z",
            "parent_ids": parent_ids or [],
        }
        index = self._read_index()
        index[voice_id] = meta
        self._write_index(index)
        return meta

    def get(self, voice_id: str) -> dict | None:
        return self._read_index().get(voice_id)

    def source_path(self, voice_id: str) -> str:
        return os.path.join(self.root, voice_id, "source.wav")

    def list(self, query: str | None = None) -> list:
        values = list(self._read_index().values())
        if query:
            q = query.lower()
            values = [
                v for v in values
                if q in v["name"].lower()
                or q in v.get("description", "").lower()
                or any(q in t.lower() for t in v.get("tags", []))
            ]
        return sorted(values, key=lambda v: v["created_at"], reverse=True)

    def delete(self, voice_id: str) -> bool:
        index = self._read_index()
        if voice_id not in index:
            return False
        del index[voice_id]
        self._write_index(index)
        shutil.rmtree(os.path.join(self.root, voice_id), ignore_errors=True)
        return True

    def save_render(self, audio, sample_rate: int) -> tuple[str, str]:
        from engine import io_utils

        token = uuid.uuid4().hex[:16]
        path = os.path.join(self.root, "renders", f"{token}.wav")
        io_utils.save_wav(path, audio, sample_rate)
        return token, path
