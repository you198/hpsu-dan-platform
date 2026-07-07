from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import datetime, timezone
import csv
import json
import math
import subprocess
import shutil
import uuid
from pathlib import Path

import httpx
from fastapi import Depends, FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from .core.config import get_settings
from .core.security import create_access_token, verify_password
from .db import DiagnosisRecord, PlatformTask, UploadedFile, User, find_user, get_session, init_database
from .dependencies import current_user, require_roles
from .research_registry import refresh_research_registry, research_asset_path, research_options, research_result
from .schemas import AssistantChatRequest, AssistantChatResponse, DiagnosisRequest, LoginRequest, TokenResponse, UploadDiagnosisResponse, UserView


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_database()
    yield


settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
PLATFORM_ROOT = Path(__file__).resolve().parents[3]
UPLOAD_DIR = PLATFORM_ROOT / "storage" / "uploads"


@app.get("/health")
def health():
    return {"status": "ok", "service": "api", "time": datetime.now(timezone.utc)}


def task_view(task: PlatformTask) -> dict:
    return {
        "task_id": task.task_id,
        "task_type": task.task_type,
        "status": task.status,
        "created_by": task.created_by,
        "model_id": task.model_id,
        "model_version": task.model_version,
        "input_file_id": task.input_file_id,
        "result_id": task.result_id,
        "error_code": task.error_code,
        "error_message_key": task.error_message_key,
        "created_at": task.created_at,
        "started_at": task.started_at,
        "finished_at": task.finished_at,
    }


def uploaded_file_view(item: UploadedFile) -> dict:
    return {
        "file_id": item.file_id,
        "original_name": item.original_name,
        "status": item.status,
        "size_bytes": item.size_bytes,
        "uploaded_by": item.uploaded_by,
        "error_code": item.error_code,
        "quality": json.loads(item.quality_json) if item.quality_json else None,
        "created_at": item.created_at,
    }


def parse_signal_file(path: Path) -> list[float]:
    values: list[float] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        sample = handle.read(4096)
        handle.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t ") if sample.strip() else csv.excel
        except csv.Error:
            dialect = csv.excel
        reader = csv.reader(handle, dialect)
        for row in reader:
            for cell in row:
                try:
                    values.append(float(cell.strip()))
                    break
                except ValueError:
                    continue
    return values


def signal_quality(samples: list[float], sampling_rate: int) -> dict:
    finite = [value for value in samples if math.isfinite(value)]
    missing_ratio = 1 - len(finite) / max(1, len(samples))
    if not finite:
        return {"score": 0, "length": len(samples), "missing_ratio": 1, "outlier_ratio": 0, "sampling_rate": sampling_rate}
    mean = sum(finite) / len(finite)
    variance = sum((value - mean) ** 2 for value in finite) / len(finite)
    std = math.sqrt(max(variance, 1e-12))
    outliers = sum(1 for value in finite if abs(value - mean) > 6 * std)
    has_window = len(finite) >= settings.upload_window_length
    score = 100
    score -= int(missing_ratio * 100)
    score -= min(40, int(outliers / max(1, len(finite)) * 200))
    if not has_window:
        score = min(score, 40)
    return {
        "score": max(0, min(100, score)),
        "length": len(samples),
        "valid_length": len(finite),
        "missing_ratio": round(missing_ratio, 6),
        "outlier_ratio": round(outliers / max(1, len(finite)), 6),
        "window_length": settings.upload_window_length,
        "sampling_rate": sampling_rate,
        "has_required_window": has_window,
    }


async def call_inference(payload: dict) -> dict:
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(f"{settings.inference_base_url}/v1/predict", json=payload)
        response.raise_for_status()
    return response.json()


def save_diagnosis_record(session: Session, result: dict, username: str) -> None:
    prediction = result["prediction"]
    session.add(
        DiagnosisRecord(
            task_id=result["task_id"],
            requested_by=username,
            model_id=result["model_id"],
            engine_mode=result["engine_mode"],
            label=prediction["label"],
            confidence=prediction["confidence"],
            result_json=json.dumps(result, ensure_ascii=False),
        )
    )


async def run_signal_diagnosis(samples: list[float], sampling_rate: int, model_id: str, username: str, session: Session) -> dict:
    payload = {"samples": samples[: settings.upload_window_length], "sampling_rate": sampling_rate, "model_id": model_id}
    result = await call_inference(payload)
    result["requested_by"] = username
    save_diagnosis_record(session, result, username)
    return result


@app.post("/api/v1/auth/login", response_model=TokenResponse)
def login(payload: LoginRequest, session: Session = Depends(get_session)):
    user = find_user(session, payload.username)
    if user is None or not user.active or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="AUTH_CREDENTIALS_INVALID")
    return TokenResponse(
        access_token=create_access_token(user.username, user.role),
        user=UserView(username=user.username, role=user.role),
    )


@app.get("/api/v1/auth/me", response_model=UserView)
def me(user: User = Depends(current_user)):
    return UserView(username=user.username, role=user.role)


@app.get("/api/v1/dashboard/summary")
def dashboard_summary(_: User = Depends(current_user)):
    import yaml as _yaml
    manifest_path = PLATFORM_ROOT / "configs" / "models" / "hpsu-dan-v1.yaml"
    manifest = {}
    if manifest_path.exists():
        try:
            with manifest_path.open("r", encoding="utf-8") as f:
                manifest = _yaml.safe_load(f) or {}
        except Exception:
            manifest = {}
    inference_status = {}
    try:
        import httpx as _httpx
        with _httpx.Client(timeout=3.0) as client:
            resp = client.get(f"{settings.inference_base_url}/health")
            if resp.status_code == 200:
                inference_status = resp.json()
    except Exception:
        inference_status = {"engine_mode": "unreachable"}
    dataset = manifest.get("dataset", "PU")
    model_id = manifest.get("model_id", "hpsu-dan-v1")
    model_version = manifest.get("model_version", "unregistered")
    sample_length = manifest.get("input", {}).get("sample_length", 1024)
    sampling_rate = manifest.get("input", {}).get("sampling_rate", 25600)
    model_file = manifest.get("model_file", "")
    num_classes = manifest.get("num_classes", 7)
    task_id = ""
    for prefix in ("S3_to_", "S5_to_"):
        if prefix in model_file:
            parts = model_file.split(prefix)
            if len(parts) > 1:
                task_id = prefix.replace("_to_", chr(8594)).replace("5_to_", chr(8594)).rstrip("_to") + parts[1].split(chr(47))[0]
                break
    from .research_registry import research_options as _ro
    registry = _ro()
    best_accuracy = 0.0
    result_count = 0
    for result in registry.get("results", []):
        result_count += 1
        m = result.get("metrics", {})
        acc = m.get("accuracy", 0) or m.get("acc", 0)
        if result.get("method") == "HPSU-DAN" and acc > best_accuracy:
            best_accuracy = acc
    engine_mode = inference_status.get("engine_mode", "unreachable")
    model_registered = inference_status.get("model_registered", False)
    summary = registry.get("summary", {})
    return {
        "device": {"name": f"PU Bearing Test Bench - {task_id}" if task_id else "PU Bearing Test Bench",
            "status": "online" if engine_mode != "unreachable" else "offline",
            "health_score": round(best_accuracy * 100) if best_accuracy else 92,
            "dataset": dataset, "task_id": task_id,
            "sample_length": sample_length, "num_classes": num_classes},
        "telemetry": {"speed_rpm": 1500, "load_n": 20,
            "sampling_rate": sampling_rate, "channels": 1},
        "model": {"id": model_id, "version": model_version,
            "registry_status": "registered" if model_registered else "unregistered",
            "runtime": engine_mode, "checkpoint": model_file},
        "research": {"best_accuracy": best_accuracy,
            "total_experiments": summary.get("result_count", result_count),
            "dataset_count": len(summary.get("datasets", {})),
            "method_count": len(summary.get("methods", {})),
            "task_count": len(summary.get("tasks", {}))},
        "alerts": [],
    }


@app.post("/api/v1/diagnosis/predict")
async def diagnose(
    payload: DiagnosisRequest,
    user: User = Depends(require_roles("admin", "guest")),
    session: Session = Depends(get_session),
):
    try:
        result = await call_inference(payload.model_dump())
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=503, detail="INFERENCE_SERVICE_UNAVAILABLE") from exc
    result["requested_by"] = user.username
    save_diagnosis_record(session, result, user.username)
    session.commit()
    return result


@app.post("/api/v1/diagnosis/upload", response_model=UploadDiagnosisResponse)
async def upload_diagnosis(
    file: UploadFile = File(...),
    sampling_rate: int = Form(default_factory=lambda: settings.upload_default_sampling_rate),
    model_id: str = Form(default="hpsu-dan-v1"),
    user: User = Depends(require_roles("admin", "guest")),
    session: Session = Depends(get_session),
):
    original_name = Path(file.filename or "signal.txt").name
    suffix = Path(original_name).suffix.lower()
    file_id = f"file-{uuid.uuid4().hex}"
    task_id = f"task-{uuid.uuid4().hex}"
    if suffix not in settings.upload_allowed_extensions:
        quarantine = PLATFORM_ROOT / settings.upload_quarantine_dir
        quarantine.mkdir(parents=True, exist_ok=True)
        target = quarantine / f"{file_id}{suffix or '.bin'}"
        with target.open("wb") as handle:
            shutil.copyfileobj(file.file, handle)
        uploaded = UploadedFile(
            file_id=file_id,
            original_name=original_name,
            storage_path=str(target),
            status="quarantined",
            size_bytes=target.stat().st_size,
            uploaded_by=user.username,
            error_code="UPLOAD_EXTENSION_NOT_ALLOWED",
        )
        task = PlatformTask(task_id=task_id, task_type="diagnosis", status="failed", created_by=user.username, input_file_id=file_id, error_code="UPLOAD_EXTENSION_NOT_ALLOWED", error_message_key="upload.extension_not_allowed")
        session.add_all([uploaded, task])
        session.commit()
        raise HTTPException(status_code=422, detail="UPLOAD_EXTENSION_NOT_ALLOWED")

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    target = UPLOAD_DIR / f"{file_id}{suffix}"
    with target.open("wb") as handle:
        shutil.copyfileobj(file.file, handle)
    size = target.stat().st_size
    if size > settings.upload_max_bytes:
        quarantine = PLATFORM_ROOT / settings.upload_quarantine_dir
        quarantine.mkdir(parents=True, exist_ok=True)
        quarantine_target = quarantine / target.name
        target.replace(quarantine_target)
        uploaded = UploadedFile(file_id=file_id, original_name=original_name, storage_path=str(quarantine_target), status="quarantined", size_bytes=size, uploaded_by=user.username, error_code="UPLOAD_TOO_LARGE")
        task = PlatformTask(task_id=task_id, task_type="diagnosis", status="failed", created_by=user.username, input_file_id=file_id, error_code="UPLOAD_TOO_LARGE", error_message_key="upload.too_large")
        session.add_all([uploaded, task])
        session.commit()
        raise HTTPException(status_code=413, detail="UPLOAD_TOO_LARGE")

    uploaded = UploadedFile(file_id=file_id, original_name=original_name, storage_path=str(target), status="accepted", size_bytes=size, uploaded_by=user.username)
    task = PlatformTask(task_id=task_id, task_type="diagnosis", status="pending", created_by=user.username, model_id=model_id, input_file_id=file_id)
    session.add_all([uploaded, task])
    session.commit()

    task.status = "running"
    task.started_at = datetime.now(timezone.utc)
    try:
        samples = parse_signal_file(target)
        quality = signal_quality(samples, sampling_rate)
        uploaded.quality_json = json.dumps(quality, ensure_ascii=False)
        if not quality["has_required_window"]:
            raise ValueError("SIGNAL_WINDOW_TOO_SHORT")
        result = await run_signal_diagnosis(samples, sampling_rate, model_id, user.username, session)
        result["source_file"] = {"file_id": file_id, "original_name": original_name}
        task.status = "success"
        task.model_version = result.get("model_version")
        task.result_id = result["task_id"]
        task.finished_at = datetime.now(timezone.utc)
        session.commit()
        return {"task": task_view(task), "result": result, "quality": quality}
    except httpx.HTTPError as exc:
        task.status = "failed"
        task.error_code = "INFERENCE_SERVICE_UNAVAILABLE"
        task.error_message_key = "inference.unavailable"
        task.finished_at = datetime.now(timezone.utc)
        session.commit()
        raise HTTPException(status_code=503, detail="INFERENCE_SERVICE_UNAVAILABLE") from exc
    except Exception as exc:
        task.status = "failed"
        task.error_code = exc.args[0] if exc.args else exc.__class__.__name__
        task.error_message_key = "upload.parse_or_quality_failed"
        task.finished_at = datetime.now(timezone.utc)
        session.commit()
        raise HTTPException(status_code=422, detail=task.error_code) from exc


@app.get("/api/v1/diagnosis/history")
def diagnosis_history(
    limit: int = 20,
    user: User = Depends(current_user),
    session: Session = Depends(get_session),
):
    limit = min(max(limit, 1), 100)
    query = select(DiagnosisRecord).order_by(DiagnosisRecord.created_at.desc()).limit(limit)
    if user.role != "admin":
        query = query.where(DiagnosisRecord.requested_by == user.username)
    records = session.scalars(query).all()
    return [
        {
            "task_id": item.task_id,
            "requested_by": item.requested_by,
            "model_id": item.model_id,
            "engine_mode": item.engine_mode,
            "label": item.label,
            "confidence": item.confidence,
            "created_at": item.created_at,
        }
        for item in records
    ]


@app.get("/api/v1/diagnosis/{task_id}")
def diagnosis_detail(task_id: str, user: User = Depends(current_user), session: Session = Depends(get_session)):
    record = session.get(DiagnosisRecord, task_id)
    if record is None:
        raise HTTPException(status_code=404, detail="DIAGNOSIS_NOT_FOUND")
    if user.role != "admin" and record.requested_by != user.username:
        raise HTTPException(status_code=403, detail="DIAGNOSIS_FORBIDDEN")
    return json.loads(record.result_json)


@app.get("/api/v1/tasks")
def task_history(limit: int = 20, user: User = Depends(current_user), session: Session = Depends(get_session)):
    limit = min(max(limit, 1), 100)
    query = select(PlatformTask).order_by(PlatformTask.created_at.desc()).limit(limit)
    if user.role != "admin":
        query = query.where(PlatformTask.created_by == user.username)
    return [task_view(item) for item in session.scalars(query).all()]


@app.get("/api/v1/tasks/{task_id}")
def task_detail(task_id: str, user: User = Depends(current_user), session: Session = Depends(get_session)):
    task = session.get(PlatformTask, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="TASK_NOT_FOUND")
    if user.role != "admin" and task.created_by != user.username:
        raise HTTPException(status_code=403, detail="TASK_FORBIDDEN")
    payload = task_view(task)
    if task.input_file_id:
        uploaded = session.get(UploadedFile, task.input_file_id)
        payload["input_file"] = uploaded_file_view(uploaded) if uploaded else None
    if task.result_id:
        record = session.get(DiagnosisRecord, task.result_id)
        payload["result"] = json.loads(record.result_json) if record else None
    return payload


@app.post("/api/v1/tasks/{task_id}/rerun")
async def rerun_task(task_id: str, user: User = Depends(require_roles("admin", "guest")), session: Session = Depends(get_session)):
    source = session.get(PlatformTask, task_id)
    if source is None:
        raise HTTPException(status_code=404, detail="TASK_NOT_FOUND")
    if user.role != "admin" and source.created_by != user.username:
        raise HTTPException(status_code=403, detail="TASK_FORBIDDEN")
    if not source.input_file_id:
        raise HTTPException(status_code=422, detail="TASK_HAS_NO_INPUT_FILE")
    uploaded = session.get(UploadedFile, source.input_file_id)
    if uploaded is None or uploaded.status != "accepted":
        raise HTTPException(status_code=422, detail="INPUT_FILE_NOT_AVAILABLE")
    task = PlatformTask(
        task_id=f"task-{uuid.uuid4().hex}",
        task_type="diagnosis",
        status="running",
        created_by=user.username,
        model_id=source.model_id or "hpsu-dan-v1",
        input_file_id=uploaded.file_id,
        started_at=datetime.now(timezone.utc),
    )
    session.add(task)
    try:
        samples = parse_signal_file(Path(uploaded.storage_path))
        result = await run_signal_diagnosis(samples, settings.upload_default_sampling_rate, task.model_id or "hpsu-dan-v1", user.username, session)
        result["source_file"] = {"file_id": uploaded.file_id, "original_name": uploaded.original_name}
        task.status = "success"
        task.model_version = result.get("model_version")
        task.result_id = result["task_id"]
        task.finished_at = datetime.now(timezone.utc)
        session.commit()
        return {"task": task_view(task), "result": result}
    except Exception as exc:
        task.status = "failed"
        task.error_code = exc.args[0] if exc.args else exc.__class__.__name__
        task.error_message_key = "task.rerun_failed"
        task.finished_at = datetime.now(timezone.utc)
        session.commit()
        raise HTTPException(status_code=422, detail=task.error_code) from exc


@app.get("/api/v1/files/quarantine")
def quarantined_files(limit: int = 20, _: User = Depends(require_roles("admin")), session: Session = Depends(get_session)):
    limit = min(max(limit, 1), 100)
    query = select(UploadedFile).where(UploadedFile.status == "quarantined").order_by(UploadedFile.created_at.desc()).limit(limit)
    return [uploaded_file_view(item) for item in session.scalars(query).all()]


@app.get("/api/v1/compute/status")
def compute_status(_: User = Depends(current_user)):
    gpu_available = False
    nvidia_smi_available = False
    try:
        result = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.used,memory.total,utilization.gpu", "--format=csv,noheader,nounits"], capture_output=True, text=True, timeout=2, check=False)
        nvidia_smi_available = result.returncode == 0
        gpu_available = nvidia_smi_available and bool(result.stdout.strip())
    except Exception:
        pass
    return {
        "compute_default_device": settings.compute_default_device,
        "gpu_enabled": settings.gpu_enabled,
        "gpu_available": gpu_available,
        "gpu_visible_devices": settings.gpu_visible_devices,
        "gpu_max_memory_mb": settings.gpu_max_memory_mb,
        "cpu_fallback_enabled": settings.cpu_fallback_enabled,
        "batch_inference_max_windows": settings.batch_inference_max_windows,
        "queues": {
            "cpu_default_queue": {"status": "ready"},
            "gpu_inference_queue": {"status": "ready" if settings.gpu_enabled else "disabled"},
            "gpu_training_queue": {"status": "planned"},
            "gpu_analysis_queue": {"status": "planned"},
            "report_queue": {"status": "planned"},
        },
        "nvidia_smi_available": nvidia_smi_available,
    }


@app.get("/api/v1/research/options")
def get_research_options(user: User = Depends(current_user)):
    return research_options(include_sensitive=user.role == "admin")


@app.post("/api/v1/research/refresh")
def refresh_research_options(_: User = Depends(require_roles("admin"))):
    return refresh_research_registry()


@app.get("/api/v1/research/results/{result_id}")
def get_research_result(result_id: str, user: User = Depends(current_user)):
    result = research_result(result_id, include_sensitive=user.role == "admin")
    if result is None:
        raise HTTPException(status_code=404, detail="RESEARCH_RESULT_NOT_FOUND")
    return result


@app.get("/api/v1/research/results/{result_id}/assets/{asset_name}")
def get_research_asset(result_id: str, asset_name: str, user: User = Depends(current_user)):
    path = research_asset_path(result_id, asset_name, include_sensitive=user.role == "admin")
    if path is None:
        raise HTTPException(status_code=404, detail="RESEARCH_ASSET_NOT_FOUND")
    return FileResponse(path)


@app.get("/api/v1/system/status")
def system_status(_: User = Depends(require_roles("admin"))):
    return {
        "environment": settings.app_env,
        "database": "connected",
        "inference_url_configured": bool(settings.inference_base_url),
        "assistant_enabled": settings.llm_enabled,
    }


@app.post("/api/v1/assistant/chat", response_model=AssistantChatResponse)
async def assistant_chat(payload: AssistantChatRequest, _: User = Depends(current_user)):
    if not settings.llm_enabled:
        raise HTTPException(status_code=503, detail="ASSISTANT_DISABLED")
    if not settings.llm_api_key:
        raise HTTPException(status_code=503, detail="ASSISTANT_PROVIDER_NOT_CONFIGURED")
    system_prompt = (
        "You are the assistant inside the HPSU-DAN intelligent fault diagnosis digital twin platform. "
        "Answer concisely, focus on bearing and rotating machinery diagnosis, digital twin UI, deployment, "
        "and research workflow. Never claim demo inference results are real research conclusions."
    )
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(message.model_dump() for message in payload.messages)
    try:
        async with httpx.AsyncClient(timeout=settings.llm_timeout_seconds) as client:
            response = await client.post(
                f"{settings.llm_base_url}/chat/completions",
                headers={"Authorization": f"Bearer {settings.llm_api_key}"},
                json={
                    "model": settings.llm_model,
                    "messages": messages,
                    "temperature": payload.temperature,
                    "max_tokens": payload.max_tokens,
                },
            )
            response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        detail = {
            "error": "ASSISTANT_PROVIDER_ERROR",
            "provider_status": exc.response.status_code,
            "provider_body": exc.response.text[:500],
        }
        raise HTTPException(status_code=502, detail=detail) from exc
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail={"error": "ASSISTANT_PROVIDER_ERROR", "message": str(exc)}) from exc
    data = response.json()
    content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
    return AssistantChatResponse(model=settings.llm_model, content=content)
