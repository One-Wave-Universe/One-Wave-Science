# G-721 Sequence Family Validation

Finite regression receipts for Fibonacci, a generic Sturmian mechanical word, the Tribonacci Arnoux-Rauzy reference word, and the plastic/Padovan three-rail substitution.

Run:

```bash
python sequence_family_validator.py
```

These receipts validate word construction only. They do not prove an android motor advantage.

## Alphabet/tonal coordinate generator

`alphabet_tonal_generator_validator.py` brute-force verifies G-721's
generator (`p=n+k, r=2p+s, s in {-1,0,+1}`) against all 26 alphabet
positions and all 12 tonal positions: collision-freedom, decoder
inversion, that it reproduces every packet form either the original
single-family or the later two-family proposal produced, that
half-mirror reversal and round-trip orientation-exchange are genuinely
different operators, the alphabet's linear boundary vs. the tonal
cycle's wraparound, and the 12-state/13-visit tonal closure
distinction.

Run:

```bash
python alphabet_tonal_generator_validator.py
```

Writes `generator_verification_receipt.json` (pass/fail summary) and
`alphabet_tonal_table.csv` (full state table for both symbol sets).
These receipts validate the coordinate generator only. They do not
validate embodied movement or any harmonic/chord claim (see E-510 for
that separate domain).
