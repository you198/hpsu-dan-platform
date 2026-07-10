from __future__ import annotations

import math
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


PLATFORM_ROOT = Path(__file__).resolve().parents[3]
ADAPTER_SRC = PLATFORM_ROOT / "packages" / "hpsu_dan_adapter"
if str(ADAPTER_SRC) not in sys.path:
    sys.path.insert(0, str(ADAPTER_SRC))

from hpsu_dan_adapter import HPSUDANLegacyBridge

load_dotenv(PLATFORM_ROOT / ".env")
MODE = os.getenv("INFERENCE_MODE", "demo").lower()
LEGACY_ROOT = Path(os.getenv("HPSU_DAN_LEGACY_ROOT", ".."))
if not LEGACY_ROOT.is_absolute():
    LEGACY_ROOT = (PLATFORM_ROOT / LEGACY_ROOT).resolve()
MANIFEST_PATH = Path(os.getenv("HPSU_DAN_MODEL_MANIFEST", "configs/models/hpsu-dan-v1.json"))
if not MANIFEST_PATH.is_absolute():
    MANIFEST_PATH = (PLATFORM_ROOT / MANIFEST_PATH).resolve()
app = FastAPI(title="HPSU-DAN Inference Service", version="0.1.0")
_bridge: HPSUDANLegacyBridge | None = None


from hpsu_dan_adapter.schemas import PredictRequest

LABELS = {
    0: ("normal", "正常状态", "Normal", "bearing"),
    1: ("inner_race_fault", "内圈故障", "Inner Race Fault", "bearing.inner_race"),
    2: ("outer_race_fault", "外圈故障", "Outer Race Fault", "bearing.outer_race"),
    3: ("rolling_element_fault", "滚动体故障", "Rolling Element Fault", "bearing.rolling_element"),
}


def bridge() -> HPSUDANLegacyBridge:
    global _bridge
    if _bridge is None:
        _bridge = HPSUDANLegacyBridge.from_manifest(
            legacy_root=LEGACY_ROOT,
            manifest_path=MANIFEST_PATH,
            platform_root=PLATFORM_ROOT,
        )
    return _bridge


def demo_predict(signal: list[float]) -> tuple[int, list[float]]:
    """Deterministic UI integration engine; never presented as a research model."""
    mean = sum(signal) / len(signal)
    normalized = [value - mean for value in signal]
    rms = math.sqrt(sum(value * value for value in normalized) / len(normalized))
    peak = max(abs(value) for value in normalized)
    crest = peak / max(rms, 1e-9)
    if rms < 0.18:
        cls = 0
    elif crest > 5.0:
        cls = 1
    elif crest > 3.2:
        cls = 2
    else:
        cls = 3
    logits = [-(rms / 0.18), crest / 5.0, crest / 3.2, rms / 0.35]
    logits[cls] += 2.2
    maximum = max(logits)
    probabilities = [math.exp(value - maximum) for value in logits]
    total = sum(probabilities)
    return cls, [value / total for value in probabilities]


def evidence_summary(signal: list[float], sampling_rate: int, markers: list[str]) -> dict:
    window = [float(value) for value in signal[:2048]]
    if not window:
        return {
            "waveform": [],
            "spectrum": [],
            "markers": markers,
            "statistics": {"mean": 0, "variance": 0, "rms": 0, "peak": 0, "kurtosis": 0, "skewness": 0, "crest_factor": 0},
            "window": {"window_index": 0, "start": 0, "length": 0},
        }
    mean = sum(window) / len(window)
    centered = [value - mean for value in window]
    variance = sum(value * value for value in centered) / len(centered)
    rms = math.sqrt(sum(value * value for value in window) / len(window))
    peak = max((abs(value) for value in centered), default=1.0) or 1.0
    std = math.sqrt(max(variance, 1e-12))
    skewness = sum((value / std) ** 3 for value in centered) / len(centered)
    kurtosis = sum((value / std) ** 4 for value in centered) / len(centered)
    crest_factor = peak / max(rms, 1e-9)
    step = max(1, len(centered) // 120)
    waveform = [
        {
            "x": round(index / max(1, len(centered) - 1), 5),
            "y": round(max(-1.0, min(1.0, centered[index] / peak)), 5),
        }
        for index in range(0, len(centered), step)
    ][:120]

    bins = 48
    spectrum = []
    nyquist = sampling_rate / 2
    for bin_index in range(bins):
        frequency = (bin_index + 1) * nyquist / bins
        real = 0.0
        imag = 0.0
        for sample_index, value in enumerate(centered):
            angle = 2 * math.pi * (bin_index + 1) * sample_index / len(centered)
            real += value * math.cos(angle)
            imag -= value * math.sin(angle)
        magnitude = math.sqrt(real * real + imag * imag) / len(centered)
        spectrum.append({"frequency": round(frequency, 2), "magnitude": magnitude})
    max_magnitude = max((item["magnitude"] for item in spectrum), default=1.0) or 1.0
    for item in spectrum:
        item["magnitude"] = round(item["magnitude"] / max_magnitude, 5)
    return {
        "waveform": waveform,
        "spectrum": spectrum,
        "markers": markers,
        "statistics": {
            "mean": round(mean, 6),
            "variance": round(variance, 6),
            "rms": round(rms, 6),
            "peak": round(peak, 6),
            "kurtosis": round(kurtosis, 6),
            "skewness": round(skewness, 6),
            "crest_factor": round(crest_factor, 6),
        },
        "window": {"window_index": 0, "start": 0, "length": min(len(signal), 2048)},
    }


def marker_names(twin_target: str, code: str) -> list[str]:
    target = twin_target.lower()
    upper_code = code.upper()
    if "inner" in target or upper_code.startswith("KI"):
        return ["BPFI", "2xBPFI"]
    if "outer" in target or upper_code.startswith("KA"):
        return ["BPFO", "2xBPFO"]
    if "rolling" in target or upper_code.startswith("KB"):
        return ["BSF", "FTF"]
    return ["1X"]


def runtime_device() -> str:
    if MODE != "real":
        return "cpu"
    try:
        bridge().load_model()
        device = getattr(bridge(), "_device", None)
        return str(device or "cpu")
    except Exception:
        return "unknown"


@app.get("/health")
def health():
    payload = {"status": "ok", "service": "inference", "engine_mode": MODE}
    if MODE == "real":
        try:
            contract = bridge().contract
            payload.update(
                {
                    "model_id": contract.model_id,
                    "model_version": contract.model_version,
                    "model_registered": contract.model_file.exists(),
                    "model_file": str(contract.model_file),
                }
            )
        except Exception as exc:
            payload.update({"model_registered": False, "model_error": exc.__class__.__name__})
    return payload


@app.post("/v1/predict")
def predict(payload: PredictRequest):
    started = time.perf_counter()
    signal = payload.samples
    if not all(math.isfinite(value) for value in signal):
        raise HTTPException(status_code=422, detail="SIGNAL_CONTAINS_NON_FINITE_VALUES")
    if MODE == "real":
        try:
            inference_started = time.perf_counter()
            result = bridge().predict(signal)
            inference_ms = round((time.perf_counter() - inference_started) * 1000, 3)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=503, detail="REAL_MODEL_NOT_REGISTERED") from exc
        except ImportError as exc:
            raise HTTPException(status_code=503, detail={"error": "REAL_MODEL_DEPENDENCY_MISSING", "message": str(exc)}) from exc
        except Exception as exc:
            raise HTTPException(status_code=500, detail={"error": "REAL_MODEL_INFERENCE_FAILED", "message": str(exc)}) from exc
        result.update(
            {
                "task_id": f"real-{time.time_ns()}",
                "input_summary": {
                    "sample_length": len(signal),
                    "sampling_rate": payload.sampling_rate,
                    "channels": ["X"],
                    "normalization": bridge().contract.normalization,
                },
                "evidence": evidence_summary(
                    signal,
                    payload.sampling_rate,
                    marker_names(
                        result.get("prediction", {}).get("twin_target", ""),
                        result.get("prediction", {}).get("code", result.get("prediction", {}).get("label", "")),
                    ),
                ),
                "runtime": {
                    "preprocess_ms": 0,
                    "inference_ms": inference_ms,
                    "postprocess_ms": round(max(0, (time.perf_counter() - started) * 1000 - inference_ms), 3),
                    "total_ms": round((time.perf_counter() - started) * 1000, 3),
                    "device": runtime_device(),
                },
                "notice": "Real DMPAN checkpoint inference through the legacy HPSU-DAN adapter.",
            }
        )
        return result
    if MODE != "demo":
        raise HTTPException(status_code=503, detail="INFERENCE_MODE_UNSUPPORTED")
    cls, probabilities = demo_predict(signal)
    key, zh, en, twin = LABELS[cls]
    topk = sorted(
        ({"label": LABELS[i][0], "label_zh": LABELS[i][1], "label_en": LABELS[i][2], "probability": p} for i, p in enumerate(probabilities)),
        key=lambda item: item["probability"],
        reverse=True,
    )[:3]
    confidence = probabilities[cls]
    return {
        "task_id": f"demo-{time.time_ns()}",
        "algorithm": "HPSU-DAN",
        "model_id": payload.model_id,
        "model_version": "unregistered",
        "engine_mode": "demo",
        "research_result": False,
        "input_summary": {"sample_length": len(signal), "sampling_rate": payload.sampling_rate, "channels": ["X"], "normalization": "mean-centered"},
        "evidence": evidence_summary(signal, payload.sampling_rate, marker_names(twin, key)),
        "prediction": {
            "label": key,
            "label_zh": zh,
            "label_en": en,
            "confidence": confidence,
            "health_score": int(round(100 if cls == 0 else max(5, 70 - 50 * confidence))),
            "twin_target": twin,
        },
        "topk": topk,
        "runtime": {"preprocess_ms": 0, "inference_ms": 0, "postprocess_ms": 0, "total_ms": round((time.perf_counter() - started) * 1000, 3), "device": "cpu"},
        "notice": "Demo integration engine only; not an SF-HDOT/HPSU-DAN research inference result.",
    }
