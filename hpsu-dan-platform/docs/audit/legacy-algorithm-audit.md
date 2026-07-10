# Phase 0 Legacy Algorithm Audit

Date: 2026-07-10

## Legacy Root

Legacy root should be configured as:

```env
HPSU_DAN_LEGACY_ROOT=E:\没有添加新对比试验之前的版本（图形保存格式修改）
```

Business code should resolve it through environment/config and `pathlib.Path`, not hard-code it in multiple files.

## Algorithm Files

Important legacy files and folders found at workspace root:

- `train.py`
- `train_utils.py`
- `opt.py`
- `utils.py`
- `models`
- `datasets`
- `checkpoints`
- `experiments`
- `comparative_experiments`
- `ablation`
- `noise_robustness_results`
- `sensitivity_experiments`
- report and aggregation scripts such as `run_comparative_experiments.py`, `run_noise_robustness.py`, `generate_averaged_results.py`, `calculate_experiment_averages_from_logs.py`

## Dataset Loaders

Found dataset loader code:

- `datasets/PU.py`
- `datasets/SDUST.py`
- `datasets/SequenceDatasets.py`
- `datasets/sequence_aug.py`
- `datasets/feature_engineering.py`

The `datasets` directory appears to contain loader code, not raw signal files. Raw data location still needs confirmation from config/code and should not be guessed from filenames alone.

## Model Manifest And Adapter

Current model manifest:

- `hpsu-dan-platform/configs/models/hpsu-dan-v1.yaml`

Manifest identifies:

- algorithm: HPSU-DAN
- implementation: DMPAN
- dataset: PU
- sample length: 1024
- sampling rate: 25600
- classes: 7
- model path: one legacy `best_model.pth`

Issue:

- Manifest text contains mojibake in Chinese labels and path display.
- The model path is absolute and should be normalized into a configured manifest in Phase 1.

Adapter:

- `packages/hpsu_dan_adapter/hpsu_dan_adapter/legacy_bridge.py`
- Loads model through PyTorch, `opt.parse_args([])`, and `models.DMPAN`.
- Uses two DMPAN models and averages softmax probabilities if the checkpoint contains `model1` and `model2`.

## Experiment Assets

Large real experiment inventory exists:

- weights: 1586 files with `.pth/.pt/.ckpt/.onnx` extensions, mostly `best_model.pth`
- config/result JSON/YAML: 2782 files
- image/PDF/SVG assets: 16269 files
- experiment result extension summary includes `.svg`, `.jpg`, `.png`, `.json`, `.log`, `.pth`, `.xlsx`, `.pdf`

Examples found under:

- `checkpoints/DMPAN/PU/S3_to_N09M07F10/...`
- `ablation/ablation/dynOff/DMPAN/PU/...`
- `noise_robustness_results`
- `sensitivity_experiments`

## Existing Import Tooling

Platform script exists:

- `scripts/index_legacy_experiments.py`

It scans legacy runs and inserts/upserts experiment runs, metrics, and assets. It was smoke-tested with a temporary fixture and imported metrics/assets successfully.

## Phase 0 Conclusion

The legacy algorithm and experiment assets are present and substantial. The next phase should create formal machine-readable dataset/model/experiment manifests from verified configs and hashes, without modifying legacy training logic or moving original files.
