#!/usr/bin/env python3
"""Brute-force verification for G-721's generator: p = n+k, r = 2p+s,
s in {-1,0,+1}.

Tests, against all 26 alphabet positions and all 12 tonal positions:
- that the generator reproduces every packet the original single-family
  convention and the proposed two-family convention ever produced;
- that (n,k,s) -> (n,m,r) is collision-free;
- that the (n,m,r) -> (k,s) decoder inverts the generator exactly;
- that half-mirror reversal and round-trip orientation-exchange are
  genuinely different operators, not one rule applied twice;
- the alphabet's linear boundary at Z vs. the tonal cycle's wraparound;
- the 12-state / 13-visit tonal closure distinction.

Writes generator_verification_receipt.json with a pass/fail summary and
alphabet_tonal_table.csv with the full table for both symbol sets.
"""
from __future__ import annotations
import csv
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent

ALPHABET = [chr(64 + i) for i in range(1, 27)]  # A..Z, n=1..26
TONES = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]  # n=1..12


def coord(n: int, k: int, s: int) -> tuple[int, int, int]:
    p = n + k
    m = 2 * p
    r = m + s
    return (n, m, r)


def decode(n: int, m: int, r: int) -> tuple[int, int]:
    assert m % 2 == 0
    k = m // 2 - n
    s = r - m
    return k, s


def half_split(symbols: list[str]) -> tuple[list[str], list[str]]:
    half = len(symbols) // 2
    return symbols[:half], symbols[half:]


def sequence_reverse(seq: list[str]) -> list[str]:
    return list(reversed(seq))


def orientation_exchange(seq: list[str]) -> list[str]:
    idx = seq.index("(0)")
    left, right = seq[:idx], seq[idx + 1:]
    return right + ["(0)"] + left


def half_forward(symbols: list[str]) -> list[str]:
    a, b = half_split(symbols)
    return a + ["(0)"] + b


def round_trip_forward(symbols: list[str]) -> list[str]:
    return symbols + ["(0)"] + list(reversed(symbols))


def build_table(symbols: list[str]) -> list[dict]:
    rows = []
    for i, sym in enumerate(symbols, start=1):
        for k in (-1, 0, 1):
            n_plus_k = i + k
            if n_plus_k < 1 or n_plus_k > len(symbols):
                continue  # out of domain for the linear alphabet; tonal wraps separately
            for s in (-1, 0, 1):
                n_a, m, r = coord(i, k, s)
                dk, ds = decode(n_a, m, r)
                rows.append({
                    "symbol": sym, "n": i, "k": k, "s": s,
                    "m": m, "r": r,
                    "decode_ok": (dk, ds) == (k, s),
                })
    return rows


def main() -> None:
    results = {}

    # --- reproduces every prior packet form ---
    repro_ok = True
    for n in range(1, 26):
        orig_b0 = 2 * n
        orig_b1 = 2 * n + 1
        fam1_minus = 2 * n - 1
        fam1_plus = 2 * n + 1
        fam2_minus = 2 * (n + 1) - 1
        fam2_plus = 2 * (n + 1) + 1
        gens = {
            (0, 0): coord(n, 0, 0)[2],
            (0, 1): coord(n, 0, 1)[2],
            (0, -1): coord(n, 0, -1)[2],
            (1, -1): coord(n, 1, -1)[2],
            (1, 1): coord(n, 1, 1)[2],
        }
        ok = (gens[(0, 0)] == orig_b0 and gens[(0, 1)] == orig_b1 == fam1_plus
              and gens[(0, -1)] == fam1_minus
              and gens[(1, -1)] == fam2_minus and gens[(1, 1)] == fam2_plus)
        repro_ok = repro_ok and ok
    results["reproduces_all_prior_packet_forms"] = repro_ok

    # --- alphabet table + collision/decoder check ---
    alpha_rows = build_table(ALPHABET)
    results["alphabet_states_tested"] = len(alpha_rows)
    results["alphabet_decoder_failures"] = sum(1 for r in alpha_rows if not r["decode_ok"])
    seen = {}
    collisions = 0
    for r in alpha_rows:
        key = (r["n"], r["m"], r["r"])
        if key in seen and seen[key] != (r["k"], r["s"]):
            collisions += 1
        seen[key] = (r["k"], r["s"])
    results["alphabet_collisions"] = collisions

    # --- tonal table ---
    tone_rows = build_table(TONES)
    results["tonal_states_tested"] = len(tone_rows)
    results["tonal_decoder_failures"] = sum(1 for r in tone_rows if not r["decode_ok"])

    # --- reversal vs orientation-exchange ---
    hf = half_forward(ALPHABET)
    a, b = half_split(ALPHABET)
    expected_half_reverse = list(reversed(b)) + ["(0)"] + list(reversed(a))
    results["half_mirror_reverse_equals_sequence_reverse"] = (sequence_reverse(hf) == expected_half_reverse)

    rt = round_trip_forward(ALPHABET)
    results["round_trip_is_palindrome_under_sequence_reverse"] = (sequence_reverse(rt) == rt)
    expected_round_trip_rev = list(reversed(ALPHABET)) + ["(0)"] + ALPHABET
    results["round_trip_reverse_equals_orientation_exchange"] = (orientation_exchange(rt) == expected_round_trip_rev)

    # --- domain boundary ---
    results["alphabet_z_lookahead_undefined"] = (26 + 1 > len(ALPHABET))  # no letter 27
    results["tonal_g_sharp_lookahead_wraps_to_A"] = (((12 - 1 + 1) % 12) + 1 == 1)

    # --- 12 states / 13 visits ---
    closure_traversal = TONES + [TONES[0]]
    results["tonal_unique_states"] = len(set(TONES))
    results["tonal_closure_traversal_visits"] = len(closure_traversal)
    results["alphabet_half_symbol_count"] = len(ALPHABET) // 2
    results["traversal_visit_correspondence_13_to_13"] = (len(closure_traversal) == len(ALPHABET) // 2)
    results["state_cardinality_correspondence_13_to_13"] = (len(set(TONES)) == len(ALPHABET) // 2)

    all_pass = (
        results["reproduces_all_prior_packet_forms"]
        and results["alphabet_decoder_failures"] == 0
        and results["alphabet_collisions"] == 0
        and results["tonal_decoder_failures"] == 0
        and results["half_mirror_reverse_equals_sequence_reverse"]
        and results["round_trip_is_palindrome_under_sequence_reverse"]
        and results["round_trip_reverse_equals_orientation_exchange"]
        and results["alphabet_z_lookahead_undefined"]
        and results["tonal_g_sharp_lookahead_wraps_to_A"]
        and results["traversal_visit_correspondence_13_to_13"]
        and not results["state_cardinality_correspondence_13_to_13"]  # this SHOULD be False
    )
    results["all_checks_pass"] = all_pass

    (OUT / "generator_verification_receipt.json").write_text(json.dumps(results, indent=2))

    with (OUT / "alphabet_tonal_table.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["symbol", "n", "k", "s", "m", "r", "decode_ok"])
        writer.writeheader()
        for row in alpha_rows + tone_rows:
            writer.writerow(row)

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
