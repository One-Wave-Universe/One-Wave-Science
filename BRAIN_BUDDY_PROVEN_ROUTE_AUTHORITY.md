# Brain Buddy Proven Route Authority

**Status:** Operational authority for Gemini / DeepSeek bridge selection  
**Rule:** A successful route is evidence. A proposed route is not a replacement until it independently passes the same probe.

## Mandatory carry-forward law

1. Every successful external-model execution must leave a receipt containing timestamp, worker, exact entry point, transport, repository/ref, probe, and returned result.
2. The newest **verified success** for a worker is its last-known-good route.
3. Refactors may add candidate routes, but MUST NOT silently replace a last-known-good route.
4. A candidate becomes preferred only after the canonical probe succeeds through that exact route.
5. Failure of a newer candidate MUST fall back to the last-known-good route when that route is still available.
6. Timeout, connection refusal, missing listener, or missing receipt is **not** evidence that the model itself is unavailable.
7. Never report "Gemini failed" or "DeepSeek failed" when only a transport failed. Report the exact failed transport.
8. Never infer success from service state, code presence, a queued packet, or a tool call. Success requires returned model text plus a receipt.
9. Never infer failure of an older route from failure of a newer route.
10. Preserve successful receipts. Do not overwrite or reinterpret them to match current architecture.

## Canonical route probe

The minimum probe is:

`Return exactly: BRAIN_BUDDY_ROUTE_OK`

For repo-grounded verification use:

`After following the mandatory repository reference chain, answer with BRAIN_BUDDY_ROUTE_OK and name the three authority files you read.`

Expected authorities:
- `GENERAL_REFERENCE_RULES.md`
- `AI_CANONICAL_START_HERE.md`
- `Governance_I_Series/I-06_Canonical_Node_Metadata_and_Alias_Resolution.md`

## Verified historical evidence

Receipt `External_Work/brain_buddy/outbox/council-both-20260929-140303.md` records a genuine Gemini return:
- result: `BRAIN_BUDDY_ROUTE_OK`
- authority files named correctly.

That receipt proves Gemini completed that execution. It does **not** prove every later relay or wrapper works.

The same receipt shows DeepSeek emitted a `jetson_run` request to read the authority files. That is evidence of worker/tool-call progress, **not** a completed DeepSeek answer. Do not upgrade it to a successful completed return.

## Current transport distinction

The council wrapper may use Dell web relay endpoints for Gemini and DeepSeek. Those relay endpoints are transport choices, not model identity.

A connection refusal from a Dell relay means:
`RELAY_UNAVAILABLE`

It must never be collapsed into:
`MODEL_UNAVAILABLE`

Direct/minimal worker paths and web-relay paths must remain separately named and separately tested.

## Required fallback behavior

For each worker maintain:

`candidate route -> probe -> PASS ? promote : retain last-known-good -> fallback/retry -> receipt`

If no verified route is currently executable, return HOLD with:
- last-known-good receipt,
- exact route that was attempted,
- exact failure,
- next recovery action.

## Forbidden assumptions

Do not assume:
- latest code = last working code;
- newest transport = preferred transport;
- service active = end-to-end return works;
- queued request = model response;
- tool call = completed answer;
- one worker's success proves the other worker;
- relay failure proves provider/model failure;
- an old successful route is obsolete unless a verified replacement supersedes it.

## Change gate

Any PR changing Brain Buddy transport/orchestration must include:
1. before-route receipt,
2. after-route canonical probe receipt,
3. explicit fallback path,
4. doctor check that distinguishes MODEL / TRANSPORT / AUTH / REPO-GROUNDING / RETURN-PATH failures.

No receipt -> no promotion.
