# HPSU-DAN Platform — 团队开发约定

## 端口分配
| 服务 | 端口 | 说明 |
|---|---|---|
| Web (Vite Dev) | 8080 | 前端开发服务器，代理 /api -> 8000 |
| API (FastAPI) | 8000 | 业务后端 |
| Inference (FastAPI) | 8010 | 推理服务 |

## 共享的 .env 模板
请将 hpsu-dan-platform/.env.example 复制为 .env，填入实际值。
.env 不入 Git，每位成员各自维护。

## 接口合同
前后端之间的唯一接口是 /api/v1/* REST API。
前端 api.ts 中每个接口的 TypeScript 类型 = 后端 schemas.py 中 Pydantic 模型的直接映射。
修改接口时，后端先更新 schemas.py，前端后更新 api.ts，保持两者一致。

## 模型配置文件
configs/models/hpsu-dan-v1.yaml 由数据/推理负责人管理。
他人修改需经过该负责人 review。
