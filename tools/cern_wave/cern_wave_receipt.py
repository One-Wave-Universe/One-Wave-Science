#!/usr/bin/env python3
"""Summarize a converted JSONL file without hiding source-lineage discrepancies."""

import argparse
import json
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("jsonl")
    p.add_argument("--output")
    args = p.parse_args()

    objects = 0
    events = 0
    inconsistent_events = 0
    max_gap = 0.0
    analog_min = None
    analog_max = None
    standard_f_min = None
    standard_f_max = None
    wavelength_min = None
    wavelength_max = None
    worst = []

    with Path(args.jsonl).open("r", encoding="utf-8") as fp:
        for line in fp:
            row = json.loads(line)
            objects += 1

            f = row.get("std_wave_frequency_Hz")
            if isinstance(f, (int, float)):
                standard_f_min = f if standard_f_min is None else min(standard_f_min, f)
                standard_f_max = f if standard_f_max is None else max(standard_f_max, f)

            wl = row.get("std_wave_de_broglie_wavelength_m")
            if isinstance(wl, (int, float)):
                wavelength_min = wl if wavelength_min is None else min(wavelength_min, wl)
                wavelength_max = wl if wavelength_max is None else max(wavelength_max, wl)

            af = row.get("analog_frequency_Hz")
            if isinstance(af, (int, float)):
                analog_min = af if analog_min is None else min(analog_min, af)
                analog_max = af if analog_max is None else max(analog_max, af)

            # Pair diagnostics are repeated for the two objects. Count once per event.
            if row.get("object_index") == 1:
                events += 1
                gap = row.get("pair_mass_rounding_gap_GeV")
                if isinstance(gap, (int, float)):
                    max_gap = max(max_gap, gap)
                    if gap > 0:
                        inconsistent_events += 1
                        worst.append(
                            {
                                "Run": row.get("Run"),
                                "Event": row.get("Event"),
                                "source_pair_mass_GeV": row.get("source_pair_mass_GeV"),
                                "recomputed_pair_mass_GeV": row.get("reconstructed_pair_mass_GeV"),
                                "center_delta_GeV": row.get("pair_mass_delta_GeV"),
                                "rounding_gap_GeV": gap,
                                "classification": "SOURCE_M_LINEAGE_NOT_REPRODUCIBLE_FROM_PUBLISHED_VALUES",
                            }
                        )

    worst.sort(key=lambda r: r["rounding_gap_GeV"], reverse=True)
    receipt = {
        "objects": objects,
        "events": events,
        "source_mass_lineage_inconsistent_events": inconsistent_events,
        "source_mass_lineage_consistent_events": events - inconsistent_events,
        "max_source_mass_rounding_gap_GeV": max_gap,
        "standard_frequency_Hz": {"min": standard_f_min, "max": standard_f_max},
        "de_broglie_wavelength_m": {"min": wavelength_min, "max": wavelength_max},
        "scaled_analog_frequency_Hz": {"min": analog_min, "max": analog_max},
        "worst_source_mass_lineage_events": worst[:10],
    }
    text = json.dumps(receipt, indent=2, sort_keys=True)
    print(text)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
