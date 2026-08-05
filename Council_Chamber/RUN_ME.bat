@echo off
where python >nul 2>nul
if errorlevel 1 (
    echo Python was not found on your PATH.
    echo Install it from https://www.python.org/downloads/ then run this again.
    echo (During install, check the box that says "Add python.exe to PATH".)
    pause
    exit /b 1
)
cd /d "%~dp0python"
python -m council_chamber.web_ui "%~dp0workspace" 8765
pause
