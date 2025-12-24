# Script di avvio per JARVIS Daemon
$ErrorActionPreference = "Stop"

$projectRoot = "C:\Users\Administrator\JARVIS_VOICE"
$pythonExe = "$projectRoot\.venv\Scripts\python.exe"

# Imposta la root del progetto come Working Directory per garantire che i moduli siano risolti
Set-Location -Path $projectRoot

Write-Host "Avvio Jarvis Daemon..."
Write-Host "Python: $pythonExe"
Write-Host "Log: C:\Temp\jarvis_daemon.log"

# Avvia Python come modulo (-m)
& $pythonExe -m src.daemon
