# Wave Reader V1 — Acquisition Pipeline

**Status:** hardware specification / proposed measurement instrument

## Purpose
Wave Reader V1 is a measurement-first acquisition path for observing voltage/current/field-related signals from experimental One-Wave hardware without assuming the hypothesis is correct.

## Pipeline
```text
sensor / probe
-> input protection
-> analog conditioning
-> reference-aware differential acquisition
-> ADC / scope capture
-> timestamp
-> calibration transform
-> raw + processed storage
-> comparison / visualization
```

## Minimum channels
1. DUT signal
2. reference node
3. supply/recovery rail
4. optional field or coil-current channel

## Required measurements
- absolute voltage relative to instrument ground;
- differential voltage relative to the declared circuit reference;
- current where relevant;
- sampling rate and bandwidth;
- noise floor;
- calibration source and date.

## Evidence rule
Never label a trace as "reinjection," "memory," "Field," "Void," or "wave collapse" solely from its shape. Store the raw observable first, then attach interpretation as metadata.

## V1 acceptance
Wave Reader V1 passes when it can:
1. capture a known test waveform;
2. reproduce amplitude/frequency within declared tolerance;
3. distinguish DUT/reference channels;
4. save raw data and metadata;
5. repeat the same measurement after restart.

## Safety
Input ranges, isolation, and probe ratings must be respected. Unknown high-energy or mains-connected circuits are outside V1 scope.
