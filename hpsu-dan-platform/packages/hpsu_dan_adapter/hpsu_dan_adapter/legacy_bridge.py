from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import importlib
import os
import sys
from typing import Any


@dataclass(frozen=True)
class LabelSpec:
    index: int
    key: str
    zh: str
    en: str
    twin_part: str


@dataclass(frozen=True)
class ModelContract:
    algorithm_name: str
    implementation_name: str
    model_id: str
    model_version: str
    dataset: str
    sample_length: int
    sampling_rate: int
    model_file: Path
    preprocess_version: str
    class_map_version: str
    normalization: str
    labels: dict[int, LabelSpec]


class HPSUDANLegacyBridge:
    """Isolation boundary for the existing experiment code."""

    def __init__(self, legacy_root: Path, contract: ModelContract):
        self.legacy_root = legacy_root.resolve()
        self.contract = contract
        self._torch = None
        self._model1 = None
        self._model2 = None
        self._device = None

    @classmethod
    def from_manifest(cls, legacy_root: Path, manifest_path: Path, platform_root: Path) -> "HPSUDANLegacyBridge":
        manifest_path = manifest_path.resolve()
        with manifest_path.open("r", encoding="utf-8") as handle:
            if manifest_path.suffix.lower() == ".json":
                manifest = json.load(handle)
            else:
                import yaml

                manifest = yaml.safe_load(handle) or {}

        raw_model_file = Path(str(manifest.get("checkpointPath") or manifest["model_file"]))
        if raw_model_file.is_absolute():
            model_file = raw_model_file
        else:
            legacy_model_file = (legacy_root / raw_model_file).resolve()
            platform_model_file = (platform_root / raw_model_file).resolve()
            model_file = legacy_model_file if legacy_model_file.exists() else platform_model_file

        labels = {}
        class_map_cfg = manifest.get("classMap") or manifest.get("class_map") or {}
        raw_labels = (class_map_cfg.get("labels")) or {}
        for raw_index, value in raw_labels.items():
            index = int(raw_index)
            labels[index] = LabelSpec(
                index=index,
                key=str(value["key"]),
                zh=str(value.get("zh", value["key"])),
                en=str(value.get("en", value["key"])),
                twin_part=str(value.get("twinPart") or value.get("twin_part", "bearing")),
            )
        if not labels:
            raise ValueError("MODEL_MANIFEST_CLASS_MAP_EMPTY")

        input_cfg = manifest.get("input") or {}
        preprocess_cfg = manifest.get("preprocess") or {}
        input_shape = manifest.get("inputShape") or []
        sample_length = input_cfg.get("sample_length")
        if sample_length is None and input_shape:
            sample_length = input_shape[-1]
        contract = ModelContract(
            algorithm_name=str(manifest.get("name") or manifest.get("algorithm_name", "HPSU-DAN")),
            implementation_name=str(manifest.get("implementationName") or manifest.get("implementation_name", "DMPAN")),
            model_id=str(manifest.get("modelId") or manifest.get("model_id", "hpsu-dan-v1")),
            model_version=str(manifest.get("version") or manifest.get("model_version", "unregistered")),
            dataset=str(manifest.get("dataset", "PU")),
            sample_length=int(sample_length or 1024),
            sampling_rate=int(preprocess_cfg.get("samplingRate") or input_cfg.get("sampling_rate", 25600)),
            model_file=model_file,
            preprocess_version=str(preprocess_cfg.get("version", "preprocess-v1")),
            class_map_version=str(class_map_cfg.get("schemaVersion") or class_map_cfg.get("version", "class-map-v1")),
            normalization=str(preprocess_cfg.get("normalization", "mean-std")),
            labels=labels,
        )
        return cls(legacy_root=legacy_root, contract=contract)

    def validate_input(self, samples: list[float]) -> dict[str, Any]:
        if len(samples) < self.contract.sample_length:
            raise ValueError("DATA_SAMPLE_LENGTH_TOO_SHORT")
        window = [float(value) for value in samples[: self.contract.sample_length]]
        return {"samples": window, "sample_length": self.contract.sample_length}

    def load_model(self):
        if self._model1 is not None and self._model2 is not None:
            return
        if not self.contract.model_file.exists():
            raise FileNotFoundError("REAL_MODEL_NOT_REGISTERED")

        if str(self.legacy_root) not in sys.path:
            sys.path.insert(0, str(self.legacy_root))

        torch = importlib.import_module("torch")
        opt = importlib.import_module("opt")
        dmpan_module = importlib.import_module("models.DMPAN")

        args = opt.parse_args([])
        args.model_name = "DMPAN"
        args.dataset = self.contract.dataset
        args.signal_size = self.contract.sample_length
        args.use_cuda = os.getenv("HPSU_DAN_USE_CUDA", "false").lower() in {"1", "true", "yes", "on"}
        args.cuda_device = os.getenv("HPSU_DAN_CUDA_DEVICE", getattr(args, "cuda_device", "0"))

        cuda_enabled = bool(args.use_cuda and torch.cuda.is_available())
        self._device = torch.device(f"cuda:{args.cuda_device}" if cuda_enabled else "cpu")

        model_cls = getattr(dmpan_module, "DMPAN")
        model1 = model_cls(args).to(self._device)
        model2 = model_cls(args).to(self._device)
        state = torch.load(str(self.contract.model_file), map_location=self._device)
        if isinstance(state, dict) and "model1" in state and "model2" in state:
            model1.load_state_dict(state["model1"])
            model2.load_state_dict(state["model2"])
        else:
            model1.load_state_dict(state)
            model2.load_state_dict(state)
        model1.eval()
        model2.eval()

        self._torch = torch
        self._model1 = model1
        self._model2 = model2

    def _preprocess(self, samples: list[float]):
        torch = self._torch
        tensor = torch.tensor(samples, dtype=torch.float32, device=self._device)
        if self.contract.normalization.lower() in {"zscore", "mean-std", "mean_std"}:
            tensor = tensor - tensor.mean()
            std = tensor.std(unbiased=False)
            tensor = tensor / torch.clamp(std, min=1e-8)
        return tensor.view(1, 1, self.contract.sample_length)

    def predict(self, samples: list[float]) -> dict[str, Any]:
        self.load_model()
        validated = self.validate_input(samples)
        tensor = self._preprocess(validated["samples"])
        torch = self._torch
        with torch.no_grad():
            logits1 = self._model1(tensor)[1]
            logits2 = self._model2(tensor)[1]
            probs = (torch.softmax(logits1, dim=1) + torch.softmax(logits2, dim=1)) / 2.0
        probabilities = probs.squeeze(0).detach().cpu().tolist()
        predicted_index = int(max(range(len(probabilities)), key=lambda index: probabilities[index]))
        label = self.contract.labels[predicted_index]
        topk = sorted(
            (
                {
                    "label": self.contract.labels[index].key,
                    "label_zh": self.contract.labels[index].zh,
                    "label_en": self.contract.labels[index].en,
                    "probability": float(probability),
                }
                for index, probability in enumerate(probabilities)
                if index in self.contract.labels
            ),
            key=lambda item: item["probability"],
            reverse=True,
        )[:3]
        confidence = float(probabilities[predicted_index])
        is_normal = label.key.upper() in {"K001", "NORMAL", "NC"}
        risk_level = "normal" if is_normal else ("severe" if confidence >= 0.85 else "warning")
        return {
            "algorithm": self.contract.algorithm_name,
            "implementation": self.contract.implementation_name,
            "model_id": self.contract.model_id,
            "model_version": self.contract.model_version,
            "preprocess_version": self.contract.preprocess_version,
            "class_map_version": self.contract.class_map_version,
            "engine_mode": "real",
            "research_result": True,
            "prediction": {
                "code": label.key,
                "label": label.key,
                "label_zh": label.zh,
                "label_en": label.en,
                "confidence": confidence,
                "risk_level": risk_level,
                "health_score": int(round(96 if is_normal else max(5, 70 - 50 * confidence))),
                "twin_target": label.twin_part,
            },
            "topk": topk,
        }
