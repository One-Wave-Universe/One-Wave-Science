# OWATCH logic kernel (next layer)

Not a cell. Not emergence. Not route-as-truth.

Gemini lock-in + DeepSeek no-inference: build this before more flower topology.

## Inputs
Sentence-level edges only for v1: SUPPORTS, CONTRADICTS.
Each edge: source span id, target span id, reference, intention, consequence.
Missing any of those three → HOLD. No derivation.

## Deterministic rules (v1)
- SUPPORTS(A,B) and SUPPORTS(B,C) → propose SUPPORTS(A,C) as DERIVED, never as canon.
- CONTRADICTS(A,B) and SUPPORTS(C,A) → propose CONTRADICTS(C,B) as DERIVED.
- CONTRADICTS(A,A) or cycle A⇔B⇔A of CONTRADICTS with no third referee → HOLD + terminate that route.
- Two derived CONTRADICTS that close a loop → HOLD. Do not write Nodes/. Do not strengthen route memory.

## Termination harness
Deliberate circular contradiction corpus. Pass if:
1. loop stops (no infinite propose),
2. HOLD fires,
3. route hysteresis for that path is decayed, not boosted,
4. later unrelated queries are not poisoned.

## Receipts
wrong_derivations, correct_derivations, holds, hysteresis_boost_on_bad_path (must be 0).

## Authority
route_memory_is_authority: false
derived ≠ source markdown
Flower/cell sims remain software twins for fan-out/contention tests only.
