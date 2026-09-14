# MATH BACKBONE 30B — CERN SOURCE MASS LINEAGE AUDIT v1

Status: **YELLOW SOURCE-LINEAGE RESULT / TRANSFORM UNAFFECTED**

Depends on:
- `30_cern_fourvector_to_wave_transform_v1.md`
- `30A_cern_csv_rounding_interval_v1.md`

CORE-RULES-PRE:
- Preserve the failed fixed-tolerance test.
- Preserve the failed displayed-rounding-only redundancy test.
- Do not invent a hidden reconstruction algorithm that the CERN record does not document.

## 1. Reference

CERN CMS Open Data record 545 describes the release as an educational derived dataset containing a subset of total event information. It defines the published `E, px, py, pz` columns as lepton energy/momentum components and `M` as the invariant mass of the two leptons.

The record does not state that the printed `M` value was generated from the exact rounded decimal values appearing in the same CSV row.

Therefore `M` must be treated as a source-provided derived observable with its own lineage unless the generation code proves otherwise.

## 2. Live audit result

For the first 5,000 events of `Dimuon_DoubleMu.csv`:

- 10,000 individual muon objects were transformed;
- maximum center-value difference between `M` and a recomputation from printed four-vectors: 0.017016449838837655 GeV;
- 52 events remained outside the interval explainable solely by the displayed decimal rounding;
- maximum remaining interval gap: 0.006236910768313564 GeV;
- 52 individual four-vectors also produced negative `E^2-p^2` after printed-value rounding;
- no object produced a beta-above-one warning beyond the declared tolerance.

The coincidence in the count of 52 is an observation, not yet a proven causal explanation.

## 3. Correct classification

The converter must expose both quantities:

\[
M_{source}
\]

and

\[
M_{recomputed}=\sqrt{(E_1+E_2)^2-|\vec p_1+\vec p_2|^2}.
\]

It must also expose their difference and the displayed-rounding interval gap.

But a nonzero gap is not, by itself, a failure of the particle-to-wave transform because that transform uses each published four-vector directly.

Instead classify the event as:

- `SOURCE_M_REPRODUCIBLE_FROM_PUBLISHED_VALUES` when the intervals overlap;
- `SOURCE_M_LINEAGE_NOT_REPRODUCIBLE_FROM_PUBLISHED_VALUES` when they do not.

The second label means exactly what it says. It does not accuse the CERN data of being wrong.

## 4. What would resolve the lineage

A stronger source audit can resolve the difference by locating the original extraction code and determining whether `M` was computed:

- before decimal truncation/rounding;
- from a higher-precision four-vector;
- with an explicit muon-mass assignment;
- from another reconstructed object representation;
- or by another documented route.

Until that source path is proven, the cause remains OPEN.

## 5. Transform kill tests after this audit

The four-vector-to-wave transform still fails if:

1. it changes the source `E,px,py,pz` values;
2. its own standard algebra is internally inconsistent;
3. it hides finite-precision warnings;
4. it labels derived values as detector measurements;
5. it labels scaled bench analogs as physical collision frequencies;
6. it uses the unexplained `M` discrepancy as evidence for One-Wave.

It does **not** fail merely because a separate source-provided `M` column cannot be exactly reconstructed from the rounded educational subset.

CORE-RULES-POST:
- Both failed checks remain recorded.
- No arbitrary tolerance was introduced.
- The discrepancy was narrowed to data lineage rather than erased.
- The One-Wave ontology gained no evidentiary credit from the discrepancy.
- Drift detected: no.
