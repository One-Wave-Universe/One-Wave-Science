# MATH BACKBONE 31 — GWOSC STRAIN WAVE ANALYSIS v1

Status: **YELLOW / DIRECT WAVE DATA PIPELINE DEFINED / ONE-WAVE MECHANISM OPEN**

## CORE-RULES-PRE

Relevant core rules: 1, 2, 3, 5, 6, 7, 10, 12, 14, 15, 16, 17, 18.

Authoritative source class: Gravitational Wave Open Science Center calibrated detector strain time series and event metadata.

This node does not translate a particle label into wave language. GWOSC strain is already a measured/calibrated wave observable: dimensionless strain as a function of time.

The job here is to preserve that direct wave measurement and derive transparent time/frequency quantities without turning a spectral feature into a One-Wave mechanism by assertion.

## 1. Source observable

Detector strain is

\[
h(t)=\frac{\Delta L(t)}{L},
\]

which is dimensionless.

For sampled data with sample rate \(f_s\),

\[
\Delta t = \frac{1}{f_s},
\]

and sample times are

\[
t_n=t_0+n\Delta t.
\]

The source strain values must remain available unchanged.

## 2. Analysis window

Choose an explicit interval containing \(N\) samples.

For event-centered work,

\[
n_c \approx (t_{event}-t_0)f_s.
\]

The window length and event offset are analysis choices and must be written into the receipt.

Subtract the sample mean

\[
\bar h = \frac{1}{N}\sum_{n=0}^{N-1}h_n,
\]

\[
x_n=h_n-\bar h.
\]

Mean subtraction is preprocessing, not a change to the stored source values.

## 3. Hann window

For spectral leakage control use

\[
w_n=\frac12\left(1-\cos\frac{2\pi n}{N-1}\right).
\]

Windowed samples are

\[
y_n=w_n x_n.
\]

The Hann choice is declared processing. A different window requires an explicit new comparison, not a silent change.

## 4. Discrete Fourier transform

Define

\[
Y_k=\sum_{n=0}^{N-1}y_n e^{-i2\pi kn/N}.
\]

Frequency bin

\[
f_k=\frac{k f_s}{N}.
\]

For real strain data, the positive-frequency half of the transform contains the non-redundant spectrum.

Frequency resolution is

\[
\Delta f=\frac{f_s}{N}.
\]

## 5. One-sided periodogram PSD

Let

\[
W_2=\sum_{n=0}^{N-1}w_n^2.
\]

The raw two-sided periodogram normalization is

\[
S_k=\frac{\Delta t}{W_2}|Y_k|^2.
\]

For positive-frequency interior bins in a one-sided spectrum,

\[
\boxed{P_k=2\frac{\Delta t}{W_2}|Y_k|^2}.
\]

At DC and Nyquist the factor of two is not applied.

Units are

\[
[P_k]=\mathrm{strain}^2/\mathrm{Hz}.
\]

Amplitude spectral density is

\[
\boxed{A_k=\sqrt{P_k}}
\]

with units

\[
[A_k]=1/\sqrt{\mathrm{Hz}}.
\]

This is a transparent raw-window periodogram. It is not a substitute for the collaboration's calibrated search pipelines, whitening, matched filtering, parameter estimation, or detector-noise characterization.

## 6. Time-domain receipts

For an analysis interval define RMS strain

\[
h_{RMS}=\sqrt{\frac1N\sum_{n=0}^{N-1}x_n^2}.
\]

Peak absolute strain is

\[
h_{peak}=\max_n |x_n|.
\]

These are direct derived descriptors of the chosen segment.

## 7. Band-limited spectrum

For declared band \([f_{min},f_{max}]\), retain only bins satisfying

\[
f_{min}\le f_k\le f_{max}.
\]

Integrated periodogram power over that band is approximately

\[
P_{band}=\sum_{k\in band}P_k\Delta f.
\]

A spectral centroid may be calculated as

\[
\boxed{f_c=\frac{\sum_{k\in band} f_k P_k}{\sum_{k\in band}P_k}}
\]

when the denominator is nonzero.

This is a descriptor of raw detector strain in the chosen interval. It must not be called the source's fundamental frequency without additional analysis.

## 8. Multi-detector comparison

For detectors A and B, source records remain separate.

A later cross-correlation or timing node may compare

\[
h_A(t)
\]

and

\[
h_B(t+\tau).
\]

The relative delay \(\tau\) must be estimated from the data or taken from an identified standard analysis result; it may not be chosen to make a One-Wave geometry fit.

Detector antenna response, calibration, sky location, and polarization sensitivity must be included before interpreting amplitude differences physically.

## 9. What this can test for One-Wave

This pipeline supplies direct wave data that can pressure-test, but does not by itself establish:

- propagation/dispersion claims;
- phase/path claims;
- multi-detector timing geometry;
- chirp evolution;
- source-scale to detector-scale mapping;
- claims that gravity is a medium displacement/wake;
- any proposed universal field propagation law.

A One-Wave test must supply a quantitative prediction in the same variables and compare it with the same strain data.

## 10. Kill conditions

The pipeline fails if:

1. downloaded source strain is silently modified;
2. detector/sample-rate/duration/source URL are not recorded;
3. an analysis preprocessing choice is hidden;
4. a raw spectral peak is called an astrophysical mode without noise/control analysis;
5. detector A and detector B are combined without preserving their separate source streams;
6. One-Wave claims are inferred merely because gravitational waves exist;
7. a mismatch is removed by changing definitions or tuning an undeclared parameter.

## 11. Scientific status

PASS:

- GWOSC source/event metadata can be resolved programmatically;
- calibrated strain is a direct wave observable;
- the DFT/periodogram/RMS transforms above are deterministic standard signal analysis;
- source and derived layers can remain separately traceable.

OPEN / YELLOW:

- any One-Wave-specific propagation equation;
- predicted dispersion beyond standard GR;
- predicted field-rotation signature;
- a unified quantitative relation between CERN excitation-scale data and LIGO strain data;
- any hardware-scale mapping claimed to represent the gravitational-wave mechanism.

## CORE-RULES-POST

- Accepted GWOSC strain remains the reference.
- Mathematics is explicit and not replaced by prose.
- Preprocessing is declared.
- Direct source strain and derived spectrum remain distinct.
- No One-Wave mechanism is promoted by the existence of the transform.
- Multi-detector and noise interpretation remain constrained by standard detector physics until independently derived alternatives reproduce the data.
- Status remains YELLOW / OPEN for One-Wave mechanism.
- Drift detected: no.
