import os
import tempfile
import uuid
from pathlib import Path

os.environ["APP_ENV"] = "test"
os.environ["JWT_SECRET"] = "test-only-secret-with-sufficient-length"
os.environ["BOOTSTRAP_ADMIN_PASSWORD"] = "admin-test-password"
os.environ["BOOTSTRAP_GUEST_PASSWORD"] = "guest-test-password"
os.environ["DATABASE_URL"] = f"sqlite:///{Path(tempfile.gettempdir()) / ('hpsu-api-' + uuid.uuid4().hex + '.db')}"

from fastapi.testclient import TestClient

from app import main
from app.main import app


def login(client: TestClient, username: str, password: str) -> str:
    response = client.post("/api/v1/auth/login", json={"username": username, "password": password})
    assert response.status_code == 200
    return response.json()["access_token"]


def test_admin_and_guest_are_isolated_by_backend_rbac():
    with TestClient(app) as client:
        admin_token = login(client, "admin", "admin-test-password")
        guest_token = login(client, "guest", "guest-test-password")

        admin = client.get("/api/v1/system/status", headers={"Authorization": f"Bearer {admin_token}"})
        guest = client.get("/api/v1/system/status", headers={"Authorization": f"Bearer {guest_token}"})

        assert admin.status_code == 200
        assert guest.status_code == 403


def test_dashboard_requires_authentication():
    with TestClient(app) as client:
        response = client.get("/api/v1/dashboard/summary")
        assert response.status_code == 401


def test_research_registry_is_visible_without_leaking_checkpoint_paths():
    with TestClient(app) as client:
        guest_token = login(client, "guest", "guest-test-password")
        admin_token = login(client, "admin", "admin-test-password")

        guest = client.get("/api/v1/research/options", headers={"Authorization": f"Bearer {guest_token}"})
        admin = client.get("/api/v1/research/options", headers={"Authorization": f"Bearer {admin_token}"})

        assert guest.status_code == 200
        guest_payload = guest.json()
        assert "PU" in guest_payload["datasets"]
        assert "SDUST" in guest_payload["datasets"]
        assert "S3_to_N15M01F10" in guest_payload["transfer_tasks"]["PU"]
        assert "HPSU-DAN" in guest_payload["methods"]
        assert guest_payload["results"]
        assert "checkpoint" not in guest_payload["results"][0]

        assert admin.status_code == 200
        admin_payload = admin.json()
        assert "checkpoint" in admin_payload["results"][0]
        assert "checkpoint_exists" in admin_payload["results"][0]

        result_id = guest_payload["results"][0]["result_id"]
        detail = client.get(f"/api/v1/research/results/{result_id}", headers={"Authorization": f"Bearer {guest_token}"})
        assert detail.status_code == 200
        detail_payload = detail.json()
        assert detail_payload["result_id"] == result_id
        assert "checkpoint" not in detail_payload
        assert detail_payload["metrics"]["accuracy"] is not None
        assert detail_payload["diagnosis_result"]["prediction"]["twin_target"]
        assert detail_payload["assets"]["confusion_matrix_image"].startswith("/api/v1/research/results/")
        assert "CHECKPOINT_ROOT" not in str(detail_payload["assets"])
        assert ":\\" not in str(detail_payload["assets"])
        assert "\\\\" not in str(detail_payload["assets"])

        asset = client.get(detail_payload["assets"]["confusion_matrix_image"], headers={"Authorization": f"Bearer {guest_token}"})
        assert asset.status_code == 200
        assert asset.headers["content-type"].startswith("image/")


def test_upload_csv_creates_successful_diagnosis_task(monkeypatch):
    calls = {"count": 0}

    async def fake_inference(payload):
        calls["count"] += 1
        return {
            "task_id": f"real-test-task-{calls['count']}",
            "algorithm": "HPSU-DAN",
            "implementation": "DMPAN",
            "model_id": payload["model_id"],
            "model_version": "1.0.0",
            "engine_mode": "real",
            "research_result": True,
            "prediction": {
                "code": "KI17",
                "label": "KI17",
                "label_zh": "inner",
                "label_en": "Inner Race Fault",
                "confidence": 0.9,
                "health_score": 25,
                "risk_level": "severe",
                "twin_target": "bearing.inner_race",
            },
            "topk": [],
            "evidence": {"waveform": [], "spectrum": [], "markers": ["BPFI"]},
            "input_summary": {"sample_length": 1024, "sampling_rate": payload["sampling_rate"], "channels": ["X"]},
            "runtime": {"total_ms": 1, "device": "cpu"},
        }

    monkeypatch.setattr(main, "call_inference", fake_inference)
    csv_data = "\n".join(str(i * 0.01) for i in range(1024))
    with TestClient(app) as client:
        token = login(client, "admin", "admin-test-password")
        response = client.post(
            "/api/v1/diagnosis/upload",
            headers={"Authorization": f"Bearer {token}"},
            files={"file": ("signal.csv", csv_data, "text/csv")},
            data={"sampling_rate": "25600", "model_id": "hpsu-dan-v1"},
        )
        assert response.status_code == 200, response.text
        payload = response.json()
        assert payload["task"]["status"] == "success"
        assert payload["result"]["engine_mode"] == "real"
        assert payload["quality"]["has_required_window"] is True

        task_id = payload["task"]["task_id"]
        result_id = payload["task"]["result_id"]
        task_detail = client.get(f"/api/v1/tasks/{task_id}", headers={"Authorization": f"Bearer {token}"})
        diagnosis_detail = client.get(f"/api/v1/diagnosis/{result_id}", headers={"Authorization": f"Bearer {token}"})
        rerun = client.post(f"/api/v1/tasks/{task_id}/rerun", headers={"Authorization": f"Bearer {token}"})
        compute = client.get("/api/v1/compute/status", headers={"Authorization": f"Bearer {token}"})

        assert task_detail.status_code == 200
        assert task_detail.json()["result"]["task_id"] == "real-test-task-1"
        assert diagnosis_detail.status_code == 200
        assert diagnosis_detail.json()["prediction"]["code"] == "KI17"
        assert rerun.status_code == 200
        assert rerun.json()["task"]["status"] == "success"
        assert compute.status_code == 200
        assert "queues" in compute.json()


def test_invalid_upload_is_quarantined_for_admin(monkeypatch):
    async def fake_inference(_):
        raise AssertionError("invalid file should not call inference")

    monkeypatch.setattr(main, "call_inference", fake_inference)
    with TestClient(app) as client:
        token = login(client, "admin", "admin-test-password")
        response = client.post(
            "/api/v1/diagnosis/upload",
            headers={"Authorization": f"Bearer {token}"},
            files={"file": ("bad.exe", b"not signal", "application/octet-stream")},
            data={"sampling_rate": "25600", "model_id": "hpsu-dan-v1"},
        )
        assert response.status_code == 422
        quarantine = client.get("/api/v1/files/quarantine", headers={"Authorization": f"Bearer {token}"})
        assert quarantine.status_code == 200
        assert any(item["error_code"] == "UPLOAD_EXTENSION_NOT_ALLOWED" for item in quarantine.json())
