# ONE-WAVE PUBLIC DATA PIPELINES — AI START HERE

Status: **SOURCE-FIRST ROADMAP / OPERATIONAL CERN + GWOSC / OTHER SOURCES QUEUED**

## CORE-RULES-PRE

Before using any external scientific dataset:

1. read `CORE_RULES_LOCK.md`;
2. read `MATH_BACKBONE/00_MATH_BACKBONE_LOCK.md`;
3. read the dataset-specific math-backbone file;
4. preserve source fields and source identity;
5. label measured, reconstructed, standard-derived, simulated, and scaled-analog quantities separately;
6. do not promote a One-Wave interpretation unless it produces a quantitative prediction and survives the same accepted target.

## 1. CERN / CMS — excitation, mass, direction, resonance, decay

Operational now:

```text
tools/cern_wave/HOWTO_FOR_AI.md
tools/cern_wave/cern_wave_convert.py
tools/cern_wave/cern_wave_receipt.py
MATH_BACKBONE/30_cern_fourvector_to_wave_transform_v1.md
```

Use for:

- four-vector -> wave-equivalent views;
- mass/excitation hypotheses;
- angular/path geometry;
- resonance structure;
- future decay-width/lifetime work;
- later jet/track/PF confinement tests.

First source:

```text
https://opendata.cern.ch/record/545
```

## 2. GWOSC / LIGO-Virgo-KAGRA — direct wave strain

Operational pipeline being qualified:

```text
tools/gwosc_wave/README.md
tools/gwosc_wave/gwosc_strain_wave.py
MATH_BACKBONE/31_gwosc_strain_wave_analysis_v1.md
```

Use for:

- direct detector strain `h(t)`;
- frequency evolution;
- phase/timing comparison across detectors;
- propagation/dispersion tests;
- waveform residual tests;
- gravity-wave claims.

Source/API:

```text
https://gwosc.org/
https://gwosc.org/api/v2/
```

First live target:

```text
GW150914-v2 / H1 + L1 / 32 s / 4 kHz
```

## 3. NASA/JPL Horizons — orbital mechanics and three-body pressure tests

Priority: **VERY HIGH**

Source/API:

```text
https://ssd.jpl.nasa.gov/horizons/
https://ssd-api.jpl.nasa.gov/doc/horizons.html
```

Use vector ephemerides for:

- Sun/Earth/Moon nested motion;
- Earth/Moon/Sun three-body comparisons;
- planetary and satellite orbital residuals;
- path curvature and timing;
- any One-Wave gravity/displacement prediction.

Required future pipeline output:

```text
time
body/source IDs
reference center
x,y,z
vx,vy,vz
source units/frame
pair distances
relative velocities
One-Wave prediction residual
standard ephemeris residual
```

Do not tune a gravity coefficient to Horizons after seeing the trajectory and call that a derivation.

## 4. IceCube — neutrino time / energy / direction

Priority: **HIGH**

Source:

```text
https://icecube.wisc.edu/science/data-releases/
```

Use for:

- arrival direction;
- reconstructed energy;
- event time;
- long-distance propagation tests;
- multi-messenger comparisons;
- neutrino-specific One-Wave "wave death" or attenuation hypotheses.

The current public IceTracks releases include long-baseline track-like event data. Treat reconstruction/systematic information as part of the source, not as optional noise to throw away.

## 5. Fermi GBM / LAT via NASA HEASARC — photons and transient timing

Priority: **HIGH**

Sources:

```text
https://heasarc.gsfc.nasa.gov/
https://heasarc.gsfc.nasa.gov/docs/archive/apis.html
```

Useful data classes:

```text
Fermi GBM Trigger Catalog
Fermi GBM Burst Catalog
Fermi GBM Daily Data
Fermi LAT source/event products
```

Use for:

- photon arrival timing;
- energy-dependent propagation tests;
- gamma-ray burst pulse structure;
- multi-messenger comparison with GWOSC and IceCube;
- redshift/propagation hypotheses when source distance/redshift is independently known.

## 6. NANOGrav — nanohertz timing / ultra-long wave baseline

Priority: **HIGH**

Source:

```text
https://nanograv.org/science/data
```

Use for:

- pulsar time-of-arrival residuals;
- ultra-low-frequency gravitational-wave structure;
- long-baseline phase/timing tests;
- scale-recursion tests between LIGO-band and pulsar-timing-band gravitational phenomena.

Do not assume a shared mechanism merely because both data sets are expressed as waves/timing residuals. Derive the scale transformation first.

## 7. Gaia DR3 — precision astrometry and orbital geometry

Priority: **HIGH**

Source:

```text
https://gea.esac.esa.int/archive/
```

Use for:

- positions;
- parallax;
- proper motions;
- radial velocities;
- binary/multiple-system orbital tests;
- wide-scale gravitational residuals.

Gaia is especially valuable for testing whether an orbital/gravity rule survives outside Solar-System tuning.

## 8. DESI — redshift / cosmology pressure tests

Priority: **HIGH for cosmology**

Source:

```text
https://data.desi.lbl.gov/doc/
```

Use for:

- spectra and measured redshifts;
- large-scale redshift distributions;
- BAO comparison products where appropriate;
- One-Wave no-expansion / tired-light / propagation alternatives.

Do not use a redshift catalog alone as proof of either expansion or no expansion. Compare explicit competing distance/redshift/time-dilation/surface-brightness predictions.

## 9. CMB archives / Planck products — early-universe / large-angle structure

Priority: **MEDIUM-HIGH**

NASA HEASARC/LAMBDA and ESA public CMB products can pressure-test:

- angular power spectra;
- scale-dependent structure;
- any One-Wave background-field claim;
- cosmology models that attempt to replace expansion-based interpretation.

A One-Wave cosmology must reproduce the measured angular/statistical structure, not only offer a different verbal origin story.

## Recommended build order

```text
1. CERN four-vectors                         [WORKING]
2. GWOSC direct strain                       [BUILDING / LIVE TEST]
3. JPL Horizons orbital + three-body vectors [NEXT]
4. IceCube event time/energy/direction
5. Fermi burst photon timing/energy
6. GWOSC + Fermi + IceCube multi-messenger joins
7. NANOGrav timing residuals
8. Gaia astrometry / multiple systems
9. DESI redshift/cosmology
10. CMB/Planck statistical structure
```

## Common output contract for every pipeline

Every durable record should carry:

```text
source_project
source_release
source_url / DOI / record ID
retrieval timestamp or release identifier
source units
source coordinate/frame conventions
source measured/reconstructed fields
source checksum when a file is downloaded
transform version
derivation class
analysis choices
uncertainty/systematic fields
One-Wave status
PASS / FAIL / OPEN
```

Recommended derivation classes:

```text
SOURCE_MEASURED
SOURCE_RECONSTRUCTED
STANDARD_DERIVED
DIRECT_WAVE_SOURCE
SIGNAL_ANALYSIS_DERIVED
SCALED_ANALOG
ONE_WAVE_PREDICTED
```

Never collapse these classes into one column called "data."

## Cross-source goal

The important future result is not a giant pile of unrelated datasets.

The goal is a shared comparison layer where the same One-Wave equation must survive different regimes:

```text
CERN          -> microscopic excitation / momentum / decay
IceCube       -> high-energy long-distance propagation
Fermi         -> photon energy / transient timing
GWOSC         -> direct gravitational strain
NANOGrav      -> nanohertz timing
JPL Horizons  -> orbital / three-body motion
Gaia          -> stellar astrometry / multiple systems
DESI          -> cosmological redshift structure
CMB           -> large-scale statistical structure
```

If a parameter or definition must quietly change from one source to another, flag drift instead of rescuing the theory.

## CORE-RULES-POST

- Data-source roles remain separate.
- No source is presented as One-Wave evidence merely because a compatible representation exists.
- Each future pipeline requires its own explicit math/transform node.
- Cross-scale analogy does not count as proof without a declared transformation law and invariant.
- The recommended order prioritizes hard quantitative tests over visual pattern hunting.
- Drift detected: no.
