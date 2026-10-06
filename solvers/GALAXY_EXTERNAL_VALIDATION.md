# Galaxy observable repair and source-qualified test

## Result

The actual, unchanged `GalaxyRotationConstantInherited` candidate was evaluated
against all 45 published Milky Way circular-speed bins, with parameters frozen
before evaluation and no fitting. Constructor-default scale **30** gives
**86.283139 km/s RMS (40.990047%)**; the separately declared sensitivity using
legacy calibration **39.23** gives **81.647035 km/s (38.787600%)**.
Both fail the predeclared coarse 10%-relative-RMS discrepancy screen. This is a
failure of these fixed candidates, not a proof that every possible One-Wave
source law fails. Passing a software test never confirms physical claims.

The executable now produces a complete, source-locked receipt instead of an
unconditional success assertion. The original model implementation remains
unchanged. `satellite_galaxy_validator_em_coherence_fixed.py` also now actually
uses its stated 38.69 scale rather than the inherited 39.23 instance value and
can be imported without printing a report. Its corrected historical comparison
is MW 26.1%, M31 3.1%, still an unmatched-observable comparison and not proof.
No satellite was removed to obtain those means.

## Reproduce

From the repository root (Python 3 with NumPy and SciPy):

```sh
python -m unittest discover -s solvers -p test_galaxy_validation.py -v
python solvers/test_galaxy_validation.py -v
python solvers/galaxy_external_validation.py --output /tmp/galaxy-result.json
```

The last command returns **1** for the measured scientific screen failure,
**0** only if every candidate passes that limited screen, and **2** for invalid
or stale inputs. It always preserves valid evaluated rows in the JSON receipt.
There is no online fetch, synthetic fallback, optimizer, dropped row, or
outcome-conditioned parameter selection. Source/input changes require a new
explicitly reviewed contract; hash mismatches fail closed.

- Frozen data and model contract: `data/mw_dr3plus_contract.json`
- Complete transcription: `data/mw_dr3plus_2023.csv`
- Executed output: `galaxy_external_validation_receipt.json`
- Source model SHA256: `d38673ac9353b1c895a5391c59786a91ec2740d819511e64308eeffc6b429efa`
- Contract SHA256: `63b215c408eb57fe89db68c71e5a71e212b1b0ad7688410e8f87dc73288765ff`

## External evidence and independence limits

Francesco Sylos Labini, Zofia Chrobakova, Roberto Capuzzo-Dolcetta and Martin
Lopez-Corredoira, *Mass Models of the Milky Way and Estimation of Its Mass from
the Gaia DR3 Data Set*, ApJ **945**, 3 (2023), Table 1, page 3.
[DOI](https://doi.org/10.3847/1538-4357/acb92c),
[primary published PDF](https://discovery.ucl.ac.uk/id/eprint/10202950/1/mass_models.pdf).
CC BY 4.0; attribution retained. All 45 rows were transcribed without change
from primary-source extracted text and independently checked row by row.
Raw PDF download was unavailable; no raw-PDF checksum is claimed.

DR3+ combines Eilers (2019) and Wang (2023). It reports inferred midplane
circular speed under time-independent, axisymmetric Jeans and tracer-density
assumptions, not raw directly measured orbital speeds. The source discusses
non-equilibrium and structural systematics. Full covariance is not supplied
here. Diagonal chi-squared values (93804.8029 and 80551.3189) are diagnostics,
not p-values or detection significances. The 10% screen is a transparent coarse
engineering discrepancy screen, not a confidence criterion.

This is an **external published-data evaluation**, not a blind or proven
independent validation. The old loader's manually embedded MW/M31 arrays are
not this 45-row table, but their ultimate calibration history is incomplete;
observational overlap cannot be excluded. Default 30 is the original rotation
constructor default. 39.23 is a reused value documented in the satellite base;
we do not claim it is the optimal rotation-model calibration. Neither was
learned from these 45 bins. Both outcomes are retained.

## Correct observable mapping

A satellite's center-of-mass orbital velocity, its internal stellar dispersion,
and a galaxy's circular rotation speed are different measurements. For any
uniform line-of-sight bulk velocity V,

`sigma² = mean[(v_i - mean(v))²] = mean[((v_i+V)-mean(v+V))²]`.

The executable tests that identity and a nonuniform-motion counterexample.
A common translation cannot supply internal dispersion or center-subtracted
disk rotation. This does **not** exclude a spatially varying wake that changes
internal restoring acceleration. Such a wake needs an explicit source law and
forward projection, rather than adding a bulk speed to a measured dispersion.

For a spherical, steady, dispersion-supported tracer with density nu, radial
variance sigma_r², anisotropy beta and inward acceleration g(r), the appropriate
conditional forward route is the Jeans relation

`d(nu sigma_r²)/dr + 2 beta nu sigma_r²/r = -nu g(r)`

followed by line-of-sight projection and the measurement aperture/selection.
This is an observable-mapping assumption, not a replacement for One-Wave gravity.
The g(r) would have to come from the independently specified One-Wave source
solution. See [Wolf et al. (2010)](https://doi.org/10.1111/j.1365-2966.2010.16753.x)
for the standard tracer/dynamical observable contract. Disrupted satellites need
an appropriate non-equilibrium treatment; selection must precede scoring.

## What the One-Wave field must actually produce

[A-115](../Nodes/A-115_Unified_Compression_Field.md) and
[C-320](../Nodes/C-320_Magnetic_Compression_Path_Coupling.md) specify
`g_OW = -alpha_g K_L grad(chi)`. Under the stated midplane circular balance,
using outward R and positive inward acceleration magnitude:

`alpha_g (K_L grad chi)_R = v_c(R)²/R`.

The measured necessary acceleration is **3.17524e-10 m/s² at 5.25 kpc** and
**3.72168e-11 m/s² at 27.25 kpc**. Every bin is retained in the receipt.
Under a chosen additive radial-acceleration decomposition with the legacy local
component, the missing requirement is `(v_c²-v_local²)/R`. For scale 39.23 its
endpoint values are **3.07151e-10** and **3.70002e-11 m/s²**. This is not the same
as assigning acceleration to a linearly added speed; squaring a sum introduces
a cross-term. It is an inverse empirical requirement, **not a prediction**, and
is never fed back into the evaluated model.

For the old *additive-speed* ansatz, the required residual speed is 160.764–
209.368 km/s across all bins with scale 39.23, rather than its fixed 110 km/s.
This identifies the missing spatial response; it does not derive that response.
If K_L=I, circular balance constrains only `d(alpha_g chi)/dR = v_c²/R` along the
midplane. Even its radial integral leaves an additive constant, vertical
structure, the displacement field and source undetermined. With unknown K_L,
there are additional tensor/gradient degeneracies.

A real forward completion must fix the source J_source, coefficients including
alpha_g, physical length/time calibration, initial/boundary conditions, and
independently constrained K_L, then solve for chi and project the resulting
tracer dynamics. Circular-speed data alone cannot uniquely identify all these
unknowns. No dark-matter, MOND or other gravity model has been substituted and
called One-Wave. No node gate has been promoted.

## Branch-step record

MAIN GOAL: build a reliable Field/Void software-construction engine for code,
apps and programs. This step adds a reproducible source-qualified science test
and executable evidence gates to that engine's solver work.

Reference: `One-Wave-Universe/One-Wave-Science`, main
`4f23a49afd17577d0b25ef3c4055eff0586b5fee`; clean ephemeral cloud execution checkout
`/workspace/shared/science-galaxy-validation-20261006`; branch
`fix/galaxy-observable-validation-20261006`. This is not device execution or a
second maintained canon. Read AGENTS, GENERAL_REFERENCE_RULES,
AI_CANONICAL_START_HERE, AI_BRIDGE_START_HERE, BRANCH_STEP_PROJECT_TEMPLATE,
Truth Computer builder specification, A-115, C-320 and Book 5 chapter 1.
The referenced JETSON_OPENCLAW_RUNTIME.md was absent; no Jetson/M4 execution is
claimed. Parent established no available connected task environment. No external
Claude connection was used or claimed; review is a separate same-model worker.

Current step: correct the fixed-parameter bug and establish one falsifiable,
properly matched external galaxy test. Protected: existing source law, catalog,
other research lanes, node metadata, device work, database and job systems.
Allowed files: the fixed-EM module, this report and summary warning, new
external runner, two data files, receipt and focused tests.

Cycle 1: Reference clean; Choice parameter restore plus import guard; independent
pre-review ALLOW; Move exactly that; View two tests and executable pass; independent
post-review ALLOW, reporting-body AST unchanged. State RESOLVED software bug,
DO NOT SCALE physical claim; Reentry continues to separate observable test.

Cycle 2: refreshed same HEAD and owned diff; fixed external contract reviewed
ALLOW before prediction. Move all-row fixture, hash locks, runner, receipt and
controls. View six tests pass, scientific screen fails as measured; independent
review reproduces both outcomes, all 45 data rows and 90 SI gap calculations.
State RESOLVED evaluation, fixed candidates fail; no broader physical closure.
Reentry identified direct-test entrypoint ordering to repair, not hide.

Cycle 3: fresh same HEAD/diff, independent pre-review ALLOW for test entrypoint,
this evidence report and narrow historical-claim warnings. Move main guard to
test-file end. Both entrypoints run all six tests at this stage. Attempt 1 per approach;
no failed implementation attempts disguised. Final post-review recorded in PR.

Look-back: the bug fix works; the forward candidate does not reproduce the
published profile. Real-data provenance, correct observables and inverse field
requirements now replace unconditional confirmation. Hypotheses remain available
for further source-derived testing. Hard stop: reviewed reproducible patch;
next permitted step requires fresh Reference and an independently closed source
model, not parameter selection against this receipt or further outcome-driven
satellite exclusions.

Cycle 4: refreshed same HEAD/owned diff; reviewer ALLOW for fixture-specific
FAIL assertions and CLI exit/receipt regression. Seven tests pass. No model or
data change. State RESOLVED and next reporting defect explicitly identified.

Cycle 5: fresh same reference, reviewer ALLOW to replace unsupported runtime
confirmation with INVALID_COMPARISON while retaining all numerical diagnostics.
A runtime report regression preserves MW 26.1% and M31 3.1% and excludes old proof
phrases. Final direct/discovery entrypoints run eight tests. The legacy docstring
retains the historical hypothesis under its explicit evidence warning.
