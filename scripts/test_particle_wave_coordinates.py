import unittest,math
from particle_wave_coordinates import convert,H,C,EV
class Tests(unittest.TestCase):
    def test_energy_roundtrip(self):
        q=convert(energy_ev=1e9)["coordinates"]
        self.assertAlmostEqual(q["energy_frequency_Hz"]*H/(1e9*EV),1)
        self.assertAlmostEqual(q["photon_equivalent_vacuum_wavelength_m"]*q["energy_frequency_Hz"]/C,1)
    def test_momentum_mass_are_distinct_coordinates(self):
        q=convert(momentum_gev_c=1,mass_kg=1)["coordinates"]
        self.assertAlmostEqual(q["de_broglie_wavelength_m"]*q["momentum_kg_m_s"]/H,1)
        self.assertNotEqual(q["de_broglie_wavelength_m"],q["compton_wavelength_m"])
    def test_invalid_quantities(self):
        for v in [0,-1,float('nan'),float('inf')]:
            with self.assertRaises(ValueError):convert(energy_ev=v)
        with self.assertRaises(ValueError):convert()
if __name__=="__main__":unittest.main()
