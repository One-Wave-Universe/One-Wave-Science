# 06 — Sources and Part Notes

Primary manufacturer references used for the V0-A selection:

- Texas Instruments, LM393B dual comparator data sheet.
- Texas Instruments, TLE2426 precision virtual-ground / rail-splitter data sheet.
- Microchip, MCP6001/2/4 low-power rail-to-rail op-amp data sheet.
- Raspberry Pi, RP2040 and Raspberry Pi Pico data sheets.

Selection logic:

- TLE2426 creates the half-supply relational reference for signal conditioning.
- LM393B supplies two comparator channels for a center-window detector.
- MCP6004 provides low-voltage buffering and filtering channels.
- Raspberry Pi Pico supplies capture, phase logic, five-level control, and pulse timing.

Part substitutions are allowed only after checking supply range, input common-mode range, output voltage compatibility, bandwidth, and package.
