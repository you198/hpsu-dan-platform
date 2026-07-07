from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from .core.config import get_settings
from .core.security import hash_password


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(64), primary_key=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(32), index=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))


class DiagnosisRecord(Base):
    __tablename__ = "diagnosis_records"

    task_id: Mapped[str] = mapped_column(String(96), primary_key=True)
    requested_by: Mapped[str] = mapped_column(String(64), index=True)
    model_id: Mapped[str] = mapped_column(String(128), index=True)
    engine_mode: Mapped[str] = mapped_column(String(32), index=True)
    label: Mapped[str] = mapped_column(String(64), index=True)
    confidence: Mapped[float] = mapped_column(Float)
    result_json: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)


class UploadedFile(Base):
    __tablename__ = "uploaded_files"

    file_id: Mapped[str] = mapped_column(String(96), primary_key=True)
    original_name: Mapped[str] = mapped_column(String(255))
    storage_path: Mapped[str] = mapped_column(String(512))
    status: Mapped[str] = mapped_column(String(32), index=True)
    size_bytes: Mapped[int] = mapped_column(Integer)
    uploaded_by: Mapped[str] = mapped_column(String(64), index=True)
    error_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    quality_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)


class PlatformTask(Base):
    __tablename__ = "platform_tasks"

    task_id: Mapped[str] = mapped_column(String(96), primary_key=True)
    task_type: Mapped[str] = mapped_column(String(32), index=True)
    status: Mapped[str] = mapped_column(String(32), index=True)
    created_by: Mapped[str] = mapped_column(String(64), index=True)
    model_id: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    model_version: Mapped[str | None] = mapped_column(String(64), nullable=True)
    input_file_id: Mapped[str | None] = mapped_column(String(96), nullable=True, index=True)
    result_id: Mapped[str | None] = mapped_column(String(96), nullable=True, index=True)
    error_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    error_message_key: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


def _engine():
    settings = get_settings()
    connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
    return create_engine(settings.database_url, connect_args=connect_args)


engine = None
SessionLocal = None


def init_database() -> None:
    global engine, SessionLocal
    engine = _engine()
    SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
    Base.metadata.create_all(engine)
    settings = get_settings()
    with SessionLocal() as session:
        for username, password, role in (
            (settings.admin_username, settings.admin_password, "admin"),
            (settings.guest_username, settings.guest_password, "guest"),
        ):
            if session.get(User, username) is None:
                session.add(User(username=username, password_hash=hash_password(password), role=role))
        session.commit()


def get_session():
    if SessionLocal is None:
        raise RuntimeError("Database is not initialized")
    with SessionLocal() as session:
        yield session


def find_user(session: Session, username: str) -> User | None:
    return session.scalar(select(User).where(User.username == username))
