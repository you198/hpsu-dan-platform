# Phase 1 Manifest And DTO Report

Date: 2026-07-10

## Scope

Phase 1 formalizes:

- Dataset Manifest for PU and SDUST.
- Model Manifest for the verified PU HPSU-DAN/DMPAN checkpoint.
- Backend catalog loading from formal manifests.
- Adapter support for JSON/YAML model manifests.
- Compatibility with the existing `DiagnosisResultDTO`.

## Files Added

- `configs/datasets/PU.json`
- `configs/datasets/SDUST.json`
- `configs/models/hpsu-dan-v1.json`
- `artifacts/datasets-manifest.json`
- `artifacts/models-manifest.json`
- `docs/phase1-manifest-dto.md`

## Files Modified

- `services/api/app/catalog.py`
- `packages/hpsu_dan_adapter/hpsu_dan_adapter/legacy_bridge.py`
- `services/inference/app/main.py`
- `.env.example`

## Dataset Manifest Changes

PU:

- Domains verified from `opt.py`: `N15_M07_F04`, `N15_M07_F10`, `N15_M01_F10`, `N09_M07_F10`.
- Fault classes verified from `opt.py` default task: `K001`, `KA04`, `KA16`, `KB23`, `KB27`, `KI16`, `KI17`.
- Loader code verified in `datasets/PU.py`.
- Raw signal directory is still unconfirmed.

SDUST:

- Domains verified from `opt.py`: `1500_20`, `1500_60`, `2000_20`, `2000_60`, `3000_20`, `3000_60`.
- Fault classes verified from `opt.py` and `datasets/SDUST.py`: `NC`, `IF0.2`, `IF0.6`, `OF0.2`, `OF0.6`, `RF0.2`, `RF0.6`.
- Loader code verified in `datasets/SDUST.py`.
- Raw signal directory and real checkpoint binding are still unconfirmed.

## Model Manifest Changes

Formal model manifest:

- `modelId`: `hpsu-dan-v1`
- alias: `hpsu-dan-pu-v1`
- checkpoint: `checkpoints/DMPAN/PU/S3_to_N15M01F10/run_10_0119-103206/best_model.pth`
- SHA-256: `fff9123c9ebb814f68fa7a1b607886bd0b506dd4cebd79163a8873d38906c2ef`
- checkpoint size: `28468365`
- class map: PU 7-class public task.

The manifest stores the checkpoint as a path relative to `HPSU_DAN_LEGACY_ROOT`, not as a browser-visible absolute path.

## API Changes

- Dataset catalog now prefers `configs/datasets/*.json`.
- Model catalog now prefers `configs/models/*.json`.
- Legacy YAML manifests remain readable as fallback.
- Model API output keeps legacy fields such as `model_id`, `model_file_exists`, and `model_file_name` for compatibility, while also exposing formal camelCase fields.

## Adapter Changes

`HPSUDANLegacyBridge.from_manifest()` now supports:

- JSON and YAML manifest files.
- `checkpointPath` and legacy `model_file`.
- `classMap` and legacy `class_map`.
- `inputShape` and legacy `input.sample_length`.
- checkpoint paths relative to `HPSU_DAN_LEGACY_ROOT`.

## Database Changes

No database schema change in Phase 1.

## Human Asset Needs

- Confirm raw PU signal root.
- Confirm raw SDUST signal root.
- Provide or identify real SDUST model checkpoint if SDUST real inference is required.
- Provide true 3D/CAD/GLB assets if the later Three.js scene must represent imported physical equipment rather than generated geometry.

## Remaining Issues

- Existing legacy YAML and several older frontend strings still contain mojibake Chinese labels.
- Frontend still consumes static/mocked dataset state in Dashboard and Digital Twin.
- Diagnosis store still needs to prefer `diagnosisResult`.
