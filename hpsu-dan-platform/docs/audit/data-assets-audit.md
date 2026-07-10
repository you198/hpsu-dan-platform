# Phase 0 Data And Asset Audit

Date: 2026-07-10

## Asset Scan Summary

Recursive scan excluding `.git`, `node_modules`, `.venv`, `.python_packages`, `.pip-cache`, and `__pycache__` found:

| Group | Count | Notes |
|---|---:|---|
| Model weights | 1586 | `.pth`, `.pt`, `.ckpt`, `.onnx`; mostly legacy `best_model.pth` |
| Signal-like files | 33 | Mostly text/CSV platform probes and requirements; raw PU/SDUST signal files not confirmed |
| Config/result files | 2782 | YAML/JSON, including many `metrics.json` |
| Image/report assets | 16269 | `.png`, `.jpg`, `.svg`, `.pdf`, experiment plots and reports |
| 3D/CAD assets | 0 | No GLB/GLTF/OBJ/FBX/STL/STEP/STP/SLDPRT/Blend found |

## Platform Research Assets

Platform-local assets exist under:

- `hpsu-dan-platform/storage/research_results/hpsu-dan-pu-task1-run10`
- `hpsu-dan-platform/storage/research_results/hpsu-dan-pu-task3-run10`
- `hpsu-dan-platform/storage/research_results/hpsu-dan-sdust-task1-run5`

Files include:

- `training_curve.json`
- `report_summary.json`
- `pseudo_label_log.json`
- `ot_transport.json`
- `feature_umap.json`
- `confusion_matrix.json`

## Legacy Experiment Assets

Legacy result folders include:

- `checkpoints`
- `experiments`
- `comparative_experiments`
- `experiment_averages`
- `experiment_details`
- `ablation`
- `noise_robustness_results`
- `sensitivity_experiments`
- `confusion_matrices_svg`

These should feed `artifacts/legacy-assets-index.json`, `artifacts/models-manifest.json`, `artifacts/datasets-manifest.json`, and `artifacts/experiments-manifest.json` in Phase 3.

## Dataset Status

Confirmed:

- Dataset loader code exists for PU and SDUST.
- PU manifest information exists in `configs/models/hpsu-dan-v1.yaml`.
- Platform catalog currently includes PU and SDUST metadata.

Not yet confirmed:

- Raw PU signal file directory.
- Raw SDUST signal file directory.
- SDUST class map from real config.
- Transfer task class/domain order from real training config.

## 3D/CAD Status

No true 3D or CAD asset files were found. Later Three.js phases must either:

- use programmatic geometry with explicit "generated scene" status, or
- wait for external GLB/CAD/modeling assets.

The final system must not present current SVG/programmatic placeholders as imported real equipment models.

## Risks

- Large experiment tree requires scanner exclusions and resumable indexing.
- Several Chinese labels in existing YAML/store files are mojibake and need normalization from verified source labels.
- Raw signal availability is not established by Phase 0 scan.
- No real 3D assets exist yet.
