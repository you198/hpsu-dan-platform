import sys, json, os
cwd = os.getcwd()

spec = {
    "openapi": "3.0.3",
    "info": {
        "title": "HPSU-DAN Platform API",
        "version": "0.1.0",
        "description": "智能装备数字孪生与健康管理平台后端 API"
    },
    "servers": [{"url": "/api/v1", "description": "API v1 base"}],
    "components": {
        "securitySchemes": {
            "bearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
        },
        "schemas": {
            "LoginRequest": {
                "type": "object",
                "required": ["username", "password"],
                "properties": {
                    "username": {"type": "string", "minLength": 1, "maxLength": 64},
                    "password": {"type": "string", "minLength": 1, "maxLength": 128}
                }
            },
            "UserView": {
                "type": "object",
                "properties": {
                    "username": {"type": "string"},
                    "role": {"type": "string", "enum": ["admin", "guest"]}
                }
            },
            "TokenResponse": {
                "type": "object",
                "properties": {
                    "access_token": {"type": "string"},
                    "token_type": {"type": "string"},
                    "user": {"$ref": "#/components/schemas/UserView"}
                }
            },
            "DiagnosisRequest": {
                "type": "object",
                "required": ["samples"],
                "properties": {
                    "samples": {"type": "array", "items": {"type": "number"}, "minItems": 1024, "maxItems": 262144},
                    "sampling_rate": {"type": "integer", "default": 25600},
                    "model_id": {"type": "string", "default": "hpsu-dan-v1"}
                }
            },
            "Evidence": {
                "type": "object",
                "properties": {
                    "waveform": {"type": "array", "items": {"type": "object", "properties": {"x": {"type": "number"}, "y": {"type": "number"}}}},
                    "spectrum": {"type": "array", "items": {"type": "object", "properties": {"frequency": {"type": "number"}, "magnitude": {"type": "number"}}}},
                    "markers": {"type": "array", "items": {"type": "string"}},
                    "statistics": {"type": "object"},
                    "window": {"type": "object"}
                }
            },
            "PredictionResult": {
                "type": "object",
                "properties": {
                    "label": {"type": "string"},
                    "label_zh": {"type": "string"},
                    "label_en": {"type": "string"},
                    "confidence": {"type": "number"},
                    "health_score": {"type": "integer"},
                    "twin_target": {"type": "string"}
                }
            },
            "DiagnosisResponse": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "string"},
                    "model_id": {"type": "string"},
                    "engine_mode": {"type": "string"},
                    "prediction": {"$ref": "#/components/schemas/PredictionResult"},
                    "evidence": {"$ref": "#/components/schemas/Evidence"},
                    "topk": {"type": "array", "items": {"type": "object"}},
                    "runtime": {"type": "object"}
                }
            },
            "TaskView": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "string"},
                    "task_type": {"type": "string"},
                    "status": {"type": "string"},
                    "created_by": {"type": "string"},
                    "created_at": {"type": "string"},
                    "model_id": {"type": "string"},
                    "error_code": {"type": "string"}
                }
            },
            "UploadDiagnosisResponse": {
                "type": "object",
                "properties": {
                    "task": {"$ref": "#/components/schemas/TaskView"},
                    "result": {"$ref": "#/components/schemas/DiagnosisResponse"},
                    "quality": {"type": "object"}
                }
            },
            "DashboardSummary": {
                "type": "object",
                "properties": {
                    "device": {"type": "object"},
                    "telemetry": {"type": "object"},
                    "model": {"type": "object"},
                    "research": {"type": "object"},
                    "alerts": {"type": "array"}
                }
            }
        }
    },
    "paths": {
        "/auth/login": {
            "post": {
                "tags": ["Auth"],
                "summary": "登录",
                "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/LoginRequest"}}}},
                "responses": {"200": {"description": "Success", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/TokenResponse"}}}}}
            }
        },
        "/auth/me": {
            "get": {
                "tags": ["Auth"],
                "summary": "当前用户",
                "security": [{"bearerAuth": []}],
                "responses": {"200": {"description": "Success", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/UserView"}}}}}
            }
        },
        "/dashboard/summary": {
            "get": {
                "tags": ["Dashboard"],
                "summary": "仪表盘概览",
                "security": [{"bearerAuth": []}],
                "responses": {"200": {"description": "Success", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/DashboardSummary"}}}}}
            }
        },
        "/diagnosis/predict": {
            "post": {
                "tags": ["Diagnosis"],
                "summary": "信号诊断",
                "security": [{"bearerAuth": []}],
                "requestBody": {"required": True, "content": {"application/json": {"schema": {"$ref": "#/components/schemas/DiagnosisRequest"}}}},
                "responses": {"200": {"description": "Success", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/DiagnosisResponse"}}}}}
            }
        },
        "/diagnosis/upload": {
            "post": {
                "tags": ["Diagnosis"],
                "summary": "上传文件诊断",
                "security": [{"bearerAuth": []}],
                "requestBody": {"required": True, "content": {"multipart/form-data": {"schema": {"type": "object", "properties": {
                    "file": {"type": "string", "format": "binary"},
                    "sampling_rate": {"type": "integer"},
                    "model_id": {"type": "string"}
                }}}}},
                "responses": {"200": {"description": "Success", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/UploadDiagnosisResponse"}}}}}
            }
        },
        "/diagnosis/history": {
            "get": {
                "tags": ["Diagnosis"],
                "summary": "诊断历史",
                "security": [{"bearerAuth": []}],
                "parameters": [{"name": "limit", "in": "query", "schema": {"type": "integer", "default": 20}}],
                "responses": {"200": {"description": "Success", "content": {"application/json": {"schema": {"type": "array", "items": {"type": "object"}}}}}}
            }
        },
        "/diagnosis/{task_id}": {
            "get": {
                "tags": ["Diagnosis"],
                "summary": "诊断详情",
                "security": [{"bearerAuth": []}],
                "parameters": [{"name": "task_id", "in": "path", "required": True, "schema": {"type": "string"}}],
                "responses": {"200": {"description": "Success", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/DiagnosisResponse"}}}}}
            }
        },
        "/tasks": {
            "get": {
                "tags": ["Tasks"],
                "summary": "任务历史",
                "security": [{"bearerAuth": []}],
                "parameters": [{"name": "limit", "in": "query", "schema": {"type": "integer", "default": 20}}],
                "responses": {"200": {"description": "Success", "content": {"application/json": {"schema": {"type": "array", "items": {"$ref": "#/components/schemas/TaskView"}}}}}}
            }
        },
        "/compute/status": {
            "get": {
                "tags": ["Compute"],
                "summary": "计算状态",
                "security": [{"bearerAuth": []}],
                "responses": {"200": {"description": "Success"}}
            }
        },
        "/research/options": {
            "get": {
                "tags": ["Research"],
                "summary": "研究选项",
                "security": [{"bearerAuth": []}],
                "responses": {"200": {"description": "Success"}}
            }
        },
        "/system/status": {
            "get": {
                "tags": ["System"],
                "summary": "系统状态",
                "security": [{"bearerAuth": []}],
                "responses": {"200": {"description": "Success"}}
            }
        },
        "/assistant/chat": {
            "post": {
                "tags": ["Assistant"],
                "summary": "LLM 对话",
                "security": [{"bearerAuth": []}],
                "responses": {"200": {"description": "Success"}}
            }
        }
    }
}

path = os.path.join(cwd, 'hpsu-dan-platform', 'docs', 'openapi.json')
json.dump(spec, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print("openapi.json written: " + str(os.path.getsize(path)) + " bytes")
