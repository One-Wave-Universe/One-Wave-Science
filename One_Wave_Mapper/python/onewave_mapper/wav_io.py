"""Minimal RIFF/WAV reader and writer supporting PCM16 and IEEE float32
(Section 2.1, 21.1).

The standard library `wave` module cannot write the IEEE-float format
(format code 3) that Section 5.1 requires for 32-bit-float capture, so
this module builds and parses RIFF chunks directly. It never resamples,
normalizes, or otherwise modifies samples on write -- the caller's array
is written byte-for-byte after format conversion only.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass

import numpy as np

PCM_FORMAT = 1
IEEE_FLOAT_FORMAT = 3


@dataclass
class WavData:
    samples: np.ndarray  # shape (n_samples, n_channels), float64 normalized to [-1, 1]
    sample_rate: int
    original_bit_depth: int
    original_format: int  # PCM_FORMAT or IEEE_FLOAT_FORMAT


def write_wav(path: str, samples: np.ndarray, sample_rate: int, bit_depth: str = "float32") -> None:
    """samples: shape (n_samples, n_channels) or (n_samples,) mono, values in [-1, 1]."""
    if samples.ndim == 1:
        samples = samples.reshape(-1, 1)
    elif samples.ndim != 2:
        raise ValueError("samples must be 1-D (mono) or 2-D (n_samples, n_channels)")

    n_samples, n_channels = samples.shape

    if bit_depth == "pcm16":
        audio_format = PCM_FORMAT
        bits_per_sample = 16
        data = np.clip(samples, -1.0, 1.0)
        data = (data * 32767.0).astype("<i2")
        data_bytes = data.tobytes()
    elif bit_depth == "pcm32":
        audio_format = PCM_FORMAT
        bits_per_sample = 32
        data = np.clip(samples, -1.0, 1.0)
        data = (data * 2147483647.0).astype("<i4")
        data_bytes = data.tobytes()
    elif bit_depth == "float32":
        audio_format = IEEE_FLOAT_FORMAT
        bits_per_sample = 32
        data = samples.astype("<f4")
        data_bytes = data.tobytes()
    elif bit_depth == "float64":
        audio_format = IEEE_FLOAT_FORMAT
        bits_per_sample = 64
        data = samples.astype("<f8")
        data_bytes = data.tobytes()
    else:
        raise ValueError(f"unsupported bit_depth: {bit_depth}")

    block_align = n_channels * bits_per_sample // 8
    byte_rate = sample_rate * block_align

    fmt_chunk = struct.pack(
        "<HHIIHH", audio_format, n_channels, sample_rate, byte_rate, block_align, bits_per_sample
    )

    chunks = b"fmt " + struct.pack("<I", len(fmt_chunk)) + fmt_chunk
    chunks += b"data" + struct.pack("<I", len(data_bytes)) + data_bytes

    if audio_format == IEEE_FLOAT_FORMAT:
        fact_chunk = struct.pack("<I", n_samples)
        chunks += b"fact" + struct.pack("<I", len(fact_chunk)) + fact_chunk

    riff_size = 4 + len(chunks)
    header = b"RIFF" + struct.pack("<I", riff_size) + b"WAVE"

    with open(path, "wb") as f:
        f.write(header + chunks)


def read_wav(path: str) -> WavData:
    with open(path, "rb") as f:
        raw = f.read()

    if raw[0:4] != b"RIFF" or raw[8:12] != b"WAVE":
        raise ValueError(f"not a RIFF/WAVE file: {path}")

    pos = 12
    fmt = None
    data_bytes = None

    while pos < len(raw) - 8:
        chunk_id = raw[pos:pos + 4]
        chunk_size = struct.unpack("<I", raw[pos + 4:pos + 8])[0]
        chunk_body = raw[pos + 8: pos + 8 + chunk_size]

        if chunk_id == b"fmt ":
            audio_format, n_channels, sample_rate, byte_rate, block_align, bits_per_sample = \
                struct.unpack("<HHIIHH", chunk_body[:16])
            fmt = dict(audio_format=audio_format, n_channels=n_channels, sample_rate=sample_rate,
                       bits_per_sample=bits_per_sample)
        elif chunk_id == b"data":
            data_bytes = chunk_body

        pos += 8 + chunk_size + (chunk_size % 2)

    if fmt is None or data_bytes is None:
        raise ValueError(f"missing fmt or data chunk in {path}")

    n_channels = fmt["n_channels"]
    bits = fmt["bits_per_sample"]
    audio_format = fmt["audio_format"]

    if audio_format == PCM_FORMAT and bits == 16:
        raw_samples = np.frombuffer(data_bytes, dtype="<i2").astype(np.float64) / 32768.0
    elif audio_format == PCM_FORMAT and bits == 24:
        n = len(data_bytes) // 3
        raw24 = np.frombuffer(data_bytes[: n * 3], dtype=np.uint8).reshape(n, 3)
        as_int32 = (raw24[:, 0].astype(np.int32) |
                    (raw24[:, 1].astype(np.int32) << 8) |
                    (raw24[:, 2].astype(np.int32) << 16))
        sign_mask = as_int32 & 0x800000
        as_int32 = as_int32 - (sign_mask << 1)
        raw_samples = as_int32.astype(np.float64) / 8388608.0
    elif audio_format == PCM_FORMAT and bits == 32:
        raw_samples = np.frombuffer(data_bytes, dtype="<i4").astype(np.float64) / 2147483648.0
    elif audio_format == IEEE_FLOAT_FORMAT and bits == 32:
        raw_samples = np.frombuffer(data_bytes, dtype="<f4").astype(np.float64)
    elif audio_format == IEEE_FLOAT_FORMAT and bits == 64:
        raw_samples = np.frombuffer(data_bytes, dtype="<f8")
    else:
        raise ValueError(f"unsupported format {audio_format}/{bits}-bit in {path}")

    samples = raw_samples.reshape(-1, n_channels)

    return WavData(
        samples=samples,
        sample_rate=fmt["sample_rate"],
        original_bit_depth=bits,
        original_format=audio_format,
    )
