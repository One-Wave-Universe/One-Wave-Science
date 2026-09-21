# Volumetric Ternary Cell (VTC-0) Breadboard Specifications

**Status:** UNVERIFIED HARDWARE/UI MAPPING — retain for testing or dismissal

## Authority boundary

For current physical CELL_V1 geometry, `CELL_V1_ANTI_DRIFT.md` and the current build packet remain the geometry authority. This file records additional VTC-0 implementation claims for verification.

## Zero/reference rule

```text
+ <-> (0) <-> -
```

## Requested state-indicator mapping

- **Yellow LED:** CLEAR / BREAK
- **Red LED:** DOWN / Compress
- **Split-Rail Power:** dual-rail setup with potentiometer regulation for differential logic thresholds

These mappings are unverified and must be tested against the current reference/rail architecture before adoption.

## Existing logical projection

Physical primitive remains:

```text
A+ <-> A-
B+ <-> B-
C+ <-> C-
```

Three physical bidirectional mirrors produce six directed edge interfaces.

## Verification questions

1. Does Yellow CLEAR/BREAK map cleanly to the current Hold/reference semantics or conflict with them?
2. Does Red DOWN/Compress preserve the ternary DOWN/HOLD/UP distinction?
3. Is a potentiometer-regulated split rail stable enough for threshold tests?
4. Does split-rail power conflict with the currently selected virtual-ground CELL_V1 path?
5. Can the mapping be measured without creating six separate physical gates?

A failed mapping should be marked DISMISSED or superseded, not silently promoted into canon.
