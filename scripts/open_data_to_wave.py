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

        raw_values = [float(sample["value"]) for sample in samples]
        amplitudes = norm(raw_values)
        for index, (sample, amplitude) in enumerate(zip(samples, amplitudes)):
            time_value = float(sample.get("t", index))
            position = float(sample.get("x", 0.0))
            if index:
                previous_time = float(samples[index - 1].get("t", index - 1))
                delta_time = time_value - previous_time
                frequency = (1.0 / abs(delta_time)) if delta_time else 0.0
            else:
                frequency = 0.0
            states.append(
                {
                    "A": amplitude,
                    "f": frequency,
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
            (key, float(value))
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
                    "f": 0.0,
                    "phi": phase,
                    "x": float(index),
                    "t": float(index),
                    "m": {"field": key, "raw_value": raw_value},
                }
            )
        representation_kind = "derived_metadata_wave"
        source_physical_wave_or_series = False
    else:
        raise ValueError("mode must be measurement_series or metadata_sequence")

    return {
        "schema": "one-wave-wave-data-v1",
        "representation_kind": representation_kind,
        "source_physical_wave_or_series": source_physical_wave_or_series,
        "provenance": provenance,
        "mapping": mapping,
        "states": states,
        "warning": (
            None
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
    text = json.dumps(output, indent=2, sort_keys=True) + "\n"
    if args.output:
        Path(args.output).write_text(text)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
