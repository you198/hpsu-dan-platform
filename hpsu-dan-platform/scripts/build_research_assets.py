from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

import yaml


PLATFORM_ROOT = Path(__file__).resolve().parents[1]
LEGACY_ROOT = PLATFORM_ROOT.parent
REGISTRY_PATH = PLATFORM_ROOT / "configs" / "research" / "experiment_results.yaml"
OUTPUT_ROOT = PLATFORM_ROOT / "storage" / "research_results"


def expand_path(value: str) -> Path:
    checkpoint_root = os.getenv("CHECKPOINT_ROOT", str(LEGACY_ROOT / "checkpoints"))
    return Path(value.replace("${CHECKPOINT_ROOT}", checkpoint_root))


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def parse_train_log(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    epoch_pattern = re.compile(r"第\s+(\d+)/(\d+)\s+轮")
    metric_pattern = re.compile(r"-\s+([^:]+):\s+([-+]?\d+(?:\.\d+)?(?:e[-+]?\d+)?)", re.IGNORECASE)
    validation_pattern = re.compile(r"Validation Acc\):\s+([-+]?\d+(?:\.\d+)?)")
    points: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        epoch_match = epoch_pattern.search(line)
        if epoch_match:
            current = {"epoch": int(epoch_match.group(1)), "max_epoch": int(epoch_match.group(2))}
            points.append(current)
            continue
        if current is None:
            continue
        validation_match = validation_pattern.search(line)
        if validation_match:
            current["validation_acc"] = float(validation_match.group(1))
            continue
        metric_match = metric_pattern.search(line)
        if not metric_match:
            continue
        key = metric_match.group(1).strip().lower().replace(" ", "_").replace("-", "_")
        current[key] = float(metric_match.group(2))
    return points


def compact_points(points: list[dict[str, Any]], every: int = 5) -> list[dict[str, Any]]:
    if not points:
        return []
    selected = [item for item in points if item["epoch"] == 1 or item["epoch"] % every == 0 or item["epoch"] == points[-1]["epoch"]]
    wanted = [
        "epoch",
        "validation_acc",
        "acc_source",
        "loss_total",
        "loss_domain_combined",
        "loss_ot",
        "loss_pseudo",
        "pl_accept",
        "pl_accept_rate",
    ]
    return [{key: item[key] for key in wanted if key in item} for item in selected]


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def build_assets() -> None:
    registry = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8")) or {}
    for result in registry.get("results", []):
        result_id = result["result_id"]
        run_dir = expand_path(result["checkpoint"]).parent
        out_dir = OUTPUT_ROOT / result_id
        metrics = read_json(run_dir / "metrics.json")
        curve = parse_train_log(run_dir / "train.log")
        compact_curve = compact_points(curve)
        final_point = curve[-1] if curve else {}

        write_json(out_dir / "training_curve.json", {
            "result_id": result_id,
            "source": "train.log",
            "points": compact_curve,
            "final": final_point,
        })
        write_json(out_dir / "pseudo_label_log.json", {
            "result_id": result_id,
            "source": "train.log",
            "description": "Pseudo-label acceptance statistics extracted from DMPAN training log.",
            "points": [
                {
                    "epoch": item.get("epoch"),
                    "pl_accept": item.get("pl_accept"),
                    "pl_accept_rate": item.get("pl_accept_rate"),
                    "loss_pseudo": item.get("loss_pseudo"),
                }
                for item in compact_curve
                if "pl_accept_rate" in item or "loss_pseudo" in item
            ],
        })
        write_json(out_dir / "ot_transport.json", {
            "result_id": result_id,
            "source": "train.log",
            "transport_matrix_available": False,
            "note": "This run stores domain/OT training losses and generated feature figures, but not the raw Sinkhorn transport matrix.",
            "points": [
                {
                    "epoch": item.get("epoch"),
                    "loss_domain_combined": item.get("loss_domain_combined"),
                    "loss_ot": item.get("loss_ot"),
                }
                for item in compact_curve
                if "loss_domain_combined" in item or "loss_ot" in item
            ],
        })
        write_json(out_dir / "confusion_matrix.json", {
            "result_id": result_id,
            "source": "confusion_matrix.png",
            "matrix_values_available": False,
            "image_asset": "confusion_matrix_image",
            "classes": result.get("class_labels", []),
            "metrics": metrics,
        })
        write_json(out_dir / "feature_umap.json", {
            "result_id": result_id,
            "source": "tsne_feature_distribution.png",
            "projection_method": "t-SNE",
            "image_asset": "feature_projection_image",
            "target_only_image_asset": "feature_projection_target_image",
            "metrics": {
                "accuracy": metrics.get("acc"),
                "macro_f1": metrics.get("f1_macro"),
                "per_class_f1": metrics.get("per_class_f1"),
            },
        })
        write_json(out_dir / "report_summary.json", {
            "result_id": result_id,
            "dataset": result.get("dataset"),
            "task_id": result.get("task_id"),
            "method": result.get("method"),
            "run_id": result.get("run_id"),
            "accuracy": metrics.get("acc"),
            "macro_f1": metrics.get("f1_macro"),
            "final_validation_acc": final_point.get("validation_acc"),
            "final_source_acc": final_point.get("acc_source"),
            "diagnosis_example": result.get("diagnosis_example", {}),
        })


if __name__ == "__main__":
    build_assets()
