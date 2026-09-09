# PowerShell Runner for ML Hypothesis Research Studio
Set-Location -Path $PSScriptRoot
& "$PSScriptRoot\.venv\Scripts\python.exe" "$PSScriptRoot\main.py" --iterations 1 $args
