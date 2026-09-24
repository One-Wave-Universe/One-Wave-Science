# Automated Referenced Quality Loop

Goal: repeatedly produce evidence-backed work until it meets a strict acceptance gate or reaches a hard stop.

```text
REFERENCE
   -> FIELD BUILD
   -> VALIDATE / TEST
   -> VOID REVIEW
   -> QUALITY GATE
        | PASS -> PUBLISH / COMMIT
        | FAIL -> TARGETED REPAIR -> loop
```

## A+ means a configured band
`A+` is not praise from the same AI that produced the work. It means the weighted quality score is at least 0.95 and the hard gates also pass:
- all explicit requirements met;
- all tests/validation pass;
- all claims that require references have references;
- Void reviewed the evidence and returned ALLOW;
- drift check passed.

## Repair law
Only failed dimensions return to Field. Passing dimensions are protected. This cuts tokens and prevents good work from being destroyed during revision.

## Reference law
References should be IDs/paths/hashes plus exact supporting ranges where available. Raw sources stay outside the prompt unless needed. The final artifact keeps an inspectable evidence map.

## Hard stop
After the configured cycle limit, stop automatic rewriting and return the unresolved criteria, evidence gaps, and last known-good candidate.

## M4 integration
M4 stores current quality pressure, repeated failure memory, and prior successful repair patterns. The quality loop can use those values to decide whether to hold, re-plan, or switch approach.
