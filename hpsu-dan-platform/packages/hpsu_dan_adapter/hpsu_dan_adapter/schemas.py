from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    """共享推理请求模型：API 服务转发给推理服务时使用。"""
    samples: list[float] = Field(min_length=1024, max_length=262144)
    sampling_rate: int = Field(default=25600, ge=1, le=1000000)
    model_id: str = Field(default="hpsu-dan-v1", max_length=128)
