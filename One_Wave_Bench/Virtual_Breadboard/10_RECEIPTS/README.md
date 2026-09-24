# Receipts

Run `node 10_RECEIPTS/generate_receipts.js` (or `npm run receipts`) after any
change. It re-runs `test/regression-builds/*.js`, `test/qualification.test.js`,
and `test/primitives.test.js`, and writes one receipt file per check in the
canonical form (`00_RULES/architecture.md`'s required shape) to:

- `current/` — this run's full receipt set, cleared and rewritten every time.
- `passing/` — this run's PASS receipts only.
- `failing/` — this run's FAIL receipts only. Empty when everything is green.

The generator exits non-zero if anything failed (or if a suite crashed before
completing — `qualification.test.js`/`primitives.test.js` throw on their first
failing check, so a crash means "everything after this check is unknown," not
"everything after this check passed").

`current/`, `passing/`, and `failing/` are gitignored, not committed: they are
regenerated output, and the real, durable permanence guarantee the canon wants
("the first time something passes, it becomes a permanent regression
requirement") comes from the version-controlled *test suites themselves*
(`test/qualification.test.js`, `test/primitives.test.js`,
`test/regression-builds/`) staying green — a committed receipt file goes stale
the moment the code it describes changes, and 145 near-duplicate text files
churning on every commit would be worse repo hygiene than the problem it
solves. Run `npm run receipts` any time you want the current, real snapshot.

## Not yet automated

- `regressions/` and `history/` (per the canon's directory list) — comparing
  today's `current/` against a prior run to flag anything that used to pass and
  now doesn't. Real, valuable, scoped future work; not built yet. Until it
  exists, "did this regress" is answered by reading `failing/` after a run and
  by the fact that all four test suites are already permanent — a real
  regression shows up as a failing suite, just not yet as a named diff.
- `test/circuit.test.js` — uses `assert.ok()`/a custom `approx()` helper, not
  the `qual()`/`check()` structured-record pattern the other three suites use,
  so it has no structured records to export yet. It still runs and must still
  pass (`npm test`); giving it the same instrumentation is separate Layer-09
  work.
