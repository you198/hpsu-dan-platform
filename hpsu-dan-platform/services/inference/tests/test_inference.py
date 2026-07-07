import math
import os

os.environ["INFERENCE_MODE"] = "demo"

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_exposes_engine_mode():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["engine_mode"] == "demo"


def test_demo_prediction_is_explicitly_non_research():
    samples = [0.1 * math.sin(i * 0.1) for i in range(1024)]
    response = client.post("/v1/predict", json={"samples": samples, "sampling_rate": 25600})
    assert response.status_code == 200
    payload = response.json()
    assert payload["engine_mode"] == "demo"
    assert payload["research_result"] is False
    assert len(payload["topk"]) == 3


def test_rejects_short_signal():
    response = client.post("/v1/predict", json={"samples": [0.0] * 100})
    assert response.status_code == 422
