# Particle / measurement to wave-coordinate conversion chart

Authority: ENGINE_EVIDENCE_PIPELINES.md and One_Wave_Bench/data/OPEN_DATA_WAVE_PIPELINE.md. Preserve original provider labels, quantities, frame, uncertainty, calibration and identifiers. These are declared coordinate transforms, not proof of a One-Wave medium or a measured particle waveform. Particle labels describe source reconstruction; excitation geometry is not inferred from a label.

| Source observable | Available wave representation | Required information / limit |
|---|---|---|
| Energy E | energy-frequency coordinate f_E = E/h | Total, kinetic and rest energy must be distinguished; f_E is not a detector time-series frequency |
| Photon energy E | vacuum wavelength lambda = hc/E | Photon, vacuum and observed/rest-frame assumptions explicit |
| Momentum p | de Broglie wavelength lambda = h/p | Momentum magnitude in a declared frame; never substitute hc/E for massive-particle momentum wavelength |
| Rest mass m | Compton scale lambda_C = h/(mc), rest-frequency mc^2/h | A comparison scale, not the spatial trajectory or a fitted knot radius |
| CERN event hits, tracks, clusters | Timestamped detector series or declared event histogram / spectrum | Detector timing/units, reconstruction, trigger, acceptance and uncertainties; detector azimuth is not wave phase |
| HEPData bins | Published distribution and its Fourier/other declared transform | Preserve bin edges, qualifiers, statistical/systematic errors and covariance; not an ordered temporal waveform |
| Hubble/JWST/TESS/HEASARC light curve | Calibrated flux/count-rate versus source time | Instrument response, time system, exposure, background, masks and quality flags |
| Telescope spectrum / DESI / ALMA | Flux versus wavelength/frequency | Vacuum/air wavelength, spectral response, observed versus rest frame; nu=c/lambda only under the stated propagation convention |
| LIGO/Virgo/KAGRA | Calibrated dimensionless strain h(t), spectrum/PSD | GPS, detector, sample rate, calibration, data-quality segment and window/normalization; not E/h conversion |
| EEG/MEG/NWB | Measured channel amplitudes and time-frequency representation | Channel, sampling rate, reference, filters, units and artifact masks; electrical/magnetic signals are not particle-energy conversions |
| MRI/fMRI | Spatial image / BOLD series and declared spatial/temporal transforms | Voxel axes, acquisition timing, sequence and preprocessing; BOLD is a hemodynamic observable, not direct neuronal voltage |
| Archive metadata alone | derived_metadata_wave, only if a declared metadata encoding is useful | Not a physical waveform; keep the source metadata and encoding contract separate |

## Energy-coordinate lookup

Exact SI definitions used: h=6.62607015e-34 J s, c=299792458 m/s, 1 eV=1.602176634e-19 J. Values below are computed from those definitions. Wavelength column is photon-equivalent only.

| Input energy | f_E (Hz) | Photon-equivalent vacuum wavelength (m) |
|---|---:|---:|
| 1 eV | 2.417989242e+14 | 1.239841984e-06 |
| 1 keV | 2.417989242e+17 | 1.239841984e-09 |
| 1 MeV | 2.417989242e+20 | 1.239841984e-12 |
| 1 GeV | 2.417989242e+23 | 1.239841984e-15 |

## Executable conversion

```bash
python3 scripts/particle_wave_coordinates.py --energy-ev 1000000000
python3 scripts/particle_wave_coordinates.py --momentum-gev-c 1
```

Energy and momentum are separate inputs with separate meanings. Preserve provider uncertainty; for a linear energy-frequency map sigma_f=sigma_E/h, and for independent small momentum error sigma_lambda/lambda=sigma_p/p. Joint quantities need covariance propagation. For sampled measured data use scripts/open_data_to_wave.py with the explicit mapping, timing, units and provenance contract. No phase, envelope, particle identity, mass hierarchy or physical geometry is created by this lookup.

NIST constants: https://www.nist.gov/si-redefinition/meet-constants and https://physics.nist.gov/cuu/Constants/index.html . Standard de Broglie/Compton definitions: https://openstax.org/books/university-physics-volume-3/pages/6-key-equations . Project-specific fold, mirror and 48-point encodings remain separately declared in Engine/WAVE_TRANSFORM.md; they do not replace source data.
