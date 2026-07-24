# G-721a Fibonacci Word Hop Validation

This directory contains the reproducible reference validator for the mirrored alphabet rabbit-hop algorithm.

Run:

```bash
python3 fibonacci_word_validator.py
```

The script regenerates:

- `fibonacci_word_generations.csv` — finite Fibonacci words, counts, recurrences, and golden-ratio errors;
- `alphabet_route_reference.csv` — A-to-Z packet branches using the first 26 Fibonacci-word tokens;
- `reference_validation.json` — positive, negative-mirror, reverse, balance, and factor-complexity checks;
- `fibonacci_word_convergence.png` — ordered convergence of length and symbol-count ratios toward the golden ratio.

The reference route is a validator demonstration. It is not a physical-motion simulation and does not replace the live `-1(0)+1` choice architecture.
