# Phase 0 Project Structure Audit

Date: 2026-07-10

## Workspace

- Workspace root: `E:\没有添加新对比试验之前的版本（图形保存格式修改）`
- Platform root: `hpsu-dan-platform`
- Legacy algorithm root expected by prompt: workspace root through `HPSU_DAN_LEGACY_ROOT`

## Top-Level Workspace Findings

The workspace is not only a web app. It contains the original research and experiment tree beside the platform:

- `datasets`: legacy dataset loader code for PU and SDUST.
- `models`: legacy model implementation package.
- `checkpoints`: many trained experiment runs and `best_model.pth` files.
- `experiments`, `comparative_experiments`, `experiment_averages`, `experiment_details`: experiment outputs and summaries.
- `ablation`, `noise_robustness_results`, `sensitivity_experiments`: competition-relevant result groups.
- root Python files such as `train.py`, `train_utils.py`, `opt.py`, `utils.py`, `run_noise_robustness.py`, and comparison/report scripts.
- `hpsu-dan-platform`: Vue/FastAPI platform under active development.

## Platform Structure

Important platform directories:

- `apps/web`: Vue 3 / TypeScript / Vite frontend.
- `services/api`: FastAPI API service.
- `services/inference`: FastAPI inference service.
- `packages/hpsu_dan_adapter`: adapter boundary for legacy HPSU-DAN/DMPAN code.
- `configs/models`: current model manifest YAML.
- `configs/research`: static research registry YAML fallback/source files.
- `storage/research_results`: platform-local research result JSON assets.
- `docs`: current architecture, API, deployment, and integration documentation.
- `scripts`: platform utility scripts, including legacy indexing.
- `deploy`: nginx, docker, Cloudflare, and Windows deployment helpers.

## Current Runtime Ports

Observed running local services:

- Frontend: `127.0.0.1:5173`
- API: `127.0.0.1:8000`
- Inference: `127.0.0.1:8010`

## Access Issues

Several `pytest-cache-files-*` directories deny access during recursive scanning. They are test cache artifacts and should be excluded from future scanners.

## Phase 0 Conclusion

The project has the expected platform structure plus a large legacy research workspace. Later phases should not move legacy files. Integration should use `HPSU_DAN_LEGACY_ROOT`, manifests, hashes, and relative paths.
