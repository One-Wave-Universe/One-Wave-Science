# Rabbit Hopping — Canonical Repository Entry Point

Status: ACTIVE consolidation owner.

This is the repository entry point for Rabbit Hopping. Existing source documents, node validators, memory architecture, and alphabet code remain in place, but new work should start here and follow the owners listed below instead of creating another independent rabbit-hop grammar.

## 1. What Rabbit Hopping is

Rabbit Hopping is the reversible relational route / coordinate / scale-address mechanism.

It answers:

```text
Where did this address come from?
Which operation order produced it?
Which side of the wrapper was used?
Was the route mirrored?
Was traversal forward or opposing?
Can the route be reconstructed exactly?
```

It does **not** by itself answer:

- what a memory means;
- which memory should be selected;
- whether generated content is true;
- which motor action should execute;
- whether a physical One-Wave interpretation is correct.

Those are downstream/domain jobs.

## 2. Locked N-based route grammar

Base address:

```text
N
```

### Double first, then shift

```text
R_after(N,m) = 2N + m
```

### Shift first, then double

```text
R_before(N,m) = 2(N+m)
```

These are not interchangeable routes even when they meet numerically.

For example:

```text
2N + 2m = 2(N+m)
```

Same destination. Different route receipt.

### Wrapper

For any selected center `X`:

```text
X-1 <- X -> X+1
```

If `X` is even, the two neighbors are odd. If `X` is odd, the two neighbors are even.

For adjacent shift-first nests:

```text
2N + 1 = 2(N+1) - 1
```

so the upper connector of one nest is the lower connector of the next.

### Signed mirror

```text
X -> -X
```

Mirroring changes sign/polarity. It does not silently reverse alphabet rank or traversal direction.

### Opposing traversal

Opposing means traverse the declared route in the reverse direction. It is not the same operation as mirroring.

### Alphabet inversion

For A..Z:

```text
A=1 ... Z=26
N_inv = 27-N
```

Alphabet inversion is an adapter operation, not part of generic route arithmetic.

## 3. Exact reconstruction

The route is only reversible when enough receipt context survives.

For double-first:

```text
X = 2N + m
N = (X-m)/2
```

For shift-first:

```text
X = 2(N+m)
N = X/2 - m
```

With wrapper side `s`:

```text
X = 2N + m + s
N = (X-m-s)/2
```

or:

```text
X = 2(N+m) + s
N = (X-s)/2 - m
```

With polarity `p`, remove the sign mirror first:

```text
X_unsigned = p * X_signed
```

then remove wrapper and offset in the recorded operation order.

## 4. Executable owner

Generic executable arithmetic now lives at:

```text
One_Wave_Bench/rabbit_hop/route_core.py
```

Tests:

```text
One_Wave_Bench/rabbit_hop/test_route_core.py
```

Package guide:

```text
One_Wave_Bench/rabbit_hop/README.md
```

The executable receipt currently preserves:

- source `N`;
- route family;
- integer offset;
- wrapper side `-1/0/+1`;
- polarity;
- traversal direction;
- resulting address.

Domain adapters may add domain-specific context, but they must not delete these route facts.

## 5. Alphabet / G-721 adapter

The current alphabet implementation is:

```text
One_Wave_Bench/brain/rabbit_hop_alphabet.py
```

It now consumes the generic route core rather than carrying an independent arithmetic implementation.

Its current A..Z coordinate packet is:

```text
±(n, 2(n+j), 2(n+j)+s)
```

where:

- `n` = forward or inverted alphabet rank;
- `j` = current/next even anchor (`0/1` in this adapter);
- `s` = lower/upper wrapper side (`-1/+1`);
- polarity is independent of alphabet orientation.

Examples preserved by regression tests:

```text
A: (1,2,1) / (1,2,3) / (1,4,3) / (1,4,5)
B: (2,4,3) / (2,4,5) / (2,6,5) / (2,6,7)
Z: (26,52,51) / (26,52,53) / (26,54,53) / (26,54,55)
```

Negative forms are exact sign mirrors. Inverted alphabet rank remains separate.

## 6. Unbounded offset rule

Do not invent a finite stopping value for the route offset merely because the alphabet adapter currently exposes only current/next anchors.

The generic grammar retains integer offsets. Tests include large offsets specifically so the executable core cannot quietly become a two-hop-only implementation.

## 7. Memory use

Rabbit Hopping is the route through memory structure, not the memory itself.

Current rebuild chain:

```text
partial cue
-> constellation neighborhood
-> rabbit-hop route
-> Hopfield-style associative completion
-> Boltzmann-style uncertain fill if required
-> state/context validation
-> rebuilt active memory
```

Keep the jobs separate:

```text
Constellation = relational structure
Rabbit Hopping = reversible navigation/address route
Hopfield = associative completion
Boltzmann = probabilistic/generative fill
Exact receipts = authoritative machine history
Field = proposal/generation
Void = validation/commitment authority
```

A rabbit-hop route receipt may help reconstruct missing memory, but it may not rewrite the exact archive.

## 8. State-machine and scale use

The shared programming loop is:

```text
Micro -> Small -> Mid -> Large -> Macro
-> MIRROR -> RELEASE
-> Large -> Mid -> Small -> Micro
-> PHASE
```

Rabbit Hopping supplies reversible addressing across relational/scale structure. The loop state machine supplies process order. Do not collapse them into the same axis.

A resolved higher-scale object may become a lower-scale anchor in another recursion only when enough receipt information survives to reconstruct how it was formed.

## 9. Point / Path / Field use

The route translator may be used to record a nested handoff such as:

```text
Point_N -> Path_N -> Field_N -> next nested address
```

The arithmetic guarantees only the declared relational map and reversibility. A claim that Point/Path/Field maps to a particular physical mechanism must be tested separately.

## 10. G-721 sequence-family material stays distinct

Existing sequence-family validation lives under:

```text
Nodes/G-721_Sequence_Validation/
```

It includes finite reference validation for Fibonacci/Sturmian, Tribonacci Arnoux-Rauzy, and plastic/Padovan sequence families.

Those sequence grammars may schedule or validate routes. They do not define Rabbit Hopping and do not replace local choice, memory reconstruction, or motor execution.

This distinction is important because several unrelated expressions use forms such as `2n+1` in the repository. Matching notation is not variable identity.

## 11. Repository inventory

### Canonical / architecture

- `RABBIT_HOPPING_CANONICAL.md` — this entry point and authority map.
- `ARCHITECTURE_RABBIT_HOPPING_SCALE_TRANSLATOR.md` — detailed source grammar and reconstruction equations.
- `ARCHITECTURE_MEMORY_REBUILD_CONSTELLATION.md` — Rabbit Hopping inside reconstructive memory.
- `FIELD_VOID_LOOP_BUILD_LADDER.md` — placement in the Micro-to-Macro programming build.
- `PRIMITIVE_BUILD_MAP.md` — integrated primitive placement.
- `ANDROID_BRAIN_ATTACK_MAP.md` — brain/M4 memory and routing constraints.
- `UPDATED_29_ROUTE_GRAMMAR_MOTOR_MEMORY_AND_SIMULATION_STANDARD.md` — route/sequence/motor-memory separation.
- `AUDIT_UPDATED_29_ROUTE_GRAMMAR_MOTOR_MEMORY_AND_MUSTACHE_MATH.md` — audit separating route variables and sequence mathematics.

### Executable

- `One_Wave_Bench/rabbit_hop/route_core.py` — generic arithmetic owner.
- `One_Wave_Bench/rabbit_hop/test_route_core.py` — generic route tests.
- `One_Wave_Bench/rabbit_hop/README.md` — executable package guide.
- `One_Wave_Bench/brain/rabbit_hop_alphabet.py` — alphabet/G-721 adapter.
- `One_Wave_Bench/brain/test_rabbit_hop_alphabet.py` — alphabet regression tests.

### Sequence validation / related route scheduling

- `Nodes/G-721_Sequence_Validation/README.md`
- `Nodes/G-721_Sequence_Validation/sequence_family_validator.py`
- `Nodes/G-721_Sequence_Validation/reference_validation.json`
- associated G-721 finite validation CSV/plot receipts in that directory.

## 12. Anti-drift rules

1. Keep the generic equations in `N`.
2. Preserve parentheses because operation order is route identity.
3. Equal address does not mean equal route.
4. Mirrored, inverted, and opposing are separate operations.
5. Wrapper side and polarity are separate receipt fields.
6. Do not divide back to `N` without first removing the recorded polarity, wrapper, and offset in the correct order.
7. Do not impose a finite offset cap without a domain reason.
8. Do not let an alphabet adapter redefine the generic grammar.
9. Do not let a sequence scheduler redefine local choice.
10. Do not let Rabbit Hopping become the memory store or validation authority.
11. Do not promote route arithmetic into a physical-law proof without a domain-specific experiment.
12. Every compressed scale handoff that depends on Rabbit Hopping must retain a reversible receipt.

## 13. Immediate build target

The next decisive Rabbit Hopping test is not more arithmetic. It is a destructive memory-rebuild benchmark:

1. store two overlapping but distinct constellations;
2. retain exact archive history separately;
3. remove part of one reconstructive memory;
4. cue it with surviving structure;
5. traverse a recorded Rabbit Hop including a wrapper boundary;
6. run associative completion;
7. use probabilistic fill only if ambiguity remains;
8. validate through the state-machine authority path;
9. compare against the untouched exact original;
10. compare against a matched no-rabbit-hop / no-constellation baseline;
11. verify the nearby memory was not collapsed into the target;
12. verify every used route can be reversed from its receipt.

That test determines whether Rabbit Hopping improves reconstruction rather than merely being reversible arithmetic.
