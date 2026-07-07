# HPSU-DAN Intelligent Fault Diagnosis Digital Twin Platform

面向研究生人工智能竞赛的智能装备数字孪生与健康管理平台。平台代码与原论文算法隔离，真实模型只通过适配器和模型清单接入。

## 当前首版能力

- FastAPI 账号登录、JWT 与后端 RBAC
- 管理员/访客由环境变量初始化，密码不进入源码
- 独立推理服务及明确标记的 demo 推理模式
- Vue 3 登录页、五大模块导航、中英双语
- Three.js 轻量实验台占位场景和故障状态联动
- Dashboard、诊断和系统状态接口

## 本地开发

1. 将 `.env.example` 复制为 `.env`，替换所有安全项。
2. 安装后端依赖：`python -m pip install -r services/api/requirements.txt -r services/inference/requirements.txt`
3. 启动推理服务：`python -m uvicorn app.main:app --app-dir services/inference --port 8010`
4. 启动业务 API：`python -m uvicorn app.main:app --app-dir services/api --port 8000`
5. 在 `apps/web` 执行 `npm install` 与 `npm run dev`。

真实 SF-HDOT/HPSU-DAN 权重注册前，诊断结果会带有 `engine_mode=demo`，不得作为科研结论。

## Current Windows Development Deployment

Local service URLs:

- Web gateway: `http://127.0.0.1:8080`
- Business API: `http://127.0.0.1:8000`
- Inference service: `http://127.0.0.1:8010`

Run:

```powershell
$env:PYTHONPATH=".python_packages"
python scripts\dev_supervisor.py start
python scripts\dev_supervisor.py health
python scripts\dev_supervisor.py stop
```

The web gateway serves `apps/web/dist` and proxies `/api` to the API service. Run `npm run build` in `apps/web` after frontend changes.

LAN access:

```powershell
.\scripts\get_lan_urls.ps1
```

Open the reported `http://<LAN-IP>:8080` URL from another device on the same network. If it is blocked, allow inbound TCP 8080 as described in `deploy/windows/firewall_notes.md`.

Cloudflare quick tunnel:

```powershell
.\scripts\start_cloudflare_quick_tunnel.ps1
```

For a stable named tunnel, use `deploy/cloudflare/tunnel.example.yml`.

Tencent TokenHub assistant configuration belongs only in `.env`:

```env
TENCENT_LLM_ENABLED=true
TENCENT_LLM_BASE_URL=https://tokenhub.tencentmaas.com/v1
TENCENT_LLM_MODEL=deepseek-v4-pro
TENCENT_LLM_API_KEY=...
```

On this Windows workspace, SQLite under the project directory can report `disk I/O error`; the current development deployment uses:

```env
DATABASE_URL=sqlite:///C:/Users/KMYH/AppData/Local/Temp/hpsu-dan-platform-runtime.db
```
