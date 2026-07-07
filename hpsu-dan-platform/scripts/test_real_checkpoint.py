from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADAPTER_SRC = ROOT / "packages" / "hpsu_dan_adapter"
if str(ADAPTER_SRC) not in sys.path:
    sys.path.insert(0, str(ADAPTER_SRC))

from hpsu_dan_adapter import HPSUDANLegacyBridge


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate real HPSU-DAN/DMPAN checkpoint inference.")
    parser.add_argument("--legacy-root", default=os.getenv("HPSU_DAN_LEGACY_ROOT", ".."))
    parser.add_argument("--manifest", default=os.getenv("HPSU_DAN_MODEL_MANIFEST", "configs/models/hpsu-dan-v1.yaml"))
    parser.add_argument("--signal", default="sine", choices=["sine", "impact"])
    return parser.parse_args()


def build_signal(kind: str, length: int) -> list[float]:
    if kind == "impact":
        return [
            0.03 * math.sin(i * 0.08) + (1.0 if i % 128 == 0 else 0.0)
            for i in range(length)
        ]
    return [0.1 * math.sin(i * 0.1) for i in range(length)]


def resolve_path(raw: str) -> Path:
    path = Path(raw)
    if path.is_absolute():
        return path
    return (ROOT / path).resolve()


def main() -> int:
    args = parse_args()
    legacy_root = resolve_path(args.legacy_root)
    manifest = resolve_path(args.manifest)
    bridge = HPSUDANLegacyBridge.from_manifest(
        legacy_root=legacy_root,
        manifest_path=manifest,
        platform_root=ROOT,
    )
    contract = bridge.contract
    signal = build_signal(args.signal, contract.sample_length)
    started = time.perf_counter()
    result = bridge.predict(signal)
    elapsed_ms = round((time.perf_counter() - started) * 1000, 3)
    output = {
        "status": "ok",
        "elapsed_ms": elapsed_ms,
        "model_file_exists": contract.model_file.exists(),
        "contract": {
            "algorithm": contract.algorithm_name,
            "implementation": contract.implementation_name,
            "model_id": contract.model_id,
            "model_version": contract.model_version,
            "dataset": contract.dataset,
            "sample_length": contract.sample_length,
            "class_count": len(contract.labels),
            "model_file": str(contract.model_file),
        },
        "prediction": result["prediction"],
        "topk": result["topk"],
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
