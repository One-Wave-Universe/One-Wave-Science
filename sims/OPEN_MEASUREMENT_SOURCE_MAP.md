# Open Measurement Source Map

All sources below feed the same no-particle-assumption pipeline.

## CERN collider data

Experiments:
- CMS
- ATLAS
- ALICE
- LHCb
- TOTEM and other portal datasets where suitable

Preferred inputs:
- detector hits / rec-hits
- calorimeter deposits
- track-associated hit coordinates
- waveforms or channel-level detector data where released
- run/event metadata
- reconstructed objects retained only as comparison labels

Transform target:
RAW -> EXCITATION -> POINT -> PATH -> FIELD -> OCTAVE STACK

## LIGO / Virgo / KAGRA via GWOSC

Preferred input:
- calibrated strain time series h(t)
- detector identity
- GPS/UTC start
- sample rate
- data-quality segments
- event/version metadata

This is already a direct continuous measurement channel.

Transform target:
strain sample -> signed excitation about reference -> temporal path -> multi-detector field relation -> octave / frequency-scale analysis

Do not begin from compact-object labels. Those remain reference interpretation metadata.

## Antimatter experiments

Sources include CERN Antiproton Decelerator / ELENA experiments such as BASE and ALPHA where public measurements or machine-readable datasets are available.

Preferred input:
- trap frequencies
- spectroscopy frequencies
- magnetic-field measurements
- annihilation detector responses
- timing/count signals
- position-sensitive detector outputs
- uncertainty and apparatus metadata

Do not begin from 'antiproton' or 'antihydrogen' as a required simulator primitive.

Represent the released measurement first, then retain the experiment's object interpretation as metadata for comparison.

## Astronomical / other observatories

When added:
- ingest calibrated sensor streams, spectra, images, timing series, visibilities, or counts
- preserve instrument response and uncertainty
- derive point/path/field representations only after raw ingest
- retain catalog object labels as reference metadata

## Universal source contract

Every adapter must output:
- source
- experiment/instrument
- run/event/observation identifier
- channel
- time
- coordinates if available
- raw value
- unit
- uncertainty if available
- quality flag
- provenance URL/DOI/file
- optional source interpretation labels
