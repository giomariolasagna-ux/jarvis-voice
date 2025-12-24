# Configurazione
$prodPath = "C:\Users\Administrator\JARVIS_VOICE"
$devPath = "C:\Users\Administrator\JARVIS_DEV"

Write-Host "--- INIZIO CLONAZIONE AMBIENTE ---" -ForegroundColor Cyan
Write-Host "ORIGINE (ReadOnly): $prodPath"
Write-Host "DESTINAZIONE (ReadWrite): $devPath"

# 1. Pulizia ambiente DEV precedente
if (Test-Path $devPath) {
    Remove-Item -Path $devPath -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "Vecchia cartella DEV rimossa." -ForegroundColor Yellow
}
New-Item -ItemType Directory -Path $devPath -Force | Out-Null

# 2. Copia Selettiva (Solo Codice, niente spazzatura)
$exclude = @(".venv", "__pycache__", ".git", ".vs", "mutable_memory", "*.log")

Get-ChildItem -Path $prodPath | ForEach-Object {
    if ($exclude -notcontains $_.Name) {
        Copy-Item -Path $_.FullName -Destination $devPath -Recurse -Force
    }
}

# 3. Creazione Identity specifica per DEV
# Quando Jarvis gira da qui, saprà di essere in modalità TEST
$devIdentity = @{
    "self_path" = $devPath
    "mutable_path" = "$devPath\mutable_memory"
    "mode" = "DEVELOPMENT"
} | ConvertTo-Json

[System.IO.File]::WriteAllText("$devPath\jarvis_identity.json", $devIdentity)

Write-Host "CLONAZIONE COMPLETATA." -ForegroundColor Green
Write-Host "Il codice è pronto per essere analizzato o modificato in: $devPath"
