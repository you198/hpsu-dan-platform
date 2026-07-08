# -*- coding: utf-8 -*-
"""生成团队环境配置文件"""
import sys, os
CWD = os.getcwd()
BASE = os.path.join(CWD, 'hpsu-dan-platform')

def write(path, content):
    full = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  {path}  ({len(content)} bytes)")

# ============================================================
# 1. .env.example — 团队统一环境变量模板
# ============================================================
env_content = r"""# ============================================================
# HPSU-DAN Platform — 环境变量配置
# ============================================================
# 使用方式：
#   1. 将此文件复制为 .env
#   2. 替换所有 replace-with-* 占位符
#   3. 不要将 .env 提交到 Git
# ============================================================

# ---------- 通用 ----------
APP_ENV=development
APP_NAME=HPSU-DAN Platform

# ---------- Web 前端 ----------
APP_PORT=8080
# 仅供 standalone 模式使用；Vite Dev 模式下前端端口是 5173

# ---------- API 服务 (FastAPI) ----------
API_HOST=0.0.0.0
API_PORT=8000

# ---------- 数据库 ----------
# 默认使用 SQLite（开发环境推荐）
DATABASE_URL=sqlite:///./storage/platform.db
# 如果遇到 SQLite 磁盘 I/O 错误，改用 TEMP 路径：
# DATABASE_URL=sqlite:///%TEMP%/hpsu-dan-platform-runtime.db

# ---------- JWT 认证 ----------
# 请随机生成一个长密钥（至少 32 字符）
JWT_SECRET=replace-with-a-long-random-secret
JWT_EXPIRE_MINUTES=120

# ---------- 初始管理员账号 ----------
# 首次启动自动创建，密码请不要用默认值
BOOTSTRAP_ADMIN_USERNAME=admin
BOOTSTRAP_ADMIN_PASSWORD=replace-with-a-strong-admin-password
BOOTSTRAP_GUEST_USERNAME=guest
BOOTSTRAP_GUEST_PASSWORD=replace-with-a-strong-guest-password

# ---------- 推理服务 ----------
INFERENCE_BASE_URL=http://127.0.0.1:8010
INFERENCE_MODE=demo
# demo  = 内置规则引擎（无需模型文件，开箱即用）
# real  = 加载真实 DMPAN 模型（需配置下方 HPSU_DAN_* 路径）

# ---------- 遗留模型配置（仅 INFERENCE_MODE=real 时需要）----------
HPSU_DAN_LEGACY_ROOT=..
HPSU_DAN_MODEL_MANIFEST=configs/models/hpsu-dan-v1.yaml
# 以下两项仅在 Windows 上用 conda 环境运行推理时需要：
# HPSU_DAN_INFERENCE_PYTHON=python
# HPSU_DAN_USE_CUDA=false
# HPSU_DAN_CUDA_DEVICE=0

# ---------- 文件上传 ----------
UPLOAD_MAX_BYTES=5242880
UPLOAD_ALLOWED_EXTENSIONS=.csv,.txt
UPLOAD_WINDOW_LENGTH=1024
UPLOAD_DEFAULT_SAMPLING_RATE=25600
UPLOAD_QUARANTINE_DIR=storage/quarantine

# ---------- 计算资源 ----------
COMPUTE_DEFAULT_DEVICE=auto
GPU_ENABLED=false
GPU_VISIBLE_DEVICES=0
GPU_MAX_MEMORY_MB=6144
CPU_FALLBACK_ENABLED=true
BATCH_INFERENCE_MAX_WINDOWS=4096

# ---------- LLM 助手（可选，对接腾讯 TokenHub）----------
# 不配置则 /api/v1/assistant/chat 返回 503
TENCENT_LLM_ENABLED=false
TENCENT_LLM_API_KEY=
TENCENT_LLM_BASE_URL=https://tokenhub.tencentmaas.com/v1
TENCENT_LLM_MODEL=deepseek-v4-pro
TENCENT_LLM_TIMEOUT_SECONDS=30

# ---------- Cloudflare Tunnel（可选，对外暴露服务）----------
CLOUDFLARE_TUNNEL_TOKEN=
"""

# ============================================================
# 2. run_dev.ps1 — 去除硬编码路径的通用启动脚本
# ============================================================
run_dev_content = r"""param(
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
"""

# ============================================================
# 3. SETUP.md — 环境搭建指南
# ============================================================
setup_content = r"""# HPSU-DAN Platform — 开发环境搭建指南

## 前置要求

| 工具 | 最低版本 | 检查命令 |
|---|---|---|
| Python | 3.10+ | `python --version` |
| Node.js | 18+ | `node --version` |
| npm | 9+ | `npm --version` |
| Git | 2.30+ | `git --version` |

> 建议使用 conda 或 venv 管理 Python 环境，避免与系统 Python 冲突。

## 一步搭建

```powershell
# 1. 克隆仓库
git clone <仓库地址>
cd hpsu-dan-platform

# 2. 配置环境变量
copy .env.example .env
# 用文本编辑器打开 .env，替换所有 replace-with-* 占位符

# 3. 一键启动（自动安装依赖 + 启动三服务）
.\scripts\run_dev.ps1
```

## 手动分步搭建

### 第 1 步：Python 虚拟环境

```powershell
# conda 方式（推荐）
conda create -n hpsu-dan python=3.12
conda activate hpsu-dan

# 或 venv 方式
python -m venv .venv
.\.venv\Scripts\activate
```

### 第 2 步：安装 Python 依赖

```powershell
# 安装到 .python_packages 目录（与 project-local 解耦）
python -m pip install -r services/api/requirements.txt -t .python_packages --upgrade
python -m pip install -r services/inference/requirements.txt -t .python_packages --upgrade
```

### 第 3 步：安装前端依赖

```powershell
cd apps/web
npm install
cd ..\..
```

### 第 4 步：启动三个服务

**终端 1 — 推理服务（端口 8010）：**
```powershell
python -m uvicorn app.main:app --app-dir services/inference --port 8010
```

**终端 2 — API 服务（端口 8000）：**
```powershell
$env:PYTHONPATH=".python_packages;packages\hpsu_dan_adapter"
python -m uvicorn app.main:app --app-dir services/api --port 8000
```

**终端 3 — 前端开发服务器（端口 5173）：**
```powershell
cd apps/web
npm run dev
```

### 第 5 步：验证

| 服务 | 地址 | 验证方法 |
|---|---|---|
| 前端 | http://127.0.0.1:5173 | 打开浏览器，应看到登录页 |
| API | http://127.0.0.1:8000/docs | 打开 Swagger 文档页 |
| 推理 | http://127.0.0.1:8010/health | 返回 `{"status":"ok","service":"inference"}` |

## 常见问题

### SQLite 磁盘 I/O 错误
Windows 上有时会出现，将 `.env` 中的 `DATABASE_URL` 改为：
```
DATABASE_URL=sqlite:///%TEMP%/hpsu-dan-platform-runtime.db
```

### 端口被占用
```powershell
netstat -ano | findstr :8000
```
找到占用端口的 PID，用任务管理器结束该进程。

### Python 模块找不到
确信你设置了 `PYTHONPATH` 环境变量指向 `.python_packages`

### npm install 失败
尝试删除 `apps/web/node_modules` 和 `apps/web/package-lock.json` 后重新安装

## 分工相关

| 角色 | 主要关注的服务 | 不需要启动的服务 |
|---|---|---|
| 前端 (人 A) | Web Dev Server (5173) | 推理服务 (8010) |
| 后端 (人 B) | API 服务 (8000), 推理 (8010) | Web Dev Server |
| 数据/推理 (人 C) | 推理服务 (8010), API (8000) | Web Dev Server |

> 启动最少服务即可开发自己负责的模块。人 A 可 mock API 数据，人 B 可用 curl/Postman 测试接口，人 C 可用独立的 HTTP 客户端测试推理服务。
"""

# 写文件
write('.env.example', env_content)
write('scripts/run_dev.ps1', run_dev_content)
write('configs/team/SETUP.md', setup_content)

print("\n所有环境配置文件已生成")
