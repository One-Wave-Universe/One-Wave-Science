"""Turn any audio or video file into a clean mono WAV via ffmpeg.

Using ffmpeg unconditionally (rather than branching on file extension)
means uploads in whatever container/codec a phone, browser, or video
export produces (mp4, mov, webm, m4a, mp3, ...) all go through the same
path and land as a plain WAV the rest of the engine already knows how
to read with soundfile.
"""
from __future__ import annotations

import os
import subprocess
import tempfile


class AudioExtractionError(RuntimeError):
    pass


def extract_audio(path: str, target_sr: int = 44100) -> str:
    """Extract mono audio at target_sr into a new temp WAV file and return
    its path. The caller owns the returned file and should delete it."""
    fd, out_path = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    cmd = [
        "ffmpeg", "-y",
        "-i", path,
        "-vn",
        "-ac", "1",
        "-ar", str(target_sr),
        out_path,
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0 or not os.path.exists(out_path) or os.path.getsize(out_path) == 0:
        if os.path.exists(out_path):
            os.unlink(out_path)
        stderr_tail = result.stderr.decode(errors="replace")[-2000:]
        raise AudioExtractionError(f"ffmpeg could not extract audio from this file: {stderr_tail}")
    return out_path
