# One-Wave Council Chamber -- local launcher
#
# Requires Python 3.10+ already installed and on PATH (nothing else --
# no pip install needed, the app uses only Python's standard library).
#
# To use a real provider (e.g. Groq, which is free with no billing),
# set its API key BEFORE running this script:
#   $env:GROQ_API_KEY = "your-real-key-here"
#   .\RUN_ME.ps1
# (the web UI's Providers panel shows this exact command, with the
# right variable name, for each provider -- click "show setup")

Set-Location "$PSScriptRoot\python"
python -m council_chamber.web_ui "$PSScriptRoot\workspace" 8765
