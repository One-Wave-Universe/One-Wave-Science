#!/usr/bin/env python3
"""Reference validator for G-721 / G-721a.

The validator checks the Fibonacci-word branch trace of the mirrored alphabet
rabbit-hop coordinate algorithm. It does not control live choice and does not
apply golden-ratio claims to unrelated geometry or physics.
"""
from __future__ import annotations

import csv
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Sequence

PHI = (1.0 + math.sqrt(5.0)) / 2.0


def fibonacci_words(max_generation: int) -> list[str]:
    if max_generation < 0:
        raise ValueError("max_generation must be nonnegative")
    words = ["0"]
    if max_generation == 0:
        return words
    words.append("01")
    for _ in range(2, max_generation + 1):
        words.append(words[-1] + words[-2])
    return words


def fibonacci_prefix(length: int) -> str:
    if length < 0:
        raise ValueError("length must be nonnegative")
    if length == 0:
        return ""
    words = fibonacci_words(1)
    while len(words[-1]) < length:
        words.append(words[-1] + words[-2])
    return words[-1][:length]


def branch_from_coordinates(identity: int, recursive: int) -> int:
    n = abs(identity)
    r = abs(recursive)
    if not 1 <= n <= 26:
        raise ValueError(f"letter identity out of range: {identity}")
    branch = r - 2 * n
    if branch not in (0, 1):
        raise ValueError(
            f"illegal recursive coordinate {recursive} for identity {identity}; "
            f"expected ±{2*n} or ±{2*n+1}"
        )
    if identity * recursive <= 0:
        raise ValueError("identity and recursive coordinate must share mirror sign")
    return branch


def decode_trace(records: Iterable[tuple[int, int]]) -> str:
    return "".join(str(branch_from_coordinates(n, r)) for n, r in records)


def mismatch_rate(observed: str, expected: str) -> float:
    if len(observed) != len(expected):
        raise ValueError("observed and expected strings must have equal length")
    if not observed:
        return 0.0
    return sum(a != b for a, b in zip(observed, expected)) / len(observed)


def is_balanced(word: str, max_factor_length: int | None = None) -> bool:
    if any(ch not in "01" for ch in word):
        raise ValueError("word must be binary")
    limit = len(word) if max_factor_length is None else min(len(word), max_factor_length)
    for width in range(1, limit + 1):
        counts = [word[i : i + width].count("1") for i in range(len(word) - width + 1)]
        if counts and max(counts) - min(counts) > 1:
            return False
    return True


def factor_complexity(word: str, width: int) -> int:
    if width < 1 or width > len(word):
        raise ValueError("width must satisfy 1 <= width <= len(word)")
    return len({word[i : i + width] for i in range(len(word) - width + 1)})


@dataclass(frozen=True)
class GenerationMetric:
    generation: int
    word: str
    length: int
    zeros: int
    ones: int
    recursive_identity: bool
    length_ratio: float | None
    zero_one_ratio: float | None
    length_phi_error: float | None
    count_phi_error: float | None


def generation_metrics(max_generation: int) -> list[GenerationMetric]:
    words = fibonacci_words(max_generation)
    rows: list[GenerationMetric] = []
    for k, word in enumerate(words):
        zeros = word.count("0")
        ones = word.count("1")
        recursive_identity = k < 2 or word == words[k - 1] + words[k - 2]
        length_ratio = None if k == 0 else len(word) / len(words[k - 1])
        zero_one_ratio = None if ones == 0 else zeros / ones
        rows.append(
            GenerationMetric(
                generation=k,
                word=word,
                length=len(word),
                zeros=zeros,
                ones=ones,
                recursive_identity=recursive_identity,
                length_ratio=length_ratio,
                zero_one_ratio=zero_one_ratio,
                length_phi_error=None if length_ratio is None else abs(length_ratio - PHI) / PHI,
                count_phi_error=None if zero_one_ratio is None else abs(zero_one_ratio - PHI) / PHI,
            )
        )
    return rows


def build_reference_route() -> list[dict[str, int | str]]:
    expected = fibonacci_prefix(26)
    rows: list[dict[str, int | str]] = []
    for n, token in enumerate(expected, start=1):
        bit = int(token)
        rows.append(
            {
                "letter": chr(64 + n),
                "n": n,
                "branch": bit,
                "recursive_coordinate": 2 * n + bit,
                "mirror_n": -n,
                "mirror_recursive_coordinate": -(2 * n + bit),
            }
        )
    return rows


def write_outputs(output_dir: Path, max_generation: int = 12) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    metrics = generation_metrics(max_generation)
    route = build_reference_route()

    generation_csv = output_dir / "fibonacci_word_generations.csv"
    with generation_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(asdict(metrics[0]).keys()))
        writer.writeheader()
        for row in metrics:
            writer.writerow(asdict(row))

    route_csv = output_dir / "alphabet_route_reference.csv"
    with route_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(route[0].keys()))
        writer.writeheader()
        writer.writerows(route)

    positive_records = [(int(row["n"]), int(row["recursive_coordinate"])) for row in route]
    negative_records = [
        (int(row["mirror_n"]), int(row["mirror_recursive_coordinate"])) for row in route
    ]
    expected = fibonacci_prefix(len(route))
    positive_trace = decode_trace(positive_records)
    negative_trace = decode_trace(negative_records)
    reverse_trace = decode_trace(reversed(positive_records))
    expected_reverse = expected[::-1]

    checks = {
        "convention": {"W0": "0", "W1": "01", "recurrence": "Wk=W(k-1)W(k-2)"},
        "phi": PHI,
        "route_length": len(route),
        "expected_prefix": expected,
        "positive_trace": positive_trace,
        "negative_mirror_trace": negative_trace,
        "reverse_trace": reverse_trace,
        "expected_reverse": expected_reverse,
        "positive_mismatch": mismatch_rate(positive_trace, expected),
        "negative_mirror_mismatch": mismatch_rate(negative_trace, expected),
        "reverse_mismatch": mismatch_rate(reverse_trace, expected_reverse),
        "all_generation_recursions_pass": all(row.recursive_identity for row in metrics),
        "prefix_is_balanced": is_balanced(expected),
        "factor_complexity": {
            str(width): factor_complexity(fibonacci_prefix(256), width)
            for width in range(1, 13)
        },
        "factor_complexity_expected": {str(width): width + 1 for width in range(1, 13)},
        "classification": "exact_fibonacci_word_route",
    }
    checks["factor_complexity_pass"] = (
        checks["factor_complexity"] == checks["factor_complexity_expected"]
    )

    receipt = output_dir / "reference_validation.json"
    receipt.write_text(json.dumps(checks, indent=2) + "\n", encoding="utf-8")

    try:
        import matplotlib.pyplot as plt

        generations = [row.generation for row in metrics if row.length_ratio is not None]
        length_ratios = [row.length_ratio for row in metrics if row.length_ratio is not None]
        count_generations = [row.generation for row in metrics if row.zero_one_ratio is not None]
        count_ratios = [row.zero_one_ratio for row in metrics if row.zero_one_ratio is not None]

        fig, ax = plt.subplots(figsize=(9, 5.4))
        ax.plot(generations, length_ratios, marker="o", label="Length ratio Lk/L(k-1)")
        ax.plot(count_generations, count_ratios, marker="s", label="Symbol ratio zeros/ones")
        ax.axhline(PHI, linestyle="--", label="Golden ratio")
        ax.set_xlabel("Fibonacci-word generation")
        ax.set_ylabel("Ratio")
        ax.set_title("Fibonacci-word metrics converge toward the golden ratio")
        ax.grid(True, alpha=0.3)
        ax.legend()
        fig.tight_layout()
        fig.savefig(output_dir / "fibonacci_word_convergence.png", dpi=180)
        plt.close(fig)
    except ImportError:
        checks["plot_status"] = "matplotlib unavailable"
        receipt.write_text(json.dumps(checks, indent=2) + "\n", encoding="utf-8")

    return checks


def main() -> None:
    output_dir = Path(__file__).resolve().parent
    checks = write_outputs(output_dir)
    failed = [
        key
        for key in (
            "positive_mismatch",
            "negative_mirror_mismatch",
            "reverse_mismatch",
        )
        if checks[key] != 0.0
    ]
    if not checks["all_generation_recursions_pass"]:
        failed.append("generation_recursion")
    if not checks["prefix_is_balanced"]:
        failed.append("balance")
    if not checks["factor_complexity_pass"]:
        failed.append("factor_complexity")
    if failed:
        raise SystemExit(f"validation failed: {', '.join(failed)}")
    print("G-721a reference validation passed")


if __name__ == "__main__":
    main()
