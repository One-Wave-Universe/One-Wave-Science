# Steinhart-Hart

NTC R(T) is not a line. Steinhart-Hart is the usual fit:

    1/T = A + B ln R + C (ln R)^3

T in kelvin. R in ohms. A B C from three calibration points or the vendor.

B-parameter shortcut (good enough for Void belts):

    1/T = 1/T0 + (1/β) ln(R / R0)

T0 = 298.15 K, R0 = 10 kΩ, β ≈ 3950 K for the common 10 k NTC.

Void does not need 0.01 °C. It needs cooler / belt / hot. B-equation is the F0 converter. Steinhart-Hart if you later log real °C.

Never feed raw ADC counts as “temperature lean” without at least the B-equation — the divider is nonlinear and the NTC is nonlinear. Two curves stacked look like weather.
