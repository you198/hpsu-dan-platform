# HPSU-DAN Platform — 开发环境搭建指南

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
