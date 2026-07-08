# -*- coding: utf-8 -*-
import sys, os
cwd = os.getcwd()

# Write comprehensive api.md
api_md = r"""# API Reference v1

所有接口前缀：`/api/v1`

认证方式：Bearer JWT（登录接口除外）

---

## Auth

| Method | Path | 说明 | 权限 |
|---|---|---|---|
| POST | /auth/login | 登录获取 token | 公开 |
| GET | /auth/me | 当前用户信息 | 已登录 |

## Dashboard

| Method | Path | 说明 | 权限 |
|---|---|---|---|
| GET | /dashboard/summary | 仪表盘概览（设备、模型、实验统计） | 已登录 |

## Diagnosis

| Method | Path | 说明 | 权限 |
|---|---|---|---|
| POST | /diagnosis/predict | 直接诊断（提交信号数组） | admin/guest |
| POST | /diagnosis/upload | 上传文件诊断（multipart） | admin/guest |
| GET | /diagnosis/history | 诊断历史列表 | 已登录 |
| GET | /diagnosis/{task_id} | 诊断详情 | 已登录 |

## Tasks

| Method | Path | 说明 | 权限 |
|---|---|---|---|
| GET | /tasks | 任务历史列表 | 已登录 |
| GET | /tasks/{task_id} | 任务详情（含文件、结果） | 已登录 |
| POST | /tasks/{task_id}/rerun | 重跑任务 | admin/guest |

## Files

| Method | Path | 说明 | 权限 |
|---|---|---|---|
| GET | /files/quarantine | 隔离区文件列表 | admin |

## Compute

| Method | Path | 说明 | 权限 |
|---|---|---|---|
| GET | /compute/status | GPU/CPU 计算状态 | 已登录 |

## Research

| Method | Path | 说明 | 权限 |
|---|---|---|---|
| GET | /research/options | 研究数据列表（数据集、方法、结果） | 已登录 |
| POST | /research/refresh | 刷新研究数据缓存 | admin |
| GET | /research/results/{result_id} | 研究结果详情 | 已登录 |
| GET | /research/results/{result_id}/assets/{asset_name} | 研究资产（图片/PDF） | 已登录 |

## System

| Method | Path | 说明 | 权限 |
|---|---|---|---|
| GET | /system/status | 系统状态 | admin |

## Assistant

| Method | Path | 说明 | 权限 |
|---|---|---|---|
| POST | /assistant/chat | LLM 对话（对接腾讯 TokenHub） | 已登录 |

## Health

| Method | Path | 说明 | 权限 |
|---|---|---|---|
| GET | /health | 服务健康检查 | 公开 |

## 完整 OpenAPI JSON

运行 API 服务后访问 `http://localhost:8000/openapi.json` 获取最新版。
"""

path_api = os.path.join(cwd, 'hpsu-dan-platform', 'docs', 'api.md')
open(path_api, 'w', encoding='utf-8').write(api_md)
print("api.md written: " + str(len(api_md)) + " bytes")
