from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv


PLATFORM_ROOT = Path(__file__).resolve().parents[4]
load_dotenv(PLATFORM_ROOT / ".env")


@dataclass(frozen=True)
class Settings:
    app_name: str
    app_env: str
    database_url: str
    jwt_secret: str
    jwt_expire_minutes: int
    admin_username: str
    admin_password: str
    guest_username: str
    guest_password: str
    inference_base_url: str
    upload_max_bytes: int
    upload_allowed_extensions: tuple[str, ...]
    upload_window_length: int
    upload_default_sampling_rate: int
    upload_quarantine_dir: str
    compute_default_device: str
    gpu_enabled: bool
    gpu_visible_devices: str
    gpu_max_memory_mb: int
    cpu_fallback_enabled: bool
    batch_inference_max_windows: int
    llm_enabled: bool
    llm_api_key: str
    llm_base_url: str
    llm_model: str
    llm_timeout_seconds: float

    @property
    def is_demo(self) -> bool:
        return self.app_env.lower() in {"development", "demo", "test"}


def _required(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value or value.startswith("replace-with"):
        raise RuntimeError(f"Missing secure configuration: {name}. Copy .env.example to .env and replace placeholders.")
    return value


@lru_cache
def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("APP_NAME", "HPSU-DAN Platform"),
        app_env=os.getenv("APP_ENV", "development"),
        database_url=os.getenv("DATABASE_URL", f"sqlite:///{PLATFORM_ROOT / 'storage' / 'platform.db'}"),
        jwt_secret=_required("JWT_SECRET"),
        jwt_expire_minutes=int(os.getenv("JWT_EXPIRE_MINUTES", "120")),
        admin_username=os.getenv("BOOTSTRAP_ADMIN_USERNAME", "admin"),
        admin_password=_required("BOOTSTRAP_ADMIN_PASSWORD"),
        guest_username=os.getenv("BOOTSTRAP_GUEST_USERNAME", "guest"),
        guest_password=_required("BOOTSTRAP_GUEST_PASSWORD"),
        inference_base_url=os.getenv("INFERENCE_BASE_URL", "http://127.0.0.1:8010").rstrip("/"),
        upload_max_bytes=int(os.getenv("UPLOAD_MAX_BYTES", "5242880")),
        upload_allowed_extensions=tuple(
            item.strip().lower()
            for item in os.getenv("UPLOAD_ALLOWED_EXTENSIONS", ".csv,.txt").split(",")
            if item.strip()
        ),
        upload_window_length=int(os.getenv("UPLOAD_WINDOW_LENGTH", "1024")),
        upload_default_sampling_rate=int(os.getenv("UPLOAD_DEFAULT_SAMPLING_RATE", "25600")),
        upload_quarantine_dir=os.getenv("UPLOAD_QUARANTINE_DIR", "storage/quarantine"),
        compute_default_device=os.getenv("COMPUTE_DEFAULT_DEVICE", "auto"),
        gpu_enabled=os.getenv("GPU_ENABLED", "false").lower() in {"1", "true", "yes", "on"},
        gpu_visible_devices=os.getenv("GPU_VISIBLE_DEVICES", "0"),
        gpu_max_memory_mb=int(os.getenv("GPU_MAX_MEMORY_MB", "6144")),
        cpu_fallback_enabled=os.getenv("CPU_FALLBACK_ENABLED", "true").lower() in {"1", "true", "yes", "on"},
        batch_inference_max_windows=int(os.getenv("BATCH_INFERENCE_MAX_WINDOWS", "4096")),
        llm_enabled=os.getenv("TENCENT_LLM_ENABLED", "false").lower() == "true",
        llm_api_key=os.getenv("TENCENT_LLM_API_KEY", "").strip(),
        llm_base_url=os.getenv("TENCENT_LLM_BASE_URL", "https://tokenhub.tencentmaas.com/v1").rstrip("/"),
        llm_model=os.getenv("TENCENT_LLM_MODEL", "deepseek-v4-pro").strip(),
        llm_timeout_seconds=float(os.getenv("TENCENT_LLM_TIMEOUT_SECONDS", "30")),
    )
