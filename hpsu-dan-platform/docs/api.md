# API Reference
## Auth
  POST /api/v1/auth/login {"username","password"}

## Dashboard
  GET /api/v1/dashboard/summary (auth required)

## Diagnosis
  POST /api/v1/diagnosis/predict {"samples","sampling_rate","model_id"}

## Research
  GET  /api/v1/research/options - List results
  POST /api/v1/research/refresh - Refresh cache
  GET  /api/v1/research/results/:id
  GET  /api/v1/research/results/:id/assets/:name

## System
  GET /api/v1/system/status (admin)
  POST /api/v1/assistant/chat {"messages"}
