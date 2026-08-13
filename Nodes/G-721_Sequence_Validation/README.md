# G-721 Sequence Family Validation

Finite regression receipts for Fibonacci, a generic Sturmian mechanical word, the Tribonacci Arnoux-Rauzy reference word, and the plastic/Padovan three-rail substitution.

Run:

```bash
python sequence_family_validator.py
```

These receipts validate word construction only. They do not prove an android motor advantage.

## Alphabet/tonal coordinate generator

`alphabet_tonal_generator_validator.py` brute-force verifies G-721's
generator. The primitive state is the triple `(n,k,s)` -- identity,
reference displacement, local polarity; `p=n+k`, `m=2p`, `r=m+s` are
derived coordinates only. Tested against all 26 alphabet positions and
all 12 tonal positions: collision-freedom, decoder inversion, that it
reproduces every packet form either the original single-family or the
later two-family proposal produced, that half-mirror reversal and
round-trip orientation-exchange are genuinely different operators, the
alphabet's linear boundary vs. the tonal cycle's wraparound, and the
12-state/13-visit tonal closure distinction.

It also verifies three further findings from the degeneracy attack on
the generator:

- **`(p,r)` degeneracy**: `(n=4,k=1)` and `(n=5,k=0)` collide on the
  derived `(p,r)` pair at equal `s`, yet are different `(n,k)` states --
  proof that `n` must be retained independently and `(p,r)` alone is
  not a sufficient coordinate.
- **No privileged `k`**: `k` tested over `[-5,+5]` (not just the
  inherited `{-1,0,1}`) with zero decoder failures and zero collisions
  anywhere in range -- `k=0,±1` are not structurally special.
- **Operator algebra**: the reference-shift operator `T_a:(n,k,s)->(n,k+a,s)`
  composes (`T_aT_b=T_(a+b)`), and the polarity-flip operator
  `P:(n,k,s)->(n,k,-s)` commutes with `T_a` (`PT_a=T_aP`) and is its own
  inverse (`P(P(x))=x`) -- verified over `a,b in [-5,5]` and 45 test
  states.

Run:

```bash
python alphabet_tonal_generator_validator.py
```

Writes `generator_verification_receipt.json` (pass/fail summary) and
`alphabet_tonal_table.csv` (full state table for both symbol sets, `k`
in `{-1,0,1}` -- the extended `k` range and operator-algebra checks are
receipt-only, not part of the CSV table).
These receipts validate the coordinate generator only. They do not
validate embodied movement or any harmonic/chord claim (see E-510 for
that separate domain).
