@echo off
cd /d %~dp0
python one_wave_virtual_lens.py --out results --ticks 90
pause
