#!/usr/bin/env python3
"""Source-first GWOSC strain -> transparent wave-analysis receipt.

Uses only Python standard library so it can run on the Jetson without adding a
scientific Python stack. It downloads GWOSC event strain in gzipped ASCII form,
preserves source identity/checksum, and derives a declared Hann-windowed raw
periodogram from an event-centered interval.

This is not a replacement for LIGO/Virgo/KAGRA calibrated analysis pipelines,
whitening, matched filtering, parameter estimation, or detector-noise studies.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import math
import pathlib
import urllib.parse
import urllib.request
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Sequence, Tuple

USER_AGENT = "One-Wave-GWOSC-source-first/1.0"
TRANSFORM_VERSION = "gwosc-strain-wave-v1"
API_ROOT = "https://gwosc.org/api/v2"


@dataclass
class SpectrumReceipt:
    sample_rate_Hz: float
    window_seconds: float
    n_samples: int
    dt_s: float
    df_Hz: float
    mean_strain_before_subtraction: float
    rms_strain: float
    peak_abs_strain: float
    band_min_Hz: float
    band_max_Hz: float
    band_power_strain2: float
    spectral_centroid_Hz: Optional[float]
    strongest_bins: List[Dict[str, float]]


def _request_bytes(url: str, timeout: int = 90) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read()


def _request_json(url: str, timeout: int = 90) -> Dict[str, object]:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        raw = response.read()
    try:
        return json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError as exc:
        preview = raw[:240].decode("utf-8", errors="replace").replace("\n", " ")
        raise ValueError(f"GWOSC API did not return JSON for {url}: {preview!r}") from exc


def _api_url(path: str, params: Optional[Dict[str, object]] = None) -> str:
    url = API_ROOT.rstrip("/") + "/" + path.lstrip("/")
    query = {"format": "json"}
    if params:
        query.update({k: v for k, v in params.items() if v is not None})
    return url + "?" + urllib.parse.urlencode(query)


def get_event_detail(event_version: str) -> Dict[str, object]:
    return _request_json(_api_url(f"event-versions/{event_version}"))


def list_strain_files(event_version: str) -> List[Dict[str, object]]:
    url: Optional[str] = _api_url(f"event-versions/{event_version}/strain-files")
    rows: List[Dict[str, object]] = []
    while url:
        page = _request_json(url)
        page_rows = page.get("results", [])
        if not isinstance(page_rows, list):
            raise ValueError("GWOSC strain-files response has no results list")
        rows.extend(x for x in page_rows if isinstance(x, dict))
        next_url = page.get("next")
        if next_url:
            text = str(next_url)
            if "format=api" in text:
                text = text.replace("format=api", "format=json")
            url = text
        else:
            url = None
    return rows


def select_strain_file(
    rows: Sequence[Dict[str, object]],
    detector: str,
    sample_rate_kHz: int,
    duration_s: int,
    file_format: str = "TXT",
) -> Dict[str, object]:
    detector = detector.upper()
    file_format = file_format.upper()
    matches = []
    for row in rows:
        if str(row.get("detector", "")).upper() != detector:
            continue
        if int(row.get("sample_rate_kHz", -1)) != sample_rate_kHz:
            continue
        if int(row.get("duration", -1)) != duration_s:
            continue
        if str(row.get("file_format", "")).upper() != file_format:
            continue
        matches.append(row)
    if not matches:
        available = sorted(
            {
                (
                    str(r.get("detector")),
                    r.get("sample_rate_kHz"),
                    r.get("duration"),
                    str(r.get("file_format")),
                )
                for r in rows
            }
        )
        raise ValueError(
            f"no GWOSC strain file for detector={detector} sample_rate={sample_rate_kHz}kHz "
            f"duration={duration_s}s format={file_format}; available={available}"
        )
    if len(matches) > 1:
        matches.sort(key=lambda r: str(r.get("download_url", "")))
    return matches[0]


def parse_gzipped_ascii_strain(payload: bytes) -> List[float]:
    text = gzip.decompress(payload).decode("utf-8")
    values: List[float] = []
    for line_number, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("%"):
            continue
        token = line.split()[0]
        try:
            value = float(token)
        except ValueError as exc:
            raise ValueError(f"non-numeric strain value at line {line_number}: {raw!r}") from exc
        if not math.isfinite(value):
            raise ValueError(f"non-finite strain value at line {line_number}: {raw!r}")
        values.append(value)
    if not values:
        raise ValueError("GWOSC ASCII file contained no numeric strain samples")
    return values


def _is_power_of_two(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0


def fft_radix2(values: Sequence[complex]) -> List[complex]:
    """Unnormalized forward FFT with exp(-i*2*pi*k*n/N) convention."""
    n = len(values)
    if not _is_power_of_two(n):
        raise ValueError(f"FFT length must be a power of two, got {n}")
    a = [complex(v) for v in values]

    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]

    length = 2
    while length <= n:
        angle = -2.0 * math.pi / length
        wlen = complex(math.cos(angle), math.sin(angle))
        half = length // 2
        for start in range(0, n, length):
            w = 1.0 + 0.0j
            for offset in range(half):
                u = a[start + offset]
                v = a[start + offset + half] * w
                a[start + offset] = u + v
                a[start + offset + half] = u - v
                w *= wlen
        length <<= 1
    return a


def hann_window(n: int) -> List[float]:
    if n < 2:
        raise ValueError("Hann window requires at least two samples")
    return [0.5 * (1.0 - math.cos(2.0 * math.pi * i / (n - 1))) for i in range(n)]


def analyze_segment(
    samples: Sequence[float],
    sample_rate_Hz: float,
    band_min_Hz: float,
    band_max_Hz: float,
    top_bins: int,
) -> SpectrumReceipt:
    n = len(samples)
    if not _is_power_of_two(n):
        raise ValueError(f"analysis segment must contain power-of-two samples, got {n}")
    if sample_rate_Hz <= 0:
        raise ValueError("sample rate must be positive")
    nyquist = sample_rate_Hz / 2.0
    if not (0.0 <= band_min_Hz < band_max_Hz <= nyquist):
        raise ValueError(
            f"band must satisfy 0 <= min < max <= Nyquist ({nyquist} Hz), got "
            f"{band_min_Hz}..{band_max_Hz}"
        )

    mean = sum(samples) / n
    centered = [x - mean for x in samples]
    rms = math.sqrt(sum(x * x for x in centered) / n)
    peak = max(abs(x) for x in centered)

    window = hann_window(n)
    w2 = sum(w * w for w in window)
    transformed = fft_radix2([x * w for x, w in zip(centered, window)])

    dt = 1.0 / sample_rate_Hz
    df = sample_rate_Hz / n
    half = n // 2
    rows: List[Tuple[float, float, float]] = []
    band_power = 0.0
    weighted_frequency = 0.0

    for k in range(half + 1):
        freq = k * df
        base_psd = dt * (abs(transformed[k]) ** 2) / w2
        if k not in (0, half):
            base_psd *= 2.0
        if band_min_Hz <= freq <= band_max_Hz:
            asd = math.sqrt(max(base_psd, 0.0))
            rows.append((freq, base_psd, asd))
            band_power += base_psd * df
            weighted_frequency += freq * base_psd * df

    centroid = weighted_frequency / band_power if band_power > 0.0 else None
    rows.sort(key=lambda item: item[1], reverse=True)
    strongest = [
        {"frequency_Hz": f, "psd_strain2_per_Hz": p, "asd_per_sqrt_Hz": a}
        for f, p, a in rows[: max(top_bins, 0)]
    ]

    return SpectrumReceipt(
        sample_rate_Hz=sample_rate_Hz,
        window_seconds=n / sample_rate_Hz,
        n_samples=n,
        dt_s=dt,
        df_Hz=df,
        mean_strain_before_subtraction=mean,
        rms_strain=rms,
        peak_abs_strain=peak,
        band_min_Hz=band_min_Hz,
        band_max_Hz=band_max_Hz,
        band_power_strain2=band_power,
        spectral_centroid_Hz=centroid,
        strongest_bins=strongest,
    )


def extract_centered_segment(
    samples: Sequence[float],
    sample_rate_Hz: float,
    file_gps_start: float,
    center_gps: float,
    window_seconds: float,
) -> Tuple[List[float], Dict[str, object]]:
    n = int(round(window_seconds * sample_rate_Hz))
    if not _is_power_of_two(n):
        raise ValueError(
            f"window_seconds * sample_rate must be an exact power of two; got {n} samples"
        )
    center_index = int(round((center_gps - file_gps_start) * sample_rate_Hz))
    start = center_index - n // 2
    stop = start + n
    if start < 0 or stop > len(samples):
        raise ValueError(
            f"requested centered segment [{start}:{stop}] is outside downloaded sample range 0:{len(samples)}"
        )
    return list(samples[start:stop]), {
        "center_gps": center_gps,
        "center_index": center_index,
        "segment_start_index": start,
        "segment_stop_index": stop,
        "segment_start_gps": file_gps_start + start / sample_rate_Hz,
        "segment_stop_gps": file_gps_start + stop / sample_rate_Hz,
    }


def analyze_detector(
    event_gps: float,
    row: Dict[str, object],
    window_seconds: float,
    band_min_Hz: float,
    band_max_Hz: float,
    top_bins: int,
    raw_dir: Optional[pathlib.Path],
) -> Dict[str, object]:
    url = str(row["download_url"])
    payload = _request_bytes(url)
    sha256 = hashlib.sha256(payload).hexdigest()
    if raw_dir is not None:
        raw_dir.mkdir(parents=True, exist_ok=True)
        name = pathlib.PurePosixPath(urllib.parse.urlparse(url).path).name or "strain.txt.gz"
        (raw_dir / name).write_bytes(payload)

    samples = parse_gzipped_ascii_strain(payload)
    sample_rate_Hz = float(int(row["sample_rate_kHz"]) * 1000)
    file_start = float(row["gps_start"])
    segment, location = extract_centered_segment(
        samples,
        sample_rate_Hz=sample_rate_Hz,
        file_gps_start=file_start,
        center_gps=event_gps,
        window_seconds=window_seconds,
    )
    spectrum = analyze_segment(
        segment,
        sample_rate_Hz=sample_rate_Hz,
        band_min_Hz=band_min_Hz,
        band_max_Hz=band_max_Hz,
        top_bins=top_bins,
    )

    expected = int(row["duration"]) * int(sample_rate_Hz)
    return {
        "derivation_class": "DIRECT_STRAIN_PLUS_STANDARD_SIGNAL_DERIVED",
        "detector": str(row["detector"]),
        "source_download_url": url,
        "source_sha256": sha256,
        "source_gps_start": file_start,
        "source_duration_s": int(row["duration"]),
        "source_sample_rate_Hz": sample_rate_Hz,
        "source_samples_parsed": len(samples),
        "source_expected_samples": expected,
        "source_sample_count_matches_metadata": len(samples) == expected,
        "segment": location,
        "analysis": asdict(spectrum),
        "interpretation_warning": (
            "Strong raw spectral bins include detector noise/lines and must not be called astrophysical "
            "source modes without appropriate noise controls, whitening/matched filtering, and comparison."
        ),
    }


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--event-version", default="GW150914-v2")
    p.add_argument("--detectors", default="H1,L1", help="comma-separated detector names")
    p.add_argument("--sample-rate-khz", type=int, default=4, choices=(4, 16))
    p.add_argument("--duration", type=int, default=32)
    p.add_argument("--window-seconds", type=float, default=4.0)
    p.add_argument("--band-min-hz", type=float, default=20.0)
    p.add_argument("--band-max-hz", type=float, default=512.0)
    p.add_argument("--top-bins", type=int, default=12)
    p.add_argument("--output", required=True)
    p.add_argument("--raw-dir")
    return p.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    event = get_event_detail(args.event_version)
    event_gps = float(event["gps"])
    files = list_strain_files(args.event_version)
    detectors = [x.strip().upper() for x in args.detectors.split(",") if x.strip()]
    if not detectors:
        raise SystemExit("no detectors supplied")

    raw_dir = pathlib.Path(args.raw_dir) if args.raw_dir else None
    detector_results = []
    for detector in detectors:
        selected = select_strain_file(
            files,
            detector=detector,
            sample_rate_kHz=args.sample_rate_khz,
            duration_s=args.duration,
            file_format="TXT",
        )
        detector_results.append(
            analyze_detector(
                event_gps=event_gps,
                row=selected,
                window_seconds=args.window_seconds,
                band_min_Hz=args.band_min_hz,
                band_max_Hz=args.band_max_hz,
                top_bins=args.top_bins,
                raw_dir=raw_dir,
            )
        )

    result = {
        "transform_version": TRANSFORM_VERSION,
        "source_class": "GWOSC calibrated strain and event metadata",
        "event_version": args.event_version,
        "event_name": event.get("name"),
        "event_gps": event_gps,
        "event_catalog": event.get("catalog"),
        "event_run": event.get("run"),
        "event_doi": event.get("doi"),
        "event_detail_api": _api_url(f"event-versions/{args.event_version}"),
        "strain_files_api": _api_url(f"event-versions/{args.event_version}/strain-files"),
        "analysis_preprocessing": {
            "mean_subtraction": True,
            "window": "Hann",
            "spectrum": "one-sided raw periodogram",
            "whitening": False,
            "matched_filtering": False,
            "parameter_estimation": False,
        },
        "detectors": detector_results,
        "one_wave_status": "YELLOW_OPEN_NO_MECHANISM_INFERRED",
    }

    output = pathlib.Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(result, indent=2, sort_keys=True, allow_nan=False)
    output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
