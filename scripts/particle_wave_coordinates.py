#!/usr/bin/env python3
"""Declared standard energy/momentum coordinates; not a waveform generator."""
import argparse,json,math
H=6.62607015e-34
C=299792458.0
EV=1.602176634e-19

def convert(energy_ev=None,momentum_gev_c=None,mass_kg=None):
    result={"classification":"derived_quantum_coordinates_not_measured_waveform","constants":{"h_J_s":H,"c_m_s":C,"eV_J":EV},"coordinates":{}}
    for name,value in [("energy_ev",energy_ev),("momentum_gev_c",momentum_gev_c),("mass_kg",mass_kg)]:
        if value is not None and (not math.isfinite(value) or value<=0):raise ValueError(name+" must be finite and positive")
    if all(v is None for v in (energy_ev,momentum_gev_c,mass_kg)):raise ValueError("Supply at least one source quantity")
    q=result["coordinates"]
    if energy_ev is not None:
        e=energy_ev*EV;q.update(energy_eV=energy_ev,energy_J=e,energy_frequency_Hz=e/H,photon_equivalent_vacuum_wavelength_m=H*C/e)
    if momentum_gev_c is not None:
        p=momentum_gev_c*1e9*EV/C;q.update(momentum_GeV_c=momentum_gev_c,momentum_kg_m_s=p,de_broglie_wavelength_m=H/p)
    if mass_kg is not None:q.update(mass_kg=mass_kg,rest_energy_J=mass_kg*C*C,compton_wavelength_m=H/(mass_kg*C))
    result["boundary"]="Preserve original measured quantity, frame and uncertainty. E/h is an energy-frequency coordinate; hc/E is a photon-equivalent scale, not a massive particle trajectory wavelength. No phase, envelope or excitation geometry is inferred."
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument("--energy-ev",type=float);p.add_argument("--momentum-gev-c",type=float);p.add_argument("--mass-kg",type=float);a=p.parse_args();print(json.dumps(convert(a.energy_ev,a.momentum_gev_c,a.mass_kg),indent=2))
if __name__=="__main__":main()
