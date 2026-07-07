param(
    [string]$Python = "C:\Users\KMYH\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe",
    [string]$InferencePython = "C:\Users\KMYH\miniconda3\envs\fdd\python.exe"
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$envFile = Join-Path $root ".env"
$packages = Join-Path $root ".python_packages"

if (-not (Test-Path -LiteralPath $envFile)) {
    throw "Missing .env. Copy .env.example to .env and replace every security placeholder first."
}
if (-not (Test-Path -LiteralPath $packages)) {
    throw "Missing .python_packages. Install requirements before starting development services."
}

if (-not (Test-Path -LiteralPath $InferencePython)) {
    $InferencePython = $Python
}
$adapterPath = Join-Path $root "packages\hpsu_dan_adapter"
$env:PYTHONPATH = $adapterPath
Start-Process -FilePath $InferencePython -ArgumentList @("-m", "uvicorn", "app.main:app", "--app-dir", (Join-Path $root "services\inference"), "--port", "8010") -WindowStyle Hidden

$env:PYTHONPATH = ($packages, $adapterPath) -join [IO.Path]::PathSeparator
Start-Process -FilePath $Python -ArgumentList @("-m", "uvicorn", "app.main:app", "--app-dir", (Join-Path $root "services\api"), "--port", "8000") -WindowStyle Hidden
Start-Process -FilePath "npm.cmd" -ArgumentList @("run", "dev") -WorkingDirectory (Join-Path $root "apps\web") -WindowStyle Hidden
Write-Host "Frontend: http://127.0.0.1:5173"
Write-Host "API docs: http://127.0.0.1:8000/docs"
