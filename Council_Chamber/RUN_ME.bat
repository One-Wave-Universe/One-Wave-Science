@echo off
setlocal
echo Checking for Python...
python --version
if errorlevel 1 (
    echo.
    echo ============================================================
    echo  Python was not found, or a Microsoft Store placeholder
    echo  opened instead of real Python.
    echo.
    echo  Install real Python from https://www.python.org/downloads/
    echo  and check "Add python.exe to PATH" during setup.
    echo ============================================================
    echo.
    pause
    exit /b 1
)
echo.
echo Starting One-Wave Council Chamber...
echo A browser window should open to http://127.0.0.1:8765/
echo Leave THIS window open while you use it. Close it (or Ctrl+C) to stop the server.
echo.
cd /d "%~dp0python"
python -m council_chamber.web_ui "%~dp0workspace" 8765
echo.
echo ============================================================
echo  The server stopped (exit code %errorlevel%).
echo  If that was unexpected, scroll up in this window to see
echo  whatever error message printed above.
echo ============================================================
pause
