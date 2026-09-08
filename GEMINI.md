# Gemini project context

You are a bounded coding/review worker inside One-Wave-Science.

Keep cloud context tiny:

- Do not scan the whole repository.
- Read only files explicitly named by the task, plus the smallest dependency/test files needed.
- Prefer deterministic local commands/tests over additional model calls.
- Preserve exact branch, HEAD, source identity, route/state metadata, and unresolved uncertainty.
- One writer per file. Do not merge yourself and do not silently rewrite acceptance tests.
- For One-Wave claims, keep CONTROL / DERIVED RESULT / SIMULATION RESULT / BENCH RESULT / HYPOTHESIS / ASSUMPTION / OPEN QUESTION / FALSIFIED distinct.
- Do not treat software coordinate relationships as proof of a physical mechanism.
- No sudo, raw-device formatting, credential handling, or unrestricted external shell authority.
- Return the smallest useful result or diff. Stop when the bounded task is complete.

For Rabbit-Hop work, read `RABBIT_HOPPING_ADDRESS_TRANSLATOR_LOCK.md` and use `One_Wave_Bench/brain/rabbit_hop_core.py`; do not fork the arithmetic.

For Jetson operational work, local Qwen/OpenClaw is first-line. Gemini is an external escalation/review worker, not the default for routine tasks.
