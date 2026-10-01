# Brain Buddy App — Branch-and-Prove Development Rule

**Status:** Mandatory development rule.

Brain Buddy is the persistent outer conversation app. Gemini is the first worker. DeepSeek and future systems are added only after the Gemini path is proven.

## Protected baseline

A last-known-good Brain Buddy behavior is never edited experimentally in place.

The historical back-and-forth discussion behavior and verified successful Gemini route are evidence-bearing baselines. Preserve their commits and receipts.

## Upgrade law

Every change follows:

`PROVEN BASELINE -> NEW BRANCH -> ONE CHANGE -> TEST -> RECEIPT -> COMPARE -> PROMOTE OR DISCARD`

1. Branch from the exact last-known-good commit/ref.
2. State the single upgrade being attempted.
3. Do not alter the protected baseline while testing.
4. Re-run the baseline probe on the new branch.
5. Test the new behavior.
6. Save receipts for both.
7. If baseline behavior regresses, the branch fails.
8. If the upgrade works and baseline still passes, it may be merged/promoted.
9. A failed experiment is abandoned or repaired on its branch; never redefine the baseline to make it pass.
10. Only one AI worker is brought to reference quality at a time.

## Brain Buddy app primitive

The app owns the continuing session:

`USER <-> OUTER SHELL <-> REFERENCE <-> GEMINI <-> REFERENCE <-> OUTER SHELL <-> USER`

The shell remains alive while a worker is thinking. Worker returns are events reinjected into the same session, not terminal responses that end it.

Back-and-forth is the primitive:
- append each real turn;
- rebuild bounded context from the same session;
- allow user redirection between rounds;
- preserve provenance;
- keep canonical repo reference in the loop;
- never invent a worker turn during timeout/failure.

## Branch naming

Use focused branches such as:
- `feature/brain-buddy-gemini-session`
- `feature/brain-buddy-async-shell`
- `feature/brain-buddy-android-ui`
- `fix/brain-buddy-gemini-return`

Do not combine unrelated upgrades merely because they touch Brain Buddy.

## Promotion gates

A branch cannot replace the current Brain Buddy baseline until it proves:
- canonical repo grounding;
- Gemini end-to-end return;
- at least two genuine back-and-forth rounds;
- user redirection is carried into the next Gemini turn;
- conversation survives process/app restart;
- worker response provenance is retained;
- transport failure does not corrupt the session;
- prior successful behavior still passes.

## Future workers

Do not build DeepSeek parity while Gemini continuity is still changing.

After Gemini passes the complete app contract, freeze that worker interface. DeepSeek then gets its own branch and must pass the same contract without changing Gemini's proven path.

**Working law: preserve what works; branch what changes; prove before promotion.**
