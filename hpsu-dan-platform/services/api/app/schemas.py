from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    password: str = Field(min_length=1, max_length=128)


class UserView(BaseModel):
    username: str
    role: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserView


from hpsu_dan_adapter.schemas import PredictRequest as DiagnosisRequest

class TaskView(BaseModel):
    task_id: str
    task_type: str
    status: str
    created_by: str
    model_id: str | None = None
    model_version: str | None = None
    input_file_id: str | None = None
    result_id: str | None = None
    error_code: str | None = None
    error_message_key: str | None = None
    created_at: object
    started_at: object | None = None
    finished_at: object | None = None


class UploadDiagnosisResponse(BaseModel):
    task: TaskView
    result: dict | None = None
    quality: dict | None = None


class AssistantMessage(BaseModel):
    role: str = Field(pattern="^(user|assistant|system)$")
    content: str = Field(min_length=1, max_length=8000)


class AssistantChatRequest(BaseModel):
    messages: list[AssistantMessage] = Field(min_length=1, max_length=20)
    temperature: float = Field(default=0.2, ge=0, le=2)
    max_tokens: int = Field(default=1200, ge=64, le=4096)


class AssistantChatResponse(BaseModel):
    model: str
    content: str
