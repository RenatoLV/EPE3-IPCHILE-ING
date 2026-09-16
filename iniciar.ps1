param([switch]$Comprobar)
$ErrorActionPreference = 'Stop'
$projectPython = Join-Path $PSScriptRoot '.venv/Scripts/python.exe'
if (-not (Test-Path -LiteralPath $projectPython)) {
    throw 'Primero ejecuta instalar.ps1 para preparar el entorno.'
}
if ($Comprobar) {
    & $projectPython (Join-Path $PSScriptRoot 'run.py') --check
} else {
    & $projectPython (Join-Path $PSScriptRoot 'run.py') --open
}
exit $LASTEXITCODE
