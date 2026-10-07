#!/usr/bin/env python3
"""Quick test: manually verify PMOS threshold calculation."""

# PMOS parameters
vth = 0.4
vgate_initial = 0.9
vsource_initial = 0.5
vgate_at_10us = 0.0

# Initial state
vgs_initial = vgate_initial - vsource_initial
print(f"Initial Vgs = {vgate_initial} - {vsource_initial} = {vgs_initial}V")
print(f"PMOS ON when Vgs <= -{vth}, i.e., Vgs <= {-vth}V")
print(f"Initial is_on = {vgs_initial <= -vth}")

# When driven at 10us with gate=0.0V and source still ~0.5V
vgs_driven = vgate_at_10us - vsource_initial
print(f"\nWhen gate driven low:")
print(f"Vgs = {vgate_at_10us} - {vsource_initial} = {vgs_driven}V")
print(f"is_on = {vgs_driven <= -vth}")

# When driven at 10us with gate=0.0V and source pulls HIGH
vsource_pulled = 0.95
vgs_pulled = vgate_at_10us - vsource_pulled
print(f"\nWhen source is pulled high by PMOS:")
print(f"Vgs = {vgate_at_10us} - {vsource_pulled} = {vgs_pulled}V")
print(f"is_on = {vgs_pulled <= -vth}")

# The issue: with source at 1.0V (+V), what happens?
vsource_vdd = 1.0
vgs_vdd = vgate_at_10us - vsource_vdd
print(f"\nWhen source reaches +V:")
print(f"Vgs = {vgate_at_10us} - {vsource_vdd} = {vgs_vdd}V")
print(f"is_on = {vgs_vdd <= -vth}")
print("If source reaches +V, then PMOS turns OFF (as it should at equilibrium)")
