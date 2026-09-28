#!/usr/bin/env python3
import importlib.util, pathlib
P=pathlib.Path(__file__).with_name("spectral_lattice_phase.py")
s=importlib.util.spec_from_file_location("g767",P); m=importlib.util.module_from_spec(s); s.loader.exec_module(m)

def test_exact_octave_phase_coherence():
    xs=[(1.0,None),(2.0,None),(4.0,None),(8.0,None),(16.0,None)]
    assert abs(m.coherence(m.phases(xs,1.0))-1.0)<1e-12

def test_quarter_offsets_cancel():
    xs=[(1.0,None),(2**0.25,None),(2**0.5,None),(2**0.75,None)]
    assert m.coherence(m.phases(xs,1.0))<1e-12

if __name__=="__main__":
    test_exact_octave_phase_coherence(); test_quarter_offsets_cancel(); print("G767_FIXTURES_PASS")
