#!/usr/bin/env python3
"""Generate fresh math practice riffs without displaying answers.

Problems are grouped by rule families that naturally work together.
The learner gets the problem, the rule-family references, and a short reminder.
Answers are intentionally not printed.
"""

import random

FAMILIES = {
    "A": "Movement, opposites, and cancellation",
    "B": "Groups, scale, multiplication, and division",
    "C": "Fractions, ratios, and matching scale",
    "D": "Equality, inverse operations, and equivalent equations",
    "E": "Terms, distribution, and factoring",
    "F": "Signs, direction, powers, and roots",
    "G": "Coordinates, change, ratios, and systems",
}


def nonzero(lo=-9, hi=9):
    n = 0
    while n == 0:
        n = random.randint(lo, hi)
    return n


def riff_ab():
    a = random.randint(2, 9)
    b = random.randint(2, 15)
    x = random.randint(1, 12)
    total = a * x + b
    return (
        f"{a}x + {b} = {total}",
        ["A", "B", "D"],
        "Undo the added amount, then undo the scale. Preserve the relationship at each move.",
    )


def riff_fraction():
    d1 = random.choice([2, 3, 4, 5, 6, 8])
    d2 = random.choice([3, 4, 5, 6, 8, 10])
    while d2 == d1:
        d2 = random.choice([3, 4, 5, 6, 8, 10])
    n1 = random.randint(1, d1 - 1)
    n2 = random.randint(1, d2 - 1)
    return (
        f"{n1}/{d1} + {n2}/{d2} = ?",
        ["C", "B"],
        "Before adding, make sure the pieces are the same size.",
    )


def riff_distribution():
    a = random.randint(2, 6)
    b = random.randint(1, 9)
    c = random.randint(5, 20)
    return (
        f"{a}(x + {b}) = {a * c}",
        ["B", "D", "E"],
        "Choose a valid path: undo the outside scale first, or distribute. Keep the structure consistent.",
    )


def riff_equivalent():
    scale = random.randint(2, 6)
    gap = random.randint(2, 9)
    return (
        f"{scale}s + {scale * gap} = {scale}t. Rewrite it in a simpler equivalent form.",
        ["B", "D"],
        "Look for a common scale shared by every term.",
    )


def riff_signs():
    a = nonzero(-9, -2)
    b = random.randint(2, 9)
    return (
        f"({a})({b}) + {-a} = ?",
        ["A", "B", "F"],
        "Track direction/sign separately from magnitude, then combine the changes.",
    )


def riff_coordinates():
    total = random.randint(6, 20)
    x = random.randint(0, total)
    return (
        f"For x + y = {total}, find y when x = {x}.",
        ["A", "D", "G"],
        "Treat the equation as a relationship between two coordinates; isolate the missing coordinate.",
    )


def riff_system():
    x = random.randint(1, 9)
    y = random.randint(1, 9)
    s = x + y
    d = x - y
    sign = "+" if d >= 0 else "-"
    return (
        f"x + y = {s}\nx - y = {d}",
        ["A", "D", "G"],
        "Both equations must be true at the same time. Look for a move that combines or cancels matching parts.",
    )


GENERATORS = [
    riff_ab,
    riff_fraction,
    riff_distribution,
    riff_equivalent,
    riff_signs,
    riff_coordinates,
    riff_system,
]


def generate():
    problem, families, reminder = random.choice(GENERATORS)()
    print("\n=== NEW MATH RIFF ===\n")
    print(problem)
    print("\nUses:")
    for code in families:
        print(f"  Family {code} — {FAMILIES[code]}")
    print(f"\nRule reminder: {reminder}")
    print("\nAnswer hidden. Work the riff first.\n")


if __name__ == "__main__":
    generate()
