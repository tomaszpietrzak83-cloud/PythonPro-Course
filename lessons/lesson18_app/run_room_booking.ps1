$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path -LiteralPath (Join-Path $PSScriptRoot "..\..")
$python = Join-Path $repoRoot ".venv\Scripts\python.exe"
$appDir = Join-Path $PSScriptRoot "room_booking"

if (-not (Test-Path -LiteralPath $python)) {
    Write-Error "Main course virtual environment was not found: $python. From the repository root, create it with: python -m venv .venv"
}

Push-Location -LiteralPath $appDir
try {
    & $python "run.py"
    exit $LASTEXITCODE
}
finally {
    Pop-Location
}
