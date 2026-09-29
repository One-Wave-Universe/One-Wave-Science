# Proof ledger — G-721 word grammar + PPF nested receipts

Date: 2026-09-29
Status:
- G-721a arithmetic/word checks: GREEN (validator mathematics)
- G-721b finite Sturmian checks: BRONZE/YELLOW (finite sample, not infinite word)
- PPF nested addressing receipts: GREEN for reconstructability
- Physical CELL_V1 / gravity / consciousness: still YELLOW, not upgraded

## Commands

```bash
python3 scripts/g721_word_grammar_proofs.py
python3 scripts/ppf_scale_hop_receipts.py
```

Locked convention remains `W0=0`, `W1=01`, `Wk=W(k-1)W(k-2)`.
Canonical 26-prefix: `01001010010010100101001001`.

PPF addressing map used for the proof only:
- Point: after, m=0, wrapper +1
- Path: before, m=1, wrapper -1
- Field/Closure: after, m=2, wrapper +1
- Resolved N' = N+1 becomes next Center
