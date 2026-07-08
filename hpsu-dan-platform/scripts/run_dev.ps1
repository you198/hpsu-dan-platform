param(
    [string]$Python = "python",
    [string]$InferencePython = "python"
)

# ============================================================
# 开发环境一键启动脚本
# 用法：
#   .\scripts\run_dev.ps1
#   .\scripts\run_dev.ps1 -Python "C:\Python312\python.exe"
# ============================================================

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$envFile = Join-Path $root ".env"
$packages = Join-Path $root ".python_packages"

if (-not (Test-Path -LiteralPath $envFile)) {
    throw "缺少 .env 文件！请将 .env.example 复制为 .env 并填入配置。"
}

# ---------- 安装后端依赖 ----------
if (-not (Test-Path -LiteralPath $packages)) {
    Write-Host "安装后端 Python 依赖..."
    & $Python -m pip install -r (Join-Path $root "services\api\requirements.txt") -t $packages --upgrade
    & $Python -m pip install -r (Join-Path $root "services\inference\requirements.txt") -t $packages --upgrade
}

# ---------- 安装前端依赖 ----------
$webDir = Join-Path $root "apps\web"
if (-not (Test-Path (Join-Path $webDir "node_modules"))) {
    Write-Host "安装前端 Node.js 依赖..."
    Push-Location $webDir
    npm install
    Pop-Location
}

# ---------- 启动三个服务 ----------
$adapterPath = Join-Path $root "packages\hpsu_dan_adapter"
$env:PYTHONPATH = $adapterPath

Write-Host "启动推理服务 (端口 8010)..."
$infProc = Start-Process -FilePath $InferencePython -ArgumentList @(
    "-m", "uvicorn", "app.main:app",
    "--app-dir", (Join-Path $root "services\inference"),
    "--port", "8010"
) -WindowStyle Hidden -PassThru

Write-Host "启动 API 服务 (端口 8000)..."
$env:PYTHONPATH = ($packages, $adapterPath) -join [IO.Path]::PathSeparator
$apiProc = Start-Process -FilePath $Python -ArgumentList @(
    "-m", "uvicorn", "app.main:app",
    "--app-dir", (Join-Path $root "services\api"),
    "--port", "8000"
) -WindowStyle Hidden -PassThru

Write-Host "启动前端开发服务器..."
$webProc = Start-Process -FilePath "npm.cmd" -ArgumentList @("run", "dev") -WorkingDirectory $webDir -WindowStyle Hidden -PassThru

Write-Host ""
Write-Host "=========================================="
Write-Host "  服务已启动"
Write-Host "=========================================="
Write-Host "  前端:    http://127.0.0.1:5173"
Write-Host "  API:     http://127.0.0.1:8000"
Write-Host "  API 文档: http://127.0.0.1:8000/docs"
Write-Host "  推理:    http://127.0.0.1:8010"
Write-Host ""
Write-Host "  停止:    python scripts\dev_supervisor.py stop"
Write-Host "  状态:    python scripts\dev_supervisor.py health"
Write-Host "=========================================="

# 保存进程 ID 以便 dev_supervisor 管理
$pidDir = Join-Path $root "storage\pids"
if (-not (Test-Path $pidDir)) { New-Item -ItemType Directory -Force -Path $pidDir | Out-Null }
$infProc.Id | Out-File (Join-Path $pidDir "inference.pid")
$apiProc.Id  | Out-File (Join-Path $pidDir "api.pid")
$webProc.Id  | Out-File (Join-Path $pidDir "web.pid")
