#!/usr/bin/env python3
"""Convert provenance-bearing measurement/metadata JSON into One-Wave wave-state JSON."""
import argparse
import json
import math
from pathlib import Path

REQUIRED_MAPPING = (
    "state_identity",
    "coupling_rule",
    "timing_relationship",
    "propagation_behavior",
)


TIME_TO_SECONDS = {"s": 1.0, "ms": 1e-3, "us": 1e-6, "ns": 1e-9}


def finite_number(value, name):
    if isinstance(value, bool):
        raise ValueError(name + " must be a finite number, not a boolean")
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(name + " must be finite")
    return number


def timing_metadata(samples, time_unit):
    """Keep inverse sample intervals separate from physical signal frequency."""
    complete = all("t" in sample for sample in samples)
    times = [finite_number(sample.get("t", index), "sample.t")
             for index, sample in enumerate(samples)]
    intervals = [None] * len(samples)
    if complete:
        for index in range(1, len(times)):
            delta = times[index] - times[index - 1]
            if not math.isfinite(delta) or delta <= 0:
                raise ValueError("source timestamps must be finite and strictly increasing")
            if time_unit in TIME_TO_SECONDS:
                seconds = delta * TIME_TO_SECONDS[time_unit]
                if not math.isfinite(seconds) or seconds <= 0 or not math.isfinite(1.0 / seconds):
                    raise ValueError("sample interval cannot be represented in seconds")
                intervals[index] = seconds
    known = [value for value in intervals if value is not None]
    uniform = (all(math.isclose(value, known[0], rel_tol=1e-9, abs_tol=0.0)
                   for value in known) if known else None)
    return times, intervals, {
        "time_unit": time_unit,
        "time_coordinates": ("source" if complete else
                             "mixed_source_and_index" if any("t" in s for s in samples)
                             else "index"),
        "uniform_sampling": uniform,
        "uniformity_relative_tolerance": 1e-9,
        "sample_rate_Hz": 1.0 / known[0] if uniform else None,
        "cadence_status": ("available" if known else "unavailable"),
        "cadence_reason": (None if known else
                           "timestamps_missing" if not complete else
                           "time_unit_unknown_or_unsupported" if time_unit not in TIME_TO_SECONDS else
                           "fewer_than_two_samples"),
    }


def norm(values):
    lo, hi = min(values), max(values)
    if hi == lo:
        return [0.0 for _ in values]
    return [2.0 * (v - lo) / (hi - lo) - 1.0 for v in values]


def transform(doc):
    mode = doc.get("mode")
    mapping = doc.get("mapping", {})
    missing = [key for key in REQUIRED_MAPPING if not mapping.get(key)]
    if missing:
        raise ValueError("missing mapping fields: " + ", ".join(missing))

    provenance = doc.get("provenance", {})
    if not provenance.get("source") or not provenance.get("record_id"):
        raise ValueError("provenance.source and provenance.record_id are required")

    states = []
    if mode == "measurement_series":
        samples = doc.get("samples", [])
        if not samples:
            raise ValueError("measurement_series requires samples")

        raw_values = [finite_number(sample["value"], "sample.value") for sample in samples]
        times, intervals, timing = timing_metadata(samples, doc.get("time_unit"))
        amplitudes = norm(raw_values)
        for index, (sample, amplitude) in enumerate(zip(samples, amplitudes)):
            time_value = times[index]
            position = finite_number(sample.get("x", 0.0), "sample.x")
            interval = intervals[index]
            states.append(
                {
                    "A": amplitude,
                    "f": None,
                    "frequency_known": False,
                    "sample_interval_s": interval,
                    "inverse_sample_interval_Hz": 1.0 / interval if interval is not None else None,
                    "phi": 0.0,
                    "x": position,
                    "t": time_value,
                    "m": {"raw_value": raw_values[index], "raw": sample},
                }
            )
        representation_kind = "source_measurement_wave"
        source_physical_wave_or_series = True
    elif mode == "metadata_sequence":
        metadata = doc.get("metadata", {})
        numeric = [
            (key, finite_number(value, "metadata." + key))
            for key, value in sorted(metadata.items())
            if isinstance(value, (int, float)) and not isinstance(value, bool)
        ]
        if not numeric:
            raise ValueError("metadata_sequence requires numeric metadata fields")

        amplitudes = norm([value for _, value in numeric])
        for index, ((key, raw_value), amplitude) in enumerate(zip(numeric, amplitudes)):
            previous = amplitudes[index - 1] if index else amplitude
            delta = amplitude - previous
            phase = math.atan2(delta, amplitude if amplitude else 1e-15)
            states.append(
                {
                    "A": amplitude,
                    "f": None,
                    "frequency_known": False,
                    "sample_interval_s": None,
                    "inverse_sample_interval_Hz": None,
                    "phi": phase,
                    "x": float(index),
                    "t": float(index),
                    "m": {"field": key, "raw_value": raw_value},
                }
            )
        timing = {
            "time_unit": None,
            "time_coordinates": "metadata_index",
            "uniform_sampling": None,
            "sample_rate_Hz": None,
            "cadence_status": "unavailable",
            "cadence_reason": "metadata_sequence_is_not_sampled_time",
        }
        representation_kind = "derived_metadata_wave"
        source_physical_wave_or_series = False
    else:
        raise ValueError("mode must be measurement_series or metadata_sequence")

    return {
        "schema": "one-wave-wave-data-v2",
        "frequency_semantics": "physical_signal_frequency_Hz_unestimated",
        "timing": timing,
        "representation_kind": representation_kind,
        "source_physical_wave_or_series": source_physical_wave_or_series,
        "provenance": provenance,
        "mapping": mapping,
        "states": states,
        "warning": (
            "Signal frequency is unestimated; normalized amplitude and zero phase are analysis coordinates."
            if source_physical_wave_or_series
            else "Derived analysis encoding of metadata; not a claim that the source metadata is a physical waveform."
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("-o", "--output")
    args = parser.parse_args()

    output = transform(json.loads(Path(args.input).read_text()))
    text = json.dumps(output, indent=2, sort_keys=True, allow_nan=False) + "\n"
    if args.output:
        Path(args.output).write_text(text)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
