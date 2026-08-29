# Updated 44 — State-Axis Authority and Evolution Rule

**Status:** Canonical terminology and evolution correction

## Why this correction exists

Later executable and M4 work has clarified structures that older files used the word `state` for too loosely. This correction preserves the newer architecture and prevents older shorthand from silently becoming canonical again.

## Current authority

### 1. Two binary choices

From Updated 43:

```text
YES / AGREE
NO / DISAGREE
```

Ground is not a third choice.

### 2. Three ternary moves

```text
DOWN / HOLD / UP
-1   /  0   / +1
```

The two choices and three moves form the six-route address space.

### 3. Six measured oscillator gates

```text
BEGIN -> BUILD(coherent) -> HOLD -> BUILD(unstable) -> BREAK -> LOOP
```

These are measured stability regions around a bidirectional oscillator. They are not lifecycle states and they are not the six-route choice addresses.

### 4. Five downstream commitment/readout states

Updated 43 currently owns the five downstream commitment/readout states:

```text
-3(0)3+ = full disagree
-2(0)2+ = partial disagree
1:1      = unity / Hold reference
+2(0)2- = partial agree
+3(0)3- = full agree
```

Their exact transition map remains unresolved until derived or calibrated. They must not be multiplied into the primitive six-route count.

### 5. Five-state self lifecycle

G-742 independently owns the nonverbal self lifecycle:

```text
IDLE -> PRIMED -> EXECUTING -> VECTORING -> RESOLVING
```

This lifecycle answers where the self/Field process is in its behavioral cycle. It is not the commitment amplitude axis.

### 6. Field/Void routing remains separate

G-740 owns the current domain routing contract:

```text
Field ternary: Express / Hold / Compress
Void ternary:  Confirm / Defer / Deny
```

Quadratic Views travel upward; quadratic Actions travel downward. Oversight is a Void view and Override is a Void action. This layer does not replace the six-route primitive.

## Legacy modulation rule

Older files use neutral `-2,-1,0,+1,+2` as a generic five-level strength/modulation wrapper. That notation may remain for compatibility or local experiments, but it is **not the canonical five-state structure** and must not override Updated 43's five commitment/readout states or G-742's five-state lifecycle.

Likewise, `Micro / Small / Medium / Large / Macro` must not be treated as aliases for lifecycle or commitment. Scale terminology requires its own declared derivation or domain contract.

## Evolution rule

When files disagree, evolve forward by authority and evidence:

1. executable/current correction beats older descriptive shorthand;
2. newer domain nodes constrain older generic files without rewriting unrelated invariants;
3. measured or testable definitions beat labels inferred only from matching counts;
4. identical counts do not imply identical axes;
5. old files are preserved as history, but conflicting claims must be marked compatibility-only or superseded;
6. do not merge a stale branch over newer `main` merely because its PR is mergeable.

## Anti-drift table

| Structure | Count | Current meaning |
|---|---:|---|
| Binary choice | 2 | YES / NO |
| Ternary move | 3 | DOWN / HOLD / UP |
| Route address | 6 | 2 choices × 3 moves |
| Oscillator gates | 6 | Begin / Build / Hold / Build / Break / Loop |
| Commitment/readout | 5 | full/partial disagree, unity, partial/full agree |
| Self lifecycle | 5 | Idle / Primed / Executing / Vectoring / Resolving |
| Field/Void ternaries | 3 + 3 | proposal and oversight resolution |

Matching numbers are not permission to collapse these structures.
