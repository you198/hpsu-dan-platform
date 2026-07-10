from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


PLATFORM_ROOT = Path(__file__).resolve().parents[3]


DATASET_CATALOG: dict[str, dict[str, Any]] = {
    "PU": {
        "id": "PU",
        "name": "Paderborn University Bearing Dataset",
        "benchProfile": "pu-bearing-rig",
        "description": "Closed bearing test rig with vibration, acoustic extension, and tachometer channels.",
        "samplingRates": [64000],
        "samplingDuration": 4,
        "channels": [
            {"code": "Vibration-X", "name": "Vibration X", "axis": "X", "sensorLocation": "bearing housing", "unit": "g"},
            {"code": "Acoustic-1", "name": "Acoustic extension", "axis": "A", "sensorLocation": "boom acoustic sensor", "unit": "Pa"},
            {"code": "Tachometer", "name": "Tachometer", "axis": "RPM", "sensorLocation": "speed display module", "unit": "rpm"},
        ],
        "conditions": [
            {"code": "N15_M07_F04", "rpmMin": 1500, "rpmMax": 1500, "loadValue": 0.7, "loadUnit": "Nm", "conditionType": "constant", "description": "1500 rpm / 0.7 Nm / F04 condition"},
            {"code": "N15_M07_F10", "rpmMin": 1500, "rpmMax": 1500, "loadValue": 0.7, "loadUnit": "Nm", "conditionType": "constant", "description": "1500 rpm / 0.7 Nm / F10 condition"},
            {"code": "N15_M01_F10", "rpmMin": 1500, "rpmMax": 1500, "loadValue": 0.1, "loadUnit": "Nm", "conditionType": "constant", "description": "1500 rpm / 0.1 Nm / F10 condition"},
            {"code": "N09_M07_F10", "rpmMin": 900, "rpmMax": 900, "loadValue": 0.7, "loadUnit": "Nm", "conditionType": "constant", "description": "900 rpm / 0.7 Nm / F10 condition"},
        ],
        "faultCatalog": [
            {"code": "K001", "nameZh": "正常基准 K001", "nameEn": "Normal K001", "faultType": "normal", "faultTarget": "machine.overall", "severityDefault": "normal"},
            {"code": "KA04", "nameZh": "外圈故障 KA04", "nameEn": "Outer race fault KA04", "faultType": "outer_race", "faultTarget": "pu.bearing.outer_race", "severityDefault": "warning"},
            {"code": "KA16", "nameZh": "外圈故障 KA16", "nameEn": "Outer race fault KA16", "faultType": "outer_race", "faultTarget": "pu.bearing.outer_race", "severityDefault": "warning"},
            {"code": "KB23", "nameZh": "滚动体故障 KB23", "nameEn": "Rolling element fault KB23", "faultType": "rolling_element", "faultTarget": "pu.bearing.rolling_element", "severityDefault": "warning"},
            {"code": "KB27", "nameZh": "滚动体故障 KB27", "nameEn": "Rolling element fault KB27", "faultType": "rolling_element", "faultTarget": "pu.bearing.rolling_element", "severityDefault": "warning"},
            {"code": "KI16", "nameZh": "内圈故障 KI16", "nameEn": "Inner race fault KI16", "faultType": "inner_race", "faultTarget": "pu.bearing.inner_race", "severityDefault": "warning"},
            {"code": "KI17", "nameZh": "内圈故障 KI17", "nameEn": "Inner race fault KI17", "faultType": "inner_race", "faultTarget": "pu.bearing.inner_race", "severityDefault": "warning"},
        ],
        "availableModels": ["hpsu-dan-v1"],
    },
    "SDUST": {
        "id": "SDUST",
        "name": "SDUST Bearing-Gear Transmission Dataset",
        "benchProfile": "sdust-bearing-gear-rig",
        "description": "Open bearing-gear transmission rig with two tri-axial piezoelectric acceleration sensors.",
        "samplingRates": [25600],
        "samplingDuration": 40,
        "channels": [
            {"code": "Bearing-X", "name": "Bearing X", "axis": "X", "sensorLocation": "bearing housing", "unit": "g"},
            {"code": "Bearing-Y", "name": "Bearing Y", "axis": "Y", "sensorLocation": "bearing housing", "unit": "g"},
            {"code": "Bearing-Z", "name": "Bearing Z", "axis": "Z", "sensorLocation": "bearing housing", "unit": "g"},
            {"code": "Gearbox-X", "name": "Gearbox X", "axis": "X", "sensorLocation": "planetary gearbox support", "unit": "g"},
            {"code": "Gearbox-Y", "name": "Gearbox Y", "axis": "Y", "sensorLocation": "planetary gearbox support", "unit": "g"},
            {"code": "Gearbox-Z", "name": "Gearbox Z", "axis": "Z", "sensorLocation": "planetary gearbox support", "unit": "g"},
        ],
        "conditions": [
            {"code": "B-1000-0N", "rpmMin": 1000, "rpmMax": 1000, "loadValue": 0, "loadUnit": "N", "conditionType": "bearing_constant"},
            {"code": "B-1500-20N", "rpmMin": 1500, "rpmMax": 1500, "loadValue": 20, "loadUnit": "N", "conditionType": "bearing_constant"},
            {"code": "B-1800-40N", "rpmMin": 1800, "rpmMax": 1800, "loadValue": 40, "loadUnit": "N", "conditionType": "bearing_constant"},
            {"code": "B-2000-60N", "rpmMin": 2000, "rpmMax": 2000, "loadValue": 60, "loadUnit": "N", "conditionType": "bearing_constant"},
            {"code": "B-800-1500", "rpmMin": 800, "rpmMax": 1500, "loadValue": 20, "loadUnit": "N", "conditionType": "bearing_variable_speed"},
            {"code": "B-1500-2500", "rpmMin": 1500, "rpmMax": 2500, "loadValue": 40, "loadUnit": "N", "conditionType": "bearing_variable_speed"},
            {"code": "G-1500-0.2A", "rpmMin": 1500, "rpmMax": 1500, "loadValue": 0.2, "loadUnit": "A", "conditionType": "gear_constant"},
            {"code": "G-2000-0.5A", "rpmMin": 2000, "rpmMax": 2000, "loadValue": 0.5, "loadUnit": "A", "conditionType": "gear_constant"},
        ],
        "faultCatalog": [
            {"code": "NC", "nameZh": "正常状态 NC", "nameEn": "Normal Condition NC", "faultType": "normal", "faultTarget": "machine.overall", "severityDefault": "normal"},
            {"code": "IF0.2", "nameZh": "内圈故障 0.2 mm", "nameEn": "Inner race fault 0.2 mm", "faultType": "inner_race", "faultTarget": "sdust.bearing.inner_race", "faultSize": 0.2, "severityDefault": "warning"},
            {"code": "IF0.6", "nameZh": "内圈故障 0.6 mm", "nameEn": "Inner race fault 0.6 mm", "faultType": "inner_race", "faultTarget": "sdust.bearing.inner_race", "faultSize": 0.6, "severityDefault": "severe"},
            {"code": "OF0.2", "nameZh": "外圈故障 0.2 mm", "nameEn": "Outer race fault 0.2 mm", "faultType": "outer_race", "faultTarget": "sdust.bearing.outer_race", "faultSize": 0.2, "severityDefault": "warning"},
            {"code": "OF0.6", "nameZh": "外圈故障 0.6 mm", "nameEn": "Outer race fault 0.6 mm", "faultType": "outer_race", "faultTarget": "sdust.bearing.outer_race", "faultSize": 0.6, "severityDefault": "severe"},
            {"code": "RF0.2", "nameZh": "滚动体故障 0.2 mm", "nameEn": "Rolling element fault 0.2 mm", "faultType": "rolling_element", "faultTarget": "sdust.bearing.rolling_element", "faultSize": 0.2, "severityDefault": "warning"},
            {"code": "RF0.6", "nameZh": "滚动体故障 0.6 mm", "nameEn": "Rolling element fault 0.6 mm", "faultType": "rolling_element", "faultTarget": "sdust.bearing.rolling_element", "faultSize": 0.6, "severityDefault": "severe"},
            {"code": "SG-PIT", "nameZh": "太阳轮点蚀", "nameEn": "Sun gear pitting", "faultType": "gear_pitting", "faultTarget": "sdust.gearbox.sun_gear", "severityDefault": "warning"},
        ],
        "availableModels": ["hpsu-dan-v1"],
    },
}


FAULT_NAME_ZH = {
    "K001": "正常基准 K001",
    "KA04": "外圈故障 KA04",
    "KA16": "外圈故障 KA16",
    "KB23": "滚动体故障 KB23",
    "KB27": "滚动体故障 KB27",
    "KI16": "内圈故障 KI16",
    "KI17": "内圈故障 KI17",
    "NC": "正常状态 NC",
    "IF0.2": "内圈故障 0.2 mm",
    "IF0.6": "内圈故障 0.6 mm",
    "OF0.2": "外圈故障 0.2 mm",
    "OF0.6": "外圈故障 0.6 mm",
    "RF0.2": "滚动体故障 0.2 mm",
    "RF0.6": "滚动体故障 0.6 mm",
    "SG-PIT": "太阳轮点蚀",
}

for dataset in DATASET_CATALOG.values():
    for fault in dataset["faultCatalog"]:
        fault["nameZh"] = FAULT_NAME_ZH.get(fault["code"], fault["nameZh"])


def dataset_manifest_paths() -> list[Path]:
    dataset_dir = PLATFORM_ROOT / "configs" / "datasets"
    return sorted(dataset_dir.glob("*.json"))


def load_dataset_manifest(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        manifest = json.load(handle)
    manifest["manifestPath"] = str(path.relative_to(PLATFORM_ROOT))
    return manifest


def normalize_dataset_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    code = str(manifest.get("datasetCode") or manifest.get("id") or "").upper()
    sampling_rates = manifest.get("samplingRates") or []
    default_rate = sampling_rates[0] if sampling_rates else None
    normalized = dict(manifest)
    normalized.update(
        {
            "id": code,
            "name": manifest.get("displayName") or manifest.get("name") or code,
            "benchProfile": manifest.get("benchProfile"),
            "samplingRates": sampling_rates,
            "samplingDuration": manifest.get("samplingDuration"),
            "signalLength": manifest.get("signalLength"),
            "defaultSamplingRate": default_rate,
            "availableModels": manifest.get("enabledModels", []),
            "conditions": manifest.get("conditions", []),
            "faultCatalog": manifest.get("faultCatalog", []),
            "channels": manifest.get("channels", []),
            "transferTasks": manifest.get("transferTasks", []),
        }
    )
    return normalized


def formal_dataset_catalog() -> dict[str, dict[str, Any]]:
    catalog: dict[str, dict[str, Any]] = {}
    for path in dataset_manifest_paths():
        try:
            item = normalize_dataset_manifest(load_dataset_manifest(path))
        except Exception:
            continue
        catalog[item["id"]] = item
    return catalog


def dataset_list() -> list[dict[str, Any]]:
    formal = formal_dataset_catalog()
    if formal:
        return [
            {
                "id": item["id"],
                "name": item["name"],
                "benchProfile": item["benchProfile"],
                "samplingRates": item["samplingRates"],
                "samplingDuration": item.get("samplingDuration"),
                "signalLength": item.get("signalLength"),
                "channelCount": len(item["channels"]),
                "faultCount": len(item["faultCatalog"]),
                "transferTaskCount": len(item.get("transferTasks", [])),
                "availableModels": item["availableModels"],
                "manifestPath": item.get("manifestPath"),
                "availability": item.get("availability", {}),
            }
            for item in formal.values()
        ]
    return [
        {
            "id": item["id"],
            "name": item["name"],
            "benchProfile": item["benchProfile"],
            "samplingRates": item["samplingRates"],
            "samplingDuration": item["samplingDuration"],
            "channelCount": len(item["channels"]),
            "faultCount": len(item["faultCatalog"]),
            "availableModels": item["availableModels"],
        }
        for item in DATASET_CATALOG.values()
    ]


def dataset_detail(dataset_id: str) -> dict[str, Any] | None:
    formal = formal_dataset_catalog()
    if formal:
        return formal.get(dataset_id.upper())
    return DATASET_CATALOG.get(dataset_id.upper())


def manifest_paths() -> list[Path]:
    model_dir = PLATFORM_ROOT / "configs" / "models"
    return sorted(model_dir.glob("*.json")) + sorted(model_dir.glob("*.yaml")) + sorted(model_dir.glob("*.yml"))


def load_model_manifest(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        if path.suffix.lower() == ".json":
            manifest = json.load(handle)
        else:
            manifest = yaml.safe_load(handle) or {}
    model_id = manifest.get("modelId") or manifest.get("model_id") or path.stem
    version = manifest.get("version") or manifest.get("model_version") or "unregistered"
    dataset = manifest.get("dataset", "unknown")
    checkpoint_path = manifest.get("checkpointPath") or manifest.get("model_file")
    if checkpoint_path:
        raw_path = Path(str(checkpoint_path))
        if raw_path.is_absolute():
            resolved = raw_path
            public_path = raw_path.name
        else:
            resolved = (PLATFORM_ROOT.parents[0] / raw_path).resolve()
            public_path = str(raw_path).replace("\\", "/")
        manifest["checkpointExists"] = resolved.exists()
        manifest["checkpointFileName"] = resolved.name
        manifest["checkpointPath"] = public_path
        # Legacy compatibility for current adapter/API consumers.
        manifest["model_file_exists"] = resolved.exists()
        manifest["model_file_name"] = resolved.name
        manifest["model_file"] = public_path
    manifest["modelId"] = model_id
    manifest["model_id"] = model_id
    manifest["model_version"] = version
    manifest["dataset"] = dataset
    manifest["manifest_path"] = str(path.relative_to(PLATFORM_ROOT))
    manifest["manifestPath"] = manifest["manifest_path"]
    return manifest


def model_list() -> list[dict[str, Any]]:
    models = []
    seen: set[str] = set()
    for path in manifest_paths():
        try:
            manifest = load_model_manifest(path)
        except Exception:
            continue
        model_id = manifest.get("model_id", path.stem)
        if model_id in seen:
            continue
        seen.add(model_id)
        models.append(
            {
                "id": model_id,
                "name": manifest.get("name") or manifest.get("algorithm_name", "HPSU-DAN"),
                "version": manifest.get("model_version", "unregistered"),
                "dataset": manifest.get("dataset", "unknown"),
                "status": manifest.get("status", "unknown"),
                "manifestPath": manifest.get("manifest_path"),
                "modelFileExists": manifest.get("model_file_exists", False),
                "engineModes": manifest.get("engineModes", []),
            }
        )
    return models


def model_manifest(model_id: str) -> dict[str, Any] | None:
    for path in manifest_paths():
        try:
            manifest = load_model_manifest(path)
        except Exception:
            continue
        aliases = manifest.get("aliases") or []
        if manifest.get("model_id") == model_id or path.stem == model_id or model_id in aliases:
            return manifest
    return None
