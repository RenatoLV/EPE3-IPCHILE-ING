param([string]$PythonPath = 'python')
$ErrorActionPreference = 'Stop'
Push-Location $PSScriptRoot
try {
    $projectPython = Join-Path $PSScriptRoot '.venv/Scripts/python.exe'
    if (-not (Test-Path -LiteralPath $projectPython)) {
        & $PythonPath -m venv .venv
        if ($LASTEXITCODE -ne 0) { throw 'No se pudo crear el entorno. Usa Python 3.12 y el parámetro -PythonPath si es necesario.' }
    }
    & $projectPython -m pip install -r requirements-lock.txt
    if ($LASTEXITCODE -ne 0) { throw 'Falló la instalación de dependencias. Revisa la conexión y la salida de pip.' }
    & $projectPython train_model.py
    if ($LASTEXITCODE -ne 0) { throw 'Falló el entrenamiento.' }
    & $projectPython -m pytest test_app.py -q
    if ($LASTEXITCODE -ne 0) { throw 'Hay pruebas pendientes de corregir.' }
    Write-Output 'Preparación terminada. Ejecuta .\iniciar.ps1.'
} finally {
    Pop-Location
}
