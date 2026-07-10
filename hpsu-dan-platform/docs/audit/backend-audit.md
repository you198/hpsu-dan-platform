# Phase 0 Backend Audit

Date: 2026-07-10

## Services

API service:

- Path: `services/api`
- Framework: FastAPI `0.115.12`
- ORM: SQLAlchemy `2.0.41`
- Migration: Alembic `1.16.2`
- Auth: JWT with RBAC helpers
- Database default: SQLite via `DATABASE_URL`

Inference service:

- Path: `services/inference`
- Framework: FastAPI
- Modes: `demo`, `real`
- Real mode delegates to `packages/hpsu_dan_adapter`

Adapter package:

- Path: `packages/hpsu_dan_adapter`
- Main bridge: `legacy_bridge.py`
- Contract source: `configs/models/hpsu-dan-v1.yaml`
- Loads legacy `models.DMPAN`, `opt`, and PyTorch from `HPSU_DAN_LEGACY_ROOT`.

## API Routes

Current route groups:

- Health: `/health`
- Auth: `/api/v1/auth/login`, `/api/v1/auth/me`
- Dashboard: `/api/v1/dashboard/summary`
- Catalog: `/api/v1/catalog/datasets`, dataset detail, conditions, faults, channels
- Models: `/api/v1/models`, model detail, model manifest
- Diagnosis: `/api/v1/diagnosis/predict`, `/api/v1/diagnosis/upload`, history, detail
- Tasks: list, detail, rerun
- Files: quarantine list
- Compute: status
- Research: options, refresh, result detail, result assets
- System: status
- Assistant: `/api/v1/assistant/chat`

## DTO And Contracts

`DiagnosisResultDTO` exists in `services/api/app/schemas.py`. Diagnosis routes preserve legacy fields and add `diagnosisResult`.

Observed contract improvement still needed:

- More route decorators should use explicit `response_model` for catalog/model/diagnosis result responses.
- Frontend store should switch from legacy `prediction/evidence` to `diagnosisResult`.

## Database Models

Existing SQLAlchemy model classes include:

- `User`, `Role`, `UserRole`
- `DiagnosisRecord`, `UploadedFile`, `PlatformTask`
- `Dataset`, `DatasetCondition`, `FaultCatalog`, `SignalChannel`
- `ModelRegistry`, `ModelVersion`
- `SignalAsset`
- `ExperimentRun`, `ExperimentMetric`, `ExperimentAsset`
- `TrainingTask`
- `SystemSnapshot`
- `AuditLog`
- `AssistantConversation`, `AssistantMessageRecord`

Alembic exists:

- `services/api/alembic.ini`
- `services/api/alembic/env.py`
- `services/api/alembic/versions/0001_initial_platform_schema.py`

## Test Results

- API tests: `6 passed`.
- Inference tests: `3 passed`.
- Alembic empty SQLite migration: passed using a temp ASCII path.

Known environment issue:

- SQLite under the Chinese workspace path can throw `disk I/O error`. For local demo use an ASCII temp path or move the DB to an ASCII-only directory. For formal deployment use PostgreSQL.

## Security Notes

- Frontend does not need database passwords or JWT secrets.
- `.env.example` contains placeholder secrets and integration notes.
- Upload route already restricts extensions and quarantines invalid files.
- Further Phase work should add request IDs, structured logging, CORS whitelist, and rate limiting.

## Phase 0 Conclusion

The backend has a usable API/inference split, JWT auth, DTO groundwork, Alembic, and catalog/model routes. It is not yet a fully layered Repository + Service architecture, and some tables named in the prompt still differ from the exact requested names, for example current task/result storage uses `platform_tasks` and `diagnosis_records`.
