from __future__ import annotations

import copy
import json
import os
import re
import time
from pathlib import Path
from typing import Any

import yaml


PLATFORM_ROOT = Path(__file__).resolve().parents[3]
LEGACY_ROOT = (PLATFORM_ROOT / "..").resolve()
RESEARCH_CONFIG_DIR = PLATFORM_ROOT / "configs" / "research"
STORAGE_ROOT = PLATFORM_ROOT / "storage"
IMAGE_ASSET_EXTENSIONS = {".jpg", ".jpeg", ".png", ".svg", ".pdf"}
COMPARATIVE_RESULTS_ROOT = LEGACY_ROOT / "comparative_experiments" / "results"
DISCOVERY_CACHE_TTL_SECONDS = int(os.getenv("RESEARCH_DISCOVERY_CACHE_TTL_SECONDS", "300"))
_DISCOVERY_CACHE: dict[str, Any] = {"created_at": 0.0, "results": []}
METHOD_DISPLAY_OVERRIDES = {
    "DMPAN": "HPSU-DAN",
    "MK_MMD": "MK-MMD",
}
FAULT_BY_TARGET = {
    "N15_M07_F04": {
        "code": "KA16",
        "label_en": "Outer race fault KA16",
        "label_zh": "轴承外圈故障 KA16",
        "twin_target": "bearing.outer_race",
        "markers": ["BPFO", "2xBPFO"],
        "health_score": 35,
        "risk_level": "severe",
    },
    "N15_M07_F10": {
        "code": "KI16",
        "label_en": "Inner race fault KI16",
        "label_zh": "轴承内圈故障 KI16",
        "twin_target": "bearing.inner_race",
        "markers": ["BPFI", "2xBPFI"],
        "health_score": 28,
        "risk_level": "severe",
    },
    "N15_M01_F10": {
        "code": "KI17",
        "label_en": "Inner race fault KI17",
        "label_zh": "轴承内圈故障 KI17",
        "twin_target": "bearing.inner_race",
        "markers": ["BPFI", "2xBPFI"],
        "health_score": 20,
        "risk_level": "severe",
    },
    "N09_M07_F10": {
        "code": "KI16",
        "label_en": "Inner race fault KI16",
        "label_zh": "轴承内圈故障 KI16",
        "twin_target": "bearing.inner_race",
        "markers": ["BPFI", "2xBPFI"],
        "health_score": 30,
        "risk_level": "severe",
    },
    "1500_20": {
        "code": "IF0.6",
        "label_en": "Inner race fault IF0.6",
        "label_zh": "轴承内圈故障 IF0.6",
        "twin_target": "bearing.inner_race",
        "markers": ["BPFI", "2xBPFI"],
        "health_score": 28,
        "risk_level": "severe",
    },
}


def _load_yaml(name: str) -> dict[str, Any]:
    path = RESEARCH_CONFIG_DIR / name
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def _expand_value(value: Any) -> Any:
    if isinstance(value, str):
        checkpoint_root = os.getenv("CHECKPOINT_ROOT", str(LEGACY_ROOT / "checkpoints"))
        return value.replace("${CHECKPOINT_ROOT}", checkpoint_root)
    if isinstance(value, list):
        return [_expand_value(item) for item in value]
    if isinstance(value, dict):
        return {key: _expand_value(item) for key, item in value.items()}
    return value


def _checkpoint_root() -> Path:
    return Path(os.getenv("CHECKPOINT_ROOT", str(LEGACY_ROOT / "checkpoints"))).resolve()


def _slug(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", value).strip("-")


def _method_display(method: str) -> str:
    return METHOD_DISPLAY_OVERRIDES.get(method, method)


def _read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _image_asset(run_dir: Path, stem: str) -> Path | None:
    for suffix in (".png", ".jpg", ".jpeg", ".svg", ".pdf"):
        candidate = run_dir / f"{stem}{suffix}"
        if candidate.exists():
            return candidate
    return None


def _run_assets(run_dir: Path) -> dict[str, str]:
    assets: dict[str, str] = {}
    mapping = {
        "training_curve_image": "training_curves",
        "confusion_matrix_image": "confusion_matrix",
        "feature_projection_image": "tsne_feature_distribution",
        "feature_projection_target_image": "tsne_feature_distribution_target_only",
    }
    for key, stem in mapping.items():
        path = _image_asset(run_dir, stem)
        if path is not None:
            assets[key] = str(path)
    return assets


def _metric_payload(run_dir: Path) -> dict[str, Any]:
    metrics = _read_json(run_dir / "metrics.json")
    if "accuracy" not in metrics and "acc" in metrics:
        metrics["accuracy"] = metrics.get("acc")
    if "macro_f1" not in metrics and "f1_macro" in metrics:
        metrics["macro_f1"] = metrics.get("f1_macro")
    return metrics


def _diagnosis_example_for(dataset: str, task_id: str) -> dict[str, Any]:
    tasks = _load_yaml("transfer_tasks.yaml").get("transfer_tasks", {})
    target = tasks.get(dataset, {}).get(task_id, {}).get("target_domain", "")
    fallback = {
        "code": "UNK",
        "label_en": "Fault state from completed experiment",
        "label_zh": "已完成实验故障状态",
        "twin_target": "bearing",
        "markers": ["1X"],
        "health_score": 60,
        "risk_level": "review",
    }
    return copy.deepcopy(FAULT_BY_TARGET.get(str(target), fallback))


def _result_from_run(
    run_dir: Path,
    *,
    dataset: str,
    task_id: str,
    method: str,
    source: str,
    source_label: str | None = None,
) -> dict[str, Any] | None:
    if not (run_dir / "metrics.json").exists():
        return None
    run_id = run_dir.name
    display_method = _method_display(method)
    metrics = _metric_payload(run_dir)
    result_id = _slug(f"{source}-{display_method}-{dataset}-{task_id}-{run_id}").lower()
    checkpoint = run_dir / "best_model.pth"
    return {
        "result_id": result_id,
        "title": f"{dataset} / {task_id} / {display_method} / {run_id}",
        "visibility": "public",
        "dataset": dataset,
        "task_id": task_id,
        "method": display_method,
        "implementation": method,
        "run_id": run_id,
        "checkpoint": str(checkpoint) if checkpoint.exists() else "",
        "model_id": f"{display_method.lower()}-{dataset.lower()}-{task_id.lower()}",
        "model_version": "discovered",
        "status": "completed",
        "source": source_label or source,
        "metrics": metrics,
        "diagnosis_example": _diagnosis_example_for(dataset, task_id),
        "assets": _run_assets(run_dir),
    }


def _discover_dmpan_results() -> list[dict[str, Any]]:
    root = _checkpoint_root() / "DMPAN"
    if not root.exists():
        return []
    results: list[dict[str, Any]] = []
    for dataset_dir in root.iterdir():
        if not dataset_dir.is_dir():
            continue
        dataset = dataset_dir.name
        for task_dir in dataset_dir.iterdir():
            if not task_dir.is_dir():
                continue
            for run_dir in task_dir.iterdir():
                if not run_dir.is_dir() or not run_dir.name.startswith("run_"):
                    continue
                item = _result_from_run(
                    run_dir,
                    dataset=dataset,
                    task_id=task_dir.name,
                    method="DMPAN",
                    source="main",
                    source_label="checkpoints/DMPAN",
                )
                if item is not None:
                    results.append(item)
    return results


def _discover_comparative_results() -> list[dict[str, Any]]:
    root = COMPARATIVE_RESULTS_ROOT
    if not root.exists():
        return []
    results: list[dict[str, Any]] = []
    for dataset_dir in root.iterdir():
        if not dataset_dir.is_dir():
            continue
        dataset = dataset_dir.name
        for task_dir in dataset_dir.iterdir():
            if not task_dir.is_dir():
                continue
            for method_dir in task_dir.iterdir():
                if not method_dir.is_dir():
                    continue
                for run_dir in method_dir.iterdir():
                    if not run_dir.is_dir() or not run_dir.name.startswith("run_"):
                        continue
                    item = _result_from_run(
                        run_dir,
                        dataset=dataset,
                        task_id=task_dir.name,
                        method=method_dir.name,
                        source="baseline",
                        source_label="comparative_experiments/results",
                    )
                    if item is not None:
                        results.append(item)
    return results


def _discover_all_raw_results() -> list[dict[str, Any]]:
    configured = _load_yaml("experiment_results.yaml").get("results", [])
    by_id: dict[str, dict[str, Any]] = {}
    for item in configured + _discover_dmpan_results() + _discover_comparative_results():
        result_id = str(item.get("result_id", ""))
        if result_id and result_id not in by_id:
            by_id[result_id] = item
    return sorted(
        by_id.values(),
        key=lambda item: (
            str(item.get("dataset", "")),
            str(item.get("task_id", "")),
            0 if str(item.get("method", "")) == "HPSU-DAN" else 1,
            str(item.get("method", "")),
            str(item.get("run_id", "")),
        ),
    )


def _all_raw_results(force_refresh: bool = False) -> list[dict[str, Any]]:
    now = time.time()
    if (
        not force_refresh
        and _DISCOVERY_CACHE["results"]
        and now - float(_DISCOVERY_CACHE["created_at"]) < DISCOVERY_CACHE_TTL_SECONDS
    ):
        return copy.deepcopy(_DISCOVERY_CACHE["results"])
    results = _discover_all_raw_results()
    _DISCOVERY_CACHE["created_at"] = now
    _DISCOVERY_CACHE["results"] = results
    return copy.deepcopy(results)


def refresh_research_registry() -> dict[str, Any]:
    results = _all_raw_results(force_refresh=True)
    return _summary_for(results)


def _summary_for(results: list[dict[str, Any]]) -> dict[str, Any]:
    datasets: dict[str, int] = {}
    methods: dict[str, int] = {}
    sources: dict[str, int] = {}
    tasks: dict[str, int] = {}
    for item in results:
        datasets[str(item.get("dataset", ""))] = datasets.get(str(item.get("dataset", "")), 0) + 1
        methods[str(item.get("method", ""))] = methods.get(str(item.get("method", "")), 0) + 1
        sources[str(item.get("source", ""))] = sources.get(str(item.get("source", "")), 0) + 1
        task_key = f"{item.get('dataset')}::{item.get('task_id')}"
        tasks[task_key] = tasks.get(task_key, 0) + 1
    return {
        "result_count": len(results),
        "datasets": datasets,
        "methods": methods,
        "sources": sources,
        "tasks": tasks,
        "cache_created_at": _DISCOVERY_CACHE["created_at"],
        "cache_ttl_seconds": DISCOVERY_CACHE_TTL_SECONDS,
    }


def _asset_url(result_id: str, asset_name: str) -> str:
    return f"/api/v1/research/results/{result_id}/assets/{asset_name}"


def _public_assets(result: dict[str, Any]) -> dict[str, str]:
    result_id = str(result.get("result_id", ""))
    assets = result.get("assets") or {}
    return {name: _asset_url(result_id, name) for name in assets}


def _diagnosis_result(result: dict[str, Any]) -> dict[str, Any]:
    example = copy.deepcopy(result.get("diagnosis_example") or {})
    confidence = result.get("metrics", {}).get("confidence_demo") or 0.9
    return {
        "task_id": result.get("result_id"),
        "algorithm": result.get("method"),
        "implementation": result.get("implementation"),
        "model_id": result.get("model_id"),
        "model_version": result.get("model_version"),
        "engine_mode": "completed_result",
        "research_result": True,
        "prediction": {
            "code": example.get("code"),
            "label": example.get("code"),
            "label_zh": example.get("label_zh"),
            "label_en": example.get("label_en"),
            "confidence": confidence,
            "health_score": example.get("health_score"),
            "risk_level": example.get("risk_level"),
            "twin_target": example.get("twin_target"),
        },
        "topk": [
            {
                "label": example.get("code"),
                "label_zh": example.get("label_zh"),
                "label_en": example.get("label_en"),
                "probability": confidence,
            }
        ],
        "evidence": {
            "markers": example.get("markers", []),
            "waveform": [],
            "spectrum": [],
            "statistics": {},
        },
        "input_summary": {
            "dataset": result.get("dataset"),
            "transfer_task": result.get("task_id"),
            "run_id": result.get("run_id"),
        },
        "runtime": {
            "device": "completed-result-registry",
            "total_ms": 0,
        },
        "report_summary": result.get("assets", {}).get("report_summary"),
    }


def _compact_metrics(metrics: dict[str, Any]) -> dict[str, Any]:
    keys = ("accuracy", "macro_f1", "precision_macro", "recall_macro", "acc", "f1_macro")
    return {key: metrics[key] for key in keys if key in metrics}


def _public_result(result: dict[str, Any], include_sensitive: bool = False, compact: bool = False) -> dict[str, Any]:
    payload = copy.deepcopy(result)
    raw_assets = payload.get("assets") or {}
    payload["assets"] = _public_assets(payload)
    if compact:
        payload["metrics"] = _compact_metrics(payload.get("metrics", {}))
        payload.pop("diagnosis_example", None)
    else:
        payload["diagnosis_result"] = _diagnosis_result(payload)
    checkpoint = payload.pop("checkpoint", None)
    if include_sensitive:
        payload["checkpoint"] = _expand_value(checkpoint)
        payload["checkpoint_exists"] = Path(str(_expand_value(checkpoint))).exists() if checkpoint else False
        payload["raw_assets"] = _expand_value(raw_assets)
    return payload


def research_asset_path(result_id: str, asset_name: str, include_sensitive: bool = False) -> Path | None:
    result = research_result(result_id, include_sensitive=include_sensitive)
    if result is None:
        return None
    raw_result = None
    for item in _all_raw_results():
        if item.get("result_id") == result_id:
            raw_result = item
            break
    if raw_result is None:
        return None
    raw_assets = raw_result.get("assets") or {}
    asset_value = raw_assets.get(asset_name)
    if not asset_value:
        return None
    path = Path(str(_expand_value(asset_value))).resolve()
    storage_allowed = path.is_relative_to(STORAGE_ROOT.resolve())
    checkpoint_allowed = (
        asset_name.endswith("_image")
        and path.suffix.lower() in IMAGE_ASSET_EXTENSIONS
        and (
            path.is_relative_to(_checkpoint_root())
            or path.is_relative_to(COMPARATIVE_RESULTS_ROOT.resolve())
        )
    )
    if not storage_allowed and not checkpoint_allowed:
        return None
    return path if path.exists() else None


def research_options(include_sensitive: bool = False) -> dict[str, Any]:
    datasets = _load_yaml("datasets.yaml").get("datasets", {})
    transfer_tasks = _load_yaml("transfer_tasks.yaml").get("transfer_tasks", {})
    methods = _load_yaml("methods.yaml").get("methods", {})
    results = _all_raw_results()

    visible_results = [
        _public_result(item, include_sensitive=include_sensitive, compact=True)
        for item in results
        if include_sensitive or item.get("visibility", "public") == "public"
    ]

    visible_methods = {
        key: value
        for key, value in methods.items()
        if include_sensitive or value.get("visitor_visible", True)
    }
    for item in visible_results:
        method = item.get("method")
        implementation = item.get("implementation") or method
        if method and method not in visible_methods:
            visible_methods[method] = {
                "display_name": method,
                "implementation": implementation,
                "type": "discovered_baseline" if method != "HPSU-DAN" else "main",
                "supports_training": False,
                "supports_inference": bool(item.get("checkpoint")),
                "visitor_visible": True,
            }

    return {
        "datasets": datasets,
        "transfer_tasks": transfer_tasks,
        "methods": visible_methods,
        "results": visible_results,
        "summary": _summary_for(results),
    }


def research_result(result_id: str, include_sensitive: bool = False) -> dict[str, Any] | None:
    results = _all_raw_results()
    for item in results:
        if item.get("result_id") == result_id:
            if not include_sensitive and item.get("visibility", "public") != "public":
                return None
            return _public_result(item, include_sensitive=include_sensitive)
    return None
