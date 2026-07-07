# Development Setup
## Prerequisites
Python 3.12+, Node 22+, CUDA (optional)

## Quick Start
  pip install -r services/api/requirements.txt
  pip install -r services/inference/requirements.txt
  cd apps/web && npm install && cd ../..
  cp .env.example .env
  python scripts/dev_supervisor.py start

## URLs
  http://localhost:8080 - Frontend
  http://localhost:8000/docs - API Docs
